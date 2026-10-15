"""G6: комната — диван длиннее и шире, мини-стол длиннее, стул к столу (запад),
карниз тонкий, шторы скрыты; лоджия сдвинута на 1 м влево, её потолок больше
не лезет в комнату."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:120]
    s = s.replace(old, new, count)


# --- лоджия на метр левее
rep("  loggia:{ x0:0.30, x1:3.20, z0:-1.20, z1:0.00 },",
    "  loggia:{ x0:-0.70, x1:2.20, z0:-1.20, z1:0.00 },")
rep("""  /* потолок лоджии ниже */
  var lgC = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 1.8), M.ceil);
  lgC.rotation.x = Math.PI/2;
  lgC.position.set(mx((LG.x0+LG.x1)/2), 2.42, (LG.z0+LG.z1)/2); gRoom.add(lgC);""",
    """  /* потолок лоджии ниже — строго по её габаритам (в комнату не лезет) */
  var lgC = new THREE.Mesh(new THREE.PlaneGeometry(LG.x1-LG.x0+0.30, LG.z1-LG.z0), M.ceil);
  lgC.rotation.x = Math.PI/2;
  lgC.position.set(mx((LG.x0+LG.x1)/2), 2.42, (LG.z0+LG.z1)/2);
  lgC.castShadow = true; gRoom.add(lgC);""")

# --- вещи на лоджии едут вместе с ней
rep("  ibox(IT, 1.50, -0.75, 0.36, 0.36, 0, 0.42, M.wood);",
    "  ibox(IT, 0.55, -0.75, 0.36, 0.36, 0, 0.42, M.wood);")
rep("  ibox(IT, 2.85, -0.70, 0.45, 0.55, 0, 0.34, M.woodDark);",
    "  ibox(IT, 1.85, -0.70, 0.45, 0.55, 0, 0.34, M.woodDark);")

# --- подписи лоджии
rep("  loggia:   [ [1.70, 1.45, -0.60],       [0,0,1] ],",
    "  loggia:   [ [0.75, 1.45, -0.60],       [0,0,1] ],")
rep("  { p:[1.75, 0.30, -0.58], t:'лоджия 2,9 × 1,2 · остеклена' },",
    "  { p:[0.75, 0.30, -0.58], t:'лоджия 2,9 × 1,2 · остеклена' },")

# --- диван: длиннее и шире
rep("""    sb(3.10, 1.90, 0.52, 1.60, 0.14, 0.26, M.woodDark);            /* каркас */
    [[2.87,1.16],[3.33,1.16],[2.87,2.64],[3.33,2.64]].forEach(function(lg){
      sb(lg[0], lg[1], 0.05, 0.05, 0, 0.14, M.woodDark);           /* ножки */
    });
    sb(3.10, 1.16, 0.56, 0.12, 0, 0.60, M.fabric2);                /* подлокотник */
    sb(3.10, 2.64, 0.56, 0.12, 0, 0.60, M.fabric2);
    var seatGrp = new THREE.Group(); grp.add(seatGrp);
    var seatC = new THREE.Mesh(new THREE.BoxGeometry(0.50, 0.20, 1.40), M.fabric);
    seatC.position.set(mx(3.09), 0.36, 1.90); seatC.castShadow = seatC.receiveShadow = true;
    seatGrp.add(seatC);
    [[3.05,1.26],[3.05,2.54]].forEach(function(lg){
      var lgm = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.26, 0.05), M.woodDark);
      lgm.position.set(mx(lg[0]), 0.13, lg[1]); lgm.castShadow = true; seatGrp.add(lgm);
    });
    var backGrp = new THREE.Group(); grp.add(backGrp);
    backGrp.position.set(mx(3.36), 0.46, 1.90);
    var backC = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.50, 1.40), M.fabric);
    backC.position.set(-sgn*0.07, 0.25, 0); backC.castShadow = backC.receiveShadow = true;
    backGrp.add(backC);
    backGrp.rotation.z = -sgn*0.10;
    var sofa = { kind:'sofa', seat:seatGrp, back:backGrp, seatX0:0,
                 dir:-sgn, rot0:-sgn*0.10, rot1: sgn*1.42, open:false, anim:null };
    grp.traverse(function(o){ if (o.isMesh){ o.userData.sofa = sofa; sofaParts.push(o); } });
    SOFAS.push(sofa);
    boxCol(2.80, 1.08, 3.40, 2.72);""",
    """    sb(3.12, 1.95, 0.58, 1.86, 0.14, 0.26, M.woodDark);            /* каркас */
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
    backGrp.position.set(mx(3.39), 0.46, 1.95);
    var backC = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.52, 1.64), M.fabric);
    backC.position.set(-sgn*0.08, 0.26, 0); backC.castShadow = backC.receiveShadow = true;
    backGrp.add(backC);
    backGrp.rotation.z = -sgn*0.10;
    var sofa = { kind:'sofa', seat:seatGrp, back:backGrp, seatX0:0,
                 dir:-sgn, rot0:-sgn*0.10, rot1: sgn*1.42, open:false, anim:null };
    grp.traverse(function(o){ if (o.isMesh){ o.userData.sofa = sofa; sofaParts.push(o); } });
    SOFAS.push(sofa);
    boxCol(2.79, 0.97, 3.41, 2.93);""")
rep("    so.seat.position.x = so.seatX0 + so.dir*0.58*k2;",
    "    so.seat.position.x = so.seatX0 + so.dir*0.64*k2;")

# --- мини-стол длиннее, стул к столу (западнее, лицом на восток)
rep("""  IT = item('Столик', '🪑', 0.25, 0.25);
  ibox(IT, 2.78, 0.50, 0.50, 0.50, 0.48, 0.52, M.white);
  [[2.57,0.29],[2.99,0.29],[2.57,0.71],[2.99,0.71]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.035, 0.035, 0, 0.48, M.white);
  });
  IT = item('Стул', '🪑', 0.19, 0.19);
  ibox(IT, 2.62, 1.04, 0.38, 0.38, 0.42, 0.46, M.white);
  ibox(IT, 2.62, 1.21, 0.38, 0.05, 0.46, 0.86, M.white);
  [[2.46,0.88],[2.78,0.88],[2.46,1.19],[2.78,1.19]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.035, 0.035, 0, 0.42, M.white);
  });""",
    """  IT = item('Столик', '🪑', 0.55, 0.25);
  ibox(IT, 2.79, 0.50, 1.06, 0.50, 0.48, 0.52, M.white);
  [[2.34,0.30],[3.24,0.30],[2.34,0.70],[3.24,0.70]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.035, 0.035, 0, 0.48, M.white);
  });
  IT = item('Стул', '🪑', 0.19, 0.19);
  (function(){
    var cg = new THREE.Group(); IT.add(cg);
    cg.position.set(mx(1.95), 0, 0.48);
    cg.rotation.y = faceRY(Math.PI/2);
    function cb(dx, dy, dz, w, h2, d, mat){
      var m = new THREE.Mesh(new THREE.BoxGeometry(w, h2, d), mat);
      m.position.set(dx, dy, dz); m.castShadow = m.receiveShadow = true; cg.add(m); return m;
    }
    cb(0, 0.44, 0, 0.38, 0.04, 0.38, M.white);            /* сиденье */
    cb(0, 0.66, -0.165, 0.38, 0.40, 0.05, M.white);       /* спинка */
    [[-0.155,-0.155],[0.155,-0.155],[-0.155,0.155],[0.155,0.155]].forEach(function(lg){
      cb(lg[0], 0.21, lg[1], 0.035, 0.42, 0.035, M.white);
    });
  })();""")

# --- карниз: тоньше и короче; шторы пока скрыты
rep("""  IT = item('Шторы', '🪟', 0, 0);
  (function(){
    var rail = new THREE.Mesh(new THREE.BoxGeometry(2.15, 0.05, 0.05), M.woodDark);
    rail.position.set(mx(2.15), 2.32, 0.11); IT.add(rail);
    [1.22, 3.08].forEach(function(cx){
      var cur = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 2.4), M.fabric);
      cur.position.set(mx(cx), 1.15, 0.14); cur.castShadow = true; IT.add(cur);
    });
  })();""",
    """  IT = item('Карниз', '🪟', 0, 0);      /* шторы пока скрыты — вернём, если попросит */
  (function(){
    var rail = new THREE.Mesh(new THREE.BoxGeometry(1.90, 0.035, 0.035), M.woodDark);
    rail.position.set(mx(2.15), 2.33, 0.10); IT.add(rail);
  })();""")

p.write_text(s, encoding='utf-8')
print('G6 ok')

# --- data.json: лоджия-телепорт
d = pathlib.Path('_tools/data.json')
t = d.read_text(encoding='utf-8')
old = '{"id": "loggia", "t": "Лоджия", "x": 1.7, "z": -0.5, "yaw": 0.0}'
assert old in t, 'loggia spot not found'
t = t.replace(old, '{"id": "loggia", "t": "Лоджия", "x": 0.8, "z": -0.5, "yaw": 0.0}', 1)
d.write_text(t, encoding='utf-8')
import json; json.loads(t)
print('G6 data ok')
