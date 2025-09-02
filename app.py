from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI   # OpenAI SDK (new version)

# Load environment variables from .env
load_dotenv(dotenv_path='.env')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

class GPTWeatherChatbot:
    """
    A chatbot that uses OpenAI GPT API for weather-related questions.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise Exception("OpenAI API key (OPENAI_API_KEY) not configured in .env file.")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def get_response(self, message):
        """
        Gets a smart, AI-generated response from OpenAI GPT.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",   # You can change to gpt-4o / gpt-4.1 / gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are a helpful weather assistant."},
                    {"role": "user", "content": message}
                ],
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "I'm sorry, I couldn't fetch the response right now. Please try again."

# Create chatbot instance
try:
    chatbot = GPTWeatherChatbot()
except Exception as e:
    print(f"Failed to initialize chatbot: {e}")
    chatbot = None

# --- API Routes ---

@app.route('/api/chat', methods=['POST'])
def chat():
    if not chatbot:
        return jsonify({'error': 'Chatbot is not initialized. Check your API key.'}), 500

    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        print(f"Incoming message: {message}")
        response_text = chatbot.get_response(message)
        print(f"GPT response: {response_text}")
        
        return jsonify({
            'response': response_text,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'source': 'openai_gpt'
        })
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({'error': str(e), 'status': 'server_error'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    api_key_status = "configured" if chatbot and chatbot.api_key else "not configured"
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Weather Chatbot API',
        'llm_integration': 'OpenAI GPT',
        'api_key_status': api_key_status,
        'model': 'gpt-4o-mini'
    })

if __name__ == '__main__':
    print("Starting Weather Chatbot API with OpenAI GPT...")
    if not chatbot:
        print("!!! CRITICAL ERROR: Chatbot failed to start. Check your OPENAI_API_KEY in the .env file. !!!")
    else:
        print("API available at: http://localhost:5000")
        print("Model: gpt-4o-mini")
        app.run(debug=True, host='0.0.0.0', port=5000)
