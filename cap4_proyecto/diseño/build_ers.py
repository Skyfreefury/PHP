import re, html, sys
D = "D:/Escuela/FP DAW/PHP/cap4_proyecto/memoria/"
md = open(D+"ERS_borrador.md", encoding="utf-8").read()
md = md.split("\n",1)[1]  # quitar título del borrador

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    return t

BREAK_BEFORE = {"7.", "8.", "9."}
out, lines, i = [], md.split("\n"), 0
while i < len(lines):
    l = lines[i]
    if not l.strip(): i += 1; continue
    if l.startswith("## "):
        txt = l[3:]; cls = ' class="nueva"' if txt.split(" ")[0] in BREAK_BEFORE else ""
        out.append(f"<h2{cls}>{inline(txt)}</h2>"); i += 1; continue
    if l.startswith("### "):
        out.append(f"<h3>{inline(l[4:])}</h3>"); i += 1; continue
    m = re.match(r"!\[(.*?)\]\((.*?)\)", l)
    if m:
        out.append(f'<figure><img src="{m.group(2)}" alt="{html.escape(m.group(1))}"></figure>'); i += 1; continue
    if l.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
        head, body = rows[0], rows[2:]
        t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
        t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
        out.append(t + "</tbody></table>"); continue
    if re.match(r"^(- |\d+\. )", l):
        tag = "ol" if l[0].isdigit() else "ul"; items = []
        while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i]):
            items.append(re.sub(r"^(- |\d+\. )", "", lines[i])); i += 1
        out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>"); continue
    para = []
    while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |\d+\. |!\[)", lines[i]):
        para.append(lines[i]); i += 1
    out.append(f"<p>{inline(' '.join(para))}</p>")

body = "\n".join(out)
css = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm;
  @bottom-left { content: "Arrivederci  ·  ERS"; font: 8pt 'Playfair Display', Georgia, serif; color: #9a8f84; }
  @bottom-right { content: counter(page); font: bold 9pt 'DM Sans', sans-serif; color: #e8590c; } }
@page :first { margin: 0; @bottom-left { content: none } @bottom-right { content: none } }
body { margin: 0; font-family: 'DM Sans', 'DM Sans', sans-serif; color: #2b2622; font-size: 10.5pt; line-height: 1.55; }
h2 { font-family: 'Playfair Display', 'Playfair Display', Georgia, serif; font-weight: 600; color: #141414; font-size: 22pt;
     margin: 26pt 0 10pt; padding-bottom: 6pt; border-bottom: 2pt solid #e8590c; break-after: avoid; }
h2.nueva { break-before: page; margin-top: 0; }
h3 { color: #141414; font-size: 11.5pt; margin: 16pt 0 6pt; break-after: avoid; }
h3::before { content: ""; display: inline-block; width: 7pt; height: 7pt; border-radius: 50%; background: #e8590c; margin-right: 7pt; vertical-align: 1pt; }
p { margin: 0 0 8pt; }
ul, ol { margin: 0 0 8pt; padding-left: 18pt; } li { margin-bottom: 3pt; } ul li::marker { color: #e8590c; }
table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 6pt 0 14pt; font-size: 9pt;
        border: 0.6pt solid #e6dfd6; border-radius: 6pt; overflow: hidden; }
tr { break-inside: avoid; }
th { background: #f6f1ea; color: #141414; text-align: left; padding: 7pt 9pt; font-weight: 700;
     border-bottom: 1.2pt solid #e8590c; font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.4pt; }
td { padding: 6pt 9pt; border-bottom: 0.5pt solid #efe9e1; vertical-align: top; }
tbody tr:last-child td { border-bottom: none; }
td:first-child, th:first-child { white-space: nowrap; }
td:first-child { font-weight: 600; color: #b8440a; }
code { font-family: Consolas, monospace; font-size: 8.5pt; background: #f6f1ea; color: #8a3a0c; padding: 0 3pt; border-radius: 3pt; }
figure { margin: 6pt 0 16pt; break-inside: avoid; text-align: center; }
figure img { max-width: 100%; max-height: 120mm; border-radius: 8pt; box-shadow: 0 2pt 8pt rgba(0,0,0,0.12); }
.portada { height: 296.5mm; position: relative; box-sizing: border-box; padding: 0 22mm; background: #141414; color: #f4efe8;
           display: flex; flex-direction: column; justify-content: flex-end; padding-bottom: 30mm; }
.portada .marca { font-family: 'Playfair Display', Georgia, serif; font-size: 15pt; color: #f4efe8; position: absolute; top: 22mm; }
.portada .marca::before { content: ""; display: inline-block; width: 9pt; height: 9pt; border-radius: 50%; background: #e8590c; margin-right: 8pt; }
.portada .kicker { color: #e8590c; font-size: 10pt; letter-spacing: 2pt; text-transform: uppercase; margin-bottom: 10pt; }
.portada h1 { font-family: 'Playfair Display', Georgia, serif; font-weight: 600; font-size: 40pt; line-height: 1.08; margin: 0 0 16pt; color: #fff; }
.portada .desc { color: #cfc6bb; max-width: 150mm; margin-bottom: 26pt; }
.portada dl { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; border-top: 0.6pt solid #4a433d; padding-top: 12pt; margin: 0; }
.portada dt { color: #9a8f84; font-size: 8pt; text-transform: uppercase; letter-spacing: 1pt; }
.portada dd { margin: 3pt 0 0; font-size: 10pt; color: #fff; }
"""
cover = """<section class="portada">
<div class="marca">Arrivederci</div>
<div class="kicker">Especificación de requisitos software</div>
<h1>Tienda web<br>de pizzería</h1>
<p class="desc">Proyecto del capítulo 4 de Desarrollo web en entorno servidor: requisitos, casos de uso, reglas de negocio, modelo de datos, prototipos, pruebas de aceptación y trazabilidad.</p>
<dl><div><dt>Versión</dt><dd>1.0</dd></div><div><dt>Fecha</dt><dd>6 nov 2026</dd></div><div><dt>Módulo</dt><dd>DWES · DAW</dd></div><div><dt>Tecnologías</dt><dd>PHP 8 · MySQL</dd></div></dl>
</section>"""
doc = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>ERS Arrivederci</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&family=Playfair+Display:wght@400;600&display=block" rel="stylesheet">
<base href="file:///D:/Escuela/FP%20DAW/PHP/cap4_proyecto/memoria/"><style>{css}</style></head>
<body>{cover}<h2 class="nueva">{body[4:] if False else ''}</h2>{body}</body></html>"""
doc = doc.replace('<h2 class="nueva"></h2>', '<div style="break-before:page"></div>', 1)
open(sys.argv[1], "w", encoding="utf-8").write(doc)
print("ok")
