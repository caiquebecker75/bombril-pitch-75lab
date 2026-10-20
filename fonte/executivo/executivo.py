# Projeto executivo das 5 peças do PDV Limpol Perfumes (Bombril), um DXF R2018 + PDF A2 por peça.
# Base de desenho reaproveitada do display Snickers (desenho.py: folha, camadas, cotas que o LibreCAD lê, carimbo com o
# logo da 75 LAB em vetor). Medidas em mm; as mesmas medidas foram usadas nas imagens das peças.
import os, sys, subprocess
sys.path.insert(0, os.path.expanduser("~/snickers-display-triangular/ferramentas"))
import desenho as D

D.DATA = "20/10/2026"
D.CLIENTE = "Bombril · Limpol Perfumes"
D.PROJETO = "Escolha o perfume da sua casa · PDV"
AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "saida")
LIBRECAD = "/Applications/LibreCAD.app/Contents/MacOS/LibreCAD"


def folha(num, titulo, esc, material, sub):
    f = D.Folha(num, 5, titulo, esc, material=material, subtitulo=sub)
    return f


def P(f, x, y):
    """ponto em mm de papel para o espaço do modelo"""
    return (x * f.esc, y * f.esc)


def notas(f, x, y, linhas, largura=250, titulo="ESPECIFICAÇÃO"):
    f.texto(titulo, P(f, x, y), h=3.2, alinh="BOTTOM_LEFT")
    f.mtexto("\\P".join(linhas), P(f, x, y - 3), h=2.3, largura=largura, espaco=1.35)


def vista_titulo(f, txt, x, y):
    f.texto(txt, P(f, x, y), h=3.0, alinh="BOTTOM_LEFT")


IMG = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "assets")


def perspectiva(f, arq, x=330, y=95, larg=230, alt=175):
    caminho = os.path.join(IMG, arq)
    if not os.path.exists(caminho): return
    f.texto("PERSPECTIVA ILUSTRATIVA (sem escala)", P(f, x, y + alt + 4), h=2.6, alinh="BOTTOM_LEFT")
    f.imagem(caminho, x, y, larg, alt)


def salvar(f, nome):
    os.makedirs(SAIDA, exist_ok=True)
    f.moldura("R00 · proposta", f"{nome}.dxf")
    dxf = os.path.join(SAIDA, f"{nome}.dxf"); pdf = os.path.join(SAIDA, f"{nome}.pdf")
    f.salvar(dxf, pdf)
    # conferência num leitor independente: o LibreCAD abre e converte o DXF
    if os.path.exists(LIBRECAD):
        subprocess.run([LIBRECAD, "dxf2pdf", "-a", "-o", os.path.join(SAIDA, f"{nome}_librecad.pdf"), dxf], capture_output=True, timeout=120)
    import fitz
    pg = fitz.open(pdf)[0]
    pg.get_pixmap(dpi=110).save(os.path.join(SAIDA, f"{nome}.png"))
    return dxf


