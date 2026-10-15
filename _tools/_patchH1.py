"""H1: юг — коридор за санузлом в 2.2 раза шире (входная дверь дальше на ~1.1 м),
ручка входной на западной стороне (петля на восточной), ниша-выпирание у входа убрана,
лифты убраны (просто стена), дверь соседа, плинтусы не лежат на полу,
петли дверей не заходят в стены, комод и подписи переставлены."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# --- коридор шире: hall тянется до 7,44
rep("  hall:  { x0:3.57, x1:4.45, z0:3.16, z1:6.32 },",
    "  hall:  { x0:3.57, x1:4.45, z0:3.16, z1:7.44 },")

# --- перегородка комната/коридор тянется до новой южной стены
rep("  solidBox(K.x0-P.LOAD, K.x0, DH.room.z1, P.room.z1+P.LOAD, 0, P.HC, { px:M.wall2, nx:M.wall2 });",
    "  solidBox(K.x0-P.LOAD, K.x0, DH.room.z1, HA.z1+P.LOAD, 0, P.HC, { px:M.wall2, nx:M.wall2 });")
rep("  seg(K.x0-P.LOAD/2, DH.room.z1, K.x0-P.LOAD/2, P.room.z1+0.16, P.LOAD/2);",
    "  seg(K.x0-P.LOAD/2, DH.room.z1, K.x0-P.LOAD/2, HA.z1+0.16, P.LOAD/2);")

# --- южные стены: комната на 6,32; коридор на 7,44 с входной дверью
rep("""  /* нижняя стена (ко входу) z=5.60 с входной дверью */
  solidBox(P.room.x0, DH.ent.x0, P.room.z1, P.room.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(DH.ent.x0, DH.ent.x1, P.room.z1, P.room.z1+P.LOAD, DH.ent.h, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(DH.ent.x1, BA.x0, P.room.z1, P.room.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  /* южная стена санузла — она же северная стена коридора перед ним */
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 0, 2.10, { pz:M.wall2, nz:M.tile2 });
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 2.10, P.HC, { pz:M.wall2, nz:M.wall2 });
  /* южная стена квартиры за санузлом — продолжение входной во всю ширину */
  solidBox(BA.x0, BA.x1+P.LOAD, HA.z1, HA.z1+P.LOAD, 0, 2.10, { pz:M.hallWall, nz:M.wall2 });
  solidBox(BA.x0, BA.x1+P.LOAD, HA.z1, HA.z1+P.LOAD, 2.10, P.HC, { pz:M.hallWall, nz:M.wall2 });
  seg(BA.x0, HA.z1+P.LOAD/2, BA.x1+P.LOAD, HA.z1+P.LOAD/2, P.LOAD/2);
  seg(P.room.x0, P.room.z1+P.LOAD/2, DH.ent.x0, P.room.z1+P.LOAD/2, P.LOAD/2);
  seg(DH.ent.x1, P.room.z1+P.LOAD/2, BA.x0, P.room.z1+P.LOAD/2, P.LOAD/2);
  seg(BA.x0, BA.z1+P.LOAD/2, BA.x1+P.LOAD, BA.z1+P.LOAD/2, P.LOAD/2);""",
    """  /* южная стена комнаты z=6,32 — до перегородки */
  solidBox(P.room.x0, K.x0-P.LOAD, P.room.z1, P.room.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  seg(P.room.x0, P.room.z1+P.LOAD/2, K.x0-P.LOAD, P.room.z1+P.LOAD/2, P.LOAD/2);
  /* южная стена коридора z=7,44 с входной дверью (коридор глубже на ~1,1 м) */
  solidBox(K.x0-P.LOAD, DH.ent.x0, HA.z1, HA.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(DH.ent.x0, DH.ent.x1, HA.z1, HA.z1+P.LOAD, DH.ent.h, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(DH.ent.x1, BA.x1+P.LOAD, HA.z1, HA.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  seg(K.x0-P.LOAD, HA.z1+P.LOAD/2, DH.ent.x0, HA.z1+P.LOAD/2, P.LOAD/2);
  seg(DH.ent.x1, HA.z1+P.LOAD/2, BA.x1+P.LOAD, HA.z1+P.LOAD/2, P.LOAD/2);
  /* южная стена санузла — она же северная стена коридора перед ним */
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 0, 2.10, { pz:M.wall2, nz:M.tile2 });
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 2.10, P.HC+0.06, { pz:M.wall2, nz:M.wall2 });
  seg(BA.x0, BA.z1+P.LOAD/2, BA.x1+P.LOAD, BA.z1+P.LOAD/2, P.LOAD/2);""")

# --- полы: шов в дверях санузла убран; пол коридора до новой стены; узкая полоса у входа
rep("  floorBox(HA, M.lam, 0.5);",
    "  floorBox({ x0:HA.x0, x1:4.41, z0:HA.z0, z1:HA.z1 }, M.lam, 0.5);")
rep("  floorBox(BA, M.bathFloor, 4);",
    "  floorBox({ x0:4.57, x1:BA.x1, z0:BA.z0, z1:BA.z1 }, M.bathFloor, 4);")
rep("  floorBox({ x0:4.61, x1:6.47, z0:5.60, z1:6.32 }, M.lam, 0.5);   /* коридор за санузлом */",
    "  floorBox({ x0:4.61, x1:6.47, z0:5.60, z1:7.44 }, M.lam, 0.5);   /* коридор за санузлом */")

# --- потолки: коридорный кусок встык (без наложений), потолок полосы у входа
rep("  ceilPlane({ x0:4.61, x1:6.47, z0:5.60, z1:6.32 });",
    "  ceilPlane({ x0:5.05, x1:6.47, z0:6.12, z1:7.44 });\n  ceilPlane({ x0:2.70, x1:3.11, z0:6.78, z1:7.30 });")

# --- плинтусы: не лежат на полу, разрез на дверях
rep("  plZ(K.x0+0.01, 3.17, P.room.z1-0.01); plZ(HA.x1-0.01, 3.17, DH.bath.z0); plZ(HA.x1-0.01, DH.bath.z1, P.room.z1-0.01);",
    "  plZ(K.x0+0.01, 3.17, DH.room.z0); plZ(K.x0+0.01, DH.room.z1, HA.z1-0.01);\n  plZ(HA.x1-0.01, 3.17, DH.bath.z0); plZ(HA.x1-0.01, DH.bath.z1, BA.z1+P.LOAD);")
rep("  pl(HA.x1+0.01, P.room.z1-0.01, DH.ent.x1+0.05, P.room.z1-0.01); pl(DH.ent.x0-0.05, P.room.z1-0.01, K.x0+0.01, P.room.z1-0.01);",
    "  pl(HA.x1+0.01, HA.z1-0.01, BA.x1+P.LOAD-0.02, HA.z1-0.01);")
rep("  pl(P.room.x0+0.01, P.room.z1-0.01, DH.ent.x0, P.room.z1-0.01);",
    "  pl(P.room.x0+0.01, P.room.z1-0.01, K.x0-P.LOAD, P.room.z1-0.01);")

# --- площадка: западная стена от южной стены комнаты, ниша у входа убрана, лифты убраны
rep("""    w(L0-0.12, L0, (WZ+LAND.z1)/2, 0.12);""",
    """    w(L0-0.12, L0, (P.room.z1+P.LOAD+LAND.z1)/2, 0.12);
    slab(L0, K.x0-P.LOAD, P.room.z1+P.LOAD, WZ);          /* полоса у входа */
    clg(L0, K.x0-P.LOAD, P.room.z1+P.LOAD, WZ);""")
rep("""    seg(LAND.x0, WZ, LAND.x0, LAND.z1, 0.08);""",
    """    seg(LAND.x0, P.room.z1, LAND.x0, LAND.z1, 0.08);""")
rep("""    /* входная дверь — открыта на площадку, в выемке (нише) по БТИ: ниша справа и напротив двери */
    var vest = 0.34;
    var vr1 = new THREE.Mesh(new THREE.BoxGeometry(0.09, 2.72, vest), M.hallWall);
    vr1.position.set(E0-0.045, 1.36, WZ+vest/2); vr1.receiveShadow = true; g.add(vr1);
    var vr2 = vr1.clone(); vr2.position.x = E1+0.045; g.add(vr2);
    var vr3 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0+0.18, 0.62, vest), M.hallWall);
    vr3.position.set((E0+E1)/2, 2.41, WZ+vest/2); vr3.receiveShadow = true; g.add(vr3);
    var th1 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0, 0.02, vest), M.concrete);
    th1.position.set((E0+E1)/2, 0.01, WZ+vest/2); g.add(th1);
    var nsh1 = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.03, 0.26), M.wood);
    nsh1.position.set(E0-0.045, 1.15, WZ+0.17); g.add(nsh1);
    var nsh2 = nsh1.clone(); nsh2.position.x = E1+0.045; g.add(nsh2);""",
    """    /* ниша-выемка у двери убрана — стена просто ровная (по отметке) */""")
rep("""    /* лифты напротив */
    [[3.0,4.0],[4.7,5.7]].forEach(function(lf){
      var a = mx(lf[0]), b = mx(lf[1]); if (a > b){ var t2 = a; a = b; b = t2; }
      var dr = new THREE.Mesh(new THREE.BoxGeometry(b-a, 2.05, 0.08), M.lift);
      dr.position.set((a+b)/2, 1.06, LAND.z1-0.09); g.add(dr);
      var fr = new THREE.Mesh(new THREE.BoxGeometry(b-a+0.14, 2.12, 0.05), M.steel);
      fr.position.set((a+b)/2, 1.08, LAND.z1-0.16); g.add(fr);
      var btn = new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.03,0.03,12), M.white);
      btn.rotation.x = Math.PI/2; btn.position.set(b+0.35, 1.1, LAND.z1-0.20); g.add(btn);
    });""",
    """    /* просто стены (лифты убраны по отметке) + дверь соседа на западной стене */
    (function(){
      var nf = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.14, 1.00), M.frame);
      nf.position.set(L0+0.015, 1.07, 7.83); g.add(nf);
      var nd = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.05, 0.88), M.doorMetal);
      nd.position.set(L0+0.055, 1.025, 7.83); nd.castShadow = true; g.add(nd);
      var nh = new THREE.Mesh(new THREE.CylinderGeometry(0.012,0.012,0.10,10), M.chrome);
      nh.rotation.x = Math.PI/2; nh.position.set(L0+0.09, 1.02, 7.52); g.add(nh);
    })();""")

# --- двери: входная петлёй на восток (ручка с запада), у всех петель подрезка от стен
rep("""  DOORS = {
    kit:  mkDoor(3.70, K.z1+P.LOAD/2, 0.79, [1,0], [0,-1]),
    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1, 0.78, [0,-1], [-1,0]),
    bath: mkDoor(4.49, DH.bath.z0, 0.58, [0,1], [1,0]),
    balc: mkDoor(RB.doorX0, 0, 0.78, [1,0], [0,1]),""",
    """  DOORS = {
    kit:  mkDoor(3.70, K.z1+P.LOAD/2-0.04, 0.79, [1,0], [0,-1]),
    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1-0.04, 0.82, [0,-1], [-1,0]),
    bath: mkDoor(BA.x0, DH.bath.z0, 0.58, [0,1], [1,0]),
    balc: mkDoor(RB.doorX0, 0, 0.78, [1,0], [0,1]),""")
rep("    ent:  mkDoor(DH.ent.x0, P.room.z1+P.LOAD/2, 0.88, [1,0], [0,1], true)",
    "    ent:  mkDoor(DH.ent.x1-0.02, HA.z1+P.LOAD/2, 0.88, [-1,0], [0,1], true)")

# --- маркер двери для универсального «использовать»
rep("""  var d = { grp: grp, w: w, a0: rot0, a1: rot1, cur: rot0, open: false, anim: null,""",
    """  var d = { kind:'door', grp: grp, w: w, a0: rot0, a1: rot1, cur: rot0, open: false, anim: null,""")

# --- комод к восточной стене пошире, подписи
rep("""  IT = item('Комод', '🗄', 0.12, 0.225);
  ibox(IT, 6.32, 5.865, 0.24, 0.45, 0, 0.85, M.wood);
  for (var ci=0; ci<3; ci++){
    ibox(IT, 6.196, 5.865, 0.012, 0.40, 0.10+ci*0.25, 0.30+ci*0.25, M.woodDark);
    ibox(IT, 6.188, 5.865, 0.012, 0.10, 0.205+ci*0.25, 0.235+ci*0.25, M.steel);
  }""",
    """  IT = item('Комод', '🗄', 0.13, 0.24);
  ibox(IT, 6.32, 6.56, 0.26, 0.48, 0, 0.85, M.wood);
  for (var ci=0; ci<3; ci++){
    ibox(IT, 6.178, 6.56, 0.012, 0.42, 0.10+ci*0.25, 0.30+ci*0.25, M.woodDark);
    ibox(IT, 6.17, 6.56, 0.012, 0.10, 0.205+ci*0.25, 0.235+ci*0.25, M.steel);
  }""")
rep("  entrance: [ [4.05, 1.55, 6.95],        [0,0,-1] ]",
    "  entrance: [ [4.05, 1.55, 8.30],        [0,0,-1] ]")
rep("  { p:[4.05, 1.55, 7.05], t:'площадка · лифт · кв. 278' }",
    "  { p:[4.05, 1.55, 8.45], t:'площадка · стена · кв. 278' }")

p.write_text(s, encoding='utf-8')
print('H1 ok')

# --- data.json: спавн на площадке глубже
d = pathlib.Path('_tools/data.json')
t = d.read_text(encoding='utf-8')
old = '"spawn": {"x": 4.2, "z": 7.0, "yaw": 0.0,'
assert old in t
t = t.replace(old, '"spawn": {"x": 4.2, "z": 8.3, "yaw": 0.0,', 1)
d.write_text(t, encoding='utf-8')
import json; json.loads(t)
print('H1 data ok')
