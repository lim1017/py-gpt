import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter


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

def get_text_chunks(raw_text):
  text_splitter = CharacterTextSplitter(
    separator="/n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
  )
  
  chunks=text_splitter.split_text(raw_text)
  return chunks

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
        #get the text chunks
        text_chunks = get_text_chunks(raw_text)
        st.write(text_chunks)
        #create vector store
        
        st.success('Done!')
      
      
if __name__ == '__main__':
  main()