from flask import Flask, request, render_template, send_file, jsonify
import pyttsx3
import os
import uuid
import threading
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def delete_file_after_delay(file_path, delay):
    time.sleep(delay)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    tts = pyttsx3.init()
    unique_filename = f'static/output_{uuid.uuid4().hex}.mp3'
    tts.save_to_file(text, unique_filename)
    tts.runAndWait()

    # Start a background thread to delete the file after 60 seconds
    threading.Thread(target=delete_file_after_delay, args=(unique_filename, 60)).start()
    
    return jsonify({"audio_file": unique_filename})

@app.route('/download/<filename>')
def download(filename):
    output_file = f'static/{filename}'
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
