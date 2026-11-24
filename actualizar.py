#!/usr/bin/env python3
"""Actualiza este sitio con el deck de la tesis.

Copia desde ../tesis_gendocsv3/presentacion solo lo que se presenta: los dos
HTML, las fuentes, las imágenes y los clips. El guion, las notas de diseño y
las capturas fuente no se copian. Después de correrlo: git add -A, commit y push.

    python3 actualizar.py
"""
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ORIGEN = AQUI.parent / 'tesis_gendocsv3' / 'presentacion'
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
INICIO = 'deck.html'  # paleta que abre el link corto: deck.html (granate) o deck-azul.html (azul)

INDEX = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{NOINDEX}
<meta http-equiv="refresh" content="0; url={INICIO}">
<title>Defensa GENDocs V3</title>
</head>
<body>
<p><a href="{INICIO}">Abrir la presentación</a></p>
</body>
</html>
'''


def main():
    if not (ORIGEN / 'deck.html').exists():
        raise SystemExit(f'no encuentro {ORIGEN / "deck.html"}')
    for nombre in ('deck.html', 'deck-azul.html'):
        html = (ORIGEN / nombre).read_text(encoding='utf-8')
        marca = '<meta charset="utf-8">'
        if marca not in html:
            raise SystemExit(f'{nombre} ya no trae {marca}')
        (AQUI / nombre).write_text(html.replace(marca, marca + '\n' + NOINDEX, 1), encoding='utf-8')
    for carpeta in ('fonts', 'img', 'video'):
        destino = AQUI / carpeta
        if destino.exists():
            shutil.rmtree(destino)
        shutil.copytree(ORIGEN / carpeta, destino)
    (AQUI / 'index.html').write_text(INDEX, encoding='utf-8')
    (AQUI / '.nojekyll').write_text('', encoding='utf-8')
    print('sitio actualizado desde', ORIGEN)


if __name__ == '__main__':
    main()
