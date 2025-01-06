from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os
from threading import Lock

# Create a lock for thread safety
pdf_lock = Lock()

def create_campaign_pdf(data, output_path):
    """
    Generate a PDF report for campaign data in a thread-safe manner.
    
    Args:
        data (dict): Campaign data dictionary containing all required fields
        output_path (str): Full path where the PDF should be saved
        
    Returns:
        str: Path to the generated PDF file
        
    Raises:
        Exception: If PDF generation fails
    """
    
    # Field mapping for the report
    field_mapping = {
        'responden_id': 'Unique ID',
        'unit': 'Unit TV',
        'brand': 'Brand',
        'program': 'Program',
        'nilai_paket': 'Revenue Bulk',
        'revenue_prorate': 'Revenue Prorate',
        'total_real_cost': 'Total Real Cost'
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with pdf_lock:  # Thread safety for PDF generation
            # Create document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Styles
            styles = getSampleStyleSheet()
            main_title_style = ParagraphStyle(
                'MainTitle',
                parent=styles['Heading1'],
                fontSize=16,
                alignment=1,
                spaceAfter=10
            )
            
            subtitle_style = ParagraphStyle(
                'SubTitle',
                parent=styles['Heading2'],
                fontSize=14,
                alignment=1,
                spaceAfter=10
            )
            
            label_style = ParagraphStyle(
                'Label',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=10,
                textColor=colors.black
            )
            
            value_style = ParagraphStyle(
                'Value',
                parent=styles['Normal'],
                fontSize=10
            )
            
            signature_style = ParagraphStyle(
                'Signature',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=8,
                alignment=1,
                textColor=colors.black,
                underline=True,
                bold=True
            )

            # Content elements
            elements = []
            
            # Main Title
            elements.append(Paragraph("FORM PROJECT CAMPAIGN", main_title_style))
            elements.append(Spacer(1, 10))
            
            # Subtitle
            elements.append(Paragraph("DETAIL OF CAMPAIGN", subtitle_style))
            elements.append(Spacer(1, 10))

            # Function to format values
            def format_value(value):
                if isinstance(value, (int, float)):
                    return f"Rp {value:,.2f}"
                return str(value)

            # Create table data
            table_data = []
            long_fields = ['breakdown_cost', 'breakdown_kpi', 'activity_type', 
                        'list_benefit', 'detail_brief', 'timeline_benefit', 'revenue_prorate']
            short_fields = [
                'responden_id',
                'responden_name',
                'campaign_name',
                'start_date',
                'end_date', 
                'unit', 
                'brand', 
                'program', 
                'jenis_paket', 
                'nilai_paket', 
                'total_real_cost',
                'product_knowledge',
                'key_visual_design',
            ]

            # Process regular fields
            for field_name in short_fields:
                display_name = field_mapping.get(field_name, field_name.replace('_', ' ').title())
                field_value = data.get(field_name, '-')
                table_data.append([
                    Paragraph(display_name, label_style),
                    Paragraph(format_value(field_value), value_style)
                ])

            # Create first table
            table = Table(table_data, colWidths=[doc.width * 0.3, doc.width * 0.7])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#D3D3D3')),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 20))

            # Detailed Information section
            elements.append(Paragraph("Detailed Information", subtitle_style))
            elements.append(Spacer(1, 5))

            # Add revenue_prorate to detailed information first
            elements.append(Paragraph("Revenue Prorate", styles['Heading3']))
            elements.append(Spacer(1, 2))
            elements.append(Paragraph(format_value(data.get('revenue_prorate', '')), value_style))
            elements.append(Spacer(1, 5))

            # Add other long fields
            for key in [f for f in long_fields if f != 'revenue_prorate']:
                elements.append(Paragraph(key.replace('_', ' ').title(), styles['Heading3']))
                elements.append(Spacer(1, 2))
                elements.append(Paragraph(str(data.get(key, '')), value_style))
                elements.append(Spacer(1, 5))

            # Add signature section
            elements.append(Spacer(1, 15))
            elements.append(Paragraph("Mengajukan,", value_style))
            elements.append(Spacer(1, 80))

            # Create signature tables
            sig_data1 = [
                ["", "", "", ""],
                ["", "", "", ""],
                ["", "", "", ""],
                [
                    Paragraph("<u>AVIAN REVENTIARI</u>", signature_style),
                    Paragraph("<u>NOER REZA</u>", signature_style),
                    Paragraph("<u>RIO</u>", signature_style),
                    Paragraph("<u>HANIF MUSLIH</u>", signature_style)
                ],
                ["Digital Commercial Officer", "Digital Commercial Section\nHead", "Digital Assets Officer", "Digital Operations Section\nHead"],
                ["", "", "", ""],
            ]

            sig_table1 = Table(sig_data1, colWidths=[doc.width/4.0]*4)
            sig_table1.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0)
            ]))
            
            elements.append(sig_table1)
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("Mengetahui,", value_style))
            elements.append(Spacer(1, 80))

            sig_data2 = [
                ["", "", "", ""],
                ["", "", "", ""],
                ["", "", "", ""],
                [
                    Paragraph("<u>ADE PRAMUDHY</u>", signature_style),
                    "", "",
                    Paragraph("<u>KAREENE SETIOBUDI</u>", signature_style)
                ],
                ["Head Of Digital Strategiest", "", "", "General Manager Of Digital\nBroadcast Marketing Dept\n3FTA & RCTI+"]
            ]

            sig_table2 = Table(sig_data2, colWidths=[doc.width/4.0]*4)
            sig_table2.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0)
            ]))
            elements.append(sig_table2)

            # Build PDF
            doc.build(elements)
            
            return output_path

    except Exception as e:
        raise Exception(f"Failed to generate PDF: {str(e)}") 