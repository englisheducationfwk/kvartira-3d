# -*- coding: utf-8 -*-
"""S1: краска 2026 — цвета и узоры (без обоев), покраска «рукой» в игре (ткнул стену —
выбрал, сохранилось само), фасады гарнитура и ручки, всё едет в пресеты."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:130]
    s = s.replace(old, new, 1)


# ---------- состояние ----------
rep("spots:true, dims:false, furn:true, map:false, mirrOn:false, view:'overview',",
    "spots:true, dims:false, furn:true, map:false, mirrOn:false, view:'overview',\n              wallPat:'solid', handle:D.palette.handles[0].hex,")

# ---------- узоры + покраска ----------
rep("""var noSave = false;   /* при полном сбросе автосейв молчит — старьё не вернётся */""",
"""var noSave = false;   /* при полном сбросе автосейв молчит — старьё не вернётся */
/* ---------- краска: узоры (без обоев) — тренды 2026 ---------- */
var PATTERNS = [
  { id:'solid',   t:'Ровный матовый' },
  { id:'lime',    t:'Лаймвош' },
  { id:'cloud',   t:'Облако' },
  { id:'stripes', t:'Тонкие полоски' },
  { id:'wide',    t:'Широкие полосы' },
  { id:'diag',    t:'Диагональ' },
  { id:'checker', t:'Шашечки' },
  { id:'scallop', t:'Волны-чешуйки' },
  { id:'arch',    t:'Арки' },
  { id:'speckle', t:'Крапинки' },
  { id:'cement',  t:'Микроцемент' }
];
var paintCache = {};
function shadeHex(hex, f){
  var n = parseInt(hex.slice(1), 16), r = n>>16 & 255, g = n>>8 & 255, b = n & 255;
  function mix(c){ var v = f >= 0 ? c + (255-c)*f : c*(1+f); return Math.round(Math.max(0, Math.min(255, v))); }
  return 'rgb(' + mix(r) + ',' + mix(g) + ',' + mix(b) + ')';
}
function texPaint(hex, pat){
  var key = hex + '|' + pat;
  if (paintCache[key]) return paintCache[key];
  var tex = ctex(512, 512, function(g, w, h){
    g.fillStyle = hex; g.fillRect(0, 0, w, h);
    var R = rng(7 + hex.length * 3 + pat.length * 5);
    var lite = shadeHex(hex, 0.16), dark = shadeHex(hex, -0.16),
        lite2 = shadeHex(hex, 0.30), dark2 = shadeHex(hex, -0.26);
    var i, x, yy, xx;
    if (pat === 'lime'){
      for (i=0;i<26;i++){ g.fillStyle = (i%2 ? 'rgba(255,255,255,.10)' : 'rgba(0,0,0,.06)');
        g.beginPath(); g.ellipse(R()*w, R()*h, 60+R()*150, 40+R()*120, R()*3.14, 0, 6.3); g.fill(); }
    } else if (pat === 'cloud'){
      for (i=0;i<40;i++){ g.fillStyle = (i%2 ? lite2 : dark2); g.globalAlpha = .35;
        g.beginPath(); g.arc(R()*w, R()*h, 26+R()*70, 0, 6.3); g.fill(); }
      g.globalAlpha = 1;
    } else if (pat === 'stripes'){
      g.globalAlpha = .28; g.fillStyle = lite;
      for (x=0; x<w; x+=42) g.fillRect(x, 0, 12, h);
      g.globalAlpha = 1;
    } else if (pat === 'wide'){
      for (x=0, i=0; x<w; x+=170, i++){ g.globalAlpha = .85; g.fillStyle = (i%2 ? dark : lite); g.fillRect(x, 0, 85, h); }
      g.globalAlpha = 1;
    } else if (pat === 'diag'){
      g.save(); g.translate(w/2, h/2); g.rotate(-Math.PI/4); g.translate(-w, -h);
      g.globalAlpha = .28; g.fillStyle = lite;
      for (x=0; x<w*3; x+=40) g.fillRect(x, 0, 11, h*3);
      g.restore(); g.globalAlpha = 1;
    } else if (pat === 'checker'){
      var cs = 64;
      g.globalAlpha = .30; g.fillStyle = dark;
      for (yy=0; yy<h; yy+=cs) for (xx=0; xx<w; xx+=cs)
        if (((xx/cs)+(yy/cs))%2 === 0) g.fillRect(xx, yy, cs, cs);
      g.globalAlpha = 1;
    } else if (pat === 'scallop'){
      var rr = 64, row = 0;
      g.globalAlpha = .30; g.fillStyle = lite;
      for (yy=-rr; yy<h+rr; yy+=rr*0.72, row++){
        var off = (row%2) ? rr/2 : 0;
        for (xx=-rr; xx<w+rr; xx+=rr){ g.beginPath(); g.arc(xx+off, yy, rr/2-4, Math.PI, 0); g.fill(); }
      }
      g.globalAlpha = 1;
    } else if (pat === 'arch'){
      var aw = 128, ah = 170;
      g.globalAlpha = .30; g.fillStyle = dark;
      for (xx=0; xx<w; xx+=aw){
        g.fillRect(xx+14, ah*0.55, aw-28, h-ah*0.55);
        g.beginPath(); g.arc(xx+aw/2, ah*0.55, (aw-28)/2, Math.PI, 0); g.fill();
      }
      g.globalAlpha = 1;
    } else if (pat === 'speckle'){
      for (i=0;i<420;i++){ g.fillStyle = (i%2 ? lite2 : dark2); g.globalAlpha = .25;
        g.fillRect(R()*w, R()*h, 2+R()*4, 2+R()*4); }
      g.globalAlpha = 1;
    } else if (pat === 'cement'){
      for (i=0;i<60;i++){ g.fillStyle = (i%2 ? 'rgba(255,255,255,.09)' : 'rgba(0,0,0,.07)');
        g.beginPath(); g.ellipse(R()*w, R()*h, 40+R()*130, 26+R()*90, R()*3.14, 0, 6.3); g.fill(); }
      for (i=0;i<240;i++){ g.fillStyle = (i%2 ? 'rgba(255,255,255,.12)' : 'rgba(0,0,0,.10)');
        g.fillRect(R()*w, R()*h, 1.6, 1.6); }
    }
  });
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  paintCache[key] = tex;
  return tex;
}
function applyWallPaint(){
  var pat = state.wallPat || 'solid';
  if (pat === 'solid'){
    M.paint.map = null; M.paint.color.set(state.wall);
  } else {
    M.paint.map = texPaint(state.wall, pat);
    M.paint.color.set('#ffffff');
  }
  M.paint.needsUpdate = true;
}
function applyHandle(){ if (state.handle) M.handleOld.color.set(state.handle); }""")

# ---------- функции выбора ----------
rep("""function pickWall(hex){ state.wall = hex; save(); M.paint.color.set(hex); $('#pw').value = hex; }
function pickFacade(hex){ state.facade = hex; save(); M.front.color.set(hex); $('#pf').value = hex; }""",
"""function pickWall(hex){ state.wall = hex; save(); applyWallPaint(); $('#pw').value = hex; markSw($('#swWalls'), hex); }
function pickFacade(hex){ state.facade = hex; save(); M.front.color.set(hex); $('#pf').value = hex; markSw($('#swFacades'), hex); }
function pickHandle(hex){ state.handle = hex; save(); applyHandle(); markSw($('#swHandles'), hex); }
function pickWallPat(id){
  state.wallPat = id; save(); applyWallPaint();
  $$('#patRow button').forEach(function(b){ b.classList.toggle('on', b.dataset.pat === id); });
  var c = D.palette.walls.filter(function(x){ return x.hex.toLowerCase() === String(state.wall).toLowerCase(); })[0];
  toast('Узор: ' + (PATTERNS.filter(function(x){ return x.id === id; })[0] || {}).t + (c ? ' · ' + c.name : ''));
}""")

rep("""function markSw(host, hex){ $$('.sw', host).forEach(function(x){ x.classList.toggle('on', x.dataset.hex===hex.toLowerCase()); }); }""",
"""function markSw(host, hex){ if (!host || !hex) return; $$('.sw', host).forEach(function(x){ x.classList.toggle('on', x.dataset.hex===String(hex).toLowerCase()); }); }""")

# ---------- вязанка свитчей и ручек ----------
rep("""swatches($('#swWalls'), D.palette.walls, state.wall, pickWall);
swatches($('#swFacades'), D.palette.facades, state.facade, pickFacade);
$('#pw').value = state.wall; $('#pf').value = state.facade;
$('#pw').addEventListener('input', function(e){ pickWall(e.target.value); });
$('#pf').addEventListener('input', function(e){ pickFacade(e.target.value); });""",
"""swatches($('#swWalls'), D.palette.walls, state.wall, pickWall);
swatches($('#swFacades'), D.palette.facades, state.facade, pickFacade);
swatches($('#swHandles'), D.palette.handles, state.handle, pickHandle);
$('#pw').value = state.wall; $('#pf').value = state.facade;
$('#pw').addEventListener('input', function(e){ pickWall(e.target.value); });
$('#pf').addEventListener('input', function(e){ pickFacade(e.target.value); });
(function(){
  var host = $('#patRow');
  PATTERNS.forEach(function(pt){
    var b = document.createElement('button'); b.textContent = pt.t; b.dataset.pat = pt.id;
    if ((state.wallPat || 'solid') === pt.id) b.classList.add('on');
    b.addEventListener('click', function(){ pickWallPat(pt.id); });
    host.appendChild(b);
  });
})();""")

# ---------- HTML: узоры и ручки в блоке «Цвета» ----------
rep("""          <p style="font-size:12.3px;color:var(--mut);margin-bottom:8px">Стены кухни</p>
          <div class="swatches" id="swWalls"></div>
          <div class="pick" style="margin-top:9px"><input type="color" id="pw"><span>свой цвет стен</span></div>
          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 8px">Фасады кухни (эмаль)</p>
          <div class="swatches" id="swFacades"></div>
          <div class="pick" style="margin-top:9px"><input type="color" id="pf"><span>свой цвет фасадов</span></div>""",
"""          <p style="font-size:12.3px;color:var(--mut);margin-bottom:8px">Стены кухни — тренды 2026</p>
          <div class="swatches" id="swWalls"></div>
          <div class="pick" style="margin-top:9px"><input type="color" id="pw"><span>свой цвет стен</span></div>
          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 0">Узор стены (краска, без обоев)</p>
          <div id="patRow"></div>
          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 8px">Фасады кухни (эмаль)</p>
          <div class="swatches" id="swFacades"></div>
          <div class="pick" style="margin-top:9px"><input type="color" id="pf"><span>свой цвет фасадов</span></div>
          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 8px">Ручки гарнитура</p>
          <div class="swatches" id="swHandles"></div>""")

# ---------- HTML пикера «рукой» ----------
rep("""<div id="tabl" class="hidden"><div class="tabl-card">""",
"""<div id="paintPick" class="hidden"><div class="pp-card">
  <div class="pp-head"><b id="ppTitle">Стена кухни</b><span id="ppClose" title="Закрыть">✕</span></div>
  <div class="swatches" id="ppSw" style="display:flex;flex-wrap:wrap;gap:6px"></div>
  <div id="ppPats" class="hidden"></div>
  <div class="pick" style="margin-top:8px"><input type="color" id="ppCustom"><span style="color:#cfc9bc">свой цвет</span></div>
