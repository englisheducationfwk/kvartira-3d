# -*- coding: utf-8 -*-
"""O4: игровой режим — основной. Всё (план, замеры, покупки, настройки) в планшете
по TAB: открывается сразу весь план, вкладка настроек с пресетами — последняя.
Пометки «что где делать» показываются прямо в игре."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# ---------- CSS ----------
rep("""
</style>""",
"""
/* ---------- игровой режим — основной: всё остальное живёт в планшете (TAB) ---------- */
header.top{display:none}
main{padding:6px}
.stage{height:calc(100vh - 12px);min-height:0;border-radius:10px}
.grid3d{grid-template-columns:1fr;gap:0}
#tab-spec,#tab-buy,#tab-plan{display:none}
#tabl{position:fixed;inset:0;z-index:80;background:rgba(18,16,12,.55);backdrop-filter:blur(6px);display:grid;place-items:center}
#tabl .tabl-card{width:min(1180px,96vw);height:min(88vh,920px);background:#fbf8f2;border-radius:20px;
  box-shadow:0 30px 90px rgba(0,0,0,.45);display:flex;flex-direction:column;overflow:hidden;border:1px solid #e6ddc9}
#tabl .tabl-bar{display:flex;align-items:center;gap:6px;padding:10px 14px;background:#f2ecdf;border-bottom:1px solid #e3dac6;flex-wrap:wrap}
#tabl .tb{padding:7px 14px;border-radius:999px;font-size:13.5px;font-weight:700;color:#6b655a}
#tabl .tb.on{background:#2c2a25;color:#fff;box-shadow:var(--shadow)}
#tabl .tabl-x{margin-left:auto;width:34px;height:34px;border-radius:999px;background:#e7dfcd;font-size:15px;font-weight:700;display:grid;place-items:center}
#tabl .tabl-x:hover{background:#ddd2ba}
#tabl .tabl-body{flex:1;overflow-y:auto;padding:16px 18px 28px}
#tabl .tpage{display:none}
#tabl .tpage.on{display:block}
#tabl .tpage .wrap{max-width:none;margin:0;padding:0}
#tpage-set .panel{position:static;display:flex;flex-direction:column;gap:14px;width:100%;max-height:none;background:none;border:0;box-shadow:none;padding:0;overflow:visible}
#tpage-set .pblock{box-shadow:none}
</style>""")

# ---------- HTML планшета ----------
rep("""<div id="bugDlg"><div class="card2">""",
"""<div id="tabl" class="hidden"><div class="tabl-card">
  <div class="tabl-bar">
    <button class="tb on" data-p="plan">🗓 План работ</button>
    <button class="tb" data-p="spec">📐 Замеры</button>
    <button class="tb" data-p="buy">🛒 Что купить</button>
    <button class="tb" data-p="set">⚙️ Настройки</button>
    <button class="tabl-x" id="tablX" title="Закрыть (TAB)">✕</button>
  </div>
  <div class="tabl-body">
    <div class="tpage on" id="tpage-plan"></div>
    <div class="tpage" id="tpage-spec"></div>
    <div class="tpage" id="tpage-buy"></div>
    <div class="tpage" id="tpage-set"></div>
  </div>
</div></div>

