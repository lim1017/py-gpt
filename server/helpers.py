
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

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

def get_vector_store(text_chunks):
  embeddings=OpenAIEmbeddings()
  vector_store=FAISS.from_texts(texts=text_chunks, embedding=embeddings)
  
  return vector_store
  
def get_conversation_chain(vector_store):
  llm = ChatOpenAI()
  memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
  
  conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vector_store.as_retriever(),
    memory = memory
  )
  return conversation_chain