</div></div>

<div id="tabl" class="hidden"><div class="tabl-card">""")

# ---------- CSS пикера ----------
rep("""#tabl{position:fixed;inset:0;z-index:80;""",
"""#paintPick{position:fixed;left:50%;bottom:118px;transform:translateX(-50%);z-index:70}
#paintPick .pp-card{background:rgba(24,22,19,.93);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:10px 12px;max-width:min(580px,92vw);box-shadow:0 14px 40px rgba(0,0,0,.4)}
.pp-head{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:8px}
#ppTitle{color:#fff;font-size:13px}
#ppClose{color:#fff;cursor:pointer;opacity:.75;font-weight:700}
#ppClose:hover{opacity:1}
#ppSw .sw{width:30px;height:30px;border-radius:8px;border:2px solid rgba(255,255,255,.22);cursor:pointer}
#ppSw .sw.on{border-color:#fff;box-shadow:0 0 0 2px rgba(255,255,255,.35)}
#ppPats{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;max-width:540px}
#ppPats button{padding:3px 9px;border-radius:999px;border:1px solid rgba(255,255,255,.3);color:#e8e2d6;font-size:11.5px}
#ppPats button.on{background:#fff;color:#221f1a;font-weight:700}
#patRow{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
#patRow button{padding:4px 9px;border:1px solid var(--line);border-radius:999px;font-size:11.5px;font-weight:600;color:#6b655a}
#patRow button.on{background:#2c2a25;color:#fff}
#tabl{position:fixed;inset:0;z-index:80;""")

