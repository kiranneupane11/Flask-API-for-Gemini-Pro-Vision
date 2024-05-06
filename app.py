import os
from flask import Flask, request, Response, g, render_template, jsonify
import marko
import google.generativeai as genai

import os
credential_path = u"C:\\Users\\Dell\\Desktop\\Credential File\\cred_file_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)
app.debug = False

config = {
  'temperature': 0,
  'top_k': 20,
  'top_p': 0.9,
  'max_output_tokens': 500
}

model = genai.GenerativeModel(model_name="gemini-pro-vision",generation_config=config)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat',methods=['POST'])
def chat():
    # Check if a file has been uploaded
    if 'user_image' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['user_image']

    # Check if the file has a non-empty filename
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    # Read the file contents and extract the MIME type
    image_data = file.read()
    image_mime_type = file.content_type

    # Get the user's prompt from the request
    user_prompt = request.form.get('user_prompt')

    # Create the prompt parts for the AI model
    prompt_parts = [
        f"User's prompt: {user_prompt}\n\n",
        "User's image:\n\n",    
        {
            "mime_type": image_mime_type,
            "data": image_data
        },
    ]

    # Call the AI model with the prepared prompt parts
    response = model.generate_content(prompt_parts)

    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  

