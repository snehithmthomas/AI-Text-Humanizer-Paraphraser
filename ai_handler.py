import google.generativeai as genai
import time

def process_text_chunk(text_chunk, mode, api_key, tone="Professional"):
    """
    Processes a single chunk of text using Google Gemini API.
    """
    if not api_key:
        return "Error: API Key is missing."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        if mode == "Paraphrase":
            prompt = f"""
            Please paraphrase the following text. 
            Tone: {tone}.
            Goal: Improve clarity and flow while retaining the original meaning.
            
            Text:
            {text_chunk}
            """
        elif mode == "Humanize":
            prompt = f"""
            Please rewrite the following text to make it sound more human-written.
            Tone: {tone}.
            Goal: Make it sound natural, conversational, and less robotic/AI-generated. Use varied sentence structure and vocabulary.
            
            Text:
            {text_chunk}
            """
        else:
            return "Error: Invalid mode selected."

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error processing text: {e}"

def process_all_text(chunks, mode, api_key, tone="Professional", progress_bar=None):
    """
    Processes all text chunks and combines the results.
    """
    full_response = ""
    total_chunks = len(chunks)
    
    for i, chunk in enumerate(chunks):
        response = process_text_chunk(chunk, mode, api_key, tone)
        if response.startswith("Error"):
            return response # Stop on error
        full_response += response + "\n\n"
        
        if progress_bar:
            progress_bar.progress((i + 1) / total_chunks)
        
        # Rate limiting handling (simple sleep to avoid hitting free tier limits too hard)
        time.sleep(1) 

    return full_response
