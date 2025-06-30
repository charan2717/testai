import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="/")

# Replace with your Together AI API Key
API_KEY = "5a812dabc044d8d9f0b7805aab68eb90929c766983f930682c22f164563bb656"
API_URL = "https://api.together.xyz/v1/chat/completions"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",  # ✅ FREE model (no need to deploy)
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        print("Full API Response:", response.json())  # Debugging

        if response.status_code == 200:
            bot_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
        else:
            bot_reply = f"Error: {response.json()}"

    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    return jsonify({"response": bot_reply})
@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
