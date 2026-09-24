"""
serial_pipeline/main.py
Main entry point for Raspberry Pi 3 RS-485 Continuous Data Acquisition.

Usage:
    python3 -m serial_pipeline.main
    or
    python3 serial_pipeline/main.py
"""
import os
import sys
import time
import signal
import logging
from logging.handlers import RotatingFileHandler

# Add repository root to path if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from serial_pipeline.config import config
from serial_pipeline.parser import PointSample
from serial_pipeline.buffer import PointBuffer
from serial_pipeline.serial_receiver import SerialReceiver
from serial_pipeline.inference import EdgeAIInferenceEngine

import argparse

def setup_logging():
    os.makedirs(config.logging.log_dir, exist_ok=True)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, config.logging.log_level, logging.INFO))

    # Rotating File Handler (prevents disk space exhaustion 24/7)
    file_handler = RotatingFileHandler(
        config.logging.log_file,
        maxBytes=config.logging.max_bytes,
        backupCount=config.logging.backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def main():
    parser_arg = argparse.ArgumentParser(description="Raspberry Pi 3 RS-485 Data Acquisition Engine")
    parser_arg.add_argument('--port', type=str, default=config.serial.port, help="Serial device port (e.g. /dev/ttyUSB0)")
    parser_arg.add_argument('--baud', type=int, default=config.serial.baudrate, help="Baud rate (default 115200)")
    parser_arg.add_argument('--enable-ai', action='store_true', help="Enable Edge AI Inference on rolling windows and cycles")
    args = parser_arg.parse_args()

    config.serial.port = args.port
    config.serial.baudrate = args.baud

    setup_logging()
    logger = logging.getLogger('serial_pipeline.main')

    logger.info("=" * 65)
    logger.info("  EDGE AI ELECTRONIC NOSE - RS-485 CONTINUOUS DATA RECEIVER  ")
    logger.info(f"  Target Port: {config.serial.port} @ {config.serial.baudrate} baud (8N1)")
    logger.info(f"  Cycle Length: {config.buffer.cycle_length} pts | Window: {config.buffer.window_length} pts")
    logger.info(f"  Edge AI Mode: {'ENABLED' if args.enable_ai else 'DISABLED (Data Acquisition Mode)'}")
    logger.info("=" * 65)

    buffer = PointBuffer(
        cycle_length=config.buffer.cycle_length,
        window_length=config.buffer.window_length
    )

    inference_engine = EdgeAIInferenceEngine() if args.enable_ai else None

    last_log_time = 0.0

    # 1. Callback on every single point received
    def on_sample(sample: PointSample):
        nonlocal last_log_time
        buffer.push(sample)

        now = time.time()
        # Log summary once every 1.0 second to prevent console flooding
        if now - last_log_time >= 1.0:
            stats = buffer.get_stats()
            pct_bar = f"{sample.point}/{config.buffer.cycle_length}"
            logger.info(
                f"[RS485-RX] Point: P{sample.point:<3} | "
                f"Voltage: {sample.voltage1:.4f}V | "
                f"Progress: [{pct_bar:>7}] | "
                f"Loss Rate: {stats['packet_loss_rate_pct']:.2f}% | "
                f"Total Recv: {stats['total_received']} | "
                f"Gaps: {stats['total_gaps']}"
            )
            last_log_time = now

    # 2. Callback when a 20-point rolling window is ready
    def on_window_ready(window_20):
        if inference_engine.is_loaded:
            base_v = float(window_20[0])
            pred = inference_engine.predict_window(window_20, base_v=base_v)
            if pred and pred['gas'] != 'Clean Air':
                logger.warning(f"⚠️ [WINDOW INFERENCE ALERT] Gas: {pred['gas']} | Conc: {pred['ppm']} ppm")

    # 3. Callback when a full 250-point WaveCycle completes (60 seconds)
    def on_cycle_complete(cycle_id, pulse_arr, metrics):
        logger.info(
            f"🎯 [WAVECYCLE #{cycle_id} COMPLETED] "
            f"Filled: {metrics['filled_points']}/{metrics['total_points']} ({metrics['completeness_pct']}%) | "
            f"Vmax: {metrics['max_v']:.4f}V | "
            f"Vmin: {metrics['min_v']:.4f}V | "
            f"DeltaV: {metrics['delta_v']:.4f}V"
        )
        if inference_engine.is_loaded:
            base_v = float(pulse_arr[0])
            pred = inference_engine.predict_cycle(pulse_arr, base_v=base_v)
            if pred:
                logger.info(f"   --> Cycle #{cycle_id} Edge AI Result: Gas={pred['gas']}, Conc={pred['ppm']} ppm")

    buffer.on_window_ready = on_window_ready
    buffer.on_cycle_complete = on_cycle_complete

    receiver = SerialReceiver(on_sample_callback=on_sample)

    # Clean termination handler
    stop_event = False
    def signal_handler(sig, frame):
        nonlocal stop_event
        if not stop_event:
            stop_event = True
            logger.info("\nReceived interrupt signal. Shutting down gracefully...")
            receiver.stop()
            sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    receiver.start()

    logger.info("Receiver running. Press Ctrl+C to terminate.")
    try:
        while not stop_event:
            time.sleep(0.5)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == '__main__':
    main()
