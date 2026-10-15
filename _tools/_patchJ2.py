"""J2: коридор — выключатель на 5,33, табличку убрать; площадка — настоящие стены
по бокам и глубина в 2 раза; тумблер «зеркала» в настройках; раковины без чёрной дыры;
второй верхний фасад — разрезной в половину (мини-ящик снизу)."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# ---------- 1) тумблер зеркал: состояние + чекбокс ----------
rep("              spots:true, dims:false, furn:true, map:false, view:'overview',",
    "              spots:true, dims:false, furn:true, map:false, mirrOn:true, view:'overview',")
rep("""          <label class="chk"><input type="checkbox" id="ckMirror"><span>Зеркальная планировка (1б) — включи, если в квартире кухня слева</span></label>""",
    """          <label class="chk"><input type="checkbox" id="ckMirror"><span>Зеркальная планировка (1б) — включи, если в квартире кухня слева</span></label>
          <label class="chk"><input type="checkbox" id="ckMirr" checked><span>🪞 Зеркала — настоящее отражение (выключи, если тормозит)</span></label>""")
rep("$('#ckMirror').checked = state.mirror;\n$('#ckSpots').checked = state.spots; $('#ckDims').checked = state.dims;",
    "$('#ckMirror').checked = state.mirror; $('#ckMirr').checked = state.mirrOn !== false;\n$('#ckSpots').checked = state.spots; $('#ckDims').checked = state.dims;")
rep("$('#ckSpots').addEventListener('change', function(e){ state.spots = e.target.checked; save(); });",
    "$('#ckMirr').addEventListener('change', function(e){ state.mirrOn = e.target.checked; save(); applyMirrors(); });\n$('#ckSpots').addEventListener('change', function(e){ state.spots = e.target.checked; save(); });")

# ---------- 2) makeMirror: реестр + выключатель ----------
rep("""var mirrorRT = null, mirrorCam = null;
function makeMirror(w, h){
  if (!mirrorRT) mirrorRT = new THREE.WebGLRenderTarget(1024, 1024);""",
    """var mirrorRT = null, mirrorCam = null, MIRROR_LIST = [];
function applyMirrors(){
  MIRROR_LIST.forEach(function(mm){ mm.material = (state.mirrOn !== false) ? mm.userData.mirrMat : M.mirror; });
}
function makeMirror(w, h){
  if (!mirrorRT) mirrorRT = new THREE.WebGLRenderTarget(1024, 1024);""")
rep("""  var mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);""",
    """  var mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  mesh.userData.mirrMat = mat;
  mesh.material = (state.mirrOn !== false) ? mat : M.mirror;
  MIRROR_LIST.push(mesh);""")
rep("""  mesh.onBeforeRender = function(rend, scn, cam){
    if (cam === mirrorCam || scn !== scene) return;""",
    """  mesh.onBeforeRender = function(rend, scn, cam){
    if (state.mirrOn === false) return;
    if (cam === mirrorCam || scn !== scene) return;""")
rep("  HINGES = []; hingeParts = []; TAPS = []; tapParts = [];",
    "  HINGES = []; hingeParts = []; TAPS = []; tapParts = []; MIRROR_LIST = [];")

# ---------- 3) выключатель на 5,33; табличку-номер убрать ----------
rep("""  (function(){
    var bx = mx(4.72);
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.09, 0.014), M.frame);
    pl.position.set(bx, 1.55, HA.z1-0.012); gRoom.add(pl);
    var rock = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.05, 0.014), M.white);
    rock.position.set(bx, 1.55, HA.z1-0.022); gRoom.add(rock);""",
    """  (function(){
    var bx = mx(5.33);
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.09, 0.014), M.frame);
    pl.position.set(bx, 1.55, HA.z1-0.012); gRoom.add(pl);
    var rock = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.05, 0.014), M.white);
    rock.position.set(bx, 1.55, HA.z1-0.022); gRoom.add(rock);""")
rep("""    var plate = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.09, 0.02), M.white);
    plate.position.set(E1+0.16, 1.55, HA.z1-0.07); g.add(plate);""", "    /* табличку-номер с внутренней стороны убрали */")

# ---------- 4) площадка: боковые стены во всю длину, глубина ×2 ----------
rep("var LAND = { x0:2.4, x1:6.9, z0:5.68, z1:8.9 };",
    "var LAND = { x0:2.4, x1:6.9, z0:5.68, z1:11.3 };")
rep("var FLAT = { x0:-0.95, x1:7.27, z0:-1.60, z1:9.10 };",
    "var FLAT = { x0:-0.95, x1:7.27, z0:-1.60, z1:11.5 };")
rep("""    w(L0-0.12, L0, (P.room.z1+P.LOAD+LAND.z1)/2, 0.12);
    slab(L0, K.x0-P.LOAD, P.room.z1+P.LOAD, WZ);          /* полоса у входа */
    clg(L0, K.x0-P.LOAD, P.room.z1+P.LOAD, WZ);
    w(L1, L1+0.12, (WZ+LAND.z1)/2, 0.12);
    w(L0, L1, LAND.z1, 0.12);""",
    """    /* боковые стены площадки — во всю длину (раньше были огрызки — светилась дыра) */
    (function(){
      var z0 = P.room.z1+P.LOAD, z1 = LAND.z1;
      var mw = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.72, z1-z0),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.concrete,M.hallWall]);
      fixBoxUV(mw.geometry, 0.12, 2.72, z1-z0, 1);
      mw.position.set(L0-0.06, 1.36, (z0+z1)/2); mw.receiveShadow = true; g.add(mw);
      var me = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.72, z1-z0),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.hallWall,M.concrete]);
      fixBoxUV(me.geometry, 0.12, 2.72, z1-z0, 1);
      me.position.set(L1+0.06, 1.36, (z0+z1)/2); me.receiveShadow = true; g.add(me);
    })();
    slab(L0, K.x0-P.LOAD, P.room.z1+P.LOAD, WZ);          /* полоса у входа */
    clg(L0, K.x0-P.LOAD, P.room.z1+P.LOAD, WZ);
    w(L0, L1, LAND.z1, 0.12);""")

# ---------- 5) раковины: светлое дно + слив вместо чёрной дыры ----------
rep("""    var bw = new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.34), M.dark);
    bw.geometry.rotateX(-Math.PI/2); bw.position.set(mx(6.18), 0.826, 4.20); IT.add(bw);""",
    """    var bw = new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.34), M.white);
    bw.geometry.rotateX(-Math.PI/2); bw.position.set(mx(6.18), 0.826, 4.20); IT.add(bw);
    var bdr = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.006, 14), M.dark);
    bdr.position.set(mx(6.18), 0.827, 4.20); IT.add(bdr);""")
rep("""    var basin = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.34), M.dark);
    basin.geometry.rotateX(-Math.PI/2); basin.position.set(mx(KX-0.31), WT+0.013, 2.44); IT.add(basin);""",
    """    var basin = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.34), M.white);
    basin.geometry.rotateX(-Math.PI/2); basin.position.set(mx(KX-0.31), WT+0.013, 2.44); IT.add(basin);
    var bdr2 = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.006, 14), M.dark);
    bdr2.position.set(mx(KX-0.31), WT+0.014, 2.44); IT.add(bdr2);""")

# ---------- 6) второй верхний фасад — разрезной в половину ----------
rep("""  var UZD = (2.99 - 0.66) / 4;
  for (var i3=0;i3<4;i3++){
    var uz = 0.66 + UZD/2 + i3*UZD;
    var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);
    d2.position.set(mx(KX-0.35), WT+AH+UPH/2, uz); d2.castShadow = d2.receiveShadow = true;
    var hu = mkHinge(d2, mx(KX-0.35), uz - (UZD-0.02)/2 + 0.01, 'шкафчик', -1.8, upGrp);
    var uh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
    uh.position.set(-0.025, WT+AH+UPH/2-(UPH/2)+0.09, UZD-0.02-0.055);
    uh.castShadow = true; handles.push(uh); hu.grp.add(uh);
  }""",
    """  var UZD = (2.99 - 0.66) / 4;
  var UY0 = WT+AH, UY1 = WT+AH+UPH, UYM = (UY0+UY1)/2;   /* низ/верх/середина шкафов */
  for (var i3=0;i3<4;i3++){
    var uz = 0.66 + UZD/2 + i3*UZD;
    if (i3 === 1){
      /* второй фасад — разрезной в половину: снизу мини-ящик, сверху дверца */
      var d2b = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);
      d2b.position.set(mx(KX-0.35), (UY0+UYM)/2+0.005, uz); d2b.castShadow = d2b.receiveShadow = true;
      var hb = mkHinge(d2b, mx(KX-0.35), uz-(UZD-0.02)/2+0.01, 'ящик', -1.8, upGrp);
      var uhb = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uhb.position.set(-0.025, 0.02, UZD-0.02-0.055);
      uhb.castShadow = true; handles.push(uhb); hb.grp.add(uhb);
      var d2c = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);
      d2c.position.set(mx(KX-0.35), (UYM+UY1)/2-0.005, uz); d2c.castShadow = d2c.receiveShadow = true;
      var hc = mkHinge(d2c, mx(KX-0.35), uz-(UZD-0.02)/2+0.01, 'шкафчик', -1.8, upGrp);
      var uhc = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uhc.position.set(-0.025, (UPH/2-0.03)-0.075, UZD-0.02-0.055);
      uhc.castShadow = true; handles.push(uhc); hc.grp.add(uhc);
    } else {
      var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);
      d2.position.set(mx(KX-0.35), UYM, uz); d2.castShadow = d2.receiveShadow = true;
      var hu = mkHinge(d2, mx(KX-0.35), uz - (UZD-0.02)/2 + 0.01, 'шкафчик', -1.8, upGrp);
      var uh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uh.position.set(-0.025, UY0-UYM+0.09, UZD-0.02-0.055);
      uh.castShadow = true; handles.push(uh); hu.grp.add(uh);
    }
  }""")

p.write_text(s, encoding='utf-8')
print('J2 ok')