# ---------------------------------------------------------------- 1 · display aramado (pesada)
def aramado():
    e = 10; f = folha(1, "Display aramado de ponta · vistas", e, "Aramado Ø4 mm + tubo 20x20 epóxi; PS 2 mm", "Conjunto pesado · hiper e atacarejo")
    L, A, Pp, rod, test = 1000, 1800, 450, 100, 300
    prateleiras = [rod + 40, 520, 890, 1260]
    ox, oy = P(f, 60, 175)
    # frente
    f.ret(ox, oy, ox + L, oy + A)
    f.ret(ox, oy, ox + L, oy + rod, "13_VISTA")
    f.ret(ox, oy + A - test, ox + L, oy + A)
    f.texto("testeira PS 2 mm com a arte do KV", (ox + L / 2, oy + A - test / 2), h=2.2, alinh="MIDDLE_CENTER")
    for y in prateleiras:
        f.linha((ox + 20, oy + y), (ox + L - 20, oy + y)); f.linha((ox + 20, oy + y + 60), (ox + L - 20, oy + y + 60), "11_OCULTO")
    for x in (ox + 20, ox + L - 20):
        f.linha((x, oy + rod), (x, oy + A - test), "10_EIXO")
    f.cota((ox, oy), (ox + L, oy), (ox, oy - 60))
    f.cota((ox, oy), (ox, oy + A), (ox - 80, oy), angulo=90)
    f.cota((ox + L, oy + A - test), (ox + L, oy + A), (ox + L + 60, oy), angulo=90)
    f.cota((ox + L, prateleiras[1] + oy), (ox + L, prateleiras[2] + oy), (ox + L + 60, oy), angulo=90)
    vista_titulo(f, "VISTA FRONTAL 1:10", 60, 158)
    # lateral
    lx = ox + L + 250
    f.ret(lx, oy, lx + Pp, oy + A - test); f.ret(lx, oy + A - test, lx + 25, oy + A)
    for y in prateleiras:
        f.linha((lx, oy + y), (lx + Pp, oy + y)); f.linha((lx + Pp, oy + y), (lx + Pp, oy + y + 60))
    f.cota((lx, oy), (lx + Pp, oy), (lx, oy - 60))
    f.chamada((lx + Pp, oy + prateleiras[3] + 60), (lx + Pp + 180, oy + 1450), "barra de retenção\\P60 mm, arame Ø6")
    vista_titulo(f, "VISTA LATERAL 1:10", (lx) / e, 158)
    # planta
    py = oy - 420 - Pp
    f.ret(ox, py, ox + L, py + Pp)
    for k in range(1, 20):
        f.linha((ox + k * 50, py), (ox + k * 50, py + Pp), "05_ZONA_DOBRA")
    f.cota((ox, py), (ox, py + Pp), (ox - 80, py), angulo=90)
    vista_titulo(f, "PLANTA · GRADE 50 MM 1:10", 60, (py + Pp + 40) / e)
    notas(f, 330, 380, [
        "Estrutura: 2 laterais em tubo 20x20 mm, pintura epóxi branca.",
        "4 prateleiras aramadas Ø4 mm, grade 50 mm, barra de retenção Ø6 a 60 mm.",
        "Vão livre entre prateleiras 310 mm: frascos de 500 ml, 1 L e 2 L em pé.",
        "Testeira 1000 x 300 mm em PS 2 mm impresso (arte do KV), encaixe por presilha.",
        "Laterais em PS 2 mm 450 x 1400 mm com as flores e as cores do KV.",
        "Rodapé em chapa 0,9 mm, 100 mm de altura, 4 sapatas niveladoras.",
        "Capacidade: cerca de 120 frascos de 1 L (5 faixas verticais de cor).",
        "Instalação: encostado no fim da gôndola (ponta), sem avançar no corredor.",
        "QR único na testeira para o One Shot; tag On Timing presa no rodapé.",
    ])
    perspectiva(f, "aramado-recorte.jpg")
    return salvar(f, "P1_display-aramado")


