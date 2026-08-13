# 0.1.0

Lizenz: BSD-3-Clause. Copyright (c) 2026 lesecuritae für Tarnkappe.info.

KorbKlar ist die überarbeitete Ausgabe des bisherigen Supermarkt-Preisvergleichs. Die Vergleichslogik und die bestehenden Quellenadapter bleiben erhalten; Name, Oberfläche und öffentliche Projektmetadaten wurden auf KorbKlar umgestellt.

## Änderungen

- Neues KorbKlar-Branding für Weboberfläche, Favicon und README-Grafik.
- Docker-Dienst, Container und Daten-Volume tragen den neuen Namen `korbklar`.
- Python-Paketmetadaten und User-Agent wurden auf KorbKlar aktualisiert.
- Native Installationen verwenden für neue Laufzeitdaten `~/.local/state/korbklar`; ein vorhandener alter Zustandspfad wird automatisch weiterverwendet.
- Dunkles Farbschema an die grüne KorbKlar-Farbwelt angepasst.
- README- und SVG-Branding bereinigt; die Header-Grafik kommt ohne problematische SVG-Filter aus.
- Bestehende Preis-, Mengen-, Marken-, Händler-, Bild- und Cache-Regressionstests bleiben erhalten.

## Docker-Hinweis beim Umstieg

Durch den neuen Compose-Projektnamen und das neue Volume `korbklar-data` wird ein bestehendes Docker-Volume der alten Ausgabe nicht automatisch eingebunden. Darin liegen nur Laufzeitdaten wie Snapshots, Signierschlüssel und Bildcache. Für einen frischen Start kann das alte Volume unangetastet bleiben; bestehende signierte Ergebnislinks gelten dann nicht im neuen Volume weiter.

---

# 0.0.1

Lizenz: BSD-3-Clause. Copyright (c) 2026 lesecuritae für Tarnkappe.info.

Erster öffentlicher GitHub-Stand des Supermarkt-Preisvergleichs.

## Enthalten

- Browseroberfläche mit Postleitzahl als einzigem Pflichtfeld.
- Direkte Händleradapter für REWE, EDEKA, Kaufland, Marktkauf und ALDI.
- Regionale Marktguru-Daten für Lidl, PENNY, Netto und GLOBUS sowie händlerspezifische Fallbacks.
- Sonntagsauswahl der kommenden Angebotswoche; Kaufland berücksichtigt seinen Donnerstag-bis-Mittwoch-Zyklus.
- Persistenter 24-Stunden-Cache für die Kaufland-Filialzuordnung und den gesetzten Browserzustand. Die Angebote selbst werden weiterhin frisch abgerufen.
- Persistenter 24-Stunden-Cache für die REWE-Marktauswahl; Angebotsdaten bleiben davon getrennt und werden frisch geladen.
- Ergebnisansicht mit Reiter zum Einblenden teurerer Dubletten; die Anzahl bezieht sich auf den aktuellen Text- und Händlerfilter.
- Normalisierung von Packungsgrößen und Grundpreisen; alternative Größen werden als Alternativen dargestellt und nicht addiert.
- Platzhalter wie `This is no brand` werden nicht als Marke angezeigt oder für den Produktabgleich verwendet. Auch Varianten mit angehängter Quell-ID wie `thisisnobrand123` werden verworfen.
- REWE-Fußnoten in Produkttiteln, etwa die Backstation-Markierung `²`, werden nicht mehr als Bestandteil des Produktnamens übernommen.
- Bei Auswahl genau eines Händlers wird die redundante Händlerspalte in der Ergebnisliste ausgeblendet.
- Bonusprogramme, Produktfilter, Sortierung und Endless Scroll.
- Persistenter Ergebnis- und Bildcache im Daten-Volume sowie signierte Ergebnis- und Bildlinks.
- Optionaler REST-Endpunkt und optionaler API-Key.
- Konfigurationswerte werden bei ungültigen Integer-Werten auf sichere Defaults und Grenzen zurückgeführt, statt den Dienst beim Import zu beenden.

## Betrieb

Die Standardinstallation besteht aus einem Anwendungscontainer auf Port 8000. Laufzeitdaten liegen ausschließlich im Docker-Volume beziehungsweise unter dem konfigurierten Datenpfad und gehören nicht ins Repository.

## Dokumentation

- Installation, Architektur und Abhängigkeiten sind im README beschrieben.
- Geplante spätere Integrationen mit Grocy und KitchenOwl sind als Roadmap gekennzeichnet.
- Die Tarnkappe.info-Spendenseite und die aktuell veröffentlichte Monero-Adresse sind im README verlinkt.
