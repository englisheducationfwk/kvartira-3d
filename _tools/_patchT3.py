# -*- coding: utf-8 -*-
"""T3: настоящие текстуры (штукатурка/дерево) для стен и гарнитура: загрузка,
применение с цветом-тонировкой, нормали и шероховатость; правильные UV дверц;
галерея текстур в панели краски и в планшете; клавиша G — покраска под прицелом."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# ---------- состояние ----------
rep("              sunReal:true, autoTime:true, hour:13, season:-1,",
    "              sunReal:true, autoTime:true, hour:13, season:-1, wallTex:null, facadeTex:null,")

# ---------- загрузчик текстур + покраска с текстурами ----------
rep("""function applyWallPaint(){
  var pat = state.wallPat || 'solid';
  if (pat === 'solid'){
    M.paint.map = null; M.paint.color.set(state.wall);
  } else {
    M.paint.map = texPaint(state.wall, pat);
    M.paint.color.set('#ffffff');
  }
  M.paint.needsUpdate = true;
}
function applyHandle(){
  if (!state.handle) return;
  M.handleOld.color.set(state.handle);
  M.handleNew.color.set(state.handle);   /* новые ручки на финале — тоже этого цвета */
}""",
"""/* ---------- настоящие текстуры (CC0-паки): галерея, загрузка, применение ---------- */
var TEXCACHE = {};
var texLoader = new THREE.TextureLoader();
function texFor(set, kind, slot){
  var key = set.def.id + ':' + kind + ':' + slot;
  if (!TEXCACHE[key]){
    var src = slot === 'color' ? set.color : (slot === 'normal' ? set.normal : set.rough);
    if (!src) return null;
    var t = src.clone();
    t.needsUpdate = true;
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.anisotropy = 8;
    var k = (set.def.k || 1) * (kind === 'wall' ? 0.85 : 0.9);
    t.repeat.set(k, k);
    TEXCACHE[key] = t;
  }
  return TEXCACHE[key];
}
function loadTexSet(id, cb){
  var def = (D.texlib || []).filter(function(x){ return x.id === id; })[0];
  if (!def) return cb && cb(null);
  var set = TEXCACHE['set:' + id];
  if (set && set.ready) return cb && cb(set);
  if (!set){
    set = { def: def, color: null, normal: null, rough: null, ready: false };
    TEXCACHE['set:' + id] = set;
    var base = def.dir + '/', pend = 3;
    function done(){ if (--pend === 0){ set.ready = true; if (cb) cb(set); } }
    function fail(){ done(); }
    texLoader.load(base + 'color.webp', function(t){ t.encoding = THREE.sRGBEncoding; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; set.color = t; done(); }, undefined, fail);
    texLoader.load(base + 'normal.webp', function(t){ t.wrapS = t.wrapT = THREE.RepeatWrapping; set.normal = t; done(); }, undefined, fail);
    texLoader.load(base + 'rough.webp', function(t){ t.wrapS = t.wrapT = THREE.RepeatWrapping; set.rough = t; done(); }, undefined, fail);
  }
}
function readySet(id){
  var set = id && TEXCACHE['set:' + id];
  return (set && set.ready) ? set : null;
}
function applyWallPaint(){
  var pat = state.wallPat || 'solid';
  var set = readySet(state.wallTex);
  M.paint.map = null; M.paint.normalMap = null; M.paint.roughnessMap = null;
  M.paint.roughness = .88;
  if (set){
    M.paint.map = texFor(set, 'wall', 'color');
    M.paint.color.set(state.wall);
    if (set.normal){ M.paint.normalMap = texFor(set, 'wall', 'normal'); M.paint.normalScale.set(0.45, 0.45); }
    if (set.rough){ M.paint.roughnessMap = texFor(set, 'wall', 'rough'); M.paint.roughness = 1.0; }
  } else if (pat !== 'solid'){
    M.paint.map = texPaint(state.wall, pat);
    M.paint.color.set('#ffffff');
  } else {
    M.paint.color.set(state.wall);
  }
  M.paint.needsUpdate = true;
}
function applyFrontPaint(){
  var set = readySet(state.facadeTex);
  M.front.map = texGroove; M.front.normalMap = null; M.front.roughnessMap = null;
  M.front.roughness = .55;
  M.front.color.set(state.facade);
  if (set){
    M.front.map = texFor(set, 'front', 'color');
    if (set.normal){ M.front.normalMap = texFor(set, 'front', 'normal'); M.front.normalScale.set(0.35, 0.35); }
    if (set.rough){ M.front.roughnessMap = texFor(set, 'front', 'rough'); M.front.roughness = 1.0; }
  }
  M.front.needsUpdate = true;
}
function pickWallTex(id){
  state.wallTex = id; save();
  if (id && !readySet(id)){ toast('Загружаю текстуру…'); loadTexSet(id, function(){ applyWallPaint(); }); }
  applyWallPaint();
  markTexRows();
}
function pickFacadeTex(id){
  state.facadeTex = id; save();
  if (id && !readySet(id)){ toast('Загружаю текстуру…'); loadTexSet(id, function(){ applyFrontPaint(); }); }
  applyFrontPaint();
  markTexRows();
}
function markTexRows(){
  $$('.tx').forEach(function(b){
    var cur = b.dataset.kind === 'front' ? (state.facadeTex || '') : (state.wallTex || '');
    b.classList.toggle('on', (b.dataset.tx || '') === cur);
  });
}
function texRow(host, kind, jumpStage){
  if (!host) return;
  host.innerHTML = '';
  function mkBtn(id, label, bg){
    var b = document.createElement('button');
    b.className = 'tx';
    b.dataset.tx = id || '';
    b.dataset.kind = kind;
    if (bg) b.style.backgroundImage = 'url(' + bg + ')';
    b.title = label;
    if (!id) b.innerHTML = '<span style="font-size:10px">гладко</span>';
    b.addEventListener('click', function(){
      if (kind === 'wall') pickWallTex(id); else pickFacadeTex(id);
      if (jumpStage && state.stage !== 5) applyStage(5);
      toast((kind === 'wall' ? 'Стена: ' : 'Фасад: ') + label);
    });
    host.appendChild(b);
  }
  mkBtn(null, 'гладкая краска', null);
  (D.texlib || []).forEach(function(t){ mkBtn(t.id, t.name, t.dir + '/color.webp'); });
  markTexRows();
}
function applyHandle(){
  if (!state.handle) return;
  M.handleOld.color.set(state.handle);
  M.handleNew.color.set(state.handle);   /* новые ручки на финале — тоже этого цвета */
}""")

# ---------- фасад через applyFrontPaint ----------
rep("function pickFacade(hex){ state.facade = hex; save(); M.front.color.set(hex); $('#pf').value = hex; markSw($('#swFacades'), hex); }",
    "function pickFacade(hex){ state.facade = hex; save(); applyFrontPaint(); $('#pf').value = hex; markSw($('#swFacades'), hex); }")

# ---------- UV дверц: метры, как у остальной мебели ----------
rep("    var pd = new THREE.Mesh(new THREE.BoxGeometry(0.02, LOWH-0.04, LWD-0.02), M.front);",
    "    var pd = new THREE.Mesh(new THREE.BoxGeometry(0.02, LOWH-0.04, LWD-0.02), M.front);\n    fixBoxUV(pd.geometry, 0.02, LOWH-0.04, LWD-0.02, 1.667);")
rep("""      var d2h = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);""",
"""      var d2h = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);
      fixBoxUV(d2h.geometry, 0.02, UPH/2-0.03, UZD-0.02, 1.667);""")
rep("""      var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);""",
"""      var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);
      fixBoxUV(d2.geometry, 0.02, UPH-0.02, UZD-0.02, 1.667);""")

# ---------- пикер: галерея текстур ----------
rep("""  <div id="ppPats" class="hidden"></div>""",
"""  <div id="ppPats" class="hidden"></div>
  <div id="ppTex" class="hidden"></div>""")

rep("""  } else pr.classList.add('hidden');
  var cust = $('#ppCustom');""",
"""  } else pr.classList.add('hidden');
  var pt = $('#ppTex');
  if (kind === 'handle'){ pt.classList.add('hidden'); }
  else { pt.classList.remove('hidden'); pt.style.display = 'flex'; texRow(pt, kind, true); }
  var cust = $('#ppCustom');""")

# ---------- CSS галереи ----------
rep("""#patRow{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}""",
"""#ppTex{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.txrow{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.tx{width:46px;height:46px;border-radius:9px;border:2px solid rgba(120,110,90,.35);background-size:cover;background-position:center;cursor:pointer;display:grid;place-items:center;color:#6b655a}
.tx.on{border-color:#2c2a25;box-shadow:0 0 0 2px rgba(44,42,37,.3)}
#ppTex .tx{border-color:rgba(255,255,255,.25);color:#cfc9bc}
#ppTex .tx.on{border-color:#fff;box-shadow:0 0 0 2px rgba(255,255,255,.35)}
#patRow{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}""")

