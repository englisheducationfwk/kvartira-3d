# -*- coding: utf-8 -*-
"""P1: розетки по отметкам (тройная у стола, низкая у пола, в санузле), реалистичный
унитаз; TAB без дребезга (repeat) и без лага (прогрев, легче блюр); P/J/V без
повторов; полный сброс — двухшаговый, без confirm (в окне игры его нет)."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# ---------- розетки ----------
rep("""  sockHole = new THREE.Mesh(new THREE.CircleGeometry(0.042, 20), M.hole);
  sockHole.rotation.y = faceRY(-Math.PI/2); sockHole.position.set(mx(KX-0.016), 1.62, 2.42); gDecals.add(sockHole);""",
"""  sockHole = new THREE.Mesh(new THREE.CircleGeometry(0.042, 20), M.hole);
  sockHole.rotation.y = faceRY(-Math.PI/2); sockHole.position.set(mx(KX-0.016), 1.62, 2.42); gDecals.add(sockHole);
  /* розетки по отметкам: тройная над столом у западной стены, низкая у пола, в санузле */
  function mkSocket(wx, wy, wz, dir, n){
    var D = (n === 3) ? 0.24 : 0.085;
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.085, D), M.frame);
    pl.position.set(wx + dir*0.007, wy, wz); pl.receiveShadow = true;
    (dir > 0 ? gKitchen : gRoom).add(pl);
    ((n === 3) ? [-0.075, 0, 0.075] : [0]).forEach(function(dz){
      var hole = new THREE.Mesh(new THREE.CircleGeometry(0.034, 18), M.hole);
      hole.rotation.y = (dir > 0) ? Math.PI/2 : -Math.PI/2;
      hole.position.set(wx + dir*0.015, wy, wz + dz);
      gDecals.add(hole);
    });
  }
  mkSocket(K.x0, 0.80, 2.138, 1, 3);
  mkSocket(K.x0, 0.16, 0.17, 1, 1);
  mkSocket(K.x1, 1.17, 3.764, -1, 1);""")

# ---------- унитаз реалистичнее ----------
rep("""  IT = item('Унитаз', '🚽', 0.19, 0.28);
  ibox(IT, 5.95, 3.45, 0.38, 0.56, 0, 0.40, M.white);
  ibox(IT, 5.95, 3.24, 0.38, 0.18, 0.40, 0.78, M.white);""",
"""  IT = item('Унитаз', '🚽', 0.19, 0.28);
  (function(){
    var cx = mx(5.95);
    /* бачок с крышкой и кнопкой */
    ibox(IT, 5.95, 3.245, 0.40, 0.17, 0.42, 0.82, M.white);
    var tlid = new THREE.Mesh(new THREE.BoxGeometry(0.43, 0.035, 0.20), M.white);
    tlid.position.set(cx, 0.838, 3.245); tlid.castShadow = true; IT.add(tlid);
    var tbtn = new THREE.Mesh(new THREE.CylinderGeometry(0.027, 0.027, 0.014, 16), M.steel);
    tbtn.position.set(cx, 0.862, 3.245); IT.add(tbtn);
    /* ножка-пьедестал — овальная */
    var tped = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.115, 0.28, 18), M.white);
    tped.scale.set(1, 1, 0.62); tped.position.set(cx, 0.14, 3.50); tped.castShadow = true; IT.add(tped);
    /* чаша — овальная */
    var tbowl = new THREE.Mesh(new THREE.CylinderGeometry(0.20, 0.115, 0.14, 22), M.white);
    tbowl.scale.set(1, 1, 1.45); tbowl.position.set(cx, 0.35, 3.50); tbowl.castShadow = true; IT.add(tbowl);
    /* ободок-сиденье (эллипс) + тёмный проём */
    var tseat = new THREE.Mesh(new THREE.TorusGeometry(0.155, 0.035, 10, 26), M.white);
    tseat.geometry.rotateX(Math.PI/2);
    tseat.scale.set(1, 1, 1.45); tseat.position.set(cx, 0.425, 3.50); tseat.castShadow = true; IT.add(tseat);
    var thole = new THREE.Mesh(new THREE.CircleGeometry(0.12, 22), M.hole);
    thole.geometry.rotateX(-Math.PI/2);
    thole.scale.set(1, 1, 1.45); thole.position.set(cx, 0.428, 3.50); IT.add(thole);
  })();""")

# ---------- TAB: без дребезга + прогрев + легче блюр ----------
rep("""  if (e.code === 'Tab'){
    e.preventDefault();
    if ($('#tabl').classList.contains('hidden')) openTablet('plan'); else closeTablet();
    return;
  }""",
"""  if (e.code === 'Tab'){
    e.preventDefault();
    if (e.repeat) return;                 /* удержание не мигает планшетом */
    if ($('#tabl').classList.contains('hidden')) openTablet('plan'); else closeTablet();
    return;
  }""")

rep("""  if (e.code === 'KeyP'){
    if (held < 0 || !inv[held]){ toast('Сначала возьми предмет (СКМ)'); return; }""",
"""  if (e.code === 'KeyP'){
    if (e.repeat) return;
    if (held < 0 || !inv[held]){ toast('Сначала возьми предмет (СКМ)'); return; }""")

rep("  if (e.code === 'KeyJ' && state.mode === 'walk'){",
    "  if (e.code === 'KeyJ' && state.mode === 'walk' && !e.repeat){")

rep("""  if (e.code === 'KeyV'){
    var to = (state.mode === 'walk') ? 'orbit' : 'walk';""",
"""  if (e.code === 'KeyV' && !e.repeat){
    var to = (state.mode === 'walk') ? 'orbit' : 'walk';""")

rep("""#tabl{position:fixed;inset:0;z-index:80;background:rgba(18,16,12,.55);backdrop-filter:blur(6px);display:grid;place-items:center}""",
"""#tabl{position:fixed;inset:0;z-index:80;background:rgba(18,16,12,.58);backdrop-filter:blur(3px);display:grid;place-items:center}""")

rep("""  tabl.addEventListener('click', function(e){ if (e.target === tabl) closeTablet(); });
})();""",
"""  tabl.addEventListener('click', function(e){ if (e.target === tabl) closeTablet(); });
  /* прогрев: первый показ — без лага */
  tabl.classList.remove('hidden'); void tabl.offsetHeight; tabl.classList.add('hidden');
})();""")

# ---------- полный сброс без confirm (в окне игры он молчит) ----------
rep("""  $('#hardReset').addEventListener('click', function(){
    if (!confirm('Полный сброс: квартира, предметы, цвета и жалобы вернутся к дефолту. Точно?')) return;
    try { localStorage.removeItem(LS); localStorage.removeItem('kitchen3d.presets'); localStorage.removeItem('kitchen3d.bugs'); } catch(e){}
    location.reload();
  });""",
"""  var resetArmed = 0;
  $('#hardReset').addEventListener('click', function(){
    var b = $('#hardReset'), now = Date.now();
    if (now - resetArmed > 5000){
      resetArmed = now;
      b.textContent = '⚠️ Точно всё стереть? Нажми ещё раз (5 сек)';
      toast('Полный сброс: нажми кнопку ещё раз в течение 5 секунд');
      setTimeout(function(){
        if (Date.now() - resetArmed > 4900) b.textContent = '♻️ Полный сброс на дефолт';
      }, 5200);
      return;
    }
    try {
      localStorage.removeItem(LS);
      localStorage.removeItem('kitchen3d.presets');
      localStorage.removeItem('kitchen3d.bugs');
    } catch(e){}
    b.textContent = '♻️ Сброшено — перезапускаю…';
    location.reload();
  });""")

p.write_text(s, encoding='utf-8')
print('P1 ok')
