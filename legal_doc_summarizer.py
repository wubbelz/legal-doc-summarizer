import streamlit as st
import openai
import PyPDF2
import docx
import os

# Voer hier handmatig je OpenAI API-key in
openai.api_key = "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"

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def summarize_text(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Je bent een AI die juridische documenten samenvat in eenvoudige taal."},
            {"role": "user", "content": f"Vat deze tekst samen in max 5 zinnen en leg het uit in eenvoudige taal: {text}"}
        ]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("Juridische Document Samenvatter")
st.write("Upload een juridisch document (PDF of Word) en krijg een samenvatting in simpele taal.")

uploaded_file = st.file_uploader("Upload een PDF of DOCX-bestand", type=["pdf", "docx"])

if uploaded_file is not None:
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    if file_extension == ".pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif file_extension == ".docx":
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Bestandstype niet ondersteund. Upload een PDF of DOCX.")
        text = None
    
    if text:
        st.write("**Originele tekst (ingekort weergegeven):**")
        st.text_area("", text[:1000] + "...", height=200)
        
        st.write("**Samenvatting in eenvoudige taal:**")
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Je bent een AI die juridische documenten samenvat in eenvoudige taal."},
                    {"role": "user", "content": f"Vat deze tekst samen in max 5 zinnen en leg het uit in eenvoudige taal: {text}"}
                ]
            )
            summary = response.choices[0].message.content
            st.success(summary)

            # Downloadknop voor de samenvatting
            st.download_button(
                label="Download Samenvatting",
                data=summary,
                file_name="samenvatting.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Er is een fout opgetreden: {e}")