import PyPDF2
import re
from datetime import datetime
from proslip.models import Profile, Payslip


def process_payslip(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader=PyPDF2.PdfReader(file)

        for page_num in range(len(pdf_reader.pages)):
            page=pdf_reader.pages[page_num]
            
            text_content=page.extract_text()

            ippis_match=re.search(r'IPPIS Number: (\d+)', text_content)
            ippis_number=ippis_match.group(1) if ippis_match else None

            
            if not ippis_number:
                print(f"skipping page {page_num + 1}: IPPIS number not found")
                continue

            try:
                profile=Profile.objects.get(ippis_no=ippis_number)
            except Profile.DoesNotExist:
                print(f"No Profile found for IPPIS number {ippis_number}")
                continue

            Payslip.objects.create(profile=profile)