<div id="bugDlg"><div class="card2">""")

# ---------- клавиша TAB ----------
rep("""  if (state.mode === 'walk' && ['Space','KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.code) >= 0) e.preventDefault();
  if (e.code === 'KeyJ' && state.mode === 'walk'){""",
"""  if (state.mode === 'walk' && ['Space','KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.code) >= 0) e.preventDefault();
  if (e.code === 'Tab'){
    e.preventDefault();
    if ($('#tabl').classList.contains('hidden')) openTablet('plan'); else closeTablet();
    return;
  }
  if (e.code === 'KeyJ' && state.mode === 'walk'){""")

# ---------- setMode ----------
rep("  if (!walking) $('.grid3d .panel').classList.remove('open');",
    "  if (!walking && typeof closeTablet === 'function') closeTablet();")

rep("    ? 'Клик — мышь · WASD — идти · ЛКМ — открыть/использовать · СКМ — взять · ПКМ — поставить · 1–9 слоты · R — поворот · J — полёт · F — что не так · V — обзор · Esc — выйти'\n    : 'ЛКМ — вращать · клик по вещи — взять · клик с вещью в руке — поставить · ←/→ — этапы';",
    "    ? 'Клик — мышь · WASD — идти · ЛКМ — открыть/использовать · СКМ — взять · ПКМ — поставить · 1–9 слоты · R — поворот · J — полёт · TAB — планшет · F — что не так · V — обзор · Esc — выйти'\n    : 'ЛКМ — вращать · клик по вещи — взять · клик с вещью в руке — поставить · ←/→ — этапы · TAB — планшет';")

# ---------- шестерёнка открывает планшет с настройками ----------
rep("""$('#gear').addEventListener('click', function(){
  var pn = $('.grid3d .panel');
  pn.classList.toggle('open');
  if (document.pointerLockElement && document.exitPointerLock) document.exitPointerLock();
  toast(pn.classList.contains('open') ? 'Панель открыта (⚙ или V — закрыть)' : 'Панель спрятана — игра на весь экран');
});""",
"""$('#gear').addEventListener('click', function(){
  openTablet('set');
  toast('Планшет: настройки. TAB — весь план, ✕ — закрыть');
});""")

# ---------- чипы режима и телепорты закрывают планшет ----------
rep("""$$('#modeChips button').forEach(function(b){
  if (!b.dataset.m) return;
  b.addEventListener('click', function(){ setMode(b.dataset.m); });
});""",
"""$$('#modeChips button').forEach(function(b){
  if (!b.dataset.m) return;
  b.addEventListener('click', function(){
    setMode(b.dataset.m);
    if (b.dataset.m === 'walk' && typeof closeTablet === 'function') closeTablet();
  });
});""")

rep("""    if (state.mode !== 'walk') setMode('walk');
    walkTo(sp.x, sp.z, sp.yaw||0);
    if (canvas.requestPointerLock) canvas.requestPointerLock();""",
"""    if (state.mode !== 'walk') setMode('walk');
    walkTo(sp.x, sp.z, sp.yaw||0);
    if (typeof closeTablet === 'function') closeTablet();
    if (canvas.requestPointerLock) canvas.requestPointerLock();""")

# ---------- пометки «что где делать» видны прямо в игре ----------
rep("  var show = state.spots && state.mode !== 'walk';",
    "  var show = state.spots;   /* пометки «что где делать» видны и в игре */")

# ---------- сам планшет ----------
rep("""/* ---------- старт: сразу игра, обзор — клавиша V ---------- */""",
"""/* ---------- планшет (TAB): план, замеры, покупки и настройки поверх игры ---------- */
(function(){
  var tabl = $('#tabl');
  $('#tpage-plan').appendChild($('#tab-plan .wrap'));
  $('#tpage-spec').appendChild($('#tab-spec .wrap'));
  $('#tpage-buy').appendChild($('#tab-buy .wrap'));
  $('#tpage-set').appendChild($('.panel'));
  var pages = { plan:'#tpage-plan', spec:'#tpage-spec', buy:'#tpage-buy', set:'#tpage-set' };
  function showPage(k){
    $$('#tabl .tb').forEach(function(b){ b.classList.toggle('on', b.dataset.p === k); });
    Object.keys(pages).forEach(function(k2){ $(pages[k2]).classList.toggle('on', k2 === k); });
  }
  window.openTablet = function(k){
    tabl.classList.remove('hidden');
    showPage(k || 'plan');
    if (document.pointerLockElement && document.exitPointerLock) document.exitPointerLock();
  };
  window.closeTablet = function(){ tabl.classList.add('hidden'); };
  $$('#tabl .tb').forEach(function(b){ b.addEventListener('click', function(){ showPage(b.dataset.p); }); });
  $('#tablX').addEventListener('click', function(){ closeTablet(); });
  tabl.addEventListener('click', function(e){ if (e.target === tabl) closeTablet(); });
})();

/* ---------- старт: сразу игра, обзор — клавиша V ---------- */""")

p.write_text(s, encoding='utf-8')
print('O4 ok')
