import os
import google.generativeai as genai
from flask import Flask,request,jsonify,render_template
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMEINI_API_KEY"))

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template ('index.html')

@app.route('/transcribe',methods=['POST','GET'])
def get_transcript():
    if request.method=='POST':
        audio = request.files['audio']
        language = request.form.get('language')
        if audio:  #If there is audio file means True
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],audio.filename)
            audio.save(file_path) #Save uploaded audio file to that path
            
            genai_file = genai.upload_file(file_path) #Audio file

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([genai_file,f"Transcript this Audio Clip in {language}"])
            transcription = response.text

            return render_template('index.html',transcription=transcription)
    return "No file is uploaded!"

if __name__ == "__main__":
    app.run(debug=True)