"""G2: комната — диван-раскладной с анимацией вместо шкафа у восточной стены,
шкаф с нишей под ТВ у западной стены, мини-столик + стул, два коврика, кровать
и тумбочка переставлены под новые стены, люстра в центр."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:120]
    s = s.replace(old, new, count)


# ---------- 1) реестры дивана на уровне модуля ----------
rep("""var doorLeaves = [];
var DOORS = {};
var WIN_SASHES = [];""",
    """var doorLeaves = [];
var DOORS = {};
var WIN_SASHES = [];
var SOFAS = [], sofaParts = [];""")
rep("  pickables = []; inv = []; held = -1; WIN_SASHES = [];",
    "  pickables = []; inv = []; held = -1; WIN_SASHES = []; SOFAS = []; sofaParts = [];")

# ---------- 2) анимация и переключатель дивана (рядом с doorTick) ----------
rep("""function doorTick(dt){
  for (var k in DOORS){
    var d = DOORS[k];
    if (!d.anim) continue;
    d.anim.t = Math.min(1, d.anim.t + dt/d.anim.dur);
    var e = d.anim.t<0.5 ? 2*d.anim.t*d.anim.t : -1+(4-2*d.anim.t)*d.anim.t;
    d.cur = d.anim.from + (d.anim.to - d.anim.from)*e;
    d.grp.rotation.y = d.cur;
    if (d.anim.t >= 1) d.anim = null;
  }
}""",
    """function doorTick(dt){
  for (var k in DOORS){
    var d = DOORS[k];
    if (!d.anim) continue;
    d.anim.t = Math.min(1, d.anim.t + dt/d.anim.dur);
    var e = d.anim.t<0.5 ? 2*d.anim.t*d.anim.t : -1+(4-2*d.anim.t)*d.anim.t;
    d.cur = d.anim.from + (d.anim.to - d.anim.from)*e;
    d.grp.rotation.y = d.cur;
    if (d.anim.t >= 1) d.anim = null;
  }
  SOFAS.forEach(function(so){
    if (!so.anim) return;
    so.anim.t = Math.min(1, so.anim.t + dt/so.anim.dur);
    var e2 = so.anim.t<0.5 ? 2*so.anim.t*so.anim.t : -1+(4-2*so.anim.t)*so.anim.t;
    var k2 = so.open ? e2 : 1-e2;
    so.seat.position.x = so.seatX0 + so.dir*0.58*k2;
    so.back.rotation.z = so.rot0 + (so.rot1 - so.rot0)*k2;
    if (so.anim.t >= 1) so.anim = null;
  });
}
function toggleSofa(so){
  so.open = !so.open;
  so.anim = { t:0, dur:0.9 };
  toast(so.open ? 'Разложил диван 🛏 — можно спать' : 'Сложил диван 🛋');
}""")

# ---------- 3) клики: диван как дверь ----------
rep("""  var d = doorUnder(ndc.x, ndc.y);
  if (d && held < 0){ toggleDoor(d); return; }""",
    """  var d = doorUnder(ndc.x, ndc.y);
  if (d && held < 0){ if (d.kind === 'sofa') toggleSofa(d); else toggleDoor(d); return; }""")
rep("""  if (e.button === 0){
    var d = doorUnder(0, 0);
    if (d && held < 0){ toggleDoor(d); return; }
    var g = itemUnder(0, 0);
    if (g) pickUp(g);
  } else if (e.button === 2){
    var d2 = doorUnder(0, 0);
    if (d2){ toggleDoor(d2); return; }
    placeHeld(0, 0);
  }""",
    """  if (e.button === 0){
    var d = doorUnder(0, 0);
    if (d && held < 0){ if (d.kind === 'sofa') toggleSofa(d); else toggleDoor(d); return; }
    var g = itemUnder(0, 0);
    if (g) pickUp(g);
  } else if (e.button === 2){
    var d2 = doorUnder(0, 0);
    if (d2){ if (d2.kind === 'sofa') toggleSofa(d2); else toggleDoor(d2); return; }
    placeHeld(0, 0);
  }""")
rep("""function doorUnder(nx, ny){
  raycaster.setFromCamera({ x:nx, y:ny }, camera);
  var hits = raycaster.intersectObjects(doorLeaves, false);
  return hits.length ? (hits[0].object.userData.door || null) : null;
}""",
    """function doorUnder(nx, ny){
  raycaster.setFromCamera({ x:nx, y:ny }, camera);
  var hits = raycaster.intersectObjects(doorLeaves.concat(sofaParts), false);
  if (!hits.length) return null;
  var u = hits[0].object.userData;
  return u.door || u.sofa || null;
}""")
rep("""    if (q.userData && q.userData.door) return 'Дверь (полотно)';""",
    """    if (q.userData && q.userData.door) return 'Дверь (полотно)';
    if (q.userData && q.userData.sofa) return 'Диван (раскладной)';""")

# ---------- 4) мебель комнаты ----------
rep("""  var IT = item('Кровать', '🛏', 0.87, 1.00);
  ibox(IT, 0.91, 4.42, 1.70, 2.00, 0, 0.28, M.woodDark);
  ibox(IT, 0.91, 4.42, 1.62, 1.92, 0.28, 0.48, M.fabric2);
  ibox(IT, 0.91, 4.75, 1.62, 1.30, 0.48, 0.54, M.fabric);
  ibox(IT, 0.91, 5.22, 1.30, 0.42, 0.54, 0.66, M.white);
  ibox(IT, 0.91, 5.44, 1.70, 0.06, 0, 1.10, M.woodDark);
  IT = item('Шкаф', '🚪', 0.30, 1.00);
  ibox(IT, 3.09, 1.90, 0.60, 2.00, 0, 2.20, M.wood);
  ibox(IT, 2.79, 1.90, 0.02, 1.90, 0, 2.10, M.woodDark);
  IT = item('Тумбочка', '🗄', 0.20, 0.18);
  ibox(IT, 2.06, 5.14, 0.40, 0.36, 0, 0.42, M.wood);
  IT = item('ТВ', '📺', 0.62, 0.18);
  ibox(IT, 2.50, 5.31, 1.24, 0.36, 0, 0.30, M.wood);
  ibox(IT, 2.50, 5.465, 0.96, 0.05, 1.30, 1.88, M.black);
  IT = item('Ковёр', '🟫', 0, 0);
  (function(){ var rug = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 1.3), M.rug);
    rug.geometry.rotateX(-Math.PI/2); rug.position.set(mx(2.05), 0.025, 3.85);
    rug.receiveShadow = true; IT.add(rug); })();""",
    """  var IT = item('Кровать', '🛏', 0.87, 1.00);
  ibox(IT, 0.91, 5.22, 1.70, 2.00, 0, 0.28, M.woodDark);
  ibox(IT, 0.91, 5.22, 1.62, 1.92, 0.28, 0.48, M.fabric2);
  ibox(IT, 0.91, 5.55, 1.62, 1.30, 0.48, 0.54, M.fabric);
  ibox(IT, 0.91, 6.02, 1.30, 0.42, 0.54, 0.66, M.white);
  ibox(IT, 0.91, 6.29, 1.70, 0.06, 0, 1.10, M.woodDark);
  /* диван-раскладной у восточной стены: клик — раскладывается/складывается */
  (function(){
    var grp = new THREE.Group(); gFurn.add(grp);
    var sgn = state.mirror ? -1 : 1;
    function sb(x, z, w, d, y0, y1, mat, parent){
      var m = new THREE.Mesh(new THREE.BoxGeometry(w, y1-y0, d), mat);
      fixBoxUV(m.geometry, w, y1-y0, d, 1);
      m.position.set(mx(x), (y0+y1)/2, z);
      m.castShadow = m.receiveShadow = true; (parent || grp).add(m); return m;
    }
    sb(3.10, 1.90, 0.52, 1.60, 0.14, 0.26, M.woodDark);            /* каркас */
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
    boxCol(2.80, 1.08, 3.40, 2.72);
  })();
  /* шкаф напротив — у западной стены, с нишей под телевизор */
  IT = item('Шкаф', '🚪', 0.28, 0.92);
  ibox(IT, -0.39, 2.26, 0.22, 1.80, 0, 2.20, M.wood);              /* корпус */
  ibox(IT, -0.15, 2.26, 0.26, 1.80, 0, 0.85, M.wood);              /* низ фасада */
  ibox(IT, -0.15, 2.26, 0.26, 1.80, 1.60, 2.20, M.wood);           /* верх фасада */
  ibox(IT, -0.15, 1.54, 0.26, 0.36, 0.85, 1.60, M.wood);           /* стойка ниши (север) */
  ibox(IT, -0.15, 2.98, 0.26, 0.36, 0.85, 1.60, M.wood);           /* стойка ниши (юг) */
  ibox(IT, -0.20, 1.545, 0.06, 0.02, 0.87, 1.58, M.woodDark);
  ibox(IT, -0.20, 2.975, 0.06, 0.02, 0.87, 1.58, M.woodDark);
  IT = item('Тумбочка', '🗄', 0.20, 0.18);
  ibox(IT, 2.06, 5.94, 0.40, 0.36, 0, 0.42, M.wood);
  IT = item('ТВ', '📺', 0.20, 0.50);
  ibox(IT, -0.23, 2.26, 0.05, 0.94, 0.95, 1.53, M.black);
  (function(){ var scr2 = new THREE.Mesh(new THREE.PlaneGeometry(0.86, 0.44), M.dark);
    scr2.rotation.y = faceRY(Math.PI/2);
    scr2.position.set(mx(-0.203), 1.24, 2.26); IT.add(scr2); })();
  IT = item('Коврик', '🟫', 0, 0);
  (function(){ var r1 = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.42), M.rug);
    r1.geometry.rotateX(-Math.PI/2); r1.position.set(mx(0.86), 0.025, 1.87);
    r1.receiveShadow = true; IT.add(r1); })();
  IT = item('Коврик', '🟫', 0, 0);
  (function(){ var r2 = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.42), M.rug);
    r2.geometry.rotateX(-Math.PI/2); r2.position.set(mx(1.52), 0.025, 1.87);
    r2.receiveShadow = true; IT.add(r2); })();
  /* мини-столик белый и стул у окна */
  IT = item('Столик', '🪑', 0.25, 0.25);
  ibox(IT, 2.78, 0.50, 0.50, 0.50, 0.48, 0.52, M.white);
  [[2.57,0.29],[2.99,0.29],[2.57,0.71],[2.99,0.71]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.035, 0.035, 0, 0.48, M.white);
  });
  IT = item('Стул', '🪑', 0.19, 0.19);
  ibox(IT, 2.62, 1.04, 0.38, 0.38, 0.42, 0.46, M.white);
  ibox(IT, 2.62, 1.21, 0.38, 0.05, 0.46, 0.86, M.white);
  [[2.46,0.88],[2.78,0.88],[2.46,1.19],[2.78,1.19]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.035, 0.035, 0, 0.42, M.white);
  });""")

# ---------- 5) люстра в центр комнаты, растение в свободный угол ----------
rep("""    var lamp = new THREE.Mesh(new THREE.CylinderGeometry(0.16,0.20,0.05,18), M.fabric2);
    lamp.position.set(mx(1.6), 2.62, 2.6); IT.add(lamp);
    var lampS = new THREE.Mesh(new THREE.SphereGeometry(0.11,14,12), M.white);
    lampS.position.set(mx(1.6), 2.56, 2.6); IT.add(lampS);""",
    """    var lamp = new THREE.Mesh(new THREE.CylinderGeometry(0.16,0.20,0.05,18), M.fabric2);
    lamp.position.set(mx(1.45), 2.62, 3.15); IT.add(lamp);
    var lampS = new THREE.Mesh(new THREE.SphereGeometry(0.11,14,12), M.white);
    lampS.position.set(mx(1.45), 2.56, 3.15); IT.add(lampS);""")
rep("""    var potR = new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.055,0.12,16), M.terra);
    potR.position.set(mx(0.28), 0.06, 1.6); IT.add(potR);
    var busR = new THREE.Mesh(new THREE.SphereGeometry(0.12,14,12), M.leaf);
    busR.position.set(mx(0.28), 0.24, 1.6); IT.add(busR);""",
    """    var potR = new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.055,0.12,16), M.terra);
    potR.position.set(mx(0.34), 0.06, 3.52); IT.add(potR);
    var busR = new THREE.Mesh(new THREE.SphereGeometry(0.12,14,12), M.leaf);
    busR.position.set(mx(0.34), 0.24, 3.52); IT.add(busR);""")

p.write_text(s, encoding='utf-8')
print('G2 ok')
