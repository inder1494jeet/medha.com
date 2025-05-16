from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ChatGPTClone"
mongo = PyMongo(app)

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"  # Replace with actual API Key

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

@app.route("/")
def home():
    chats = mongo.db.chats.find()
    myChats = [{"question": chat["question"], "answer": chat["answer"]} for chat in chats]
    return render_template("index.html", myChats=myChats)

@app.route("/api", methods=["POST"])
def qu():
    try:
        request_data = request.json
        if not request_data or "question" not in request_data:
            return jsonify({"error": "Invalid request, missing 'question'"}), 400
        
        question = request_data["question"]
        chat = mongo.db.chats.find_one({"question": question})
        
        if chat:
            return jsonify({"question": question, "answer": chat["answer"]})
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": question}]
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response from API")
            
            if content:
                mongo.db.chats.insert_one({"question": question, "answer": content})
               # return jsonify({"question": question, "answer": content})
                return jsonify({"question": question, "answer": f"<pre>{content}</pre>"})          
        return jsonify({"error": "Failed to fetch response from API"}), 500  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True, port=5001)