"""
Backboard.io API client for bird chat functionality.
"""
import requests
import os

# Toggle for using real API vs canned responses
USE_BACKBOARD_API = True  # Set to True to use real API calls

BASE_URL = "https://app.backboard.io/api"

def _load_api_key():
    """Load API key from secrets.txt file."""
    secrets_path = os.path.join(os.path.dirname(__file__), '..', '..', 'secrets.txt')
    try:
        with open(secrets_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('BACKBOARD_API_KEY='):
                    return line.split('=', 1)[1]
    except FileNotFoundError:
        print("Warning: secrets.txt not found. API calls will fail.")
    return None

API_KEY = _load_api_key()
HEADERS = {"X-API-Key": API_KEY} if API_KEY else {}


class BackboardClient:
    """Client for interacting with backboard.io API."""
    
    def __init__(self, bird_data, event_data=None):
        self.bird_data = bird_data
        self.event_data = event_data
        self.assistant_id = bird_data.get('backboard_assistant_id')
        self.thread_id = bird_data.get('backboard_thread_id')
        self.species = bird_data.get('species', 'Bird')
        
    def _build_system_prompt(self):
        """Build a system prompt based on bird data."""
        species = self.species
        personality = self.bird_data.get('personality', '')
        
        prompt = f"You are a {species}. Use short chirpy sentences with occasional bird sounds (*chirp*, *tweet*). Max 1-2 sentences."
        if personality:
            prompt += f" {personality}"
            
        if self.event_data:
            prompt += f" {self.event_data['prompt']}"
            
        return prompt
    
    def ensure_assistant_and_thread(self):
        """Create assistant and thread if they don't exist."""
        if not USE_BACKBOARD_API or not API_KEY:
            return False
            
        try:
            # Create assistant if needed
            if not self.assistant_id:
                response = requests.post(
                    f"{BASE_URL}/assistants",
                    json={
                        "name": f"{self.species} Chat",
                        "system_prompt": self._build_system_prompt(),
                        "llm_provider": "openai",
                        "llm_model_name": "gpt-5-chat-latest", 
                        "embedding_provider": "openai",
                        "embedding_model_name": "text-embedding-3-large",
                        "memory": "Auto"
                    },
                    headers=HEADERS,
                    timeout=10
                )
                if response.status_code == 200:
                    self.assistant_id = response.json().get("assistant_id")
                else:
                    print(f"Failed to create assistant: {response.text}")
                    return False
            
            # Create thread if needed
            if not self.thread_id and self.assistant_id:
                response = requests.post(
                    f"{BASE_URL}/assistants/{self.assistant_id}/threads",
                    json={},
                    headers=HEADERS,
                    timeout=10
                )
                if response.status_code == 200:
                    self.thread_id = response.json().get("thread_id")
                else:
                    print(f"Failed to create thread: {response.text}")
                    return False
             
            
            # If we have event data and an assistant exists, force update the prompt
            if self.event_data and self.assistant_id:
                try:
                    requests.patch(
                        f"{BASE_URL}/assistants/{self.assistant_id}",
                        json={"system_prompt": self._build_system_prompt()},
                        headers=HEADERS
                    )
                except:
                    print("Failed to update assistant prompt for event.")

            return True
            
        except requests.RequestException as e:
            print(f"Backboard API error: {e}")
            return False
    
    def send_message(self, message):
        """Send a message and get a response."""
        if not USE_BACKBOARD_API or not API_KEY:
            return None
            
        if not self.thread_id:
            if not self.ensure_assistant_and_thread():
                return None
        
        try:
            response = requests.post(
                f"{BASE_URL}/threads/{self.thread_id}/messages",
                headers=HEADERS,
                data={
                    "content": message,
                    "stream": "false",
                    "memory": "Auto"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("content")
            else:
                print(f"Message send failed: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"Backboard API error: {e}")
            return None
    
    def get_ids_for_storage(self):
        """Return IDs to be saved in bird_data."""
        return {
            'backboard_assistant_id': self.assistant_id,
            'backboard_thread_id': self.thread_id
        }
