# -*- coding: utf-8 -*-
"""R1: плесень у эркера (только там), подсказки «вентшахта» и «розетка» перевешены
на реальные места, восточная розетка убрана, лоджия расчищена, точки-подсказки:
своя комната — ярко, чужие — блеклые; лок 144 fps."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:130]
    s = s.replace(old, new, 1)


# 1) лоджия — расчищена
rep("""  /* лоджия */
  IT = item('Табурет', '🪑', 0.18, 0.18);
  ibox(IT, 0.55, -0.75, 0.36, 0.36, 0, 0.42, M.wood);
  IT = item('Ящик', '📦', 0.23, 0.28);
  ibox(IT, 1.85, -0.70, 0.45, 0.55, 0, 0.34, M.woodDark);""",
"""  /* лоджия — пустая, расчищена (по отметке) */""")

# 2) восточная розетка убрана (по отметке «тут розетки нет»)
rep("""  socket = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.085, 0.085), M.frame);
  socket.position.set(mx(KX-0.017), 1.62, 2.42); gKitchen.add(socket);
  sockHole = new THREE.Mesh(new THREE.CircleGeometry(0.042, 20), M.hole);
  sockHole.rotation.y = faceRY(-Math.PI/2); sockHole.position.set(mx(KX-0.016), 1.62, 2.42); gDecals.add(sockHole);""",
"""  /* (восточная розетка убрана — по отметке «тут розетки нет»; настоящая — тройная на западной стене) */""")

# 3) плесень — только у эркера (на полу и на низу стенки)
rep("""  mold1 = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 0.4), M.mold);
  mold1.rotation.y = faceRY(-Math.PI/2); mold1.position.set(mx(KX-0.016), 0.24, 0.62); gDecals.add(mold1);
  mold2 = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.3), M.mold);
  mold2.position.set(mx(KX-0.14), 0.22, 0.016); gDecals.add(mold2);""",
"""  mold1 = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 0.4), M.mold);
  mold1.geometry.rotateX(-Math.PI/2);                 /* плесень на полу у эркера */
  mold1.position.set(mx(5.42), 0.012, -0.26); gDecals.add(mold1);
  mold2 = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.3), M.mold);
  mold2.position.set(mx(5.42), 0.15, -0.415); gDecals.add(mold2);   /* и на низу стенки эркера */""")

# 4) подсказки на реальные места: вентшахта — круглый вывод, розетка — тройная у стола
rep("  vent:     [ [6.05, 1.85, 2.80],        [-1,0,0] ],",
    "  vent:     [ [4.95, 2.28, 2.94],        [0,0,-1] ],")
rep("  socket:   [ [K.x1-0.05, 1.62, 2.42],   [-1,0,0] ],",
    "  socket:   [ [K.x0+0.07, 0.86, 2.14],   [1,0,0] ],")
rep("  mold:     [ [K.x1-0.06, 0.26, 0.66],   [-1,0,0] ],",
    "  mold:     [ [5.42, 0.16, -0.30],       [0,1,0] ],")

# 5) точки-пометки: своя комната — ярко, чужие — блеклые
rep("""function updateOverlays(){
  var show = state.spots;   /* пометки «что где делать» видны и в игре */
  hsEls.forEach(function(x){
    var v = project(x.anchor, scr);
    if (v.behind){ x.el.style.opacity = '0'; return; }
    var f = camera.position.clone().sub(x.anchor).normalize();
    var n = new THREE.Vector3(x.nrm[0] * (state.mirror?-1:1), x.nrm[1], x.nrm[2]);
    var facing = n.dot(f) > -0.25;
    x.el.style.transform = 'translate(-50%,-50%) translate('+(v.x+14)+'px,'+(v.y-14)+'px)';
    x.el.style.opacity = show ? (facing?1:0.3) : 0;
    x.el.style.pointerEvents = show ? 'auto' : 'none';
  });""",
"""function updateOverlays(){
  var show = state.spots;   /* пометки «что где делать» видны и в игре */
  var curRoom = flatPlace(camera.position.x, camera.position.z);
  hsEls.forEach(function(x){
    var v = project(x.anchor, scr);
    if (v.behind){ x.el.style.opacity = '0'; return; }
    var f = camera.position.clone().sub(x.anchor).normalize();
    var n = new THREE.Vector3(x.nrm[0] * (state.mirror?-1:1), x.nrm[1], x.nrm[2]);
    var facing = n.dot(f) > -0.25;
    x.el.style.transform = 'translate(-50%,-50%) translate('+(v.x+14)+'px,'+(v.y-14)+'px)';
    var sameRoom = (flatPlace(x.anchor.x, x.anchor.z) === curRoom);
    x.el.style.opacity = show ? (sameRoom ? (facing?1:0.35) : 0.15) : 0;
    x.el.style.pointerEvents = show ? 'auto' : 'none';
  });""")

# 6) лок 144 fps
rep("""function tick(){
  requestAnimationFrame(tick);
  var now = performance.now(), dt = Math.min(0.05, (now-lastT)/1000); lastT = now;""",
"""function tick(){
  requestAnimationFrame(tick);
  var now = performance.now();
  if (now - lastT < 1000/144 - 0.7) return;   /* лок 144 fps */
  var dt = Math.min(0.05, (now-lastT)/1000); lastT = now;""")

p.write_text(s, encoding='utf-8')
print('R1 ok')
