import fitz
import pandas as pd
import os


def clean_text(text):

    # Elimina caracteres problemáticos de PDFs
    text = text.replace("´", "")
    text = text.replace("˜", "")

    return text


def extract_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        text = ""

        doc = fitz.open(file_path)

        for page in doc:

            page_text = page.get_text()

            if not page_text:
                continue

            page_lower = page_text.lower()

            # Ignorar páginas de índice
            if (
                "índice" in page_lower
                or "indice" in page_lower
            ):
                continue

            # Ignorar tablas de contenido
            if page_text.count("...") > 10:
                continue

            text += page_text + "\n"

        doc.close()

        text = clean_text(text)

        return text

    elif extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    elif extension == ".csv":

        df = pd.read_csv(file_path)

        return df.to_string(
            index=False
        )

    elif extension == ".xlsx":

        excel_file = pd.ExcelFile(
            file_path,
            engine="openpyxl"
        )

        text = ""

        for sheet_name in excel_file.sheet_names:

            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                engine="openpyxl"
            )

            text += f"\nHoja: {sheet_name}\n"
            text += df.to_string(
                index=False
            )
            text += "\n"

        return text

    else:

        raise ValueError(
            f"Formato no soportado: {extension}"
        )
