from PyPDF2 import PdfReader, PdfWriter

Path="Payslip.pdf"
file_ext=Path.replace('.pdf','')
pdf=PdfReader(Path)
pdfpages=[0,2,4,8]
PdfWriter=PdfWriter()
for page_num in pdfpages:
    PdfWriter.add_page(pdf.pages[page_num]) 

with open('{0}_slip.pdf'.format(file_ext),'wb')as a:
    PdfWriter.write(a)
    a.close()
