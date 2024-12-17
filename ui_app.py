import streamlit as st
import requests
import os
import pandas as pd

# API endpoints
UPLOAD_API = "http://127.0.0.1:8000/upload/"
DOWNLOAD_API = "http://127.0.0.1:8000/download/"

# Title and Styling
st.set_page_config(page_title="Invoice Data Extractor", layout="wide")
st.title("📄 Invoice Data Extractor")
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("📤 Upload Invoice (PDF/Image)", type=["pdf", "jpg", "jpeg", "png"])

# Process file upload
if uploaded_file:
    st.info("🔄 Processing file...")

    # Save file locally
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.read())

    # Send file to FastAPI backend
    with open(uploaded_file.name, "rb") as f:
        response = requests.post(UPLOAD_API, files={"file": f})

    if response.status_code == 200:
        st.success("✅ File processed successfully!")

        # Extract Excel file path
        response_json = response.json()
        excel_file_name = os.path.basename(response_json["file_path"])

        # Display extracted data in a structured format
        st.subheader("📊 Extracted Invoice Data")
        excel_path = f"output/{excel_file_name}"

        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path)

            # Corporate Style Display
            with st.container():
                for col in df.columns:
                    value = df[col][0] if not pd.isnull(df[col][0]) else "N/A"
                    st.markdown(
                        f"""
                        <div style='background-color: #f9f9f9; padding: 10px; margin: 5px; border-radius: 8px;'>
                            <span style='font-weight: bold; color: #4b4b4b;'>{col}:</span>
                            <span style='color: #0078D7;'>{value}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # Download button
            st.markdown("---")
            st.download_button(
                label="📥 Download Excel File",
                data=requests.get(f"{DOWNLOAD_API}?file_name={excel_file_name}").content,
                file_name=excel_file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Click to download the extracted data as an Excel file."
            )
        else:
            st.warning("⚠️ Failed to fetch extracted data.")
    else:
        st.error("❌ Error processing file.")
