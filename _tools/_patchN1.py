"""N1: отметки 00:00–00:02 — окна (три одинаковых 0.48: скос, фронт по центру, второй
скос), двери (петли сдвинуты так, что полотно при открывании не проходит сквозь стену),
шкафчик-половинка без низа, у нижних шкафов появились внутренности (полки+задник),
ручки верхних фасадов больше не висят в воздухе, зеркала по умолчанию выкл,
пресеты сохраняют и зеркала вкл/выкл, стены площадки одного цвета — просто стена."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    s = s.replace(old, new, count)


# ================= 1) ОКНА: три одинаковых 0.48 =================
# фронт: одна створка 0.48 по центру + стена по бокам
rep("    var parts = [ [0.85, 0.00], [0.85, 0.85] ];",
    "    var parts = [ [0.48, 0.61] ];")
rep("""    sub(0, 1, 0, P.bay.sillY);                 /* низ по всей ширине */
    sub(0, 1, BWP0, P.HC);                     /* верх по всей ширине */""",
    """    sub(0, 1, 0, P.bay.sillY);                 /* низ по всей ширине */
    sub(0, 1, BWP0, P.HC);                     /* верх по всей ширине */
    sub(0, 0.61/1.70, P.bay.sillY, BWP0);      /* стена слева от створки */
    sub(1.09/1.70, 1, P.bay.sillY, BWP0);      /* стена справа от створки */""")
# второй скос (92): тоже окно 0.48 — как первое
rep("""  [ [ [BAY.p0,BAY.p1], true ], [ [BAY.p1,BAY.p2], false ], [ [BAY.p2,BAY.p3], true ] ].forEach(function(pr, pi){""",
    """  [ [ [BAY.p0,BAY.p1], true ], [ [BAY.p1,BAY.p2], false ], [ [BAY.p2,BAY.p3], true ] ].forEach(function(pr, pi){""")
rep("""    if (pr[1] && pi > 0){                 /* правый скос глухой; на левом — окно */
      var mMid = solidBeam(a, b, P.LOAD, P.bay.sillY, BWP, null, M.facade2, 1.35, gRoom);
      stagedFaces.push({ mesh:mMid, idx:mMid.userData.innerIdx });
    }""",
    """    /* оба скоса — с окнами 0.48, средние полосы глухие не нужны */
    if (false){
      var mMid = solidBeam(a, b, P.LOAD, P.bay.sillY, BWP, null, M.facade2, 1.35, gRoom);
      stagedFaces.push({ mesh:mMid, idx:mMid.userData.innerIdx });
    }""")
rep("""  /* первое окно — вертикально на левом скосе (диагонали), открывается кликом */
  (function(){
    var a = BAY.p0, b = BAY.p1;""",
    """  /* окна на скосах (по 0.48, как просил) — вертикально, открываются кликом */
  [ [BAY.p0, BAY.p1], [BAY.p2, BAY.p3] ].forEach(function(sl){
  (function(){
    var a = sl[0], b = sl[1];""")
rep("""    var d = { grp: grp, w: w, a0: rot0, a1: rot0 - 1.25, cur: rot0, open:false, anim:null, noSeg:true };
    fr.children.forEach(function(o){ doorLeaves.push(o); o.userData.door = d; });
    WIN_SASHES.push(d);
  })();
  /* две створки переднего окна — открываются кликом */""",
    """    var d = { grp: grp, w: w, a0: rot0, a1: rot0 - 1.25, cur: rot0, open:false, anim:null, noSeg:true };
    fr.children.forEach(function(o){ doorLeaves.push(o); o.userData.door = d; });
    WIN_SASHES.push(d);
  })();
  });
  /* створка переднего окна — открывается кликом */""")

# ================= 2) ДВЕРИ: полотно не проходит сквозь стену при открывании =================
rep("    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1-0.01, 0.79, [0,-1], [-1,0]),",
    "    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1-0.025, 0.775, [0,-1], [-1,0]),")
rep("    kit:  mkDoor(3.70, K.z1+P.LOAD/2-0.06, 0.79, [1,0], [0,-1]),",
    "    kit:  mkDoor(3.73, K.z1+P.LOAD/2, 0.77, [1,0], [0,-1]),")
rep("    bath: mkDoor(BA.x0, DH.bath.z0, 0.58, [0,1], [1,0]),",
    "    bath: mkDoor(BA.x0+0.03, DH.bath.z0, 0.58, [0,1], [1,0]),")
rep("    ent:  mkDoor(DH.ent.x1-0.02, HA.z1+P.LOAD, 0.88, [-1,0], [0,1], true)",
    "    ent:  mkDoor(DH.ent.x1-0.02, HA.z1+P.LOAD+0.03, 0.88, [-1,0], [0,1], true)")

# ================= 3) КУХНЯ =================
# 3а) шкафчик-половинка: убрать полку и задник снизу — низ полностью открыт
rep("""      var shelf2 = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.03, UZD-0.02), M.carcass);
      shelf2.position.set(mx(KX-0.17), UYM-0.02, uz); shelf2.castShadow = shelf2.receiveShadow = true;
      upGrp.add(shelf2);
      var back2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.carcass);
      back2.position.set(mx(KX-0.335), (UY0+UYM)/2, uz); upGrp.add(back2);
""", "")
# 3б) ручки верхних фасадов — на своём месте (были в локальных координатах — свисали к полу)
rep("      uhh.position.set(-0.025, (UPH/2-0.03)-0.075, UZD-0.02-0.055);",
    "      uhh.position.set(-0.025, UYM+0.045, UZD-0.02-0.055);")
rep("      uh.position.set(-0.025, UY0-UYM+0.09, UZD-0.02-0.055);",
    "      uh.position.set(-0.025, UY0+0.09, UZD-0.02-0.055);")
# 3в) нижние шкафы: полые внутри — полки + тёмный задник видны при открытой дверце
rep("""  solidBox(KX-0.60, KX-0.01, 0.50, 2.99, BASE, BASE+LOWH, { nx:M.carcass, side:M.carcass }, 1, ITcnt);
  solidBox(KX-0.60, KX-0.01, 0.50, 2.99, 0, BASE, { side:M.dark }, 1, ITcnt);""",
    """  /* корпус низа — полый: дно, крышка, задник, стойки; внутри полки */
  solidBox(KX-0.60, KX-0.01, 0.50, 2.99, 0, BASE, { side:M.dark }, 1, ITcnt);
  solidBox(KX-0.60, KX-0.01, 0.50, 2.99, BASE, BASE+0.03, { side:M.carcass }, 1, ITcnt);
  solidBox(KX-0.60, KX-0.01, 0.50, 2.99, BASE+LOWH-0.03, BASE+LOWH, { side:M.carcass }, 1, ITcnt);
  solidBox(KX-0.04, KX-0.01, 0.50, 2.99, BASE, BASE+LOWH, { side:M.dark, nx:M.dark }, 1, ITcnt);
  solidBox(KX-0.60, KX-0.01, 0.50, 0.52, BASE, BASE+LOWH, { side:M.carcass }, 1, ITcnt);
  solidBox(KX-0.60, KX-0.01, 2.97, 2.99, BASE, BASE+LOWH, { side:M.carcass }, 1, ITcnt);
  for (var i2d=0;i2d<4;i2d++){
    solidBox(KX-0.60, KX-0.01, 1.11+i2d*0.6225, 1.13+i2d*0.6225, BASE, BASE+LOWH, { side:M.carcass }, 1, ITcnt);
  }
  for (var i2s=0;i2s<4;i2s++){
    var zc2 = 0.81 + i2s*0.6225;
    solidBox(KX-0.58, KX-0.03, zc2-0.29, zc2+0.29, BASE+0.30, BASE+0.33, { side:M.carcass }, 1, ITcnt);
  }""")

# ================= 4) ЗЕРКАЛА: по умолчанию выкл; пресеты сохраняют вкл/выкл =================
rep("              spots:true, dims:false, furn:true, map:false, mirrOn:true, view:'overview',",
    "              spots:true, dims:false, furn:true, map:false, mirrOn:false, view:'overview',")
rep("""function snapshot(){
  return { inv: state.inv.slice(), moved: JSON.parse(JSON.stringify(state.moved)),
           wall: state.wall, facade: state.facade, stage: state.stage, mirror: state.mirror };
}""",
    """function snapshot(){
  return { inv: state.inv.slice(), moved: JSON.parse(JSON.stringify(state.moved)),
           wall: state.wall, facade: state.facade, stage: state.stage, mirror: state.mirror,
           mirrOn: state.mirrOn !== false, spots: state.spots, dims: state.dims, map: state.map };
}""")
rep("""  state.mirror = !!d.mirror;
  save();
  if (flip) flipView();""",
    """  state.mirror = !!d.mirror;
  if (typeof d.mirrOn === 'boolean') state.mirrOn = d.mirrOn;
  if (typeof d.spots === 'boolean') state.spots = d.spots;
  if (typeof d.dims === 'boolean') state.dims = d.dims;
  if (typeof d.map === 'boolean') state.map = d.map;
  applyMirrors();
  if ($('#ckMirr')) $('#ckMirr').checked = state.mirrOn !== false;
  save();
  if (flip) flipView();""")

# ================= 5) СТЕНЫ ПЛОЩАДКИ — одного цвета, просто стена =================
rep("""      var nz = new THREE.Mesh(new THREE.BoxGeometry(K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.concrete,M.concrete]);""",
    """      var nz = new THREE.Mesh(new THREE.BoxGeometry(K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.hallWall,M.concrete]);""")
rep("""      var nz2 = new THREE.Mesh(new THREE.BoxGeometry(L1+0.12-(K.x1+P.LOAD), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.concrete,M.concrete]);""",
    """      var nz2 = new THREE.Mesh(new THREE.BoxGeometry(L1+0.12-(K.x1+P.LOAD), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.hallWall,M.concrete]);""")

p.write_text(s, encoding='utf-8')
print('N1 ok')
