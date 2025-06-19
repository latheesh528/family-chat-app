from flask import Flask, request, jsonify, send_from_directory
import os
import json

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# File to store messages
MESSAGES_FILE = 'messages.json'

# Ensure messages file exists
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    return "✅ Flask server is running!"

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'user' not in data or 'msg' not in data:
        return jsonify({"error": "Invalid data"}), 400

    with open(MESSAGES_FILE, 'r') as f:
        messages = json.load(f)

    messages.append({"user": data['user'], "msg": data['msg']})

    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f)

    return jsonify({"status": "Message sent"})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    with open(MESSAGES_FILE, 'r') as f:
        messages = json.load(f)
    return jsonify(messages)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    filename = image.filename
    if not filename:
        return jsonify({"error": "No filename"}), 400

    path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(path)

    return jsonify({
        "status": "Image uploaded",
        "url": f"/uploads/{filename}"
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
