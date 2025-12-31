"""
PDF report generation using ReportLab.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from io import BytesIO
from utils.logger import logger


def generate_analytics_report(
    kpi_data: Dict[str, Any],
    events_df: pd.DataFrame,
    service_perf_df: pd.DataFrame,
    output_path: str = None
) -> BytesIO:
    """
    Generate a PDF report for analytics data.
    
    Args:
        kpi_data: Dictionary with KPI metrics
        events_df: DataFrame with events data
        service_perf_df: DataFrame with service performance data
        output_path: Optional file path to save PDF. If None, returns BytesIO buffer.
    
    Returns:
        BytesIO buffer with PDF content
    """
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(output_path or buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Validate inputs
        if not kpi_data:
            kpi_data = {
                "total_events": 0,
                "completion_rate": 0.0,
                "error_rate": 0.0,
                "avg_journey_time": 0.0
            }
        
        if events_df is None or events_df.empty:
            events_df = pd.DataFrame()
        
        if service_perf_df is None or service_perf_df.empty:
            service_perf_df = pd.DataFrame()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12
        )

        # Title
        story.append(Paragraph("Digital Service Analytics Report", title_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))

        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        summary_text = f"""
        This report provides a comprehensive analysis of digital service performance,
        including key performance indicators, event analytics, and service-level metrics.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        # KPI Section
        story.append(Paragraph("Key Performance Indicators", heading_style))
        kpi_table_data = [
            ['Metric', 'Value'],
            ['Total Events', f"{kpi_data.get('total_events', 0):,}"],
            ['Completion Rate', f"{kpi_data.get('completion_rate', 0):.2f}%"],
            ['Error Rate', f"{kpi_data.get('error_rate', 0):.2f}%"],
            ['Average Journey Time', f"{kpi_data.get('avg_journey_time', 0):.2f}s"]
        ]

        kpi_table = Table(kpi_table_data, colWidths=[3 * inch, 2 * inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 0.3 * inch))

        # Service Performance
        if not service_perf_df.empty:
            story.append(Paragraph("Service Performance", heading_style))
            service_data = [['Service', 'Completion Rate (%)', 'Total Events']]
            for _, row in service_perf_df.iterrows():
                service_data.append([
                    str(row.get('service', 'N/A')),
                    f"{row.get('completion_rate', 0):.2f}",
                    str(row.get('total_events', 0))
                ])

            service_table = Table(service_data, colWidths=[2.5 * inch, 2 * inch, 1.5 * inch])
            service_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(service_table)
            story.append(Spacer(1, 0.3 * inch))

        # Event Summary
        if not events_df.empty:
            story.append(Paragraph("Event Summary", heading_style))
            story.append(Paragraph(f"Total events analyzed: {len(events_df)}", styles['Normal']))
            
            # Status distribution
            if 'status' in events_df.columns:
                status_counts = events_df['status'].value_counts()
                status_data = [['Status', 'Count', 'Percentage']]
                for status, count in status_counts.items():
                    percentage = (count / len(events_df)) * 100
                    status_data.append([str(status), str(count), f"{percentage:.2f}%"])

                status_table = Table(status_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
                status_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(status_table)

        # Insights Section
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("Key Insights", heading_style))
        
        insights = []
        if kpi_data.get('completion_rate', 0) >= 95:
            insights.append("✓ Excellent completion rate indicates stable service performance.")
        elif kpi_data.get('completion_rate', 0) >= 90:
            insights.append("⚠ Completion rate is good but could be improved.")
        else:
            insights.append("⚠ Low completion rate requires immediate attention and investigation.")

        if kpi_data.get('error_rate', 0) < 5:
            insights.append("✓ Error rate is within acceptable limits.")
        else:
            insights.append("⚠ High error rate detected - review error patterns and root causes.")

        for insight in insights:
            story.append(Paragraph(f"• {insight}", styles['Normal']))

        # Build PDF
        doc.build(story)
        if output_path:
            logger.info(f"PDF report saved to {output_path}")
        else:
            buffer.seek(0)
            return buffer
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise


def generate_uat_report(
    test_cases_df: pd.DataFrame,
    defects_df: pd.DataFrame,
    output_path: str = None
) -> BytesIO:
    """
    Generate a PDF report for UAT and testing data.
    
    Args:
        test_cases_df: DataFrame with test cases
        defects_df: DataFrame with defects
        output_path: Optional file path to save PDF. If None, returns BytesIO buffer.
    
    Returns:
        BytesIO buffer with PDF content
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(output_path or buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12
    )

    # Title
    story.append(Paragraph("UAT & Regression Testing Report", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))

    # Test Cases Section
    story.append(Paragraph("Test Cases Summary", heading_style))
    if not test_cases_df.empty:
        story.append(Paragraph(f"Total Test Cases: {len(test_cases_df)}", styles['Normal']))
        
        if 'status' in test_cases_df.columns:
            status_counts = test_cases_df['status'].value_counts()
            tc_data = [['Status', 'Count']]
            for status, count in status_counts.items():
                tc_data.append([str(status), str(count)])

            tc_table = Table(tc_data, colWidths=[3 * inch, 2 * inch])
            tc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(tc_table)
    else:
        story.append(Paragraph("No test cases data available.", styles['Normal']))

    story.append(Spacer(1, 0.3 * inch))

    # Defects Section
    story.append(Paragraph("Defects Summary", heading_style))
    if not defects_df.empty:
        story.append(Paragraph(f"Total Defects: {len(defects_df)}", styles['Normal']))
        
        # By Severity
        if 'severity' in defects_df.columns:
            severity_counts = defects_df['severity'].value_counts()
            sev_data = [['Severity', 'Count']]
            for severity, count in severity_counts.items():
                sev_data.append([str(severity), str(count)])

            sev_table = Table(sev_data, colWidths=[3 * inch, 2 * inch])
            sev_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(sev_table)

        story.append(Spacer(1, 0.2 * inch))

        # By Status
        if 'status' in defects_df.columns:
            status_counts = defects_df['status'].value_counts()
            stat_data = [['Status', 'Count']]
            for status, count in status_counts.items():
                stat_data.append([str(status), str(count)])

            stat_table = Table(stat_data, colWidths=[3 * inch, 2 * inch])
            stat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(stat_table)
    else:
        story.append(Paragraph("No defects data available.", styles['Normal']))

    # Build PDF
    try:
        doc.build(story)
        if output_path:
            logger.info(f"UAT PDF report saved to {output_path}")
        else:
            buffer.seek(0)
            return buffer
    except Exception as e:
        logger.error(f"Error generating UAT PDF report: {e}")
        raise



