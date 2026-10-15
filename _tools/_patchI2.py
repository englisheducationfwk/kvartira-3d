"""I2: комната — диван больше на 1.2, стенка с полкой на 30–40 см и ТВ ниже,
тень-мерцание на стыке стены комнаты и кухни убрать."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# --- мерцание в углу комнаты/кухни: стена кухни (z=3,00..3,16) больше не совпадает гранью
rep("  solidBox(K.x0-P.LOAD, DH.kit.x0, K.z1, K.z1+P.LOAD, 0, P.HC, { nz:null, staged:['nz'], pz:M.wall2 });",
    "  solidBox(K.x0, DH.kit.x0, K.z1, K.z1+P.LOAD, 0, P.HC, { nz:null, staged:['nz'], pz:M.wall2 });")

# --- диван больше на 1.2
rep("""    sb(3.12, 1.95, 0.58, 1.86, 0.14, 0.26, M.woodDark);            /* каркас */
    [[2.85,1.06],[3.37,1.06],[2.85,2.84],[3.37,2.84]].forEach(function(lg){
      sb(lg[0], lg[1], 0.05, 0.05, 0, 0.14, M.woodDark);           /* ножки */
    });
    sb(3.12, 1.06, 0.62, 0.14, 0, 0.62, M.fabric2);                /* подлокотник */
    sb(3.12, 2.84, 0.62, 0.14, 0, 0.62, M.fabric2);
    var seatGrp = new THREE.Group(); grp.add(seatGrp);
    var seatC = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.20, 1.64), M.fabric);
    seatC.position.set(mx(3.10), 0.36, 1.95); seatC.castShadow = seatC.receiveShadow = true;
    seatGrp.add(seatC);
    [[3.06,1.20],[3.06,2.70]].forEach(function(lg){
      var lgm = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.26, 0.05), M.woodDark);
      lgm.position.set(mx(lg[0]), 0.13, lg[1]); lgm.castShadow = true; seatGrp.add(lgm);
    });
    var backGrp = new THREE.Group(); grp.add(backGrp);
    backGrp.position.set(mx(3.39), 0.44, 1.95);
    var backC = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.52, 1.64), M.fabric);
    backC.position.set(-sgn*0.08, 0.26, 0); backC.castShadow = backC.receiveShadow = true;
    backGrp.add(backC);
    backGrp.rotation.z = -sgn*0.10;
    var sofa = { kind:'sofa', seat:seatGrp, back:backGrp, seatX0:0,
                 dir:-sgn, rot0:-sgn*0.10, rot1: sgn*1.57, open:false, anim:null };
    grp.traverse(function(o){ if (o.isMesh){ o.userData.sofa = sofa; sofaParts.push(o); } });
    SOFAS.push(sofa);
    boxCol(2.79, 0.97, 3.41, 2.93);""",
    """    sb(3.06, 1.95, 0.70, 2.23, 0.17, 0.31, M.woodDark);            /* каркас */
    [[2.73,0.90],[3.36,0.90],[2.73,3.00],[3.36,3.00]].forEach(function(lg){
      sb(lg[0], lg[1], 0.06, 0.06, 0, 0.17, M.woodDark);           /* ножки */
    });
    sb(3.06, 0.90, 0.74, 0.17, 0, 0.74, M.fabric2);                /* подлокотник */
    sb(3.06, 3.00, 0.74, 0.17, 0, 0.74, M.fabric2);
    var seatGrp = new THREE.Group(); grp.add(seatGrp);
    var seatC = new THREE.Mesh(new THREE.BoxGeometry(0.67, 0.24, 1.97), M.fabric);
    seatC.position.set(mx(3.06), 0.48, 1.95); seatC.castShadow = seatC.receiveShadow = true;
    seatGrp.add(seatC);
    [[3.00,1.12],[3.00,2.78]].forEach(function(lg){
      var lgm = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.32, 0.06), M.woodDark);
      lgm.position.set(mx(lg[0]), 0.16, lg[1]); lgm.castShadow = true; seatGrp.add(lgm);
    });
    var backGrp = new THREE.Group(); grp.add(backGrp);
    backGrp.position.set(mx(3.40), 0.60, 1.95);
    var backC = new THREE.Mesh(new THREE.BoxGeometry(0.19, 0.62, 1.97), M.fabric);
    backC.position.set(-sgn*0.095, 0.31, 0); backC.castShadow = backC.receiveShadow = true;
    backGrp.add(backC);
    backGrp.rotation.z = -sgn*0.10;
    var sofa = { kind:'sofa', seat:seatGrp, back:backGrp, seatX0:0,
                 dir:-sgn, rot0:-sgn*0.10, rot1: sgn*1.57, open:false, anim:null };
    grp.traverse(function(o){ if (o.isMesh){ o.userData.sofa = sofa; sofaParts.push(o); } });
    SOFAS.push(sofa);
    boxCol(2.69, 0.79, 3.41, 3.11);""")
rep("    so.seat.position.x = so.seatX0 + so.dir*0.64*k2;",
    "    so.seat.position.x = so.seatX0 + so.dir*0.77*k2;")

# --- стенка: полка на 30–40 см по всей длине, ТВ ниже, секции открытые
rep("""  IT = item('Стенка', '🚪', 0.28, 1.82);
  ibox(IT, -0.39, 2.45, 0.22, 3.60, 0, 2.20, M.wood);              /* корпус */
  ibox(IT, -0.15, 2.45, 0.26, 3.60, 0, 0.85, M.wood);              /* низ фасада */
  ibox(IT, -0.15, 2.45, 0.26, 3.60, 1.60, 2.20, M.wood);           /* верх фасада */
  [0.75, 1.70, 2.82, 4.15].forEach(function(zz){                    /* стойки и секции */
    ibox(IT, -0.15, zz, 0.26, 0.10, 0.85, 1.60, M.wood);
  });
  ibox(IT, -0.20, 1.755, 0.06, 0.02, 0.87, 1.58, M.woodDark);
  ibox(IT, -0.20, 2.775, 0.06, 0.02, 0.87, 1.58, M.woodDark);
  ibox(IT, -0.28, 1.225, 0.02, 0.70, 1.10, 1.13, M.woodDark);
  ibox(IT, -0.28, 3.485, 0.02, 0.70, 1.10, 1.13, M.woodDark);""",
    """  IT = item('Стенка', '🚪', 0.28, 1.82);
  ibox(IT, -0.39, 2.45, 0.22, 3.60, 0, 2.20, M.wood);              /* корпус */
  ibox(IT, -0.15, 2.45, 0.26, 3.60, 0, 0.32, M.wood);              /* цоколь */
  ibox(IT, -0.15, 2.45, 0.26, 3.60, 0.32, 0.38, M.wood);           /* полка по всей длине (35 см) */
  [0.75, 1.70, 2.82, 4.15].forEach(function(zz){                    /* стойки и открытые секции */
    ibox(IT, -0.15, zz, 0.26, 0.10, 0.38, 2.20, M.wood);
  });
  ibox(IT, -0.15, 2.45, 0.26, 3.60, 2.14, 2.20, M.wood);           /* верхняя планка */
  ibox(IT, -0.20, 1.755, 0.06, 0.02, 0.40, 2.12, M.woodDark);
  ibox(IT, -0.20, 2.775, 0.06, 0.02, 0.40, 2.12, M.woodDark);""")

# --- ТВ ниже (в нише на полке)
rep("""  IT = item('ТВ', '📺', 0.20, 0.50);
  ibox(IT, -0.23, 2.26, 0.05, 0.94, 0.95, 1.53, M.black);
  (function(){ var scr2 = new THREE.Mesh(new THREE.PlaneGeometry(0.86, 0.44), M.dark);
    scr2.rotation.y = faceRY(Math.PI/2);
    scr2.position.set(mx(-0.203), 1.24, 2.26); IT.add(scr2); })();""",
    """  IT = item('ТВ', '📺', 0.20, 0.50);
  ibox(IT, -0.23, 2.26, 0.05, 0.94, 0.40, 0.98, M.black);
  (function(){ var scr2 = new THREE.Mesh(new THREE.PlaneGeometry(0.86, 0.44), M.dark);
    scr2.rotation.y = faceRY(Math.PI/2);
    scr2.position.set(mx(-0.203), 0.69, 2.26); IT.add(scr2); })();""")

p.write_text(s, encoding='utf-8')
print('I2 ok')
