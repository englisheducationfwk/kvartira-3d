# -*- coding: utf-8 -*-
"""T2: реалистичное освещение — солнце по времени суток и сезону (широта Москвы),
небо-шейдер со звёздами и закатом, PMREM-свет из неба, ACES-тонмаппинг,
сезоны со снегом на дворе, притухание города ночью, выключатель кухни."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# ---------- состояние ----------
rep("spots:true, dims:false, furn:true, map:false, mirrOn:false, view:'overview',",
    "spots:true, dims:false, furn:true, map:false, mirrOn:false, view:'overview',\n              sunReal:true, autoTime:true, hour:13, season:-1,")

# ---------- рендер: ACES ----------
rep("""renderer.outputEncoding = THREE.sRGBEncoding;
renderer.shadowMap.enabled = true;""",
"""renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;""")

# ---------- именованные светильники ----------
rep("""scene.add(new THREE.AmbientLight(0xffffff, 0.34));
scene.add(new THREE.HemisphereLight(0xfff6e8, 0x9d9484, 0.5));
var sun = new THREE.DirectionalLight(0xfff2dd, 1.1);""",
"""var ambLight = new THREE.AmbientLight(0xffffff, 0.34);
scene.add(ambLight);
var hemiLight = new THREE.HemisphereLight(0xfff6e8, 0x9d9484, 0.5);
scene.add(hemiLight);
var sun = new THREE.DirectionalLight(0xfff2dd, 1.1);""")

# ---------- небо + солнце + сезоны ----------
rep("""var fill = new THREE.DirectionalLight(0xdde7f2, 0.32); fill.position.set(-4, 4.5, 4); scene.add(fill);
var fill2 = new THREE.DirectionalLight(0xfff0e0, 0.18); fill2.position.set(6, 3.0, 6.5); scene.add(fill2);""",
"""var fill = new THREE.DirectionalLight(0xdde7f2, 0.32); fill.position.set(-4, 4.5, 4); scene.add(fill);
var fill2 = new THREE.DirectionalLight(0xfff0e0, 0.18); fill2.position.set(6, 3.0, 6.5); scene.add(fill2);

/* =====================================================================
   РЕАЛИСТИЧНОЕ ОСВЕЩЕНИЕ: солнце по времени суток и сезону (Москва),
   небо-шейдер, свет из неба (PMREM), снег зимой
   ===================================================================== */
