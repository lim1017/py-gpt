import streamlit as st
from dotenv import load_dotenv


from helpers import get_pdf_text, get_text_chunks, get_vector_store, get_conversation_chain




def main():
  load_dotenv()
  st.set_page_config(page_title='Crawl PDFs', page_icon=':books:')
  
  if 'conversation' not in st.session_state:
    st.session_state.conversation = None
  
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
        
        #create vector store
        vector_store = get_vector_store(text_chunks)
        
        #create conversation
        st.session_state.conversation = get_conversation_chain(vector_store)
        
        st.success('Done!')
      
      
if __name__ == '__main__':
  main()