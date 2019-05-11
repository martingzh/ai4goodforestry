from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def insertStopSymbols (targetpdf):

    existing_pdf = PdfFileReader(open(targetpdf, "rb"))
    output = PdfFileWriter()

    for i in range(existing_pdf.numPages):
        packet = io.BytesIO()
        # Create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('Helvetica', 13)
        can.drawString(5, 730, "G1L33")
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))# index out of range
        output.addPage(page)    
    
    # Finally, write "output" to a real file
    outputStream = open("destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

insertStopSymbols ("exampleDocument.pdf")
