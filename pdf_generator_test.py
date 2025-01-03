from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

def create_campaign_pdf(output_filename="campaign_report.pdf"):
    # Field mapping
    field_mapping = {
        'responden_id': 'Unique ID',
        'unit': 'Unit TV',
        'brand': 'Brand',
        'program': 'Program',
        'nilai_paket': 'Revenue Bulk',
        'revenue_prorate': 'Revenue Prorate',
        'total_real_cost': 'Total Real Cost'
    }

    # Sample data (similar to our Campaign model)
    data = {
        "responden_id": "RESP123",
        "responden_name": "John Doe",
        "campaign_name": "Summer Digital Campaign 2024",
        "start_date": "2024-06-01",
        "end_date": "2024-08-31",
        "unit": "Digital Marketing",
        "brand": "TechBrand Pro",
        "program": "Brand Awareness Campaign",
        "jenis_paket": "Premium Package",
        "nilai_paket": 150000000.0,
        "revenue_prorate": "50,000,000 (Prorated for Q3 2024)",
        "total_real_cost": 35000000.0,
        "breakdown_cost": """
        1. Media Placement: Rp 15,000,000
        2. Content Creation: Rp 8,000,000
        3. Influencer Partnership: Rp 7,000,000
        4. Analytics Tools: Rp 5,000,000
        """,
        "breakdown_kpi": """
        1. Reach: 1,000,000 users
        2. Engagement Rate: 5%
        3. Click-through Rate: 2.5%
        4. Conversion Rate: 1.2%
        """,
        "activity_type": """
        - Social Media Marketing
        - Content Marketing
        - Influencer Marketing
        - Performance Marketing
        """,
        "list_benefit": """
        1. Brand Visibility Enhancement
        2. Lead Generation
        3. Market Share Increase
        4. Customer Engagement Boost
        """,
        "detail_brief": """
        This campaign aims to increase brand awareness and market penetration 
        through integrated digital marketing approaches. The strategy includes 
        multi-platform content distribution, influencer collaborations, and 
        targeted advertising campaigns.
        """,
        "timeline_benefit": """
        Month 1: Initial brand awareness push
        Month 2: Influencer campaign rollout
        Month 3: Performance optimization
        """,
        "product_knowledge": "Yes",
        "key_visual_design": "Yes"
    }

    # Create document
    doc = SimpleDocTemplate(
        output_filename,
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
    
    # Add new style for signature names
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

    # Function to create formatted paragraph
    def format_value(value):
        if isinstance(value, float):
            return f"Rp {value:,.2f}"
        return str(value)

    # Create table data
    table_data = []
    long_fields = ['breakdown_cost', 'breakdown_kpi', 'activity_type', 
                   'list_benefit', 'detail_brief', 'timeline_benefit', 'revenue_prorate']

    # Process regular fields
    for key, value in data.items():
        if key not in long_fields:
            display_name = field_mapping.get(key, key.replace('_', ' ').title())
            table_data.append([
                Paragraph(display_name, label_style),
                Paragraph(format_value(value), value_style)
            ])

    # Create first table
    table = Table(table_data, colWidths=[doc.width * 0.3, doc.width * 0.7])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#D3D3D3')),  # Lighter grey
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
    elements.append(Paragraph(format_value(data['revenue_prorate']), value_style))
    elements.append(Spacer(1, 5))

    for key in [f for f in long_fields if f != 'revenue_prorate']:
        elements.append(Paragraph(key.replace('_', ' ').title(), styles['Heading3']))
        elements.append(Spacer(1, 2))
        elements.append(Paragraph(data[key], value_style))
        elements.append(Spacer(1, 5))

    # Add signature section
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("Mengajukan,", value_style))

    # Create signature table with proper formatting
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
        ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Remove left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 0)  # Remove right padding
    ]))
    
    elements.append(sig_table1)

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Mengetahui,", value_style))

    sig_data2 = [["", "", "", ""],
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
        ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Remove left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 0)  # Remove right padding
    ]))
    elements.append(sig_table2)

    # Build PDF
    doc.build(elements)

if __name__ == "__main__":
    create_campaign_pdf()
    print("PDF has been generated successfully!") 