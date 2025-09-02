from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv(dotenv_path='.env')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for all routes

class GeminiWeatherChatbot:
    """
    A chatbot that uses the Google Gemini API for weather-related questions.
    """
    def __init__(self):
        # Configure the Gemini API with the key from the .env file
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise Exception("Google AI API key (GOOGLE_API_KEY) not configured in .env file.")
        
        genai.configure(api_key=self.api_key)
        
        # Create the Gemini model instance
        # Using gemini-1.5-flash for speed, or you can use 'gemini-1.5-pro'
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_response(self, message):
        """
        Gets a smart, AI-generated response from the Gemini model.
        """
        try:
            # Simple prompt for the model
            prompt = f"You are a helpful weather assistant. Answer this question concisely: {message}"
            
            # Generate content using the Gemini API
            response = self.model.generate_content(prompt)
            
            # Extract and return the text part of the response
            return response.text.strip()
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try again."

# Create an instance of the chatbot
try:
    chatbot = GeminiWeatherChatbot()
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
        print(f"Gemini response: {response_text}")
        
        return jsonify({
            'response': response_text,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'source': 'google_gemini'
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
        'llm_integration': 'Google Gemini',
        'api_key_status': api_key_status,
        'model': 'gemini-1.5-flash-latest'
    })

if __name__ == '__main__':
    print("Starting Weather Chatbot API with Google Gemini...")
    if not chatbot:
        print("!!! CRITICAL ERROR: Chatbot failed to start. Check your GOOGLE_API_KEY in the .env file. !!!")
    else:
        print("API available at: http://localhost:5000")
        print("Model: gemini-1.5-flash-latest")
        app.run(debug=True, host='0.0.0.0', port=5000)