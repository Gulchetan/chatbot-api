import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
token = os.getenv('HF_TOKEN')
print(f'Token loaded: {bool(token)}')
print(f'Token preview: {token[:20] if token else "Not found"}')

if token:
    headers = {'Authorization': f'Bearer {token}'}
    # Test the API with GPT-2
    data = {
        'inputs': 'Weather Assistant: What is the weather like today?\nResponse:',
        'parameters': {
            'max_new_tokens': 50, 
            'temperature': 0.7,
            'do_sample': True,
            'return_full_text': False,
            'pad_token_id': 50256
        },
        'options': {'wait_for_model': True}
    }
    
    try:
        print("Testing Hugging Face API with GPT-2...")
        response = requests.post(
            'https://api-inference.huggingface.co/models/gpt2',
            headers=headers,
            json=data,
            timeout=15
        )
        print(f'Response status: {response.status_code}')
        print(f'Response: {response.text}')
        
        if response.status_code == 200:
            result = response.json()
            print(f'Parsed result: {result}')
        
    except Exception as e:
        print(f'Error: {e}')
else:
    print("No HF token found!")