# ---------------------------------------------------------------- 2 · estação de aroma (pesada, ativação)
def estacao():
    e = 10; f = folha(2, "Estação de aroma · vistas", e, "MDF 18 mm laminado; tubo Ø25; PS 2 mm", "Conjunto pesado · ativação em loja")
    L, A, Pp, tampo, Atot, test = 1200, 950, 500, 20, 2100, 400
    ox, oy = P(f, 60, 150)
    f.ret(ox, oy, ox + L, oy + A - tampo); f.ret(ox - 20, oy + A - tampo, ox + L + 20, oy + A)
    f.ret(ox + 40, oy + 80, ox + L - 40, oy + A - 80, "11_OCULTO")
    f.texto("frente impressa com a arte do KV", (ox + L / 2, oy + A / 2), h=2.2, alinh="MIDDLE_CENTER")
    for x in (ox + 100, ox + L - 100):
        f.ret(x - 12.5, oy + A, x + 12.5, oy + Atot - test)
    f.ret(ox, oy + Atot - test, ox + L, oy + Atot)
    f.texto("testeira 1200 x 400, PS 2 mm", (ox + L / 2, oy + Atot - test / 2), h=2.2, alinh="MIDDLE_CENTER")
    for k in range(5):
        cx = ox + 160 + k * 220
        f.ret(cx - 30, oy + A, cx + 30, oy + A + 180, "12_PRODUTO")
    f.cota((ox, oy), (ox + L, oy), (ox, oy - 60))
    f.cota((ox, oy), (ox, oy + A), (ox - 80, oy), angulo=90)
    f.cota((ox, oy), (ox, oy + Atot), (ox - 160, oy), angulo=90)
    vista_titulo(f, "VISTA FRONTAL 1:10", 60, 133)
    lx = ox + L + 260
    f.ret(lx, oy, lx + Pp, oy + A - tampo); f.ret(lx - 20, oy + A - tampo, lx + Pp + 20, oy + A)
    f.ret(lx + Pp / 2 - 12.5, oy + A, lx + Pp / 2 + 12.5, oy + Atot - test); f.ret(lx + Pp / 2 - 15, oy + Atot - test, lx + Pp / 2 + 15, oy + Atot)
    f.ret(lx + 40, oy + 60, lx + Pp - 40, oy + 600, "11_OCULTO")
    f.texto("porta de serviço no verso", (lx + Pp / 2, oy + 330), h=2.0, alinh="MIDDLE_CENTER")
    f.cota((lx, oy), (lx + Pp, oy), (lx, oy - 60))
    vista_titulo(f, "VISTA LATERAL 1:10", lx / e, 133)
    py = oy - 380 - (Pp + 40)
    f.ret(ox - 20, py, ox + L + 20, py + Pp + 40)
    for k in range(5):
        f.circulo((ox + 160 + k * 220, py + (Pp + 40) / 2), 30, "12_PRODUTO")
    f.cota((ox - 20, py), (ox + L + 20, py), (ox, py - 60))
    vista_titulo(f, "PLANTA DO TAMPO 1:10", 60, (py + Pp + 80) / e)
    notas(f, 330, 380, [
        "Balcão em MDF 18 mm laminado branco, 1200 x 950 x 500 mm, tampo 1240 x 540 mm.",
        "Frente em PS 2 mm impresso com a arte do KV, fixada com fita VHB.",
        "Testeira 1200 x 400 mm em PS 2 mm sobre 2 hastes em tubo Ø25 mm, altura total 2100 mm.",
        "Tampo com 5 borrifadores (um por fragrância) e porta-fitas olfativas.",
        "Porta de serviço no verso para estoque de fitas e frascos.",
        "Desmonta em 3 volumes (balcão, hastes, testeira) para transporte.",
        "Lugar: área promocional ao lado da entrada do corredor de limpeza, sem bloquear a passagem.",
        "Operação: 1 promotor em turnos de 6 h, fim de semana.",
    ])
    perspectiva(f, "estacao-recorte.jpg")
    return salvar(f, "P2_estacao-de-aroma")


