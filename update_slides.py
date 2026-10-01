from pathlib import Path
import shutil
import win32com.client

BASE = Path(__file__).parent
SLIDES = BASE / "slides"
OUTPUT = BASE / "docs" / "assets" / "slides"

powerpoint = win32com.client.Dispatch("PowerPoint.Application")
powerpoint.Visible = True

for pptx in SLIDES.glob("*.pptx"):
    out = OUTPUT / pptx.stem

    if out.exists():
        shutil.rmtree(out)

    out.mkdir(parents=True)

    presentation = powerpoint.Presentations.Open(str(pptx.resolve()))

    # Export every slide as JPG
    presentation.Export(str(out.resolve()), "JPG")

    presentation.Close()

    print(f"Updated {pptx.stem}")

powerpoint.Quit()

print("Done.")