from fpdf import FPDF
from pathlib import Path


def create_pdf_document(data: dict,
                        questions: dict,
                        pdf_file_path: Path) -> None:

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.add_font('RobotoFlex-Regular', '', 'fonts/RobotoFlex-Regular.ttf', uni=True)
    pdf.set_font("RobotoFlex-Regular", size=14)

    pdf.cell(200, 10, txt="Накладная на груз", ln=1, align="C")

    for keys, text in data.items():

        if keys != "dimensions_cargo":

            line_text = str(questions[keys]) + " : " + str(text)
            pdf.cell(200, 10, txt=line_text, ln=1, align="L")

        else:
            line_text = \
                str(questions[keys]) + " : " + \
                " см  х ".join([str(x_y_z) for x_y_z in text]) + " см "
            pdf.cell(200, 10, txt=line_text, ln=1, align="L")

    pdf.output(str(pdf_file_path))
