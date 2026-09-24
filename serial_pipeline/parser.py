"""
serial_pipeline/parser.py
Robust Packet Parser for RS-485 Text Stream:
Format: 'Pxxx:valueV, Pxxx:valueV, ...'

Handles:
- Arbitrary byte/string chunks from serial stream
- Packets split across multiple read() operations
- Multiple packets coalesced in a single read()
- Fragment buffering to prevent dropping split tokens
- Noise rejection for corrupted bytes
"""
import re
import time
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class PointSample:
    point: int
    voltage1: float
    timestamp: float

class StreamPacketParser:
    # Pattern to match complete point tokens like: P172:0.0183V, 222:0.0060V, p172:0.0183v
    TOKEN_PATTERN = re.compile(r'(?:P\s*)?(\d{1,4})\s*:\s*([0-9]*\.?[0-9]+)\s*V', re.IGNORECASE)

    def __init__(self):
        self._fragment_buffer: str = ""
        self._total_parsed: int = 0
        self._invalid_tokens: int = 0

    def parse_chunk(self, chunk: str) -> List[PointSample]:
        """
        Receives an arbitrary text chunk, combines with any previous fragment,
        extracts all valid Pxxx:valueV samples, and keeps incomplete trailing data.
        """
        if not chunk:
            return []

        # Combine previously unparsed tail with new chunk
        text = self._fragment_buffer + chunk
        now = time.time()
        samples: List[PointSample] = []
        last_match_end = 0

        for match in self.TOKEN_PATTERN.finditer(text):
            try:
                pt_str, v_str = match.groups()
                pt = int(pt_str)
                v = float(v_str)

                # Validate point range (0 to 249 expected for 250-point cycle)
                if 0 <= pt <= 999 and 0.0 <= v <= 10.0:
                    samples.append(PointSample(point=pt, voltage1=v, timestamp=now))
                    self._total_parsed += 1
                else:
                    self._invalid_tokens += 1
                last_match_end = match.end()
            except (ValueError, IndexError):
                self._invalid_tokens += 1

        # The remainder after the last complete match is preserved as fragment buffer
        remaining = text[last_match_end:]
        # Prevent runaway fragment buffer if garbage data is received
        if len(remaining) > 512:
            # Keep only the last 64 characters
            remaining = remaining[-64:]
        self._fragment_buffer = remaining

        return samples

    def reset(self):
        """Clears the fragment buffer on reconnect/flush."""
        self._fragment_buffer = ""

    @property
    def total_parsed(self) -> int:
        return self._total_parsed

    @property
    def invalid_tokens(self) -> int:
        return self._invalid_tokens