# ---------- логика пикера + луч ----------
rep("""/* точная подгонка: двигаем вещь стрелками по 5 см */""",
"""/* покраска «рукой»: ткнуть в стену/фасад/ручку — выбрать цвет и узор, сохранится само */
function paintUnder(nx, ny){
  raycaster.setFromCamera({ x:nx, y:ny }, camera);
  var hits = raycaster.intersectObjects([gRoom, gKitchen, gFurn], true);
  for (var i=0;i<hits.length;i++){
    var m = hits[i].object;
    if (!m || !m.isMesh || !m.material) continue;
    var mats = Array.isArray(m.material) ? m.material : [m.material];
    if (mats.indexOf(M.paint) >= 0 || mats.indexOf(M.primer) >= 0 || mats.indexOf(M.plaster) >= 0) return 'wall';
    if (mats.indexOf(M.front) >= 0) return 'front';
    if (mats.indexOf(M.handleOld) >= 0) return 'handle';
    return null;
  }
  return null;
}
function openPaintPick(kind){
  var pp = $('#paintPick'); pp.classList.remove('hidden');
  $('#ppTitle').textContent = kind === 'wall' ? 'Стена кухни — краска'
    : (kind === 'front' ? 'Фасады гарнитура — эмаль' : 'Ручки гарнитура');
  var list = kind === 'wall' ? D.palette.walls : (kind === 'front' ? D.palette.facades : D.palette.handles);
  var cur = kind === 'wall' ? state.wall : (kind === 'front' ? state.facade : state.handle);
  var host = $('#ppSw'); host.innerHTML = '';
  list.forEach(function(c){
    var b = document.createElement('button'); b.className = 'sw'; b.style.background = c.hex;
    b.title = c.name + ' · ' + c.hex;
    if (c.hex.toLowerCase() === String(cur).toLowerCase()) b.classList.add('on');
    b.addEventListener('click', function(){
      if (kind === 'wall'){ pickWall(c.hex); if (state.stage < 4) applyStage(4); }
      else if (kind === 'front') pickFacade(c.hex);
      else pickHandle(c.hex);
      toast((kind === 'wall' ? 'Стена: ' : kind === 'front' ? 'Фасад: ' : 'Ручки: ') + c.name);
      openPaintPick(kind);
    });
    host.appendChild(b);
  });
  var pr = $('#ppPats');
  if (kind === 'wall'){
    pr.classList.remove('hidden'); pr.innerHTML = '';
    PATTERNS.forEach(function(pt){
      var b = document.createElement('button'); b.textContent = pt.t; b.dataset.pat = pt.id;
      if ((state.wallPat || 'solid') === pt.id) b.classList.add('on');
      b.addEventListener('click', function(){ pickWallPat(pt.id); openPaintPick('wall'); });
      pr.appendChild(b);
    });
  } else pr.classList.add('hidden');
  var cust = $('#ppCustom');
  cust.value = kind === 'wall' ? state.wall : (kind === 'front' ? state.facade : (state.handle || '#999999'));
  cust.oninput = function(e){
    if (kind === 'wall') pickWall(e.target.value);
    else if (kind === 'front') pickFacade(e.target.value);
    else pickHandle(e.target.value);
  };
}
$('#ppClose').addEventListener('click', function(){ $('#paintPick').classList.add('hidden'); });

/* точная подгонка: двигаем вещь стрелками по 5 см */""")

