import traceback
import streamlit as st
from genppt import GenPPT
from utils import *

max_pages=20
max_chars=max_pages*2000
def get_upload_file(uploaded_file,page_range):
        import fitz  # PyMuPDF
        import pymupdf4llm 

        if uploaded_file  is not None:
            # Open the uploaded file with PyMuPDF
            
            document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            pages=parse_page_ranges(page_range, document.page_count, max_pages)
            markdown_content=pymupdf4llm.to_markdown(document, pages=pages)

            
        return markdown_content

def create_ui():
    st.set_page_config(page_title="GenSlides", page_icon="📊", layout="wide")
    
    st.title("GenSlides")
    st.subheader("Generate PowerPoint slides from your text or PDF")

    col1, col2 = st.columns(2)

    with col1:
        agenda = st.text_input("Enter the main points or topics you want to cover in your presentation.")
        
        content_type = st.radio("Choose content type:", ("Text", "PDF"))
        
        if content_type == "Text":
            content = st.text_area("Enter your text:", height=400)
        else:
            uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
            if uploaded_file:
                st.success("PDF uploaded successfully!")

    with col2:
        st.subheader("Advanced Options")
        #max_pages = st.number_input("Maximum number of pages:", min_value=1, max_value=200, value=100)
        page_range = st.text_input(f"Page range (e.g. 2,3,5-8,9 or leave empty for all) (Max of {max_pages} pages):", "")

    if st.button("Generate Slides", type="primary"):
        try:
            with st.spinner("Generating slides..."):
                if content_type == "Text" and content:
                    pp = GenPPT(text=content[:max_chars], agenda=agenda, pages=page_range)
                    
                elif content_type == "PDF" and uploaded_file:
                    content=get_upload_file(uploaded_file,page_range)
                    pp = GenPPT(text=content, agenda=agenda, pages=page_range)
                else:
                    st.error("Please provide either text content or upload a PDF file.")
                    return

                filename = pp.run()
                st.success(f"Slides generated successfully! File: {filename}")
                
                # Add a download button for the generated file
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Download Slides",
                        data=file,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
        except Exception as e:
            st.error("Error in generating slides.")
            st.error(traceback.format_exc())

if __name__ == "__main__":
    create_ui()