"""Build a self-contained PDF lab report with rendered console evidence."""

from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
OUT = HERE / "evidence"
OUT.mkdir(exist_ok=True)


def run(args, cwd=HERE):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    return (result.stdout + result.stderr).strip() or f"(exit code {result.returncode})"


baseline = """from pathlib import Path
import sys
sys.path.insert(0, str((Path.cwd() / 'Lab 6').resolve()))
from movie_tickets import ticket_price, group_discount, snack_combo
cases = [
    ('ticket_price wrong type', lambda: ticket_price('regular', None, 12, False)),
    ('ticket_price negative age', lambda: ticket_price('regular', -1, 12, False)),
    ('group_discount wrong type', lambda: group_discount('five', False)),
    ('snack_combo wrong type', lambda: snack_combo(None, False)),
    ('snack_combo unknown size silently accepted', lambda: snack_combo('mystery', False)),
]
for label, operation in cases:
    try:
        print(f'{label}: {operation()}')
    except Exception as exc:
        print(f'{label}: {type(exc).__name__}: {exc}')
"""
base_text = run([str(PYTHON), "-c", baseline], cwd=ROOT)
app_text = run([str(PYTHON), "processor.py"])
test_text = run([str(PYTHON), "-m", "pytest", "-q", "test_processor.py"])


def render(title, body, filename):
    width, margin = 1500, 60
    font_path = Path("C:/Windows/Fonts/consola.ttf")
    font = ImageFont.truetype(str(font_path), 24) if font_path.exists() else ImageFont.load_default()
    title_font = ImageFont.truetype(str(font_path), 32) if font_path.exists() else font
    lines = body.splitlines() or [""]
    height = max(440, 150 + 38 * (len(lines) + 2))
    im = Image.new("RGB", (width, height), "#101820")
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((24, 24, width - 24, height - 24), radius=18, fill="#17232e", outline="#465563", width=2)
    draw.text((margin, 48), title, fill="#7dd3fc", font=title_font)
    draw.text((margin, 108), "PS> python / lab evidence transcript", fill="#a3b8c7", font=font)
    y = 160
    for line in lines:
        draw.text((margin, y), line[:105], fill="#e2e8f0", font=font)
        y += 38
    path = OUT / filename
    im.save(path)
    return im


screens = [
    render("Before hardening: fuzz style probes", base_text, "baseline_failures.png"),
    render("Hardened processor.py", app_text, "fixed_application.png"),
    render("Hypothesis test_processor.py", test_text, "passing_tests.png"),
]

pages = [Image.new("RGB", (screens[0].width, 220), "white")] + screens
cover = ImageDraw.Draw(pages[0])
cover.text((70, 55), "LAB 7: FUZZ TESTING", fill="#102a43", font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40))
cover.text((70, 115), "Movie ticket input validation | Hypothesis evidence", fill="#334e68", font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26))
cover.text((70, 165), "Adapted to the three pricing functions supplied in Lab 6.", fill="#486581", font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22))

pdf_path = HERE / "Lab7_FuzzTesting_Report.pdf"
pages[0].save(pdf_path, "PDF", resolution=120.0, save_all=True, append_images=pages[1:])
print(f"Created {pdf_path}")
