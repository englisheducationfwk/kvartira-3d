"""G5: юг квартиры — вместо ниши площадки за санузлом настоящий коридор внутри
квартиры (зеркало + комод), стена площадки убрана, комод к восточной стене,
входная стена тянется во всю ширину, площадка глубже на метр."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:120]
    s = s.replace(old, new, count)


# --- площадка глубже на метр
rep("var LAND = { x0:2.4, x1:6.9, z0:5.68, z1:7.9 };",
    "var LAND = { x0:2.4, x1:6.9, z0:5.68, z1:8.9 };")
rep("var FLAT = { x0:-0.95, x1:7.27, z0:-1.60, z1:8.10 };",
    "var FLAT = { x0:-0.95, x1:7.27, z0:-1.60, z1:9.10 };")

# --- восточная межквартирная: плитка только у санузла, дальше обои (коридор)
rep("""  solidBox(K.x1, K.x1+P.LOAD, BA.z0, P.room.z1+P.LOAD, 0, 2.10, { nx:M.tile2 });
  solidBox(K.x1, K.x1+P.LOAD, BA.z0, P.room.z1+P.LOAD, 2.10, P.HC, { nx:M.wall2 });""",
    """  solidBox(K.x1, K.x1+P.LOAD, BA.z0, BA.z1, 0, 2.10, { nx:M.tile2 });
  solidBox(K.x1, K.x1+P.LOAD, BA.z0, BA.z1, 2.10, P.HC, { nx:M.wall2 });
  solidBox(K.x1, K.x1+P.LOAD, BA.z1+P.LOAD, HA.z1+P.LOAD, 0, P.HC, { nx:M.wall2 });""")

# --- южная стена санузла = северная стена коридора (обои), плюс южная стена квартиры во всю ширину
rep("""  /* южная стена санузла осталась на месте — за ней ниша площадки */
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 0, 2.10, { pz:M.hallWall, nz:M.tile2 });
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 2.10, P.HC, { pz:M.hallWall, nz:M.wall2 });""",
    """  /* южная стена санузла — она же северная стена коридора перед ним */
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 0, 2.10, { pz:M.wall2, nz:M.tile2 });
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 2.10, P.HC, { pz:M.wall2, nz:M.wall2 });
  /* южная стена квартиры за санузлом — продолжение входной во всю ширину */
  solidBox(BA.x0, BA.x1+P.LOAD, HA.z1, HA.z1+P.LOAD, 0, 2.10, { pz:M.hallWall, nz:M.wall2 });
  solidBox(BA.x0, BA.x1+P.LOAD, HA.z1, HA.z1+P.LOAD, 2.10, P.HC, { pz:M.hallWall, nz:M.wall2 });
  seg(BA.x0, HA.z1+P.LOAD/2, BA.x1+P.LOAD, HA.z1+P.LOAD/2, P.LOAD/2);""")

# --- перегородка санузла укорачивается до его южной стены (дальше открытый коридор)
rep("""  solidBox(HA.x1, BA.x0, DH.bath.z1, HA.z1, 0, 2.10, { px:M.tile2, nx:M.wall2 });
  solidBox(HA.x1, BA.x0, DH.bath.z1, HA.z1, 2.10, P.HC, { px:M.wall2, nx:M.wall2 });
  /* продолжение перегородки: торцы мини-коридора и ниши площадки */
  solidBox(HA.x1, BA.x0, HA.z1, HA.z1+P.LOAD, 0, P.HC, { px:M.hallWall, nx:M.hallWall });
  seg((HA.x1+BA.x0)/2, K.z1+P.LOAD, (HA.x1+BA.x0)/2, DH.bath.z0, P.PART/2);
  seg((HA.x1+BA.x0)/2, DH.bath.z1, (HA.x1+BA.x0)/2, HA.z1+0.16, P.PART/2);""",
    """  solidBox(HA.x1, BA.x0, DH.bath.z1, BA.z1+P.LOAD, 0, 2.10, { px:M.tile2, nx:M.wall2 });
  solidBox(HA.x1, BA.x0, DH.bath.z1, BA.z1+P.LOAD, 2.10, P.HC, { px:M.wall2, nx:M.wall2 });
  /* дальше на юг перегородки нет — там общий коридор перед санузлом */
  seg((HA.x1+BA.x0)/2, K.z1+P.LOAD, (HA.x1+BA.x0)/2, DH.bath.z0, P.PART/2);
  seg((HA.x1+BA.x0)/2, DH.bath.z1, (HA.x1+BA.x0)/2, BA.z1+P.LOAD, P.PART/2);""")

# --- полы: коридор за санузлом + пол эркера без «затекстуренной» щели
rep("  floorBox(K, M.lino, 1.0);",
    "  floorBox({ x0:K.x0, x1:K.x1, z0:-0.50, z1:K.z1 }, M.lino, 1.0);   /* включая пол эркера */")
rep("  floorBox(BA, M.bathFloor, 4);",
    """  floorBox(BA, M.bathFloor, 4);
  floorBox({ x0:4.61, x1:6.47, z0:5.60, z1:6.32 }, M.lam, 0.5);   /* коридор за санузлом */""")
rep("  ceilPlane(P.room); ceilPlane(K); ceilPlane(HA); ceilPlane(BA);",
    """  ceilPlane(P.room); ceilPlane(K); ceilPlane(HA); ceilPlane(BA);
  ceilPlane({ x0:4.61, x1:6.47, z0:5.60, z1:6.32 });""")

# --- площадка: одна плита пола/потолка, стены вокруг
rep("""    var WZ = HA.z1 + P.LOAD;                       /* южная плоскость входной стены */
    var BW = Math.min(mx(BA.x0), mx(BA.x1));       /* восточная плита начинается у санузла */""",
    """    var WZ = HA.z1 + P.LOAD;                       /* южная плоскость входной стены */""")
rep("""    slab(L0, BW, WZ, LAND.z1);
    slab(BW, L1, LAND.z0, LAND.z1);""",
    "    slab(L0, L1, WZ, LAND.z1);")
rep("""    clg(L0, BW, WZ, LAND.z1);
    clg(BW, L1, LAND.z0, LAND.z1);""",
    "    clg(L0, L1, WZ, LAND.z1);")
rep("""    w(L0-0.12, L0, (WZ+LAND.z1)/2, 0.12);
    w(L1, L1+0.12, (LAND.z0+LAND.z1)/2, 0.12);
    w(L0, L1, LAND.z1, 0.12);
    /* север: входная стена квартиры (E0..E1 — дверь) и стена санузла за нишей */
    w(L0-0.12, E0, WZ, 0.12);
    w(E1, BW, WZ, 0.12);
    w(E0, E1, WZ, 0.12, 2.10, 2.72);
    w(BW, L1+0.12, LAND.z0, 0.12);
    seg(BW, LAND.z0, LAND.x1, LAND.z0, 0.07);
    seg(LAND.x0, WZ, LAND.x0, LAND.z1, 0.08);
    seg(LAND.x1, LAND.z0, LAND.x1, LAND.z1, 0.08);
    seg(LAND.x0, LAND.z1, LAND.x1, LAND.z1, 0.08);""",
    """    w(L0-0.12, L0, (WZ+LAND.z1)/2, 0.12);
    w(L1, L1+0.12, (WZ+LAND.z1)/2, 0.12);
    w(L0, L1, LAND.z1, 0.12);
    /* север — стена квартиры целиком (входная дверь в нише, см. ниже) */
    seg(LAND.x0, WZ, LAND.x0, LAND.z1, 0.08);
    seg(LAND.x1, WZ, LAND.x1, LAND.z1, 0.08);
    seg(LAND.x0, LAND.z1, LAND.x1, LAND.z1, 0.08);""")

# --- комод: к восточной стене коридора (где хозяин его и поставил)
rep("""  IT = item('Комод', '🗄', 0.12, 0.225);
  ibox(IT, 4.30, 5.885, 0.24, 0.45, 0, 0.85, M.wood);
  for (var ci=0; ci<3; ci++){
    ibox(IT, 4.172, 5.885, 0.012, 0.40, 0.10+ci*0.25, 0.30+ci*0.25, M.woodDark);
    ibox(IT, 4.164, 5.885, 0.012, 0.10, 0.205+ci*0.25, 0.235+ci*0.25, M.steel);
  }""",
    """  IT = item('Комод', '🗄', 0.12, 0.225);
  ibox(IT, 6.32, 5.865, 0.24, 0.45, 0, 0.85, M.wood);
  for (var ci=0; ci<3; ci++){
    ibox(IT, 6.196, 5.865, 0.012, 0.40, 0.10+ci*0.25, 0.30+ci*0.25, M.woodDark);
    ibox(IT, 6.188, 5.865, 0.012, 0.10, 0.205+ci*0.25, 0.235+ci*0.25, M.steel);
  }""")

p.write_text(s, encoding='utf-8')
print('G5 ok')
