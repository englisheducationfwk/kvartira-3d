# -*- coding: utf-8 -*-
"""N3: режим полёта (noclip) по клавише J — летишь сквозь стены куда смотришь,
Пробел — вверх, Ctrl — вниз, Shift — быстрее; состояние и высота запоминаются."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# флаг в walk + сохранение высоты/режима
rep("var walk = { on:false, locked:false, yaw:0, pitch:0, pos:new THREE.Vector3(4.3, 0, 6.6), vy:0, grounded:true, keys:{} };",
    "var walk = { on:false, locked:false, yaw:0, pitch:0, pos:new THREE.Vector3(4.3, 0, 6.6), vy:0, grounded:true, keys:{}, noclip:false };")

rep("variant:{}, bought:{}, stepDone:{}, inv:[], moved:{}, wpos:null, wyaw:0, wpitch:0 };",
    "variant:{}, bought:{}, stepDone:{}, inv:[], moved:{}, wpos:null, wyaw:0, wpitch:0, wpoy:0, noclip:false };")

rep("""  state.wpos = [ +walk.pos.x.toFixed(3), +walk.pos.z.toFixed(3) ];
  state.wyaw = +walk.yaw.toFixed(3);
  state.wpitch = +walk.pitch.toFixed(3);
  save();""",
"""  state.wpos = [ +walk.pos.x.toFixed(3), +walk.pos.z.toFixed(3) ];
  state.wyaw = +walk.yaw.toFixed(3);
  state.wpitch = +walk.pitch.toFixed(3);
  state.wpoy = +walk.pos.y.toFixed(3);
  state.noclip = !!walk.noclip;
  save();""")

rep("""  walk.pos.set(p[0], 0, p[1]); walk.vy = 0; walk.grounded = true;
  walk.yaw = +state.wyaw || 0;
  walk.pitch = +state.wpitch || 0;""",
"""  walk.pos.set(p[0], +state.wpoy || 0, p[1]); walk.vy = 0; walk.grounded = true;
  walk.noclip = !!state.noclip;
  walk.yaw = +state.wyaw || 0;
  walk.pitch = +state.wpitch || 0;""")

# полёт: без гравитации и без стен — куда смотришь
rep("""function walkUpdate(dt){
  var sp = (walk.keys['ShiftLeft']||walk.keys['ShiftRight']) ? 4.4 : 2.2;""",
"""function walkUpdate(dt){
  if (walk.noclip){
    /* режим полёта (J): сквозь стены, куда смотришь; Пробел — вверх, Ctrl — вниз */
    var cp = Math.cos(walk.pitch);
    var fv = new THREE.Vector3(-Math.sin(walk.yaw)*cp, Math.sin(walk.pitch), -Math.cos(walk.yaw)*cp);
    var rv = new THREE.Vector3(-fv.z, 0, fv.x);
    if (rv.lengthSq() < 1e-6) rv.set(1, 0, 0); else rv.normalize();
    var spN = (walk.keys['ShiftLeft']||walk.keys['ShiftRight']) ? 7.5 : 3.0;
    var wn = new THREE.Vector3();
    if (walk.keys['KeyW']||walk.keys['ArrowUp']) wn.add(fv);
    if (walk.keys['KeyS']||walk.keys['ArrowDown']) wn.sub(fv);
    if (walk.keys['KeyD']||walk.keys['ArrowRight']) wn.add(rv);
    if (walk.keys['KeyA']||walk.keys['ArrowLeft']) wn.sub(rv);
    if (walk.keys['Space']) wn.y += 1;
    if (walk.keys['ControlLeft']||walk.keys['ControlRight']) wn.y -= 1;
    if (wn.lengthSq() > 0) wn.normalize().multiplyScalar(spN*dt);
    walk.pos.add(wn);
    walk.vy = 0; walk.grounded = false;
    camera.position.set(walk.pos.x, walk.pos.y+EYE, walk.pos.z);
    camera.rotation.y = walk.yaw;
    camera.rotation.x = walk.pitch;
    camera.rotation.z = 0;
    if (playerCube){
      playerCube.visible = (state.mode === 'walk');
      playerCube.position.set(walk.pos.x, 0.86 + walk.pos.y, walk.pos.z);
      playerCube.rotation.y = walk.yaw;
    }
    return;
  }
  var sp = (walk.keys['ShiftLeft']||walk.keys['ShiftRight']) ? 4.4 : 2.2;""")

# клавиша J
rep("""  walk.keys[e.code] = true;
  if (state.mode === 'walk' && ['Space','KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.code) >= 0) e.preventDefault();""",
"""  walk.keys[e.code] = true;
  if (state.mode === 'walk' && ['Space','KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.code) >= 0) e.preventDefault();
  if (e.code === 'KeyJ' && state.mode === 'walk'){
    walk.noclip = !walk.noclip;
    state.noclip = walk.noclip; state.wpoy = +walk.pos.y.toFixed(3); save();
    toast(walk.noclip
      ? '✈️ Полёт включён: WASD — куда смотришь, Пробел — вверх, Ctrl — вниз, Shift — быстрее. J — выключить'
      : '✈️ Полёт выключен — снова идёшь ногами');
  }""")

# подсказка внизу
rep("· 1–9 слоты · R — поворот · F — что не так · V — обзор · Esc — выйти",
    "· 1–9 слоты · R — поворот · J — полёт · F — что не так · V — обзор · Esc — выйти")

p.write_text(s, encoding='utf-8')
print('N3 ok')