var OUT_MATS = [];   /* материалы улицы — тонируются светом дня */
var applySnow = null;   /* назначается при сборке мира */
var skyMat = new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false, fog: false,
  uniforms: {
    sunDir: { value: new THREE.Vector3(0, 1, 0) },
    dayT:   { value: 1 }, dusk: { value: 0 }, night: { value: 0 },
    skyTop: { value: new THREE.Color(0x79b9ea) },
    skyHor: { value: new THREE.Color(0xdfeaf2) },
    sunCol: { value: new THREE.Color(0xfff3e2) }
  },
  vertexShader: 'varying vec3 vDir; void main(){ vDir = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
  fragmentShader: [
    'varying vec3 vDir;',
    'uniform vec3 sunDir; uniform float dayT, dusk, night;',
    'uniform vec3 skyTop, skyHor, sunCol;',
    'void main(){',
    '  float h = clamp(vDir.y, -0.05, 1.0);',
    '  vec3 col = mix(skyHor, skyTop, pow(max(h, 0.0), 0.55));',
    '  float s = max(dot(normalize(vDir), normalize(sunDir)), 0.0);',
    '  col += sunCol * pow(s, 200.0) * 2.4;',                       /* диск солнца */
    '  col += sunCol * pow(s, 5.0) * (0.22 + 0.5*dusk);',           /* ореол, на закате шире */
    '  if (night > 0.02){',
    '    vec3 sd = floor(vDir * 230.0);',
    '    float st = fract(sin(dot(sd, vec3(12.9898, 78.233, 45.164))) * 43758.5453);',
    '    float star = smoothstep(0.9976, 1.0, st) * night * smoothstep(0.02, 0.22, vDir.y);',
    '    col += vec3(star);',
    '  }',
    '  gl_FragColor = vec4(col, 1.0);',
    '}'
  ].join('\\n')
});
var skyMesh = new THREE.Mesh(new THREE.SphereGeometry(88, 32, 18), skyMat);
skyMesh.frustumCulled = false;
scene.add(skyMesh);
var pmrem = null, envRT = null, skyScratch = null, skyScratchMesh = null;
var lastSunSig = '';
function nowHour(){ var d2 = new Date(); return d2.getHours() + d2.getMinutes()/60; }
function seasonDoy(){
  if (state.season >= 0 && state.season <= 3) return [355, 80, 172, 266][state.season];
  var now = new Date(), start = new Date(now.getFullYear(), 0, 0);
  return Math.floor((now - start) / 86400000);
}
function isWinter(){
  if (state.season === 0) return true;
  if (state.season > 0) return false;
  var m2 = new Date().getMonth();
  return (m2 === 11 || m2 === 0 || m2 === 1);
}
function sunPos(hour, doy){
  var lat = 55.9 * Math.PI/180;
  var decl = 23.44 * Math.PI/180 * Math.sin(2*Math.PI*(doy - 81)/365);
  var H = (hour - 12.5) * Math.PI/12;
  var el = Math.asin(Math.sin(lat)*Math.sin(decl) + Math.cos(lat)*Math.cos(decl)*Math.cos(H));
  var az = Math.atan2(-Math.sin(H), Math.tan(decl)*Math.cos(lat) - Math.sin(lat)*Math.cos(H));
  return { el: el, az: az };   /* az: 0 = юг (у нас юг = +z) */
}
function regenEnv(){
  if (!pmrem) pmrem = new THREE.PMREMGenerator(renderer);
  if (!skyScratch){
    skyScratch = new THREE.Scene();
    skyScratchMesh = new THREE.Mesh(new THREE.SphereGeometry(80, 24, 14), skyMat);
    skyScratchMesh.frustumCulled = false;
    skyScratch.add(skyScratchMesh);
  }
  var rt = pmrem.fromScene(skyScratch, 0.05);
  if (envRT) envRT.dispose();
  envRT = rt;
  scene.environment = envRT.texture;
}
function applySun(force){
  if (state.sunReal === false){                       /* «студийный» свет как раньше */
    skyMesh.visible = false;
    scene.background = new THREE.Color(0xdfe3e6);
    scene.environment = null;
    lastSunSig = '';
    ambLight.intensity = 0.34; hemiLight.intensity = 0.5;
    sun.color.set(0xfff2dd); sun.intensity = 1.1;
    sun.position.set(3.2, 7.5, -9.5);
    fill.intensity = 0.32; fill2.intensity = 0.18;
    OUT_MATS.forEach(function(m){ m.color.set(0xffffff); });
    if (M.outside) M.outside.map = texOutside;
    M.outside.needsUpdate = true;
    if (applySnow) applySnow(false);
    return;
  }
  skyMesh.visible = true;
  scene.background = new THREE.Color(0x0a1024);
  var hour = state.autoTime ? nowHour() : (state.hour || 13);
  var doy = seasonDoy();
  var sp = sunPos(hour, doy);
  var elD = sp.el * 180/Math.PI;
  var day = clamp((elD + 4) / 10, 0, 1);              /* 0 ночь → 1 день */
  var dusk = clamp(1 - Math.abs(elD - 2)/9, 0, 1);    /* у горизонта */
  var night = 1 - clamp((elD + 2)/7, 0, 1);
  var sunI = Math.max(0, Math.sin(Math.max(sp.el, 0))) * 1.75;
  var r2 = 26;
  var sx = Math.cos(sp.el)*Math.sin(sp.az), sy = Math.sin(sp.el), sz = Math.cos(sp.el)*Math.cos(sp.az);
  sun.position.set(3.2 + sx*r2, Math.max(sy*r2, 0.3), 3.5 + sz*r2);
  sun.visible = sunI > 0.02;
  sun.intensity = sunI;
  sun.color.set(0xff6a26).lerp(new THREE.Color(0xfff3e2), clamp(elD/25, 0, 1));
  /* небо */
  var top = new THREE.Color(0x0a1024).lerp(new THREE.Color(0x79b9ea), day);
  var hor = new THREE.Color(0x161e36).lerp(new THREE.Color(0xdfeaf2), day);
  hor.lerp(new THREE.Color(0xff9d5c), dusk*0.7);
  skyMat.uniforms.skyTop.value.copy(top);
  skyMat.uniforms.skyHor.value.copy(hor);
  skyMat.uniforms.dayT.value = day;
  skyMat.uniforms.dusk.value = dusk;
  skyMat.uniforms.night.value = night;
  skyMat.uniforms.sunCol.value.copy(sun.color);
  skyMat.uniforms.sunDir.value.set(sx, sy, sz);
  /* общий свет */
  ambLight.intensity = 0.07 + 0.26*day;
  hemiLight.intensity = 0.12 + 0.42*day;
  hemiLight.color.copy(hor);
  fill.intensity = 0.32*day;
  fill2.intensity = 0.18*day;
  /* улица: тон дня */
  var tint = new THREE.Color(0x2a3450).lerp(new THREE.Color(0xffffff), day);
  tint.lerp(new THREE.Color(0xffc79a), dusk*0.4);
  OUT_MATS.forEach(function(m){ m.color.copy(tint); });
  /* снег по сезону */
  if (applySnow) applySnow(isWinter());
  /* свет из неба — пересчёт только при заметном изменении */
  var sig = day.toFixed(2) + '|' + dusk.toFixed(2) + '|' + (state.season) + '|' + (isWinter()?1:0);
  if (force || sig !== lastSunSig){
    lastSunSig = sig;
    regenEnv();
  }
}
var lastSunT = 0;""")

# ---------- текстуры зимнего двора: пейнтеры с параметром ----------
rep("var texOutside = ctex(1024,512,function(g,w,h){",
    "function paintOutside(g, w, h, winter){")
rep("""    g.fillStyle='rgba(104,138,88,'+(0.5+R()*0.4).toFixed(2)+')'; g.beginPath(); g.arc(tx, ty, tr, 0, 6.3); g.fill();
  }
});
/* земля далеко внизу (12-й этаж): двор, парковки, шоссе — если смотреть вниз */""",
"""    g.fillStyle='rgba(104,138,88,'+(0.5+R()*0.4).toFixed(2)+')'; g.beginPath(); g.arc(tx, ty, tr, 0, 6.3); g.fill();
  }
  if (winter){                                  /* зима: двор засыпан, дорога проступает */
    g.fillStyle='rgba(244,248,253,.9)'; g.fillRect(0, HZ, w, h-HZ);
    var ry2 = HZ + h*0.02, rh2 = h*0.05;
    g.fillStyle='rgba(148,153,160,.55)'; g.fillRect(0, ry2, w, rh2);
    g.fillStyle='rgba(255,250,235,.45)';
    for (var xw=8; xw<w; xw+=48) g.fillRect(xw, ry2+rh2/2-1.5, 22, 3);
    for (var tw2=0; tw2<36; tw2++){
      var fw=R(), txw=R()*w, tyw=HZ+4+fw*(h-HZ-8), trw=4+fw*26;
      g.fillStyle='rgba(150,158,168,'+(0.25+R()*0.25).toFixed(2)+')';
      g.beginPath(); g.arc(txw, tyw, trw, 0, 6.3); g.fill();
    }
  }
}
var texOutside = ctex(1024,512,function(g,w,h){ paintOutside(g,w,h,false); });
var texOutsideWinter = null;
/* земля далеко внизу (12-й этаж): двор, парковки, шоссе — если смотреть вниз */""")

rep("var texYard = ctex(1024,1024,function(g,w,h){",
    "function paintYard(g, w, h, winter){")
rep("""  g.fillStyle='#d8b56a'; g.fillRect(w*0.42, h*0.60, w*0.14, h*0.10);
  g.fillStyle='#b45b4a'; g.fillRect(w*0.44, h*0.62, 40, 40); g.fillRect(w*0.49, h*0.64, 60, 24);
});""",
"""  g.fillStyle='#d8b56a'; g.fillRect(w*0.42, h*0.60, w*0.14, h*0.10);
  g.fillStyle='#b45b4a'; g.fillRect(w*0.44, h*0.62, 40, 40); g.fillRect(w*0.49, h*0.64, 60, 24);
  if (winter){                                  /* зима: снег, сквозь него дорожки и шоссе */
    g.fillStyle='rgba(245,249,253,.88)'; g.fillRect(0, 0, w, h);
    g.fillStyle='rgba(150,155,162,.5)';
    g.fillRect(w*0.18, 0, 34, h); g.fillRect(0, h*0.34, w, 30); g.fillRect(w*0.62, h*0.34, 30, h*0.66);
    g.fillStyle='rgba(140,146,154,.55)'; g.fillRect(0, h*0.80, w, h*0.13);
    g.fillStyle='rgba(255,250,235,.5)';
    for (var xs=14; xs<w; xs+=80) g.fillRect(xs, h*0.80+h*0.065-3, 40, 6);
  }
}
var texYard = ctex(1024,1024,function(g,w,h){ paintYard(g,w,h,false); });
var texYardWinter = null;""")

# ---------- материал двора — в переменную + реестр улицы ----------
rep("""  var yard = new THREE.Mesh(new THREE.PlaneGeometry(420, 420),
    new THREE.MeshBasicMaterial({ map: texYard }));
  yard.rotation.x = -Math.PI/2;""",
"""  var yardMat = new THREE.MeshBasicMaterial({ map: texYard });
  var yard = new THREE.Mesh(new THREE.PlaneGeometry(420, 420), yardMat);
  yard.rotation.x = -Math.PI/2;""")
rep("""    nb.receiveShadow = true; gRoom.add(nb);
  });""",
"""    nb.receiveShadow = true; gRoom.add(nb);
    OUT_MATS.push(nb.material);
  });
  OUT_MATS.push(M.outside, yardMat, towerMat);""")

# applySnow: переключение текстур двора по сезону
rep("""  /* индексы подсказок/размеров пересобрать по MX */""",
"""  /* зима: снег на дворе и за окном */
  applySnow = function(winter){
    if (!M.outside) return;
    if (winter){
      if (!texOutsideWinter) texOutsideWinter = ctex(1024,512,function(g,w,h){ paintOutside(g,w,h,true); });
      if (!texYardWinter) texYardWinter = ctex(1024,1024,function(g,w,h){ paintYard(g,w,h,true); });
      M.outside.map = texOutsideWinter;
      yardMat.map = texYardWinter;
    } else {
      M.outside.map = texOutside;
      yardMat.map = texYard;
    }
    M.outside.needsUpdate = true;
    yardMat.needsUpdate = true;
  };
  /* индексы подсказок/размеров пересобрать по MX */""")

# ---------- выключатель кухни + лампа по умолчанию выключена ----------
rep("""  var kitLight = new THREE.PointLight(0xffe8c0, 0.45, 6.5, 2);
  kitLight.position.set(mx(4.60), 2.30, 1.10); gRoom.add(kitLight);""",
"""  var kitLight = new THREE.PointLight(0xffe8c0, 0.0, 6.5, 2);   /* включается выключателем, как в жизни */
  kitLight.position.set(mx(4.60), 2.30, 1.10); gRoom.add(kitLight);
  /* выключатель кухни — на южной стене слева от двери */
  (function(){
    var bx = mx(3.62);
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.09, 0.014), M.frame);
    pl.position.set(bx, 1.55, K.z1-0.012); gRoom.add(pl);
    var rock = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.05, 0.014), M.white);
    rock.position.set(bx, 1.55, K.z1-0.022); gRoom.add(rock);
    var sw = { kind:'tap', sub:'switch', on:false, light:kitLight, rocker:rock, bulbs:[M.bulb] };
    pl.userData.tap = sw; tapParts.push(pl);
    rock.userData.tap = sw; tapParts.push(rock);
    TAPS.push(sw);
  })();""")

# ---------- старт + тик ----------
rep("""buildWorld();
applyWallPaint();
applyHandle();""",
"""buildWorld();
applyWallPaint();
applyHandle();
applySun(true);""")

rep("""  if (state.mode === 'walk' && (++bugAim.cnt % 6 === 0)) invHintTick();""",
"""  if (now - lastSunT > 15000){ lastSunT = now; if (state.sunReal !== false && state.autoTime !== false) applySun(); }
  if (state.mode === 'walk' && (++bugAim.cnt % 6 === 0)) invHintTick();""")

# ---------- настройки: блок «Свет» ----------
rep("""          <label class="chk"><input type="checkbox" id="ckMap"><span>Мини-карта в прогулке</span></label>
        </div>""",
"""          <label class="chk"><input type="checkbox" id="ckMap"><span>Мини-карта в прогулке</span></label>
        </div>
        <div class="pblock">
          <h3>Свет · время суток и сезон</h3>
          <label class="chk"><input type="checkbox" id="ckSunReal" checked><span>Реалистичное освещение — солнце, небо, тени как в жизни</span></label>
          <label class="chk"><input type="checkbox" id="ckAutoTime" checked><span>Время — по часам компьютера (живое)</span></label>
          <p style="font-size:12.3px;color:var(--mut);margin:10px 0 4px">Время: <b id="hourLbl">13:00</b></p>
          <input type="range" id="hourR" min="0" max="24" step="0.25" value="13">
          <div class="chips" id="timeChips" style="margin-top:6px">
            <button data-h="7.5">🌅 Утро</button><button data-h="13">☀️ День</button>
            <button data-h="20.5">🌇 Закат</button><button data-h="1">🌙 Ночь</button>
          </div>
          <p style="font-size:12.3px;color:var(--mut);margin:12px 0 4px">Сезон: <b id="seasonLbl">по дате</b></p>
          <div class="chips" id="seasonChips">
            <button data-s="-1">По дате</button><button data-s="0">❄️ Зима</button>
            <button data-s="1">🌱 Весна</button><button data-s="2">☀️ Лето</button><button data-s="3">🍂 Осень</button>
          </div>
          <p style="font-size:11.8px;color:#9a9384;margin-top:8px">Зимой двор и крыши в снегу, солнце низкое. Ночью квартира тёмная — свет включается выключателями у дверей.</p>
        </div>""")

# ---------- вязанка настроек света ----------
rep("""$('#ckSpots').checked = state.spots; $('#ckDims').checked = state.dims;""",
"""$('#ckSpots').checked = state.spots; $('#ckDims').checked = state.dims;
/* свет: время и сезон */
(function(){
  function fmtHour(v){ var h = Math.floor(v)%24, m = Math.round((v - Math.floor(v))*60); return (h<10?'0':'')+h+':'+(m<10?'0':'')+m; }
  var hr = $('#hourR');
  $('#ckSunReal').checked = state.sunReal !== false;
  $('#ckAutoTime').checked = state.autoTime !== false;
  hr.value = state.hour || 13;
  $('#ckSunReal').addEventListener('change', function(e){
    state.sunReal = e.target.checked; save(); applySun(true);
    toast(state.sunReal ? 'Реалистичное освещение: солнце по времени и сезону' : 'Обычный свет вернулся');
  });
  $('#ckAutoTime').addEventListener('change', function(e){
    state.autoTime = e.target.checked; save(); applySun(true);
  });
  function setHour(v){
    state.hour = v; state.autoTime = false; save();
    $('#ckAutoTime').checked = false; hr.value = v;
    $('#hourLbl').textContent = fmtHour(v);
    applySun(true);
  }
  hr.addEventListener('input', function(e){ setHour(+e.target.value); });
  Array.prototype.forEach.call($$('#timeChips button'), function(b){ b.addEventListener('click', function(){ setHour(+b.dataset.h); }); });
  Array.prototype.forEach.call($$('#seasonChips button'), function(b){
    b.addEventListener('click', function(){
      state.season = +b.dataset.s; save();
      $$('#seasonChips button').forEach(function(x){ x.classList.toggle('on', x === b); });
      $('#seasonLbl').textContent = b.textContent.replace(/[^А-Яа-яЁё\\s]/g, '').trim() || 'по дате';
      applySun(true);
    });
  });
  if (state.season >= 0){
    var sb = $$('#seasonChips button').filter(function(x){ return +x.dataset.s === state.season; })[0];
    if (sb){ sb.classList.add('on'); $('#seasonLbl').textContent = sb.textContent.replace(/[^А-Яа-яЁё\\s]/g, '').trim(); }
  }
  $('#hourLbl').textContent = fmtHour(state.autoTime !== false ? nowHour() : (state.hour || 13)) + (state.autoTime !== false ? ' · живое' : '');
  setInterval(function(){
    if (state.autoTime !== false){ var nh = nowHour(); hr.value = nh; $('#hourLbl').textContent = fmtHour(nh) + ' · живое'; }
  }, 20000);
})();""")

# ---------- пресеты: свет ----------
rep("""           wallPat: state.wallPat || 'solid', handle: state.handle || '',""",
"""           wallPat: state.wallPat || 'solid', handle: state.handle || '',
           sunReal: state.sunReal !== false, autoTime: state.autoTime !== false,
           hour: state.hour || 13, season: (typeof state.season === 'number' ? state.season : -1),""")
rep("""  state.wallPat = d.wallPat || 'solid';
  state.handle = d.handle || state.handle;""",
"""  state.wallPat = d.wallPat || 'solid';
  state.handle = d.handle || state.handle;
  if (typeof d.sunReal === 'boolean') state.sunReal = d.sunReal;
  if (typeof d.autoTime === 'boolean') state.autoTime = d.autoTime;
  if (typeof d.hour === 'number') state.hour = d.hour;
  if (typeof d.season === 'number') state.season = d.season;""")
rep("""  applyWallPaint();
  M.front.color.set(state.facade);
  applyHandle();""",
"""  applyWallPaint();
  M.front.color.set(state.facade);
  applyHandle();
  applySun(true);
  if ($('#ckSunReal')) $('#ckSunReal').checked = state.sunReal !== false;
  if ($('#ckAutoTime')) $('#ckAutoTime').checked = state.autoTime !== false;""")

p.write_text(s, encoding='utf-8')
print('T2 ok')
