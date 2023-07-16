import streamlit as st

def main():
  st.set_page_config(page_title='Crawl PDFs', page_icon=':books:')
  
  st.header('Crawl PDFs :books:')
  
  st.text_input("Ask a Question")
  
  with st.sidebar:
    st.subheader("Your PDFs")
    st.file_uploader("Upload PDFs", type=['pdf', 'txt'])
    st.button('Process PDFs')

if __name__ == '__main__':
  main()