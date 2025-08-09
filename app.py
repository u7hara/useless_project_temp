from dotenv import load_dotenv
load_dotenv() 

import os
from flask import Flask, render_template, request
# The correct import for the configure method is from google.generativeai
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API with the key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# The correct way to configure the API is by assigning the key directly
genai.configure(api_key=gemini_api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
def review():
    file = request.files.get('file')
    code_content = None

    if file and file.filename != '':
        code_content = file.read().decode('utf-8')
    else:
        code_content = request.form.get('code')

    if not code_content or code_content.strip() == '':
        return render_template('review.html', review="No code provided. Please upload a file or paste your code.")

    if not gemini_api_key:
        return render_template('review.html', review="Gemini API key not set. Please set the GEMINI_API_KEY environment variable.")

    prompt = (
        "You are a Shakespearean code reviewer. Read the following code and provide a poetic critique in Shakespearean English. "
        "Include an opening, three suggestions for improvement, and a closing line.\n\n"
        f"Code:\n{code_content}"
    )

    try:
        # Use a GenerativeModel for the Gemini API
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # The generate_content method replaces the chat.completions.create method
        response = model.generate_content(prompt)
        review_text = response.text.strip()
    except Exception as e:
        review_text = f"Error communicating with Gemini API: {e}"

    return render_template('review.html', review=review_text)

if __name__ == '__main__':
    app.run(debug=True)