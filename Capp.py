from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = 'sk-proj-7Lv0uHPJj2CaBuX9Be83T3BlbkFJne3b2rF7A8n9pB93XfW9'

@app.route('/message', methods=['POST'])
def handle_message():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        bot_message = response.choices[0].message['content']
        return jsonify({"message": bot_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
        app.run(debug=True, port=6000)

