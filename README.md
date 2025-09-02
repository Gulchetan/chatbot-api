# AI Chatbot Setup Guide

## Overview
Your weather chatbot has been upgraded with Hugging Face AI integration! It now supports intelligent responses using the `openai/gpt-oss-120b:groq` model.

## Features
- ✅ **Intelligent AI Responses**: Uses Hugging Face's router API for natural language processing
- ✅ **Fallback System**: Works even without API token with pre-programmed responses
- ✅ **Weather-Focused**: Specialized prompts for weather-related conversations
- ✅ **Error Handling**: Robust error handling and timeout management
- ✅ **CORS Enabled**: Works with React frontend

## Setup Instructions

### 1. Get Your Hugging Face Token
1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Create a new token with read permissions
3. Copy the token

### 2. Configure Environment Variables
Edit the `.env` file in the chatbot directory:
```bash
# Replace 'your_huggingface_token_here' with your actual token
HF_TOKEN=hf_your_actual_token_here

# Flask Configuration (optional)
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Install Dependencies
```bash
cd d:\rick-site\chatbot
pip install -r requirements.txt
```

### 4. Start the Chatbot Service
```bash
python app.py
```

## Usage

### Testing the API Directly
```bash
# Health check
curl http://localhost:5000/api/health

# Send a message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather like in Paris?"}'
```

### Frontend Integration
The React frontend automatically connects to the chatbot service. You can:
- Use the floating chat button in the bottom right
- Visit the dedicated chatbot page through navigation
- Get intelligent responses about weather topics

## API Endpoints

### POST /api/chat
Send messages to the chatbot
```json
{
  "message": "Your message here"
}
```

Response:
```json
{
  "response": "AI generated response",
  "timestamp": "2025-09-01T22:00:00",
  "status": "success"
}
```

### GET /api/health
Check service status
```json
{
  "status": "healthy",
  "service": "Weather Chatbot API",
  "hf_integration": "configured",
  "timestamp": "2025-09-01T22:00:00"
}
```

### GET /api/suggestions
Get conversation starter suggestions
```json
{
  "suggestions": [
    "What's the weather like today?",
    "Show me weather analytics",
    "Tell me about climate trends"
  ]
}
```

## How It Works

1. **AI-First Approach**: If HF_TOKEN is configured, the bot uses Hugging Face's intelligent model
2. **Graceful Fallback**: If the AI service is unavailable, it falls back to keyword-based responses
3. **Weather Specialization**: The system prompt focuses the AI on weather-related topics
4. **Error Recovery**: Network timeouts and API errors are handled gracefully

## Troubleshooting

### Bot Returns Simple Responses
- Check if HF_TOKEN is set in the `.env` file
- Verify your Hugging Face token is valid
- Check the console for error messages

### Service Won't Start
- Ensure Python dependencies are installed
- Check if port 5000 is available
- Verify the `.env` file exists and is readable

### Frontend Can't Connect
- Ensure the chatbot service is running on port 5000
- Check for CORS errors in browser console
- Verify React app is running on the correct port

## Example Conversations

**User**: "What causes thunderstorms?"
**AI**: "Thunderstorms form when warm, moist air rises rapidly in the atmosphere. This creates strong updrafts that can reach heights of 40,000-60,000 feet..."

**User**: "Tell me about Paris weather"
**AI**: "Paris has a temperate oceanic climate with mild winters and warm summers. You can search for current conditions in our City Search section..."

## Development Notes

- The AI model `openai/gpt-oss-120b:groq` is optimized for conversational AI
- Maximum response length is set to 150 tokens for concise answers
- Temperature is set to 0.7 for creative but focused responses
- 10-second timeout prevents hanging requests

Your AI assistant is now ready to provide intelligent, weather-focused conversations!