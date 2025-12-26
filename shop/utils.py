from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.http import HttpResponse
from io import BytesIO
from datetime import datetime


def generate_invoice(order):
    buffer = BytesIO()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order.id}.pdf'

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    # 🔥 Brand Title
    elements.append(Paragraph(
        "<b>ShopKart</b> <font size=10>- Tax Invoice</font>",
        ParagraphStyle(
            name="title",
            fontSize=18,
            spaceAfter=20
        )
    ))

    # 🧾 Invoice Info
    invoice_info = f"""
    <b>Invoice Date:</b> {datetime.now().strftime('%d %b %Y')}<br/>
    <b>Order ID:</b> #{order.id}<br/>
    <b>Customer:</b> {order.user.username}
    """
    elements.append(Paragraph(invoice_info, styles["Normal"]))
    elements.append(Spacer(1, 20))

    # 📍 Shipping Address
    address = order.address
    address_text = f"""
    <b>Shipping Address</b><br/>
    {address.full_name}<br/>
    {address.address_line}<br/>
    {address.city}, {address.state} - {address.pincode}<br/>
    Phone: {address.phone}
    """
    elements.append(Paragraph(address_text, styles["Normal"]))
    elements.append(Spacer(1, 25))

    # 🛍 Items Table
    table_data = [
        ["Item", "Qty", "Price", "Total"]
    ]

    grand_total = 0
    for item in order.items.all():
        total = item.price * item.quantity
        grand_total += total
        table_data.append([
            item.product.name,
            str(item.quantity),
            f"₹{item.price}",
            f"₹{total}"
        ])

    table = Table(table_data, colWidths=[220, 60, 90, 90])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),

        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # 💰 Total
    elements.append(Paragraph(
        f"<b>Total Amount: ₹{grand_total}</b>",
        ParagraphStyle(
            name="total",
            fontSize=12,
            alignment=2,  # right
            spaceBefore=10
        )
    ))

    elements.append(Spacer(1, 30))

    # ✅ Footer
    elements.append(Paragraph(
        "This is a computer generated invoice. No signature required.",
        ParagraphStyle(
            name="footer",
            fontSize=9,
            textColor=colors.grey,
            alignment=1
        )
    ))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
