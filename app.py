import streamlit as st
from utils import read_file, chunk_text
from ai_handler import process_all_text

st.set_page_config(page_title="AI Text Humanizer & Paraphraser", layout="wide")

def main():
    st.title("🤖 AI Text Humanizer & Paraphraser")
    st.markdown("Transform your text or documents with AI. Paraphrase for clarity or humanize for a natural touch.")

    # Sidebar for Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        # api_key = st.text_input("Enter Google Gemini API Key", type="password", help="Get your key from https://aistudio.google.com/")
        api_key = "API KEY"
        
        mode = st.radio("Select Mode", ["Paraphrase", "Humanize"])
        
        tone = st.selectbox("Select Tone", ["Professional", "Casual", "Academic", "Creative", "Simple"])
        
        st.markdown("---")
        st.markdown("### About")
        st.info("This app uses Google's Gemini model to process your text. Upload a file or paste text to get started.")

    # Main Content Area
    tab1, tab2 = st.tabs(["📝 Input Text", "📂 Upload File"])

    input_text = ""

    with tab1:
        text_input = st.text_area("Enter your text here:", height=300)
        if text_input:
            input_text = text_input

    with tab2:
        uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
        if uploaded_file:
            with st.spinner("Reading file..."):
                file_text = read_file(uploaded_file)
                if file_text.startswith("Error"):
                    st.error(file_text)
                else:
                    st.success("File read successfully!")
                    with st.expander("View extracted text"):
                        st.text(file_text[:1000] + "..." if len(file_text) > 1000 else file_text)
                    input_text = file_text

    # Process Button
    if st.button("🚀 Process Text", type="primary"):
        # if not api_key:
        #     st.warning("Please enter your Google Gemini API Key in the sidebar.")
        if not input_text:
            st.warning("Please enter some text or upload a file.")
        else:
            with st.spinner(f"{mode}ing text... This may take a while for long documents."):
                # Chunk text if it's long
                chunks = chunk_text(input_text)
                st.write(f"Processing {len(chunks)} chunk(s)...")
                
                progress_bar = st.progress(0)
                result = process_all_text(chunks, mode, api_key, tone, progress_bar)
                progress_bar.empty()

                if result.startswith("Error"):
                    st.error(result)
                else:
                    st.subheader("✨ Result")
                    st.text_area("Output", value=result, height=400)
                    st.download_button("Download Result", result, file_name=f"{mode.lower()}_output.txt")

if __name__ == "__main__":
    main()

