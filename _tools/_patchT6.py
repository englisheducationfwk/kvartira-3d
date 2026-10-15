# -*- coding: utf-8 -*-
"""T6: фотореалистичный рендер — пост-обработка (SSAO-затемнения, свечение, FXAA),
AO-карты в материалы стен/фасадов, мягкие тени 4К, пресет «Реалистичная графика»."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# ---------- состояние ----------
rep("              sunReal:true, autoTime:true, hour:13, season:-1, wallTex:null, facadeTex:null,",
    "              sunReal:true, autoTime:true, hour:13, season:-1, wallTex:null, facadeTex:null, gfxReal:true,")

# ---------- тени мягче + 4К на ПК ----------
rep("""sun.shadow.camera.near=1; sun.shadow.camera.far=26; sun.shadow.bias=-0.0004; sun.shadow.normalBias=0.02;""",
"""sun.shadow.camera.near=1; sun.shadow.camera.far=26; sun.shadow.bias=-0.0004; sun.shadow.normalBias=0.02;
if (!(('ontouchstart' in window) || navigator.maxTouchPoints > 0)){ sun.shadow.mapSize.set(4096, 4096); }
sun.shadow.radius = 3;""")

# ---------- uv2 для AO-карт ----------
rep("""  for (var f=0; f<6; f++) for (var i=f*4; i<f*4+4; i++)
    uv.setXY(i, uv.getX(i)*dims[f][0]*s, uv.getY(i)*dims[f][1]*s);""",
"""  for (var f=0; f<6; f++) for (var i=f*4; i<f*4+4; i++)
    uv.setXY(i, uv.getX(i)*dims[f][0]*s, uv.getY(i)*dims[f][1]*s);
  g.setAttribute('uv2', new THREE.BufferAttribute(uv.array.slice(), 2));   /* для AO-карт */""")

# ---------- композер ----------
rep("""var lastSunT = 0;""",
"""var lastSunT = 0;

/* =====================================================================
   ФОТОРЕАЛИСТИЧНЫЙ РЕНДЕР: SSAO (затемнение в углах), свечение, сглаживание
   ===================================================================== */
