"""I3: рабочее зеркало (проективный шейдер с мировухой — то, чего не хватало),
плита ровно над ящиком (1,434), верхние фасады во всю высоту, струи воды из изливов,
окно эркера скошено под углом внутрь."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# ---------- рабочее зеркало v3 ----------
rep("""/* рабочие краны и душ */""",
    """/* рабочее зеркало: проективное отражение (как Reflector из three.js) */
var mirrorRT = null, mirrorCam = null;
function makeMirror(w, h){
  if (!mirrorRT) mirrorRT = new THREE.WebGLRenderTarget(512, 512);
  if (!mirrorCam){ mirrorCam = new THREE.PerspectiveCamera(); mirrorCam.layers.enable(1); }
  var mat = new THREE.ShaderMaterial({
    uniforms: { tDiffuse: { value: mirrorRT.texture }, textureMatrix: { value: new THREE.Matrix4() } },
    vertexShader: 'uniform mat4 textureMatrix;\\nvarying vec4 vUv;\\n' +
      'void main(){ vUv = textureMatrix * vec4(position, 1.0);' +
      ' gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform sampler2D tDiffuse;\\nvarying vec4 vUv;\\n' +
      'void main(){ gl_FragColor = texture2DProj(tDiffuse, vUv); }'
  });
  var mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  var rp = new THREE.Vector3(), cp = new THREE.Vector3(), nrm = new THREE.Vector3(),
      view = new THREE.Vector3(), look = new THREE.Vector3(), tgt = new THREE.Vector3(),
      rotM = new THREE.Matrix4(), tm = mat.uniforms.textureMatrix.value;
  mesh.onBeforeRender = function(rend, scn, cam){
    if (cam === mirrorCam || scn !== scene) return;
    rp.setFromMatrixPosition(mesh.matrixWorld);
    cp.setFromMatrixPosition(cam.matrixWorld);
    rotM.extractRotation(mesh.matrixWorld);
    nrm.set(0, 0, 1).applyMatrix4(rotM);
    view.subVectors(rp, cp);
    if (view.dot(nrm) > 0) return;
    view.reflect(nrm).negate().add(rp);
    rotM.extractRotation(cam.matrixWorld);
    look.set(0, 0, -1).applyMatrix4(rotM).add(cp);
    tgt.subVectors(rp, look).reflect(nrm).negate().add(rp);
    mirrorCam.position.copy(view);
    mirrorCam.up.set(0, 1, 0).applyMatrix4(rotM).reflect(nrm);
    mirrorCam.lookAt(tgt);
    mirrorCam.far = cam.far;
    mirrorCam.updateMatrixWorld();
    mirrorCam.projectionMatrix.copy(cam.projectionMatrix);
    tm.set(0.5,0,0,0.5, 0,0.5,0,0.5, 0,0,0.5,0.5, 0,0,0,1);
    tm.multiply(mirrorCam.projectionMatrix);
    tm.multiply(mirrorCam.matrixWorldInverse);
    tm.multiply(mesh.matrixWorld);
    var was = mesh.visible; mesh.visible = false;
    var oldRT = rend.getRenderTarget();
    rend.setRenderTarget(mirrorRT);
    rend.render(scn, mirrorCam);
    rend.setRenderTarget(oldRT);
    mesh.visible = was;
  };
  return mesh;
}
/* рабочие краны и душ */""")

# ---------- зеркала на новый материал ----------
rep("""    var mirr = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 1.2), M.mirror);
    mirr.rotation.y = faceRY(0); mirr.position.set(mx(5.21), 1.45, 5.682); IT.add(mirr);""",
    """    var mirr = makeMirror(0.5, 1.2);
    mirr.rotation.y = faceRY(0); mirr.position.set(mx(5.21), 1.45, 5.682); IT.add(mirr);""")
rep("""    var mirr2 = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.7), M.mirror);
    mirr2.rotation.y = faceRY(-Math.PI/2);
    mirr2.position.set(mx(6.44), 1.60, 4.20); IT.add(mirr2);""",
    """    var mirr2 = makeMirror(0.5, 0.7);
    mirr2.rotation.y = faceRY(-Math.PI/2);
    mirr2.position.set(mx(6.44), 1.60, 4.20); IT.add(mirr2);""")

# ---------- плита ровно над ящиком (z = 1,434) ----------
rep("""    var ct = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.013, 0.50), M.black);
    ct.position.set(mx(KX-0.31), WT+0.006, 1.05); IT.add(ct);
    [[KX-0.17,0.94],[KX-0.45,0.94],[KX-0.17,1.17],[KX-0.45,1.17]].forEach(function(b){""",
    """    var ct = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.013, 0.50), M.black);
    ct.position.set(mx(KX-0.31), WT+0.006, 1.434); IT.add(ct);
    [[KX-0.17,1.324],[KX-0.45,1.324],[KX-0.17,1.544],[KX-0.45,1.544]].forEach(function(b){""")
rep("""    [0.87,0.99,1.11,1.23].forEach(function(z){
      var k2 = new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.015,0.022,12), M.black);
      k2.position.set(mx(KX-0.055), WT+0.011, z); IT.add(k2);
    });""",
    """    [1.254,1.374,1.494,1.614].forEach(function(z){
      var k2 = new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.015,0.022,12), M.black);
      k2.position.set(mx(KX-0.055), WT+0.011, z); IT.add(k2);
    });""")

# ---------- верхние фасады во всю высоту шкафа ----------
rep("    var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.04, UZD-0.02), M.front);",
    "    var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);")

# ---------- струи воды: падают из излива, а не из середины ----------
rep("""    var kStream = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, 0.26, 10), M.water);
    kStream.position.set(mx(KX-0.17), WT+0.16, 2.44); kStream.visible = false; IT.add(kStream);""",
    """    var kStream = new THREE.Mesh(new THREE.CylinderGeometry(0.0075, 0.006, 0.26, 10), M.water);
    kStream.position.set(mx(KX-0.27), WT+0.155, 2.44); kStream.visible = false; IT.add(kStream);""")
rep("""    var sf = new THREE.Mesh(new THREE.CylinderGeometry(0.014,0.014,0.17,12), M.chrome);
    sf.position.set(mx(6.36), 0.90, 4.20); IT.add(sf);
    var sn = new THREE.Mesh(new THREE.CylinderGeometry(0.011,0.011,0.14,12), M.chrome);
    sn.rotation.z = Math.PI/2; sn.position.set(mx(6.30), 0.985, 4.20); IT.add(sn);
    var sStream = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.13, 10), M.water);
    sStream.position.set(mx(6.30), 0.965, 4.20); sStream.visible = false; IT.add(sStream);""",
    """    var sf = new THREE.Mesh(new THREE.CylinderGeometry(0.014,0.014,0.17,12), M.chrome);
    sf.position.set(mx(6.40), 0.885, 4.20); IT.add(sf);
    var sn = new THREE.Mesh(new THREE.CylinderGeometry(0.011,0.011,0.18,12), M.chrome);
    sn.rotation.z = Math.PI/2; sn.position.set(mx(6.31), 0.97, 4.20); IT.add(sn);
    var sStream = new THREE.Mesh(new THREE.CylinderGeometry(0.0075, 0.006, 0.15, 10), M.water);
    sStream.position.set(mx(6.23), 0.90, 4.20); sStream.visible = false; IT.add(sStream);""")

# ---------- окно эркера — скошено под углом (верх внутрь) ----------
rep("""      var rot0 = Math.atan2(-uz, ux);
      grp.rotation.y = rot0;
      var y0 = P.bay.sillY, y1 = BWP, hgt = y1-y0;
      var fr = new THREE.Group(); grp.add(fr);
      function bar(bw,bh,bx,by){ var m = new THREE.Mesh(new THREE.BoxGeometry(bw,bh,0.10), M.frame);
        m.position.set(bx, by, 0); fr.add(m); return m; }""",
    """      var rot0 = Math.atan2(-uz, ux);
      grp.rotation.y = rot0;
      var y0 = P.bay.sillY, y1 = BWP, hgt = y1-y0;
      var fr = new THREE.Group(); grp.add(fr);
      fr.position.y = y0; fr.rotation.x = 0.10;    /* окно скошено под углом внутрь */
      function bar(bw,bh,bx,by){ var m = new THREE.Mesh(new THREE.BoxGeometry(bw,bh,0.10), M.frame);
        m.position.set(bx, by - y0, 0); fr.add(m); return m; }""")

p.write_text(s, encoding='utf-8')
print('I3 ok')
