from io import BytesIO

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import SummarySerializer, TimePointSerializer
from .services import filtered_occurrences, summary_counts, time_series
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from occurrences.models import Occurrence

import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
from django.utils.dateformat import format as dj_format

# JSON summary (KPIs)
class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs, date_field = filtered_occurrences(request.query_params)
        data = summary_counts(qs)
        return Response(SummarySerializer(data).data)

# JSON time-series (day/week/month)
@method_decorator(cache_page(60 * 5), name="dispatch")  # cache 5 mins
class TrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        granularity = request.query_params.get("granularity", "month")
        qs, date_field = filtered_occurrences(request.query_params)
        data = time_series(qs, date_field, granularity=granularity)
        return Response(TimePointSerializer(data, many=True).data)
    

class OccurrencesPDFView(APIView):
    """
    Returns a generated PDF. Admin-only by default.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs, date_field = filtered_occurrences(request.query_params)
        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=25
        )
        styles = getSampleStyleSheet()
        elements = []

        title = "DOBS – Occurrences Report"
        elements.append(Paragraph(title, styles["Title"]))

        # Summary section
        sums = summary_counts(qs)
        summary_lines = (
            f"Total: {sums['total']} | Open: {sums['open']} | In Progress: {sums['in_progress']} | "
            f"Closed: {sums['closed']} | High: {sums['sev_high']} | Med: {sums['sev_medium']} | Low: {sums['sev_low']}"
        )
        elements.append(Paragraph(summary_lines, styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Table header
        data = [[
            "ID", "Title", "Category", "Status", "Severity",
            "Reporter", "Date"
        ]]

        
        date_attr = "occurred_at" if hasattr(Occurrence, "occurred_at") else "created_at"

        for o in qs.select_related("reported_by").order_by(f"-{date_attr}")[:1000]:  # cap rows
            data.append([
                str(o.id),
                (o.title or "")[:40],
                getattr(o, "category", "") or "",
                o.status,
                getattr(o, "severity", "") or "",
                getattr(o.reported_by, "username", ""),
                getattr(o, date_attr).strftime("%Y-%m-%d %H:%M") if getattr(o, date_attr) else ""
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ]))
        elements.append(table)

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        filename = "occurrences-report.pdf"
        resp = HttpResponse(content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        resp.write(pdf)
        return resp

"""
Implementation of charts & graphs for incidents trends through Server-rendered PND which does not require front end.

"""
class TrendPNGView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        granularity = request.query_params.get("granularity", "month")
        qs, date_field = filtered_occurrences(request.query_params)
        series = time_series(qs, date_field, granularity)

        x = [dj_format(p["bucket"], "Y-m") if granularity == "month"
             else dj_format(p["bucket"], "Y-m-d") for p in series]
        y = [p["count"] for p in series]

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(x, y, marker="o")
        ax.set_title("Incident Trends")
        ax.set_xlabel("Period")
        ax.set_ylabel("Incidents")
        ax.grid(True)
        fig.tight_layout()

        png_io = BytesIO()
        fig.savefig(png_io, format="png")
        plt.close(fig)
        png_io.seek(0)

        resp = HttpResponse(png_io.read(), content_type="image/png")
        resp["Content-Disposition"] = 'inline; filename="trends.png"'
        return resp