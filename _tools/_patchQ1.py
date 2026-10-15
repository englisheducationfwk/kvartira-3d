# -*- coding: utf-8 -*-
"""Q1: адаптив под телефоны — тач-управление как в топ-играх: джойстик слева,
обзор свайпом справа, кнопки действий (использовать/взять/поставить/прыжок/планшет),
безопасные зоны iPhone, планшет во весь экран на маленьких."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:130]
    s = s.replace(old, new, 1)


# viewport: без зума
rep('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">')

# CSS
rep("#paintPick{position:fixed;left:50%;bottom:118px;transform:translateX(-50%);z-index:70}",
"""/* ---------- телефон: тач-управление как в топ-играх ---------- */
#joy{position:absolute;left:16px;bottom:calc(88px + env(safe-area-inset-bottom));width:124px;height:124px;
  border-radius:50%;background:rgba(18,16,12,.30);border:2px solid rgba(255,255,255,.35);z-index:41;touch-action:none;display:none}
#joy .knob{position:absolute;left:50%;top:50%;width:54px;height:54px;margin:-27px 0 0 -27px;border-radius:50%;
  background:rgba(255,255,255,.75);box-shadow:0 4px 14px rgba(0,0,0,.35)}
#tbtns{position:absolute;right:14px;bottom:calc(92px + env(safe-area-inset-bottom));display:none;flex-direction:column;gap:10px;z-index:41}
#tbtns .tb2{width:62px;height:62px;border-radius:50%;background:rgba(24,22,19,.75);border:1.5px solid rgba(79,217,255,.45);
  color:#fff;display:grid;place-items:center;font-size:11px;font-weight:700;touch-action:none;user-select:none;-webkit-user-select:none;text-align:center;line-height:1.15}
#tbtns .tb2:active{background:rgba(79,217,255,.35)}
body.touch #joy{display:block}
body.touch #tbtns{display:flex}
body.touch #bigplay{display:none !important}
body.touch #paintPick{bottom:calc(210px + env(safe-area-inset-bottom))}
#cv{touch-action:none}
@media(max-width:640px){
  #tabl .tabl-card{width:100vw;height:100dvh;border-radius:0;border:0}
  #tabl .tabl-bar{padding:8px 10px}
  #tabl .tb{padding:8px 11px;font-size:12.5px}
  #tbtns .tb2{width:58px;height:58px;font-size:10.5px}
  #joy{width:112px;height:112px}
}
#paintPick{position:fixed;left:50%;bottom:118px;transform:translateX(-50%);z-index:70}""")

# HTML в сцене
rep("""        <div class="invbar hidden" id="invBar"></div>""",
"""        <div class="invbar hidden" id="invBar"></div>
        <div id="joy"><div class="knob" id="joyKnob"></div></div>
        <div id="tbtns">
          <div class="tb2" id="tbUse">🖐<br>использ.</div>
          <div class="tb2" id="tbPick">✋<br>взять</div>
          <div class="tb2" id="tbPlace">📦<br>постав.</div>
          <div class="tb2" id="tbJump">⤒<br>прыжок</div>
          <div class="tb2" id="tbMenu">☰<br>планшет</div>
        </div>""")

# JS: блок тача (перед планшетом)
rep("""/* ---------- планшет (TAB): план, замеры, покупки и настройки поверх игры ---------- */""",
"""/* =====================================================================
   ТЕЛЕФОН: тач-управление — джойстик слева, обзор свайпом справа
   ===================================================================== */
var TOUCH = { on: ('ontouchstart' in window) || navigator.maxTouchPoints > 0, move:{x:0,y:0}, lookId:-1, joyId:-1 };
if (TOUCH.on){
  document.body.classList.add('touch');
  (function(){
    var joy = $('#joy'), knob = $('#joyKnob'), joyR = 40, joyC = { x:0, y:0 };
    function joySet(dx, dy){
      var d = Math.hypot(dx, dy) || 1, cl = Math.min(1, d / joyR);
      var nx = dx / d * cl, ny = dy / d * cl;
      knob.style.transform = 'translate(' + (nx*joyR) + 'px,' + (ny*joyR) + 'px)';
      TOUCH.move.x = nx; TOUCH.move.y = -ny;       /* вверх по экрану = вперёд */
    }
    joy.addEventListener('pointerdown', function(e){
      TOUCH.joyId = e.pointerId;
      try { joy.setPointerCapture(e.pointerId); } catch(err){}
      var r = joy.getBoundingClientRect(); joyC = { x: r.left + r.width/2, y: r.top + r.height/2 };
      joySet(e.clientX - joyC.x, e.clientY - joyC.y);
      e.preventDefault(); e.stopPropagation();
    });
    joy.addEventListener('pointermove', function(e){
      if (e.pointerId !== TOUCH.joyId) return;
      joySet(e.clientX - joyC.x, e.clientY - joyC.y);
      e.preventDefault();
    });
    function joyEnd(e){
      if (e.pointerId !== TOUCH.joyId) return;
      TOUCH.joyId = -1; knob.style.transform = ''; TOUCH.move.x = TOUCH.move.y = 0;
    }
    joy.addEventListener('pointerup', joyEnd);
    joy.addEventListener('pointercancel', joyEnd);
    /* обзор: свайп по экрану */
    var lx = 0, ly = 0;
    canvas.addEventListener('pointerdown', function(e){
      if (state.mode !== 'walk') return;
      TOUCH.lookId = e.pointerId; lx = e.clientX; ly = e.clientY;
      try { canvas.setPointerCapture(e.pointerId); } catch(err){}
      e.preventDefault();
    });
    canvas.addEventListener('pointermove', function(e){
      if (e.pointerId !== TOUCH.lookId) return;
      walk.yaw -= (e.clientX - lx) * 0.0042;
      walk.pitch = clamp(walk.pitch - (e.clientY - ly) * 0.0042, -1.35, 1.35);
      lx = e.clientX; ly = e.clientY;
      walkUpdate(0); paint();
      e.preventDefault();
    });
    function lookEnd(e){ if (e.pointerId === TOUCH.lookId) TOUCH.lookId = -1; }
    canvas.addEventListener('pointerup', lookEnd);
    canvas.addEventListener('pointercancel', lookEnd);
    /* кнопки действий */
    function tapBtn(id, fn){
      var b = $(id);
      b.addEventListener('pointerdown', function(e){ e.preventDefault(); e.stopPropagation(); fn(); });
    }
    tapBtn('#tbUse', function(){
      var d = doorUnder(0, 0);
      if (d) useThing(d);
      else { var pv = paintUnder(0, 0); if (pv) openPaintPick(pv); }
    });
    tapBtn('#tbPick', function(){ var g = itemUnder(0, 0); if (g) pickUp(g); else toast('Наведись на предмет'); });
    tapBtn('#tbPlace', function(){
      if (held >= 0 && inv[held]) placeHeld(0, 0);
      else { var pv = paintUnder(0, 0); if (pv) openPaintPick(pv); }
    });
    tapBtn('#tbJump', function(){ if (walk.grounded){ walk.vy = JUMP; walk.grounded = false; } });
    tapBtn('#tbMenu', function(){ openTablet('plan'); });
  })();
}

/* ---------- планшет (TAB): план, замеры, покупки и настройки поверх игры ---------- */""")

