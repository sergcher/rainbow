from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas


def generate_pdf(data):
    # create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 750, "Hello world.")

    # close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="apartment_receipt.pdf"'
    response.write(pdf)
    return response