# ---------------------------------------------------------------- 3 · display de chão em polionda (média)
def polionda():
    e = 8; f = folha(3, "Display de chão em polionda · vistas", e, "Polionda 4 mm impresso", "Conjunto médio · supermercado")
    L, A, Pp, base, header = 600, 1600, 400, 100, 300
    bandejas = [base, 380, 660, 940]
    ox, oy = P(f, 70, 150)
    f.ret(ox, oy, ox + L, oy + A - header); f.ret(ox, oy + A - header, ox + L, oy + A)
    f.texto("header 600 x 300 com o título", (ox + L / 2, oy + A - header / 2), h=2.2, alinh="MIDDLE_CENTER")
    for y in bandejas:
        f.ret(ox + 8, oy + y, ox + L - 8, oy + y + 60)
    f.cota((ox, oy), (ox + L, oy), (ox, oy - 60))
    f.cota((ox, oy), (ox, oy + A), (ox - 80, oy), angulo=90)
    f.cota((ox + L, oy + bandejas[1]), (ox + L, oy + bandejas[2]), (ox + L + 60, oy), angulo=90)
    vista_titulo(f, "VISTA FRONTAL 1:8", 70, 131)
    lx = ox + L + 300
    pts = [(lx, oy), (lx + Pp, oy), (lx + Pp, oy + A - header), (lx + 40, oy + A - header), (lx + 40, oy + A), (lx, oy + A)]
    f.poli(pts, fechado=True)
    for y in bandejas:
        f.linha((lx, oy + y), (lx + Pp, oy + y), "02_DOBRA_QUENTE")
    f.cota((lx, oy), (lx + Pp, oy), (lx, oy - 60))
    vista_titulo(f, "VISTA LATERAL 1:8", lx / e, 131)
    py = oy - 360 - Pp
    f.ret(ox, py, ox + L, py + Pp)
    f.linha((ox, py + Pp - 60), (ox + L, py + Pp - 60), "03_VINCO")
    f.cota((ox, py), (ox, py + Pp), (ox - 80, py), angulo=90)
    vista_titulo(f, "PLANTA 1:8", 70, (py + Pp + 40) / e)
    notas(f, 330, 380, [
        "Corpo, 4 bandejas e header em polionda 4 mm, impressão digital UV.",
        "Bandejas com aba frontal de 60 mm, encaixe por macho e fêmea nas laterais.",
        "Vão entre bandejas 220 mm livre: frascos de 500 ml e 1 L em pé.",
        "Carga por bandeja até 8 kg (8 frascos de 1 L).",
        "Chega plano numa caixa; monta em 10 minutos sem ferramenta.",
        "Lugar: encostado na gôndola de limpeza, junto da categoria, sem bloquear o corredor.",
        "QR único no header para o One Shot.",
    ])
    perspectiva(f, "polionda-recorte.jpg")
    return salvar(f, "P3_display-polionda")


# ---------------------------------------------------------------- 4 · wobbler (leve)
def wobbler():
    e = 1; f = folha(4, "Wobbler de fragrância · vistas", e, "PS 2 mm + haste PET 0,5 mm", "Conjunto leve · todos os canais")
    R, haste_l, haste_c = 60, 20, 80
    ox, oy = P(f, 120, 230)
    f.circulo((ox, oy), R)
    f.ret(ox - haste_l / 2, oy - R - haste_c, ox + haste_l / 2, oy - R + 10)
    f.ret(ox - haste_l / 2, oy - R - haste_c, ox + haste_l / 2, oy - R - haste_c + 20, "14_FITA")
    f.texto("fita dupla face 20 x 20", (ox + 18, oy - R - haste_c + 10), h=2.0, alinh="MIDDLE_LEFT")
    f.cota((ox - R, oy), (ox + R, oy), (ox, oy + R + 20))
    f.cota((ox + haste_l / 2, oy - R - haste_c), (ox + haste_l / 2, oy - R + 10), (ox + 50, oy), angulo=90)
    vista_titulo(f, "VISTA FRONTAL 1:1", 60, 330)
    lx = ox + 160
    f.ret(lx, oy - R, lx + 2, oy + R)
    f.poli([(lx + 2, oy - R + 10), (lx + 2, oy - R - 40), (lx + 30, oy - R - 80)])
    f.texto("haste PET flexível", (lx + 34, oy - R - 80), h=2.0, alinh="MIDDLE_LEFT")
    f.cota((lx, oy + R), (lx + 2, oy + R), (lx, oy + R + 20), override={"dimtix": 0})
    vista_titulo(f, "VISTA LATERAL 1:1", lx - 10, 330)
    notas(f, 330, 380, [
        "Disco Ø120 mm em PS 2 mm, impressão UV frente e verso, corte reto.",
        "5 versões, uma por fragrância (Lavander, Blue Flowers, Jardin, Passion, Luxury).",
        "Haste PET cristal 0,5 mm, 20 x 90 mm, colada com fita VHB.",
        "Fixação na borda da prateleira com fita dupla face 20 x 20 mm.",
        "Fica na frente do bloco da fragrância, sem cobrir o preço.",
        "Kit por loja: 2 de cada versão (10 peças).",
    ])
    perspectiva(f, "wobbler-recorte.jpg")
    return salvar(f, "P4_wobbler")


