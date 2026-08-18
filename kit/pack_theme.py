#!/usr/bin/env python3
"""Baut ein `.ottotheme` aus `themes/<id>/` — und prueft es mit Ottos EIGENEM Verifizierer.

WARUM DIE PRUEFUNG HIER STEHT. Ein Paketierer, der nur zippt, verschiebt den Fehler an
die Stelle, an der er am teuersten ist: in die Installation beim Nutzer. Otto prueft
`.ottotheme` ohnehin fail-closed (Schema, Dateitypen per MAGIC BYTES, Groessen) — dieselbe
Funktion hier aufzurufen kostet nichts und faengt einen kaputten Baustein, bevor er ein
Release wird.

Ohne erreichbaren Otto-Core wird NICHT still gezippt: dann ist "kann nicht pruefen" die
Antwort, nicht "ist in Ordnung".
"""

import argparse
import io
import json
import pathlib
import sys
import zipfile

ASSET_SUFFIXE = (".png", ".jpg", ".jpeg", ".webp", ".woff2")


def baue(quelle: pathlib.Path) -> bytes:
    theme = quelle / "theme.json"
    if not theme.exists():
        raise SystemExit(f"ABBRUCH: {theme} fehlt — ein Theme ohne Manifest gibt es nicht.")
    json.loads(theme.read_text("utf-8"))  # frueh scheitern, nicht erst im Verifizierer
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("theme.json", theme.read_text("utf-8"))
        for datei in sorted((quelle / "assets").rglob("*")) if (quelle / "assets").exists() else []:
            if datei.is_file():
                if datei.suffix.lower() not in ASSET_SUFFIXE:
                    # Frueh und laut: SVG ist der bekannte XSS-Weg, der Verifizierer
                    # lehnt es ohnehin ab — hier steht der Grund lesbar dabei.
                    raise SystemExit(f"ABBRUCH: {datei.name} ist kein erlaubtes Asset "
                                     f"(nur {', '.join(ASSET_SUFFIXE)}; SVG ist verboten).")
                z.writestr(f"assets/{datei.relative_to(quelle / 'assets').as_posix()}",
                           datei.read_bytes())
    return buf.getvalue()


def pruefe(daten: bytes, core: pathlib.Path):
    src = core / "10_platform" / "src"
    if not src.exists():
        raise SystemExit(
            f"ABBRUCH: Otto-Core nicht gefunden ({src}). Ohne den Verifizierer wird nicht "
            "gepackt — 'ungeprueft' ist kein Ergebnis. Pfad mit --core angeben."
        )
    sys.path.insert(0, str(src))
    from otto_mcp.id122_theme.id122_03_package import verify_theme_package
    return verify_theme_package(daten)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("quelle", help="Ordner unter themes/, z.B. themes/otto-hell")
    ap.add_argument("--out", required=True)
    ap.add_argument("--core", default="../boess-lib/v7", help="Pfad zum Otto-Core")
    a = ap.parse_args()
    daten = baue(pathlib.Path(a.quelle))
    res = pruefe(daten, pathlib.Path(a.core))
    ziel = pathlib.Path(a.out)
    ziel.write_bytes(daten)
    print(f"{ziel} ({len(daten)} Bytes) | id={res['theme']['id']} | {res['content_hash']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
