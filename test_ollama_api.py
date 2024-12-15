import requests

def test_ollama_api():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:latest",
        "prompt": "What is the meaning of life?",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ollama_api()