# ---------- планшет: галереи текстур в «Цветах» ----------
rep("""          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 0">Узор стены (краска, без обоев)</p>
          <div id="patRow"></div>""",
"""          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 0">Узор стены (краска, без обоев)</p>
          <div id="patRow"></div>
          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 0">Текстура стены — настоящие (штукатурка, бетон)</p>
          <div class="txrow" id="swWallTex"></div>""")
rep("""          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 8px">Ручки гарнитура</p>
          <div class="swatches" id="swHandles"></div>""",
"""          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 0">Текстура фасадов — настоящее дерево</p>
          <div class="txrow" id="swFacadeTex"></div>
          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 8px">Ручки гарнитура</p>
          <div class="swatches" id="swHandles"></div>""")

rep("""(function(){
  var host = $('#patRow');
  PATTERNS.forEach(function(pt){""",
"""texRow($('#swWallTex'), 'wall', false);
texRow($('#swFacadeTex'), 'front', false);
(function(){
  var host = $('#patRow');
  PATTERNS.forEach(function(pt){""")

# ---------- клавиша G ----------
rep("""  if (e.code === 'KeyP'){
    if (e.repeat) return;
    if (held < 0 || !inv[held]){ toast('Сначала возьми предмет (СКМ)'); return; }""",
"""  if (e.code === 'KeyG' && !e.repeat){
    var pkG = (state.mode === 'walk') ? paintUnder(0, 0) : paintUnder(ndc.x, ndc.y);
    if (pkG) openPaintPick(pkG);
    else toast('Наведись на стену кухни или гарнитур — и жми G');
    return;
  }
  if (e.code === 'KeyP'){
    if (e.repeat) return;
    if (held < 0 || !inv[held]){ toast('Сначала возьми предмет (СКМ)'); return; }""")

