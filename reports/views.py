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

import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
from django.utils.dateformat import format as dj_format
from .models import Report
from rest_framework import generics, filters
from .serializers import ReportSerializer
from .filters import ReportFilter

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
    
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import Occurrence
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class OccurrencesPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Occurrence.objects.all()
        date_str = request.GET.get("date")
        category = request.GET.get("category")
        status_param = request.GET.get("status")

        # Safe date parsing
        if date_str:
            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(occurred_at__date=parsed_date)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if category:
            queryset = queryset.filter(category__icontains=category)
        if status_param:
            queryset = queryset.filter(status__icontains=status_param)

        # No results found
        if not queryset.exists():
            return Response(
                {"error": "No occurrences found for the given filters."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Generate PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="occurrences.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        y = height - 50
        p.setFont("Helvetica", 12)
        p.drawString(100, y, "Occurrences Report")
        y -= 30

        for occ in queryset:
            text = f"{occ.id} | {occ.title} | {occ.status} | {occ.category} | {occ.occurred_at.date()}"
            p.drawString(100, y, text)
            y -= 20
            if y < 50:
                p.showPage()
                y = height - 50

        p.save()
        return response

    
"""
class OccurrencesPDFView(APIView):

    #Returns a generated PDF. Admin-only by default.

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
    
class ReportListView(generics.ListCreateAPIView):
    queryset = Report.objects.all().order_by("-created_at")
    serializer_class = ReportSerializer
    filterset_class = ReportFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "summary", "location", "category"]
    ordering_fields = ["created_at", "location", "category"]

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

from io import BytesIO
from datetime import datetime

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Report

class ExportReportsPDF(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Start with all reports
        queryset = Report.objects.select_related("created_by").all()

        # Optional filtering by date (match only the day)
        date_str = request.query_params.get("date")
        if date_str:
            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(
                    created_at__year=parsed_date.year,
                    created_at__month=parsed_date.month,
                    created_at__day=parsed_date.day
                )
            except ValueError:
                return HttpResponse("Invalid date format. Use YYYY-MM-DD.", status=400)

        # Optional filtering by category (case-insensitive contains)
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__icontains=category)

        # Optional filtering by status (if you add a status field later)
        status_param = request.query_params.get("status")
        if status_param and hasattr(Report, "status"):
            queryset = queryset.filter(status__icontains=status_param)

        # Build PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("Reports Export", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Table headers
        data = [["ID", "Title", "Category", "Location", "Created At", "Created By"]]

        if queryset.exists():
            for report in queryset:
                data.append([
                    str(report.id) if report.id else "N/A",
                    report.title or "N/A",
                    report.category or "N/A",
                    report.location or "N/A",
                    report.created_at.strftime("%Y-%m-%d %H:%M") if report.created_at else "N/A",
                    report.created_by.username if report.created_by else "N/A",
                ])
        else:
            # If no reports match, still show headers and a row with a message
            data.append(["No reports found"] + [""] * 5)

        # Table styling
        table = Table(data, colWidths=[40, 120, 100, 100, 100, 80])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        # Build and return PDF
        doc.build(elements)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="reports.pdf"'
        return response
