import streamlit as st
from dotenv import load_dotenv

from htmlTemplate import css, bot_template, user_template
from helpers import (
    get_pdf_text,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
)


def clear_text():
    print("inclear text")
    st.session_state["input"] = ""


def handle_user_input():
    response = st.session_state.conversation({"question": st.session_state["input"]})
    st.session_state.chat_history = response["chat_history"]

    st.session_state["input"] = ""

    for i, msg in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True
            )


def main():
    load_dotenv()
    st.set_page_config(page_title="Crawl Files", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Crawl Files :books:")

    st.text_input("Ask a Question", key="input", on_change=handle_user_input)

    with st.sidebar:
        st.subheader("Your Files")
        documents = st.file_uploader(
            "Upload Files (pdf/txt)", type=["pdf", "txt"], accept_multiple_files=True
        )

        if st.button("Process Files"):
            with st.spinner("Processing... This could take a while"):
                # get pdfs/text files
                raw_text = get_pdf_text(documents)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vector_store = get_vectorstore(text_chunks)

                # create conversation
                st.session_state.conversation = get_conversation_chain(vector_store)

                st.success("Done!")


if __name__ == "__main__":
    main()
