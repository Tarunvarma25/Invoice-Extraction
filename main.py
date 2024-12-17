from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from project.form_extractor import analyze_invoice

import pandas as pd
import os

app = FastAPI()

# Directory to save output Excel files
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload invoice files.
    """
    # Save uploaded file locally
    file_path = f"{OUTPUT_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Analyze file using Azure Form Recognizer
    invoice_data = analyze_invoice(file_path)

    # Convert data to Excel
    excel_path = file_path.replace(".pdf", ".xlsx").replace(".jpg", ".xlsx")
    df = pd.DataFrame([invoice_data])
    df.to_excel(excel_path, index=False)

    return {"message": "File processed successfully", "file_path": excel_path}

@app.get("/download/")
def download_file(file_name: str):
    """
    Endpoint to download processed Excel file.
    """
    file_path = f"{OUTPUT_DIR}/{file_name}"
    return FileResponse(file_path, filename=file_name)
