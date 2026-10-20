#target photoshop
app.displayDialogs = DialogModes.NO;
app.preferences.rulerUnits = Units.PIXELS; app.preferences.typeUnits = TypeUnits.POINTS;
var K = "/Volumes/hd caique becker/Mac Caique/Projetos/bombril-pitch-75lab/fonte/kv/";
function cor(r, g, b) { var c = new SolidColor(); c.rgb.red = r; c.rgb.green = g; c.rgb.blue = b; return c; }
function colocar(doc, arq, nome, x0, y0, x1, y1) {
  var d = new ActionDescriptor(); d.putPath(charIDToTypeID('null'), new File(arq));
  d.putEnumerated(charIDToTypeID('FTcs'), charIDToTypeID('QCSt'), charIDToTypeID('Qcsa'));
  executeAction(charIDToTypeID('Plc '), d, DialogModes.NO);
  var L = doc.activeLayer; L.name = nome;
  var b = L.bounds; var w = b[2].as('px') - b[0].as('px'), h = b[3].as('px') - b[1].as('px');
  L.resize((x1 - x0) / w * 100, (y1 - y0) / h * 100, AnchorPosition.MIDDLECENTER);
  b = L.bounds; L.translate((x0 + x1) / 2 - (b[0].as('px') + b[2].as('px')) / 2, (y0 + y1) / 2 - (b[1].as('px') + b[3].as('px')) / 2);
  return L;
}
function sombra(op, dist, size) {
  var desc = new ActionDescriptor(); var ref = new ActionReference();
  ref.putProperty(charIDToTypeID('Prpr'), charIDToTypeID('Lefx')); ref.putEnumerated(charIDToTypeID('Lyr '), charIDToTypeID('Ordn'), charIDToTypeID('Trgt'));
  desc.putReference(charIDToTypeID('null'), ref);
  var fx = new ActionDescriptor(); fx.putUnitDouble(charIDToTypeID('Scl '), charIDToTypeID('#Prc'), 100);
  var ds = new ActionDescriptor(); ds.putBoolean(charIDToTypeID('enab'), true);
  ds.putEnumerated(charIDToTypeID('Md  '), charIDToTypeID('BlnM'), charIDToTypeID('Mltp'));
  var c = new ActionDescriptor(); c.putDouble(charIDToTypeID('Rd  '), 40); c.putDouble(charIDToTypeID('Grn '), 30); c.putDouble(charIDToTypeID('Bl  '), 60);
  ds.putObject(charIDToTypeID('Clr '), charIDToTypeID('RGBC'), c);
  ds.putUnitDouble(charIDToTypeID('Opct'), charIDToTypeID('#Prc'), op);
  ds.putBoolean(charIDToTypeID('uglg'), false); ds.putUnitDouble(charIDToTypeID('lagl'), charIDToTypeID('#Ang'), 90);
  ds.putUnitDouble(charIDToTypeID('Dstn'), charIDToTypeID('#Pxl'), dist); ds.putUnitDouble(charIDToTypeID('Ckmt'), charIDToTypeID('#Pxl'), 0);
  ds.putUnitDouble(charIDToTypeID('blur'), charIDToTypeID('#Pxl'), size);
  fx.putObject(charIDToTypeID('DrSh'), charIDToTypeID('DrSh'), ds);
  desc.putObject(charIDToTypeID('T   '), charIDToTypeID('Lefx'), fx);
  executeAction(charIDToTypeID('setd'), desc, DialogModes.NO);
}
function mancha(doc, nome, pts, pena, c, op) {
  var L = doc.artLayers.add(); L.name = nome;
  doc.selection.select(pts, SelectionType.REPLACE, pena, true);
  doc.selection.fill(c); doc.selection.deselect(); L.opacity = op; return L;
}
function elipse(doc, nome, x0, y0, x1, y1, pena, c, op) {
  var L = doc.artLayers.add(); L.name = nome;
  var d = new ActionDescriptor(); var r = new ActionReference(); r.putProperty(charIDToTypeID('Chnl'), charIDToTypeID('fsel')); d.putReference(charIDToTypeID('null'), r);
  var e = new ActionDescriptor(); e.putUnitDouble(charIDToTypeID('Top '), charIDToTypeID('#Pxl'), y0); e.putUnitDouble(charIDToTypeID('Left'), charIDToTypeID('#Pxl'), x0);
  e.putUnitDouble(charIDToTypeID('Btom'), charIDToTypeID('#Pxl'), y1); e.putUnitDouble(charIDToTypeID('Rght'), charIDToTypeID('#Pxl'), x1);
  d.putObject(charIDToTypeID('T   '), charIDToTypeID('Elps'), e); d.putBoolean(charIDToTypeID('AntA'), true);
  executeAction(charIDToTypeID('setd'), d, DialogModes.NO);
  doc.selection.feather(pena); doc.selection.fill(c); doc.selection.deselect(); L.opacity = op; return L;
}
function texto(doc, nome, conteudo, fonte, pt, c, cx, cy, larg) {
  var L = doc.artLayers.add(); L.kind = LayerKind.TEXT; L.name = nome;
  var t = L.textItem; t.font = fonte; t.size = new UnitValue(pt, 'pt'); t.color = c; t.justification = Justification.CENTER; t.contents = conteudo;
  t.position = [new UnitValue(cx, 'px'), new UnitValue(cy, 'px')];
  var b = L.bounds; var w = b[2].as('px') - b[0].as('px');
  if (larg && w > 0) L.resize(larg / w * 100, larg / w * 100, AnchorPosition.MIDDLECENTER);
  b = L.bounds; L.translate(cx - (b[0].as('px') + b[2].as('px')) / 2, cy - (b[1].as('px') + b[3].as('px')) / 2);
  return L;
}
var doc = app.documents.add(1920, 1080, 72, "KV Limpol Perfumes", NewDocumentMode.RGB, DocumentFill.WHITE);
colocar(doc, K + "kv_base.png", "Cena base (ChatGPT)", 0, -40, 1920, 1240);
mancha(doc, "Luz para o título", [[470, 0], [1920, 0], [1920, 300], [470, 300]], 110, cor(255, 255, 255), 62);
elipse(doc, "Sombra de contato", 880, 880, 1610, 935, 22, cor(40, 30, 60), 38);
var linha = colocar(doc, K + "linha_limpol_perfumes.png", "Linha Limpol Perfumes (embalagens reais)", 858, 300, 1622, 900);
doc.activeLayer = linha; sombra(22, 10, 26);
texto(doc, "Título linha 1", "Escolha o perfume", "Montserrat-ExtraBold", 72, cor(27, 42, 107), 1240, 110, 880);
texto(doc, "Título linha 2", "da sua casa.", "Montserrat-ExtraBold", 72, cor(110, 62, 170), 1240, 205, 640);
mancha(doc, "Faixa da assinatura", [[860, 948], [1620, 948], [1620, 1004], [860, 1004]], 0, cor(255, 255, 255), 86);
texto(doc, "Assinatura", "Limpol Perfumes  ·  Lavander, Blue Flowers, Jardin, Passion e Luxury", "Montserrat-SemiBold", 18, cor(27, 42, 107), 1240, 976, 700);
var lg = colocar(doc, K + "bombril_logo.png", "Logo Bombril", 1716, 34, 1880, 129);
var po = new PhotoshopSaveOptions(); po.layers = true; po.embedColorProfile = true; po.maximizeCompatibility = true;
doc.saveAs(new File(K + "KV_Limpol_Perfumes.psd"), po, false);
var jo = new JPEGSaveOptions(); jo.quality = 11; jo.embedColorProfile = true;
doc.saveAs(new File(K + "KV_Limpol_Perfumes_1920x1080.jpg"), jo, true);
doc.close(SaveOptions.DONOTSAVECHANGES);
"ok";
