# Imagens das peças (fonte/pecas/*.png, geradas a partir do KV final) viram os assets do deck em JPG, e os executivos
# (fonte/executivo/saida) vão para assets/executivo com PNG, PDF e DXF.
import os, shutil, glob
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(RAIZ, "fonte")
ASSETS = os.path.join(RAIZ, "assets")

for png in sorted(glob.glob(os.path.join(FONTE, "pecas", "*.png"))):
    nome = os.path.basename(png)[:-4]            # ex.: aramado_loja
    peca, tipo = nome.rsplit("_", 1)
    im = Image.open(png).convert("RGB")
    im.thumbnail((1700, 1700) if tipo == "loja" else (1400, 1400), Image.LANCZOS)
    destino = os.path.join(ASSETS, f"{peca}-{tipo}.jpg")
    im.save(destino, "JPEG", quality=84, optimize=True, progressive=True)
    print(destino, im.size)

exec_dst = os.path.join(ASSETS, "executivo")
os.makedirs(exec_dst, exist_ok=True)
for arq in glob.glob(os.path.join(FONTE, "executivo", "saida", "P*")):
    if arq.endswith("_librecad.pdf"):
        continue
    if os.path.isdir(arq):
        continue
    if arq.endswith(".png"):
        im = Image.open(arq).convert("RGB"); im.thumbnail((2200, 2200), Image.LANCZOS)
        im.save(os.path.join(exec_dst, os.path.basename(arq)), "PNG", optimize=True)
    else:
        shutil.copy2(arq, exec_dst)
imgs = os.path.join(FONTE, "executivo", "saida", "imagens")
if os.path.isdir(imgs):
    shutil.copytree(imgs, os.path.join(exec_dst, "imagens"), dirs_exist_ok=True)
print(sorted(os.listdir(exec_dst)))
