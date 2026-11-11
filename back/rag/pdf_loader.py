import fitz
import pandas as pd
import os
import re


def clean_text(text):

    text = text.replace("´", "")
    text = text.replace("˜", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"

        doc.close()
        return clean_text(text)

    elif extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return clean_text(
                file.read()
            )

    elif extension == ".csv":

        df = pd.read_csv(file_path)

        return clean_text(
            df.to_string(index=False)
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
            text += df.to_string(index=False)
            text += "\n"
        return clean_text(text)

    else:

        raise ValueError(
            f"Formato no soportado: {extension}"
        )