# ---------------------------------------------------------------- 5 · régua de gôndola (leve)
def regua():
    e = 2; f = folha(5, "Régua de escolha · vistas", e, "PS 1 mm impresso", "Conjunto leve · todos os canais")
    L, A, aba = 1000, 40, 15
    ox, oy = P(f, 40, 300)
    f.ret(ox, oy, ox + L, oy + A)
    nomes = ["Lavander", "Blue Flowers", "Jardin", "Passion", "Luxury"]
    tit, seg = 250, 150
    f.linha((ox + tit, oy), (ox + tit, oy + A), "11_OCULTO")
    f.texto("título + logo", (ox + tit / 2, oy + A / 2), h=2.6, alinh="MIDDLE_CENTER")
    for k in range(5):
        x0 = ox + tit + k * seg
        if k: f.linha((x0, oy), (x0, oy + A), "11_OCULTO")
        f.texto(nomes[k], (x0 + seg / 2, oy + A / 2), h=2.6, alinh="MIDDLE_CENTER")
    f.cota((ox, oy), (ox + L, oy), (ox, oy - 40))
    f.cota((ox, oy + A), (ox + tit, oy + A), (ox, oy + A + 30))
    f.cota((ox + tit, oy + A), (ox + tit + seg, oy + A), (ox, oy + A + 30))
    f.cota((ox + L, oy), (ox + L, oy + A), (ox + L + 30, oy), angulo=90)
    vista_titulo(f, "VISTA FRONTAL 1:2", 40, 345)
    # corte A com a aba de encaixe, desenhado 5 vezes maior que a folha (2,5:1); as cotas mostram o valor real
    cx, cy = P(f, 120, 150)
    k = 5
    f.ret(cx, cy, cx + 1 * k, cy + A * k, "13_VISTA")
    f.ret(cx - aba * k, cy, cx, cy + 1 * k, "13_VISTA")
    f.cota((cx + 1 * k, cy), (cx + 1 * k, cy + A * k), (cx + 1 * k + 60, cy), angulo=90, lfac=1 / k)
    f.cota((cx - aba * k, cy), (cx, cy), (cx, cy - 50), lfac=1 / k)
    f.cota((cx, cy + A * k), (cx + 1 * k, cy + A * k), (cx, cy + A * k + 40), lfac=1 / k)
    f.chamada((cx, cy + 2), (cx - 120, cy + 120), "dobra quente 90°")
    f.texto("frente impressa", (cx + 1 * k + 90, cy + A * k * 0.75), h=2.2, alinh="MIDDLE_LEFT")
    f.texto("aba de encaixe no porta-preço", (cx - aba * k - 10, cy + 3), h=2.2, alinh="MIDDLE_RIGHT")
    vista_titulo(f, "CORTE A · DETALHE 2,5:1", 60, 110)
    notas(f, 330, 260, [
        "PS 1 mm, impressão UV, 1000 x 40 mm, com aba de 15 mm dobrada a quente.",
        "Encaixa no porta-preço da prateleira, sem cola e sem cobrir a etiqueta.",
        "Faixa de título de 250 mm (frase e logo) e 5 faixas de 150 mm, uma por fragrância.",
        "Vai num perfil cristal de PVC para porta-preço; corta no vinco para prateleira de 800 mm.",
        "Kit por loja: 4 réguas (2 prateleiras da linha).",
    ])
    perspectiva(f, "regua-recorte.jpg", y=95, alt=90)
    return salvar(f, "P5_regua-de-escolha")


if __name__ == "__main__":
    for fn in (aramado, estacao, polionda, wobbler, regua):
        print(fn())
