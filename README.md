# otto-extensions

Bausteine für **[Otto](https://github.com/philipp-tch/otto)** — Erweiterungen (`.ottoext`),
Themes (`.ottotheme`), Sprachpakete (`.ottolang`) und Regel-Pakete (`.ottopack`).

Otto lädt sie über seinen Katalog: der Cockpit fragt die **Releases dieses Repos** ab, lädt
ein Paket, prüft es und installiert es. Der Katalog folgt dabei **nie** einer freien URL aus
Release-Metadaten — Otto konstruiert jede Adresse selbst aus Repo, Tag und Dateiname und
prüft sie gegen eine Herkunfts-Allowlist.

## Was hier liegt

| Ordner | Inhalt |
|---|---|
| `themes/` | Beispiel-Themes als `.ottotheme`-Quellen |
| `kit/` | Prüf-Kit: dieselben Klassen wie im Core, als wiederverwendbares Paket |

Ein Ordner je Baustein, ein gemeinsames Release-Schema (`<id>-v<version>`).

## Die zwei Paketarten unterscheiden sich grundsätzlich

**Themes sind code-frei.** Ein `.ottotheme` enthält `theme.json` und Bilder — es führt
nichts aus. Deshalb braucht es **keine Signatur**; geprüft werden Schema, Dateitypen (nur
Pixelformate und WOFF2, **kein SVG** — das wäre ein XSS-Weg) und Grössen.

**Erweiterungen enthalten Code.** Ein `.ottoext` wird **vor dem Auspacken** gegen eine
Ed25519-Signatur geprüft; erst danach sieht Otto den Inhalt. Ohne bekannten Schlüssel wird
nichts installiert — die Vertrauensliste ist absichtlich leer, bis ein Schlüssel bewusst
eingetragen wird.

> Dass Themes ohne Signatur auskommen, ist kein Rabatt, sondern die Folge davon, dass sie
> nichts ausführen können. Wer hier eine Erweiterung ohne Signatur unterbringen will, muss
> das Format wechseln — und das Format bestimmt die Prüfung.

## Gates: kein Rabatt gegenüber dem Core

Dieselben Prüfklassen wie im Hauptprojekt laufen hier als CI: Namensschema, Dateigrössen,
fail-loud statt stiller Fehler, Blob-Wächter (keine Secrets/Dumps), Firmenfrei (keine
Kunden-Identifikatoren). Ein Baustein, der hier durchfällt, gehört nicht ins Release.

## Beitragen

Noch kein offener Beitrags-Prozess — dieses Repo begleitet die Otto-Entwicklung.
Lizenz und Vorgehen richten sich nach dem Hauptprojekt.
