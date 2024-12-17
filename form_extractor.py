from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Azure Form Recognizer Configuration
AZURE_FORM_RECOGNIZER_ENDPOINT = "YOUR_ENDPOINT"
AZURE_FORM_RECOGNIZER_KEY = "YOUR_KEY"


def analyze_invoice(file_path: str):
    """
    Analyze the invoice file using Azure Form Recognizer.
    """
    client = DocumentAnalysisClient(AZURE_FORM_RECOGNIZER_ENDPOINT, AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY))

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-invoice", f)
    result = poller.result()

    # Extract relevant fields
    invoice_data = {}
    for document in result.documents:
        for name, field in document.fields.items():
            invoice_data[name] = field.value if field.value else "N/A"

    return invoice_data
