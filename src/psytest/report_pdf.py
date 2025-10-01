from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def render_pdf(scores: dict, chart_path: Path, out_path: Path, title: str = "Отчёт по психологическому тестированию (PAEI)"):
    c = canvas.Canvas(str(out_path), pagesize=A4)
    width, height = A4

    c.setFont("Times-Roman", 16)
    c.drawString(2*cm, height - 2*cm, title)

    c.setFont("Times-Roman", 12)
    c.drawString(2*cm, height - 3*cm, f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    y = height - 4*cm
    for k in sorted(scores.keys()):
        c.drawString(2*cm, y, f"{k}: {scores[k]}")
        y -= 0.7*cm

    if chart_path and chart_path.exists():
        c.drawImage(str(chart_path), width - 14*cm, 2*cm, width=12*cm, preserveAspectRatio=True, mask='auto')

    c.showPage()
    c.save()
    return out_path
