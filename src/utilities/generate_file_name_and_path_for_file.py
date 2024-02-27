from pathlib import Path
from datetime import datetime


def generate_file_name_and_path_for_file(user_id: int) -> Path:

    pdf_file_path = \
        Path(__file__).resolve().parents[1] / \
        Path('archive_documents') / \
        Path(f"{user_id}_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.pdf")

    return pdf_file_path
