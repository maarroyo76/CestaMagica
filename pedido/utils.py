from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image
from tempfile import NamedTemporaryFile
import os

def generar_pdf_pedido(pedido_data, items_data, logo_path=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50

    if logo_path:
        try:
            with Image.open(logo_path) as im:
                if im.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', im.size, (255, 255, 255))
                    background.paste(im, mask=im.split()[3])
                    tmp = NamedTemporaryFile(delete=False, suffix=".jpg")
                    tmp.close()
                    background.save(tmp.name, format='JPEG')

                    logo_width = 150
                    logo_height = 100
                    x_position = width - logo_width - 40
                    y_position = y - logo_height + 10

                    pdf.drawImage(tmp.name, x_position, y_position, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')

                    os.unlink(tmp.name)
                else:
                    logo_width = 150
                    logo_height = 50
                    x_position = width - logo_width - 40
                    y_position = y - logo_height + 10
                    pdf.drawImage(logo_path, x_position, y_position, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')

        except Exception as e:
            pass

    # Datos del pedido
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, f"Comprobante de Pedido: {pedido_data['codigo_pedido']}")
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, y, f"Fecha: {pedido_data['fecha']}")
    y -= 20
    pdf.drawString(40, y, f"Estado: {pedido_data['estado']}")
    y -= 20
    pdf.drawString(40, y, f"Método de Retiro: {pedido_data['metodo_retiro']}")
    y -= 20
    pdf.drawString(40, y, f"Método de Pago: {pedido_data['metodo_pago']}")
    y -= 30

    # Tabla de productos
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(40, y, "Producto")
    pdf.drawString(220, y, "Cantidad")
    pdf.drawString(300, y, "Precio Unitario")
    pdf.drawString(430, y, "Subtotal")
    y -= 15
    pdf.line(40, y, 550, y)
    y -= 15

    pdf.setFont("Helvetica", 10)
    for item in items_data:
        if y < 80:
            pdf.showPage()
            y = height - 50
        pdf.drawString(40, y, item["producto"])
        pdf.drawString(230, y, str(item["cantidad"]))
        pdf.drawString(310, y, f"$ {item['precio_unitario']}")
        pdf.drawString(440, y, f"$ {item['subtotal']}")
        y -= 18

    y -= 15
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, f"Total: $ {pedido_data['total']}")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
