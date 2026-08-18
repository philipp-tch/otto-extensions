#!/usr/bin/env python3
"""Prueft die Bausteine im Baum — dieselben Klassen wie die Core-Gates, ohne Rabatt.

Bewusst OHNE Otto-Core-Abhaengigkeit: diese Pruefungen sollen auch in einem frischen
Checkout laufen, in dem der Core nicht daneben liegt. Was NUR mit dem Core geht (die
volle `.ottotheme`-Verifikation), macht `pack_theme.py` beim Bauen.
"""

import json
import pathlib
import sys

PFLICHT = ("id", "name", "version", "kind", "farben")


def main() -> int:
    wurzel = pathlib.Path(__file__).resolve().parent.parent
    fehler = []
    themes = sorted((wurzel / "themes").glob("*/"))
    if not themes:
        fehler.append("themes/ ist leer — dann prueft dieses Gate nichts und waere still gruen.")
    for d in themes:
        manifest = d / "theme.json"
        if not manifest.exists():
            fehler.append(f"{d.name}: theme.json fehlt")
            continue
        try:
            t = json.loads(manifest.read_text("utf-8"))
        except ValueError as e:
            fehler.append(f"{d.name}: theme.json ist kein gueltiges JSON ({e})")
            continue
        for k in PFLICHT:
            if k not in t:
                fehler.append(f"{d.name}: Pflichtfeld '{k}' fehlt")
        if t.get("kind") != "theme":
            fehler.append(f"{d.name}: kind={t.get('kind')!r}, erwartet 'theme'")
        # Ordnername == id: sonst zeigt das Release-Schema <id>-v<version> auf einen
        # anderen Ordner, als der Inhalt behauptet — eine stille Verwechslung beim
        # Ausliefern, die erst der Nutzer merkt.
        if t.get("id") != d.name:
            fehler.append(f"{d.name}: Ordnername != id ({t.get('id')!r})")
        else:
            print(f"  ok  {d.name} v{t.get('version')}")
    if fehler:
        print("\nFEHLER:", file=sys.stderr)
        for f in fehler:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"\n{len(themes)} Baustein(e) geprueft, alle in Ordnung.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
