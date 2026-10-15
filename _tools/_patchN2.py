# -*- coding: utf-8 -*-
"""N2: (1) позиция игрока сохраняется — где вышел, там и появишься;
(2) кухонный эркер по рисунку: три РАВНЫЕ створки 700 — первая диагональная
на скосе (~49° к стене), две прямые на фронте; блок 3×700 как в макете."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# ============ 1) ПОЗИЦИЯ ИГРОКА ============

rep("variant:{}, bought:{}, stepDone:{}, inv:[], moved:{} };",
    "variant:{}, bought:{}, stepDone:{}, inv:[], moved:{}, wpos:null, wyaw:0, wpitch:0 };")

rep("""function walkTo(x, z, yaw, pitch){
  walk.pos.set(mx(x), 0, z); walk.vy = 0;
  walk.yaw = state.mirror ? -(yaw||0) : (yaw||0);
  walk.pitch = pitch || 0;
  walkUpdate(0); paint(); updateMap();
}
""",
"""function walkTo(x, z, yaw, pitch){
  walk.pos.set(mx(x), 0, z); walk.vy = 0;
  walk.yaw = state.mirror ? -(yaw||0) : (yaw||0);
  walk.pitch = pitch || 0;
  walkUpdate(0); paint(); updateMap();
}
/* позиция запоминается сама: где вышел — там и появишься в следующий раз */
var wposT = 0;
function wposSave(){
  if (state.mode !== 'walk') return;
  state.wpos = [ +walk.pos.x.toFixed(3), +walk.pos.z.toFixed(3) ];
  state.wyaw = +walk.yaw.toFixed(3);
  state.wpitch = +walk.pitch.toFixed(3);
  save();
}
function wposRestore(){
  var p = state.wpos;
  if (!p || p.length !== 2 || !isFinite(p[0]) || !isFinite(p[1])) return false;
  if (p[0] < -9 || p[0] > 9 || p[1] < -3 || p[1] > 13) return false;
  walk.pos.set(p[0], 0, p[1]); walk.vy = 0; walk.grounded = true;
  walk.yaw = +state.wyaw || 0;
  walk.pitch = +state.wpitch || 0;
  walkUpdate(0); paint(); updateMap();
  return true;
}
window.addEventListener('beforeunload', wposSave);
document.addEventListener('visibilitychange', function(){ if (document.hidden) wposSave(); });
""")

rep("""  if (state.mode === 'walk'){
    if (walk.locked || Object.keys(walk.keys).some(function(k2){ return walk.keys[k2]; })) walkUpdate(dt);
    updateMap();
  } else if (tween){""",
"""  if (state.mode === 'walk'){
    if (walk.locked || Object.keys(walk.keys).some(function(k2){ return walk.keys[k2]; })) walkUpdate(dt);
    updateMap();
    wposT += dt; if (wposT > 0.9){ wposT = 0; wposSave(); }
  } else if (tween){""")

rep("walkTo(D.walk.spawn.x, D.walk.spawn.z, D.walk.spawn.yaw);",
    "if (!wposRestore()) walkTo(D.walk.spawn.x, D.walk.spawn.z, D.walk.spawn.yaw);")

rep("setViewNow:setViewNow, applyStage:applyStage, paint:paint, setMode:setMode, walkTo:walkTo,",
    "setViewNow:setViewNow, applyStage:applyStage, paint:paint, setMode:setMode, walkTo:walkTo, wposSave:wposSave,")

# ============ 2) ЭРКЕР: ТРИ РАВНЫЕ СТВОРКИ 0.70 ============

rep("""  bay:   { d:0.50, stubL:0.13, diagL:0.52, front:1.70, split:1.00, diagR:0.92, stubR:0.16,
           sillY:1.00, winH:1.50, board:0.20 },""",
"""  /* эркер по рисунку 2100×1500 = 3×700: первая створка — на скосе (диагональ ~49°
     к стене), две такие же прямые на фронте; глубина 50 см */
  bay:   { d:0.50, stubL:0.13, run1:0.572, front:1.58, stubR:0.118,
           sillY:1.00, winH:1.50, board:0.20 },""")

rep("""var BAY = {
  p0: [K.x0 + P.bay.stubL, 0],
  p1: [K.x0 + P.bay.stubL + 0.14, -P.bay.d],
  p2: [K.x0 + P.bay.stubL + 0.14 + P.bay.front, -P.bay.d],
  p3: [K.x1 - P.bay.stubR, 0]
};""",
"""var BAY = {
  p0: [K.x0 + P.bay.stubL, 0],
  p1: [K.x0 + P.bay.stubL + P.bay.run1, -P.bay.d],
  p2: [K.x0 + P.bay.stubL + P.bay.run1 + P.bay.front, -P.bay.d],
  p3: [K.x1 - P.bay.stubR, 0]
};""")

# стойки фронта: узкие по краям (3 см) + средник 12 см — три окна одного размера
rep("""    /* белые стойки по бокам — окна все три одного размера */
    var BWPx = P.bay.winH + P.bay.sillY;
    [0, 1].forEach(function(side){
      var t0 = side ? 1.35/1.70 : 0, t1 = side ? 1 : 0.35/1.70;
      var post = new THREE.Mesh(new THREE.BoxGeometry((t1-t0)*len, BWPx-P.bay.sillY, P.LOAD), M.frame);
      post.position.set(A2[0]+ux*(t0+t1)/2*len, (P.bay.sillY+BWPx)/2, A2[1]+uz*(t0+t1)/2*len);
      post.rotation.y = Math.atan2(-uz, ux);
      post.castShadow = post.receiveShadow = true; gRoom.add(post);
    });""",
"""    /* стойки блока: узкие по краям и средник — створки одинаковые, как в макете */
    var BWPx = P.bay.winH + P.bay.sillY;
    [ [0, 0.03], [0.73, 0.85], [1.55, 1.58] ].forEach(function(pp){
      var pw = pp[1]-pp[0];
      var post = new THREE.Mesh(new THREE.BoxGeometry(pw, BWPx-P.bay.sillY, P.LOAD), M.frame);
      post.position.set(A2[0]+ux*(pp[0]+pw/2), (P.bay.sillY+BWPx)/2, A2[1]+uz*(pp[0]+pw/2));
      post.rotation.y = Math.atan2(-uz, ux);
      post.castShadow = post.receiveShadow = true; gRoom.add(post);
    });""")

# скос: створка ровно 0.70 (как фронтальные) + узкие стойки по краям скоса
rep("""  /* окна на скосах (по 0.48, как просил) — вертикально, открываются кликом */""",
"""  /* створка на левом скосе — такая же, как две фронтальные (0.70), диагональ ~49° */""")

rep("""    var w = 0.50, off = (len - 0.50)/2;""",
"""    var w = 0.70, off = (len - 0.70)/2;""")

rep("""    fr.traverse(function(o){ if (o.isMesh){ o.castShadow = (o.material !== M.glass); o.receiveShadow = true; } });
    gRoom.add(grp);
    var d = { grp: grp, w: w, a0: rot0, a1: rot0 - 1.25, cur: rot0, open:false, anim:null, noSeg:true };""",
"""    fr.traverse(function(o){ if (o.isMesh){ o.castShadow = (o.material !== M.glass); o.receiveShadow = true; } });
    gRoom.add(grp);
    /* стойки по краям скоса — створка скоса ровно как фронтальные */
    [0, 1].forEach(function(s2){
      var t0 = s2 ? (off + w)/len : 0, t1 = s2 ? 1 : off/len;
      if (t1 - t0 < 0.001) return;
      var post = new THREE.Mesh(new THREE.BoxGeometry((t1-t0)*len, hgt, 0.10), M.frame);
      post.position.set(A2[0]+ux*(t0+t1)/2*len, (y0+y1)/2, A2[1]+uz*(t0+t1)/2*len);
      post.rotation.y = rot0;
      post.castShadow = post.receiveShadow = true; gRoom.add(post);
    });
    var d = { grp: grp, w: w, a0: rot0, a1: rot0 - 1.25, cur: rot0, open:false, anim:null, noSeg:true };""")

# фронт: две створки по 0.70
rep("""    var parts = [ [0.50, 0.35], [0.50, 0.85] ];""",
"""    var parts = [ [0.70, 0.03], [0.70, 0.85] ];""")

p.write_text(s, encoding='utf-8')
print('N2 ok')
