import PyPDF2
import re
from datetime import datetime
from proslip.models import Profile, Payslip


def process_payslip(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader=PyPDF2.PdfFileReader(file)

        for page_num in range(pdf_reader.numPages):
            page=pdf_reader.getPage(page_num)
            
            text_content=page.extract_text()

            ippis_match=re.search(r'IPPIS Number: (\d+)', text_content)
            ippis_number=ippis_match.group(1) if ippis_match else None

            date_match= re.search(r'Date: (\w+-\d+)', text_content) 
            date_str=date_match.group(1) if date_match else None

            if not ippis_number or not date_str:
                print(f"skipping page {page_num + 1}: IPPIS number or date not found")
                continue

            try:
                profile=Profile.objects.get(ippis_no=ippis_number)
            except Profile.DoesNotExist:
                print(f"No Profile found for IPPIS number {ippis_number}")
                continue

            month_year=datetime.strptime(date_str, "%b-%Y")

            Payslip.objects.create(profile=profile,month=month_year)