# walkUpdate: вклад джойстика
rep("""  if (wish.lengthSq() > 0) wish.normalize().multiplyScalar(sp*dt);
  walk.pos.x += wish.x; walk.pos.z += wish.z;""",
"""  if (typeof TOUCH !== 'undefined' && (TOUCH.move.x || TOUCH.move.y)){
    wish.addScaledVector(f, TOUCH.move.y).addScaledVector(r, TOUCH.move.x);
  }
  if (wish.lengthSq() > 0) wish.normalize().multiplyScalar(sp*dt);
  walk.pos.x += wish.x; walk.pos.z += wish.z;""")

# tick: ходить и когда двигает джойстик
rep("    if (walk.locked || Object.keys(walk.keys).some(function(k2){ return walk.keys[k2]; })) walkUpdate(dt);",
    "    if (walk.locked || (typeof TOUCH !== 'undefined' && (TOUCH.move.x || TOUCH.move.y)) || Object.keys(walk.keys).some(function(k2){ return walk.keys[k2]; })) walkUpdate(dt);")

# без захвата мыши на телефоне
rep("""canvas.addEventListener('click', function(){
  var pp = $('#paintPick');
  if (pp) pp.classList.add('hidden');          /* клик по игре — закрыть выбор краски */
  if (state.mode === 'walk' && !walk.locked) canvas.requestPointerLock && canvas.requestPointerLock();
});""",
"""canvas.addEventListener('click', function(){
  var pp = $('#paintPick');
  if (pp) pp.classList.add('hidden');          /* клик по игре — закрыть выбор краски */
  if (state.mode === 'walk' && !walk.locked && !TOUCH.on) canvas.requestPointerLock && canvas.requestPointerLock();
});""")

rep("$('#bigplay').addEventListener('click', function(){ if (canvas.requestPointerLock) canvas.requestPointerLock(); });",
    "$('#bigplay').addEventListener('click', function(){ if (!TOUCH.on && canvas.requestPointerLock) canvas.requestPointerLock(); });")

rep("  if (state.mode === 'walk' && canvas.requestPointerLock) canvas.requestPointerLock();",
    "  if (state.mode === 'walk' && !TOUCH.on && canvas.requestPointerLock) canvas.requestPointerLock();")

rep("""    if (state.mode !== 'walk') setMode('walk');
    walkTo(sp.x, sp.z, sp.yaw||0);
    if (typeof closeTablet === 'function') closeTablet();
    if (canvas.requestPointerLock) canvas.requestPointerLock();""",
"""    if (state.mode !== 'walk') setMode('walk');
    walkTo(sp.x, sp.z, sp.yaw||0);
    if (typeof closeTablet === 'function') closeTablet();
    if (!TOUCH.on && canvas.requestPointerLock) canvas.requestPointerLock();""")

# подсказка внизу — для телефона
rep("""  $('#hint').textContent = walking
    ? 'Клик — мышь · WASD — идти · ЛКМ — открыть/использовать · СКМ — взять · ПКМ — поставить · 1–9 слоты · R — поворот · P — подгонка · J — полёт · TAB — планшет · F — что не так · V — обзор · Esc — выйти'
    : 'ЛКМ — вращать · клик по вещи — взять · клик с вещью в руке — поставить · ←/→ — этапы · TAB — планшет';""",
"""  $('#hint').textContent = walking
    ? (TOUCH.on
        ? 'Джойстик слева — идти · свайп — смотреть · кнопки справа — действия · ☰ — планшет'
        : 'Клик — мышь · WASD — идти · ЛКМ — открыть/использовать · СКМ — взять · ПКМ — поставить · 1–9 слоты · R — поворот · P — подгонка · J — полёт · TAB — планшет · F — что не так · V — обзор · Esc — выйти')
    : 'ЛКМ — вращать · клик по вещи — взять · клик с вещью в руке — поставить · ←/→ — этапы · TAB — планшет';""")

p.write_text(s, encoding='utf-8')
print('Q1 ok')
