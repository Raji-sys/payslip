from PyPDF2 import PdfReader, PdfWriter
import re
from proslip.models import Profile, Payslip
from django.core.files.base import ContentFile


def process_payslip(pdf_path):
    pdf = PdfReader(pdf_path)

    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text_content = page.extract_text()

        ippis_match = re.search(r'(\d{6})', text_content)
        ippis_number = ippis_match.group(1) if ippis_match else None

        if not ippis_number:
            print(f"Skipping page {page_num + 1}: IPPIS number not found")
            continue

        try:
            profile = Profile.objects.get(ippis_no=ippis_number)
        except Profile.DoesNotExist:
            print(f"No Profile found for IPPIS number {ippis_number}")
            continue

        payslip_exists = Payslip.objects.filter(profile=profile).exists()

        if not payslip_exists:
            payslip = Payslip(profile=profile)

            # Create a new PDF using PyPDF2 PdfWriter
            Pdf_writer=PdfWriter()
            Pdf_writer.add_page(page)

            # Save the new PDF to Payslip model
            payslip_file_path = f'media/payslips/{profile.ippis_no}_payslip_page_{page_num + 1}.pdf'
            with open(payslip_file_path, 'wb') as payslip_file:
                Pdf_writer.write(payslip_file)
                payslip.file.save(payslip_file_path, ContentFile(open(payslip_file_path, 'rb').read()))
                payslip_file.close()

            print(f"Payslip created for: {profile.user.get_full_name} (Page {page_num + 1})")
        else:
            payslip=Payslip.objects.get(profile=profile)
            Pdf_writer=PdfWriter()
            Pdf_writer.add_page(page)

            payslip_file_path = f'media/payslips/{profile.ippis_no}_payslip_page_{page_num + 1}.pdf'
            with open(payslip_file_path, 'wb') as payslip_file:
                Pdf_writer.write(payslip_file)
                payslip.file.save(payslip_file_path, ContentFile(open(payslip_file_path, 'rb').read()))
                payslip_file.close()
            print(f"Payslip updated for: {profile.user.get_full_name} (Page {page_num + 1})")
 