from io import BytesIO
from html import escape
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook

def report_html(reviews, runs):
    rows = "".join(f"<tr><td>{escape(r['agent'])}</td><td>{escape(r['title'])}</td><td>{escape(r['status'])}</td><td>{escape(r['created_at'])}</td></tr>" for r in reviews)
    run_rows = "".join(f"<tr><td>{escape(r['agent'])}</td><td>{escape(r['title'])}</td><td>{escape(r['created_at'])}</td></tr>" for r in runs)
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>QA Evidence Report</title>
    <style>body{{font:14px Arial;margin:36px;color:#172033}}h1{{color:#b4232d}}table{{border-collapse:collapse;width:100%;margin:16px 0 28px}}td,th{{border:1px solid #ddd;padding:9px;text-align:left}}th{{background:#f3f4f6}}</style></head>
    <body><h1>Agentic QA Hub — Evidence Report</h1><p>Generated from records stored in this local workspace.</p>
    <h2>Human review queue</h2><table><tr><th>Agent</th><th>Item</th><th>Status</th><th>Created</th></tr>{rows}</table>
    <h2>Agent runs</h2><table><tr><th>Agent</th><th>Run</th><th>Created</th></tr>{run_rows}</table></body></html>'''

def report_pdf(reviews, runs):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [Paragraph("Agentic QA Hub — Evidence Report", styles["Title"]), Spacer(1, 12),
             Paragraph("Human review queue", styles["Heading2"])]
    data = [["Agent", "Item", "Status"]] + [[r["agent"], r["title"][:45], r["status"]] for r in reviews[:100]]
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#eeeeee")),
                               ("GRID",(0,0),(-1,-1),0.4,colors.grey),("FONTSIZE",(0,0),(-1,-1),8)]))
    story += [table, Spacer(1, 16), Paragraph("Agent runs", styles["Heading2"])]
    data2 = [["Agent", "Run"]] + [[r["agent"], r["title"][:55]] for r in runs[:100]]
    table2 = Table(data2, repeatRows=1)
    table2.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#eeeeee")),
                                ("GRID",(0,0),(-1,-1),0.4,colors.grey),("FONTSIZE",(0,0),(-1,-1),8)]))
    story.append(table2)
    doc.build(story)
    return buf.getvalue()

def report_xlsx(reviews, runs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Review Queue"
    ws.append(["Agent", "Item", "Status", "Created", "Reviewer note"])
    for r in reviews:
        ws.append([r["agent"], r["title"], r["status"], r["created_at"], r.get("reviewer_note","")])
    ws2 = wb.create_sheet("Agent Runs")
    ws2.append(["Agent", "Run", "Created"])
    for r in runs:
        ws2.append([r["agent"], r["title"], r["created_at"]])
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()
