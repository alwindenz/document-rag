import streamlit as st
import sys
sys.path.append("..")

from ui.ops.add_css import add_css

from genai.ingestion.ingestion import ingestion
from genai.llm.get_response import get_response


def main():
    add_css('ui/css/chatbot.css')

    st.header('Hello!')
    st.header('What can I help with?')    

    col1, col2 = st.columns((0.15, 0.85))  
    with col1:
        with st.popover("Upload"):
            st.write("Please upload your files here:")
            uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, key="file_upload", label_visibility="collapsed")
            
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

    with col2:
        if uploaded_files:
            if "processed_data" not in st.session_state:
                vectorstore = ingestion(uploaded_files)  # Calls the ingestion pipeline
                st.session_state.processed_data = {"vectorstore": vectorstore}
            else:
                vectorstore = st.session_state.processed_data["vectorstore"]
            
            question = st.chat_input("Ask questions here")
            _placeholder = st.empty()

            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if question:
                with st.chat_message("user"):
                    st.markdown(question)

                st.session_state.chat_history.append({"role": "user", "content": question})
                
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    
                    with st.spinner(""):
                        response = get_response(question, st.session_state.chat_history)
                        placeholder.markdown(response)

                st.session_state.chat_history.append({"role": "assistant", "content": response})

        else:
            question = st.chat_input("Ask questions here")
            _placeholder = st.empty()

            if question:
                with st.chat_message("user"):
                    st.markdown(question)

                with st.chat_message("assistant"):
                    st.markdown("Please upload a file first to ask questions.")

                st.session_state.chat_history.append({"role": "user", "content": question})
                st.session_state.chat_history.append({"role": "assistant", "content": "Please upload a file first to ask questions."})

if __name__ == "__main__":
    main()