# ---------- клики в прогулке ----------
rep("""  if (e.button === 0){                  /* ЛКМ — активация: дверь, ящик, кран, выключатель */
    var d = doorUnder(0, 0);
    if (d) useThing(d);
  } else if (e.button === 1){           /* СКМ — взять предмет */
    e.preventDefault();
    var g = itemUnder(0, 0);
    if (g) pickUp(g);
  } else if (e.button === 2){           /* ПКМ — поставить */
    placeHeld(0, 0);
  }""",
"""  if (e.button === 0){                  /* ЛКМ — активация: дверь, ящик, кран, выключатель; иначе — покрасить стену */
    var d = doorUnder(0, 0);
    if (d) useThing(d);
    else { var pvW = paintUnder(0, 0); if (pvW) openPaintPick(pvW); }
  } else if (e.button === 1){           /* СКМ — взять предмет */
    e.preventDefault();
    var g = itemUnder(0, 0);
    if (g) pickUp(g);
  } else if (e.button === 2){           /* ПКМ — поставить; руки пусты — покрасить фасад/ручку/стену */
    if (held >= 0 && inv[held]) placeHeld(0, 0);
    else { var pvP = paintUnder(0, 0); if (pvP) openPaintPick(pvP); }
  }""")

# ---------- пресеты: узор и ручки ----------
rep("""  return { inv: state.inv.slice(), moved: JSON.parse(JSON.stringify(state.moved)),
           wall: state.wall, facade: state.facade, stage: state.stage, mirror: state.mirror,
           mirrOn: state.mirrOn !== false, spots: state.spots, dims: state.dims, map: state.map };""",
"""  return { inv: state.inv.slice(), moved: JSON.parse(JSON.stringify(state.moved)),
           wall: state.wall, facade: state.facade, stage: state.stage, mirror: state.mirror,
           wallPat: state.wallPat || 'solid', handle: state.handle || '',
           mirrOn: state.mirrOn !== false, spots: state.spots, dims: state.dims, map: state.map };""")

