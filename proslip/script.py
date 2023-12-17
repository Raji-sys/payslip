from PyPDF2 import PdfReader, PdfFileWriter
import re
from reportlab.pdfgen import canvas
import io
from datetime import datetime
from proslip.models import Profile, Payslip
from django.core.files.base import ContentFile


def process_payslip(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader=PdfReader(file)

        for page_num in range(len(pdf_reader.pages)):
            page=pdf_reader.pages[page_num]
            
            text_content=page.extract_text()

            ippis_match=re.search(r'(\d{6})', text_content)
            ippis_number=ippis_match.group(1) if ippis_match else None

            
            if not ippis_number:
                print(f"skipping page {page_num + 1}: IPPIS number not found")
                continue

            try:
                profile=Profile.objects.get(ippis_no=ippis_number)
            except Profile.DoesNotExist:
                print(f"No Profile found for IPPIS number {ippis_number}")
                continue
            
            payslip_exists=Payslip.objects.filter(profile=profile).exists()

            if not payslip_exists:
                payslip=Payslip(profile=profile)

                buffer=io.BytesIO()
                p=canvas.Canvas(buffer)
                p.drawString(100,100,text_content)
                p.save()
                payslip.file.save(f'{profile.ippis_no}_payslip_page_{page_num + 1}.pdf',ContentFile(buffer.getvalue()))
                payslip.save()
                print(f"payslip created for: {profile.user.get_full_name} (Page {page_num+1})")
            else:
                print(f"payslip exist already for: {profile.user.get_full_name} (Page {page_num+1})")


Path="Payslip.pdf"
file_ext=Path.replace('.pdf','')
pdf=PdfReader(Path)
pdfpages=[0,2,4,8]
PdfFileWriter=PdfFileWriter()
for page_num in pdfpages:
    PdfFileWriter.addPage(pdf.getPage(page_num)) 

with open('{0}_slip.pdf'.format(file_ext),'wb')as a:
    PdfFileWriter.write(a)
    a.close()