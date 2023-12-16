import PyPDF2
import re
from datetime import datetime
from proslip.models import Profile, Payslip
from django.core.files.base import ContentFile


def process_payslip(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader=PyPDF2.PdfReader(file)

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
                payslip.file.save(f'{profile.ippis_no}_payslip_page_{page_num + 1}.pdf',ContentFile(page.extract_text()))
                payslip.save()
                print(f"payslip created for: {profile.user.get_full_name} (Page {page_num+1})")
            else:
                print(f"payslip exist already for: {profile.user.get_full_name} (Page {page_num+1})")
