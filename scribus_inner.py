print("SCRIPT STARTED")

import scribus
import sys
import json
import os
import traceback

def main():
    try:
        print("Reading config...")

        config = json.load(open(sys.argv[1]))

        # Base directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print("Base dir:", base_dir)

        # Load data (JSON for now)
        json_path = os.path.join(base_dir, "cards.json")
        print("Loading cards from:", json_path)

        data = json.load(open(json_path))

        # Reverse order (OWASP requirement)
        cards = list(reversed(data["cards"]))

        # Load template
        sla_path = config["sla"]
        print("Opening template:", sla_path)

        scribus.openDoc(sla_path)

        # Fill data into pages
        for i, card in enumerate(cards):
            if i > 0:
                scribus.newPage(-1)

            scribus.gotoPage(i + 1)

            print(f"Filling card {i+1}")

            scribus.setText(card["code"], "CARD_CODE")
            scribus.setText(card["title"], "CARD_TITLE")
            scribus.setText(card["description"], "CARD_DESC")

        # Export PDF (PRINT READY)
        pdf = scribus.PDFfile()

        output_path = config["output"]
        print("Saving PDF to:", output_path)

        pdf.file = output_path

        # OWASP print requirements
        pdf.version = 11  # PDF/X-1a:2001
        pdf.info = "OWASP Cornucopia Print Deck"

        # 3mm bleed (~8.5 points)
        pdf.bleedTop = 8.5
        pdf.bleedBottom = 8.5
        pdf.bleedLeft = 8.5
        pdf.bleedRight = 8.5

        # Fonts (PDF/X requires embedding)
        pdf.embedFonts = True

        print("Exporting print-ready PDF...")
        pdf.save()

        print("DONE ✅")

        scribus.closeDoc()
        scribus.quit()

    except Exception as e:
        print("❌ ERROR OCCURRED:")
        traceback.print_exc()

main()