rep("""  state.wall = d.wall || state.wall;
  state.facade = d.facade || state.facade;""",
"""  state.wall = d.wall || state.wall;
  state.facade = d.facade || state.facade;
  state.wallPat = d.wallPat || 'solid';
  state.handle = d.handle || state.handle;""")

rep("""  M.paint.color.set(state.wall);
  M.front.color.set(state.facade);
  $('#pw').value = state.wall; $('#pf').value = state.facade;
  $('#ckMirror').checked = state.mirror;
  markSw($('#swWalls'), state.wall); markSw($('#swFacades'), state.facade);""",
"""  applyWallPaint();
  M.front.color.set(state.facade);
  applyHandle();
  $('#pw').value = state.wall; $('#pf').value = state.facade;
  $('#ckMirror').checked = state.mirror;
  markSw($('#swWalls'), state.wall); markSw($('#swFacades'), state.facade); markSw($('#swHandles'), state.handle);
  $$('#patRow button').forEach(function(b){ b.classList.toggle('on', b.dataset.pat === (state.wallPat || 'solid')); });""")

# ---------- старт: применить краску и ручки ----------
rep("""/* ---------- старт: сразу игра, обзор — клавиша V ---------- */
if (state.mirror){ flipView(); }
buildWorld();""",
"""/* ---------- старт: сразу игра, обзор — клавиша V ---------- */
if (state.mirror){ flipView(); }
buildWorld();
applyWallPaint();
applyHandle();""")

p.write_text(s, encoding='utf-8')
print('S1 ok')