rep("· 1–9 слоты · R — поворот · P — подгонка · J — полёт",
    "· 1–9 слоты · R — поворот · P — подгонка · G — покраска · J — полёт")

# ---------- пресеты: текстуры ----------
rep("""           sunReal: state.sunReal !== false, autoTime: state.autoTime !== false,
           hour: state.hour || 13, season: (typeof state.season === 'number' ? state.season : -1),""",
"""           sunReal: state.sunReal !== false, autoTime: state.autoTime !== false,
           hour: state.hour || 13, season: (typeof state.season === 'number' ? state.season : -1),
           wallTex: state.wallTex || null, facadeTex: state.facadeTex || null,""")
rep("""  if (typeof d.sunReal === 'boolean') state.sunReal = d.sunReal;
  if (typeof d.autoTime === 'boolean') state.autoTime = d.autoTime;
  if (typeof d.hour === 'number') state.hour = d.hour;
  if (typeof d.season === 'number') state.season = d.season;""",
"""  if (typeof d.sunReal === 'boolean') state.sunReal = d.sunReal;
  if (typeof d.autoTime === 'boolean') state.autoTime = d.autoTime;
  if (typeof d.hour === 'number') state.hour = d.hour;
  if (typeof d.season === 'number') state.season = d.season;
  state.wallTex = d.wallTex || null;
  state.facadeTex = d.facadeTex || null;""")
rep("""  applyWallPaint();
  M.front.color.set(state.facade);
  applyHandle();
  applySun(true);""",
"""  applyWallPaint();
  applyFrontPaint();
  applyHandle();
  applySun(true);
  markTexRows();""")

# ---------- старт ----------
rep("""buildWorld();
applyWallPaint();
applyHandle();
applySun(true);""",
"""buildWorld();
applyWallPaint();
applyFrontPaint();
applyHandle();
applySun(true);""")

p.write_text(s, encoding='utf-8')
print('T3 ok')