var composer = null, ssaoPass = null, bloomPass = null, fxaaPass = null;
function postSize(){
  if (!composer) return;
  var w = stageEl.clientWidth, h = stageEl.clientHeight;
  if (!w || !h) return;
  composer.setSize(w, h);
  if (ssaoPass) ssaoPass.setSize(w, h);
  if (bloomPass) bloomPass.setSize(w, h);
  if (fxaaPass && fxaaPass.material && fxaaPass.material.uniforms.resolution){
    var pr = renderer.getPixelRatio();
    fxaaPass.material.uniforms.resolution.value.set(1/(w*pr), 1/(h*pr));
  }
}
function initPost(){
  if (composer || !THREE.EffectComposer) return;
  try {
    composer = new THREE.EffectComposer(renderer);
    composer.setPixelRatio(renderer.getPixelRatio());
    composer.addPass(new THREE.RenderPass(scene, camera));
    ssaoPass = new THREE.SSAOPass(scene, camera, stageEl.clientWidth || 1280, stageEl.clientHeight || 720);
    ssaoPass.kernelRadius = 0.12;
    ssaoPass.minDistance = 0.0015;
    ssaoPass.maxDistance = 0.055;
    composer.addPass(ssaoPass);
    bloomPass = new THREE.UnrealBloomPass(new THREE.Vector2(512, 512), 0.18, 0.55, 0.88);
    composer.addPass(bloomPass);
    fxaaPass = new THREE.ShaderPass(THREE.FXAAShader);
    composer.addPass(fxaaPass);
    postSize();
  } catch(e){ composer = null; }
}
function setPost(on){
  if (on) initPost(); else { composer = null; ssaoPass = bloomPass = fxaaPass = null; }
  postSize(); paint();
}""")

# ---------- рендер через композер ----------
rep("function paint(){ renderer.render(scene, camera); }",
"""function paint(){
  if (composer && state.gfxReal !== false) composer.render();
  else renderer.render(scene, camera);
}""")
rep("""  updateOverlays();
  renderer.render(scene, camera);
}""",
"""  updateOverlays();
  paint();
}""")

# ---------- зеркало: не рисоваться во время проходов SSAO ----------
rep("    if (cam === mirrorCam || scn !== scene) return;",
    "    if (cam === mirrorCam || scn !== scene) return;\n    if (scn.overrideMaterial) return;   /* проходы SSAO — зеркало не трогаем */")

# ---------- ресайз ----------
rep("""  renderer.setSize(w, h, false);
  camera.aspect = w/h; camera.updateProjectionMatrix();
  paint();""",
"""  renderer.setSize(w, h, false);
  camera.aspect = w/h; camera.updateProjectionMatrix();
  postSize();
  paint();""")

# ---------- AO-карты в загрузку и материалы ----------
rep("""    var base = def.dir + '/', pend = 3;""",
    """    var base = def.dir + '/', pend = 4;""")
rep("""    texLoader.load(base + 'rough.webp', function(t){ t.wrapS = t.wrapT = THREE.RepeatWrapping; set.rough = t; done(); }, undefined, fail);
  }
}""",
"""    texLoader.load(base + 'rough.webp', function(t){ t.wrapS = t.wrapT = THREE.RepeatWrapping; set.rough = t; done(); }, undefined, fail);
    texLoader.load(base + 'ao.webp', function(t){ t.wrapS = t.wrapT = THREE.RepeatWrapping; set.ao = t; done(); }, undefined, fail);
  }
}""")
rep("""    set = { def: def, color: null, normal: null, rough: null, ready: false };""",
    """    set = { def: def, color: null, normal: null, rough: null, ao: null, ready: false };""")
rep("""    var src = slot === 'color' ? set.color : (slot === 'normal' ? set.normal : set.rough);""",
    """    var src = slot === 'color' ? set.color
            : (slot === 'normal' ? set.normal
            : (slot === 'ao' ? set.ao : set.rough));""")
rep("""  M.paint.map = null; M.paint.normalMap = null; M.paint.roughnessMap = null;
  M.paint.roughness = .88;
  if (set){
    M.paint.map = texFor(set, 'wall', 'color');
    M.paint.color.set(state.wall);
    if (set.normal){ M.paint.normalMap = texFor(set, 'wall', 'normal'); M.paint.normalScale.set(0.45, 0.45); }
    if (set.rough){ M.paint.roughnessMap = texFor(set, 'wall', 'rough'); M.paint.roughness = 1.0; }
  } else if (pat !== 'solid'){""",
"""  M.paint.map = null; M.paint.normalMap = null; M.paint.roughnessMap = null; M.paint.aoMap = null;
  M.paint.roughness = .88;
  if (set){
    M.paint.map = texFor(set, 'wall', 'color');
    M.paint.color.set(state.wall);
    if (set.normal){ M.paint.normalMap = texFor(set, 'wall', 'normal'); M.paint.normalScale.set(0.45, 0.45); }
    if (set.rough){ M.paint.roughnessMap = texFor(set, 'wall', 'rough'); M.paint.roughness = 1.0; }
    if (set.ao){ M.paint.aoMap = texFor(set, 'wall', 'ao'); M.paint.aoMapIntensity = 0.9; }
  } else if (pat !== 'solid'){""")
rep("""  M.front.map = texGroove; M.front.normalMap = null; M.front.roughnessMap = null;
  M.front.roughness = .55;
  M.front.color.set(state.facade);
  if (set){
    M.front.map = texFor(set, 'front', 'color');
    if (set.normal){ M.front.normalMap = texFor(set, 'front', 'normal'); M.front.normalScale.set(0.35, 0.35); }
    if (set.rough){ M.front.roughnessMap = texFor(set, 'front', 'rough'); M.front.roughness = 1.0; }
  }""",
"""  M.front.map = texGroove; M.front.normalMap = null; M.front.roughnessMap = null; M.front.aoMap = null;
  M.front.roughness = .55;
  M.front.color.set(state.facade);
  if (set){
    M.front.map = texFor(set, 'front', 'color');
    if (set.normal){ M.front.normalMap = texFor(set, 'front', 'normal'); M.front.normalScale.set(0.35, 0.35); }
    if (set.rough){ M.front.roughnessMap = texFor(set, 'front', 'rough'); M.front.roughness = 1.0; }
    if (set.ao){ M.front.aoMap = texFor(set, 'front', 'ao'); M.front.aoMapIntensity = 0.85; }
  }""")

# ---------- настройки: графика ----------
rep("""          <p style="font-size:11.8px;color:#9a9384;margin-top:8px">Зимой двор и крыши в снегу, солнце низкое. Ночью квартира тёмная — свет включается выключателями у дверей.</p>
        </div>""",
"""          <p style="font-size:11.8px;color:#9a9384;margin-top:8px">Зимой двор и крыши в снегу, солнце низкое. Ночью квартира тёмная — свет включается выключателями у дверей.</p>
          <label class="chk" style="margin-top:10px"><input type="checkbox" id="ckGfx" checked><span>Реалистичная графика — затемнение в углах (AO), свечение, сглаживание; на телефоне лучше выключать</span></label>
        </div>""")
rep("""  $('#ckSunReal').checked = state.sunReal !== false;""",
"""  $('#ckGfx').checked = state.gfxReal !== false;
  $('#ckGfx').addEventListener('change', function(e){
    state.gfxReal = e.target.checked; save(); setPost(state.gfxReal);
    toast(state.gfxReal ? 'Реалистичная графика включена ✨' : 'Облегчённая графика');
  });
  $('#ckSunReal').checked = state.sunReal !== false;""")

# ---------- пресеты ----------
rep("""           wallTex: state.wallTex || null, facadeTex: state.facadeTex || null,""",
"""           wallTex: state.wallTex || null, facadeTex: state.facadeTex || null,
           gfxReal: state.gfxReal !== false,""")
rep("""  state.wallTex = d.wallTex || null;
  state.facadeTex = d.facadeTex || null;""",
"""  state.wallTex = d.wallTex || null;
  state.facadeTex = d.facadeTex || null;
  if (typeof d.gfxReal === 'boolean') state.gfxReal = d.gfxReal;
  if ($('#ckGfx')) $('#ckGfx').checked = state.gfxReal !== false;
  setPost(state.gfxReal !== false);""")

# ---------- старт ----------
rep("""buildWorld();
applyWallPaint();
applyFrontPaint();
applyHandle();
applySun(true);""",
"""buildWorld();
applyWallPaint();
applyFrontPaint();
applyHandle();
applySun(true);
if (TOUCH.on) state.gfxReal = false;      /* на телефоне — облегчённая графика по умолчанию */
if (state.gfxReal !== false) initPost();""")

p.write_text(s, encoding='utf-8')
print('T6 ok')
