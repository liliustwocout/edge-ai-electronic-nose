/* ==========================================================================
   STANDEE CONTROLLER SCRIPT - ADVANTECH AIoT INNOWORKS
   Clean Light Theme Edition (No Icons, No Emojis)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initWaveCycleCanvas();
  initZoomControls();
  initLiveEditMode();
  initPrintHandler();
});

/* --------------------------------------------------------------------------
   1. WAVECYCLE CANVAS OSCILLOSCOPE (CLEAN LIGHT THEME)
   -------------------------------------------------------------------------- */
function initWaveCycleCanvas() {
  const canvas = document.getElementById('waveCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  // Retina / HiDPI crispness
  const dpr = window.devicePixelRatio || 2;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  ctx.scale(dpr, dpr);

  const w = rect.width;
  const h = rect.height;

  // Clean light canvas background
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, w, h);

  // Subtle grid lines
  ctx.strokeStyle = 'rgba(15, 23, 42, 0.08)';
  ctx.lineWidth = 1;
  const cols = 10;
  const rows = 6;
  for (let i = 0; i <= cols; i++) {
    const x = (w / cols) * i;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
  }
  for (let j = 0; j <= rows; j++) {
    const y = (h / rows) * j;
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(w, y);
    ctx.stroke();
  }

  // 4 Risk Zones (Pastel Light Backgrounds)
  const zones = [
    { top: 0, bottom: h * 0.28, color: 'rgba(239, 68, 68, 0.07)' },    // Emergency
    { top: h * 0.28, bottom: h * 0.55, color: 'rgba(249, 115, 22, 0.05)' }, // Hazardous
    { top: h * 0.55, bottom: h * 0.8, color: 'rgba(245, 158, 11, 0.04)' },  // Warning
    { top: h * 0.8, bottom: h, color: 'rgba(16, 185, 129, 0.03)' }          // Normal
  ];

  zones.forEach(z => {
    ctx.fillStyle = z.color;
    ctx.fillRect(0, z.top, w, z.bottom - z.top);
  });

  const totalPoints = 250;

  // 1. Ghost Trace (Previous Cycle - Dotted Slate Gray)
  ctx.beginPath();
  ctx.strokeStyle = 'rgba(100, 116, 139, 0.6)';
  ctx.lineWidth = 1.5;
  ctx.setLineDash([3, 3]);
  for (let i = 0; i < totalPoints; i++) {
    const t = i / totalPoints;
    let v = 0.03;
    if (t > 0.15 && t < 0.35) {
      v += 0.82 * Math.sin(((t - 0.15) / 0.2) * (Math.PI / 2));
    } else if (t >= 0.35) {
      v += 0.82 * Math.exp(-(t - 0.35) * 4.5);
    }
    const x = (i / totalPoints) * w;
    const y = h - (v * (h * 0.88) + h * 0.06);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.setLineDash([]); // Reset line dash

  // 2. Clean Air Baseline (Deep Emerald Green, ~0.02V)
  ctx.beginPath();
  ctx.strokeStyle = '#059669';
  ctx.lineWidth = 2;
  for (let i = 0; i < totalPoints; i++) {
    const noise = Math.sin(i * 0.5) * 0.008;
    const v = 0.025 + noise;
    const x = (i / totalPoints) * w;
    const y = h - (v * (h * 0.88) + h * 0.06);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // 3. NH3 Curve (Amber Orange)
  ctx.beginPath();
  ctx.strokeStyle = '#d97706';
  ctx.lineWidth = 2.2;
  for (let i = 0; i < totalPoints; i++) {
    const t = i / totalPoints;
    let v = 0.03;
    if (t > 0.12 && t < 0.28) {
      v += 0.55 * Math.sin(((t - 0.12) / 0.16) * (Math.PI / 2));
    } else if (t >= 0.28) {
      v += 0.55 * Math.exp(-(t - 0.28) * 3.2);
    }
    const x = (i / totalPoints) * w;
    const y = h - (v * (h * 0.88) + h * 0.06);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // 4. H2S Curve (High Contrast Deep Red)
  ctx.beginPath();
  ctx.strokeStyle = '#dc2626';
  ctx.lineWidth = 2.5;
  for (let i = 0; i < totalPoints; i++) {
    const t = i / totalPoints;
    let v = 0.03;
    if (t > 0.18 && t < 0.32) {
      v += 0.92 * Math.sin(((t - 0.18) / 0.14) * (Math.PI / 2));
    } else if (t >= 0.32) {
      v += 0.92 * Math.exp(-(t - 0.32) * 4.0);
    }
    const x = (i / totalPoints) * w;
    const y = h - (v * (h * 0.88) + h * 0.06);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // 5. Anchor Points with Clean Text Labels
  const anchors = [
    { pt: 50,  time: '12s', color: '#0284c7' },
    { pt: 75,  time: '18s (Đỉnh)', color: '#dc2626' },
    { pt: 100, time: '24s', color: '#d97706' },
    { pt: 230, time: '55s (Hồi phục)', color: '#059669' }
  ];

  anchors.forEach(a => {
    const x = (a.pt / totalPoints) * w;
    ctx.strokeStyle = 'rgba(15, 23, 42, 0.25)';
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 2]);
    ctx.beginPath();
    ctx.moveTo(x, 15);
    ctx.lineTo(x, h - 15);
    ctx.stroke();
    ctx.setLineDash([]);

    // Anchor Marker dot
    ctx.fillStyle = a.color;
    ctx.beginPath();
    ctx.arc(x, 20, 3.5, 0, Math.PI * 2);
    ctx.fill();

    // Text Label
    ctx.font = 'bold 9px "JetBrains Mono", monospace';
    ctx.fillStyle = '#0f172a';
    ctx.fillText(`${a.time}`, x - 10, 13);
  });

  // Vertical scan line
  const sweepX = (165 / totalPoints) * w;
  ctx.strokeStyle = '#004b87';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(sweepX, 0);
  ctx.lineTo(sweepX, h);
  ctx.stroke();
}

/* --------------------------------------------------------------------------
   2. SVG QR CODE (CLEAN NAVY & WHITE)
   -------------------------------------------------------------------------- */
function initQrCode() {
  const container = document.getElementById('qrCodeContainer');
  if (!container) return;

  const color = '#004b87';
  const svg = `
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <rect width="100" height="100" fill="#ffffff"/>
      <!-- Detection Patterns (Top-Left) -->
      <rect x="6" y="6" width="26" height="26" fill="${color}"/>
      <rect x="10" y="10" width="18" height="18" fill="#ffffff"/>
      <rect x="14" y="14" width="10" height="10" fill="${color}"/>
      
      <!-- Top-Right -->
      <rect x="68" y="6" width="26" height="26" fill="${color}"/>
      <rect x="72" y="10" width="18" height="18" fill="#ffffff"/>
      <rect x="76" y="14" width="10" height="10" fill="${color}"/>
      
      <!-- Bottom-Left -->
      <rect x="6" y="68" width="26" height="26" fill="${color}"/>
      <rect x="10" y="72" width="18" height="18" fill="#ffffff"/>
      <rect x="14" y="76" width="10" height="10" fill="${color}"/>

      <!-- Timing tracks -->
      <rect x="36" y="10" width="4" height="4" fill="${color}"/>
      <rect x="44" y="10" width="4" height="4" fill="${color}"/>
      <rect x="52" y="10" width="4" height="4" fill="${color}"/>
      <rect x="60" y="10" width="4" height="4" fill="${color}"/>

      <rect x="10" y="36" width="4" height="4" fill="${color}"/>
      <rect x="10" y="44" width="4" height="4" fill="${color}"/>
      <rect x="10" y="52" width="4" height="4" fill="${color}"/>
      <rect x="10" y="60" width="4" height="4" fill="${color}"/>

      <!-- Alignment Pattern -->
      <rect x="70" y="70" width="18" height="18" fill="${color}"/>
      <rect x="74" y="74" width="10" height="10" fill="#ffffff"/>
      <rect x="77" y="77" width="4" height="4" fill="${color}"/>

      <!-- Payload Dots -->
      <rect x="38" y="24" width="6" height="6" fill="${color}"/>
      <rect x="48" y="24" width="6" height="6" fill="${color}"/>
      <rect x="58" y="24" width="6" height="6" fill="${color}"/>
      
      <rect x="38" y="36" width="6" height="6" fill="${color}"/>
      <rect x="48" y="36" width="8" height="8" fill="${color}"/>
      <rect x="60" y="36" width="6" height="6" fill="${color}"/>

      <rect x="36" y="48" width="6" height="6" fill="${color}"/>
      <rect x="46" y="48" width="6" height="6" fill="${color}"/>
      <rect x="56" y="48" width="8" height="8" fill="${color}"/>
      
      <rect x="38" y="60" width="6" height="6" fill="${color}"/>
      <rect x="48" y="60" width="6" height="6" fill="${color}"/>
      <rect x="58" y="60" width="6" height="6" fill="${color}"/>

      <rect x="38" y="74" width="8" height="8" fill="${color}"/>
      <rect x="50" y="74" width="6" height="6" fill="${color}"/>
      <rect x="60" y="74" width="6" height="6" fill="${color}"/>

      <rect x="38" y="86" width="6" height="6" fill="${color}"/>
      <rect x="48" y="86" width="8" height="8" fill="${color}"/>
      <rect x="60" y="86" width="6" height="6" fill="${color}"/>
    </svg>
  `;
  container.innerHTML = svg;
}

/* --------------------------------------------------------------------------
   3. ZOOM CONTROLLER
   -------------------------------------------------------------------------- */
let currentZoom = 1;
function initZoomControls() {
  const viewport = document.getElementById('standeeViewport');
  const btnFit = document.getElementById('btnFit');
  const btn50 = document.getElementById('btn50');
  const btn75 = document.getElementById('btn75');
  const btn100 = document.getElementById('btn100');

  function applyZoom(scale) {
    currentZoom = scale;
    viewport.style.transform = `scale(${scale})`;
    const baseH = 1890;
    const diff = (baseH * scale) - baseH;
    viewport.style.marginBottom = `${diff}px`;

    [btnFit, btn50, btn75, btn100].forEach(b => b && b.classList.remove('active'));
    if (scale === 0.5 && btn50) btn50.classList.add('active');
    else if (scale === 0.75 && btn75) btn75.classList.add('active');
    else if (scale === 1 && btn100) btn100.classList.add('active');
  }

  function fitScreen() {
    const isMobile = window.innerWidth <= 768;
    const topMargin = isMobile ? 120 : 90;
    const sideMargin = isMobile ? 16 : 40;
    const availHeight = Math.max(window.innerHeight - topMargin, 200);
    const availWidth = Math.max(window.innerWidth - sideMargin, 200);
    const scale = Math.min(availHeight / 1890, availWidth / 840, 1);
    applyZoom(scale);
    if (btnFit) btnFit.classList.add('active');
  }

  if (btnFit) btnFit.addEventListener('click', fitScreen);
  if (btn50) btn50.addEventListener('click', () => applyZoom(0.5));
  if (btn75) btn75.addEventListener('click', () => applyZoom(0.75));
  if (btn100) btn100.addEventListener('click', () => applyZoom(1));

  fitScreen();

  window.addEventListener('resize', () => {
    if (btnFit && btnFit.classList.contains('active')) {
      fitScreen();
    }
  });
}

/* --------------------------------------------------------------------------
   4. LIVE EDIT MODE (INLINE CONTENTEDITABLE + LOCALSTORAGE)
   -------------------------------------------------------------------------- */
function initLiveEditMode() {
  const btnEdit = document.getElementById('btnEdit');
  const btnSave = document.getElementById('btnSave');
  const btnReset = document.getElementById('btnReset');
  const standeeCanvas = document.getElementById('standeeCanvas');

  // Restore saved content
  const savedContent = localStorage.getItem('standee_light_html');
  if (savedContent && standeeCanvas) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(savedContent, 'text/html');
    const restoredContent = doc.querySelector('.standee-content');
    const currentContent = standeeCanvas.querySelector('.standee-content');
    if (restoredContent && currentContent) {
      currentContent.innerHTML = restoredContent.innerHTML;
      initWaveCycleCanvas();
    }
  }

  let isEditing = false;
  if (btnEdit) {
    btnEdit.addEventListener('click', () => {
      isEditing = !isEditing;
      document.body.classList.toggle('edit-mode', isEditing);
      btnEdit.classList.toggle('active', isEditing);
      btnEdit.innerText = isEditing ? 'Dang sua (Nhan de tat)' : 'Che do sua chu';

      const editableElements = standeeCanvas.querySelectorAll('h1, h2, h3, h4, p, span, li, td, th, strong');
      editableElements.forEach(el => {
        if (!el.closest('.institution-logo-box') && !el.closest('#waveCanvas') && !el.closest('.arch-image-wrapper')) {
          el.setAttribute('contenteditable', isEditing ? 'true' : 'false');
        }
      });
    });
  }

  if (btnSave) {
    btnSave.addEventListener('click', () => {
      if (standeeCanvas) {
        localStorage.setItem('standee_light_html', standeeCanvas.innerHTML);
        alert('Da luu thanh cong noi dung vao trinh duyet!');
      }
    });
  }

  if (btnReset) {
    btnReset.addEventListener('click', () => {
      if (confirm('Ban co chac chan muon khoi phuc lai noi dung goc ban dau?')) {
        localStorage.removeItem('standee_light_html');
        window.location.reload();
      }
    });
  }
}

/* --------------------------------------------------------------------------
   5. PRINT / EXPORT PDF HANDLER
   -------------------------------------------------------------------------- */
function initPrintHandler() {
  const btnPrint = document.getElementById('btnPrint');
  if (!btnPrint) return;

  btnPrint.addEventListener('click', () => {
    const viewport = document.getElementById('standeeViewport');
    const prevTransform = viewport.style.transform;
    const prevMargin = viewport.style.marginBottom;
    viewport.style.transform = 'none';
    viewport.style.marginBottom = '0';

    window.print();

    setTimeout(() => {
      viewport.style.transform = prevTransform;
      viewport.style.marginBottom = prevMargin;
    }, 500);
  });
}
