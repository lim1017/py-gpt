import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

def get_pdf_text(documents):
  text=''
  for doc in documents:
    if doc.type=='application/pdf':
      pdf_reader = PdfReader(doc)
      for page in pdf_reader.pages:
        text += page.extract_text()
    else:
      text += doc.getvalue()
  return text



def main():
  load_dotenv()
  st.set_page_config(page_title='Crawl PDFs', page_icon=':books:')
  
  st.header('Crawl PDFs :books:')
  
  st.text_input("Ask a Question")
  
  with st.sidebar:
    st.subheader("Your PDFs")
    documents=st.file_uploader("Upload PDFs", type=['pdf', 'txt'], accept_multiple_files=True)
    
    if st.button('Process PDFs'):
      with st.spinner('Processing your PDFs...'):
        #get pdfs/text files
        raw_text = get_pdf_text(documents)
        st.write(raw_text)
        #get the text chunks
        
        #create vector store
        
        st.success('Done!')
      
      
if __name__ == '__main__':
  main()