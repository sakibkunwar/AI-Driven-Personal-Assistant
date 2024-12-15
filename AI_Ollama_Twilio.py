import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import requests


def handle_incoming_call(call_status, caller_number, recipient_number):
    """
    Handles incoming calls and directs them to the AI assistant if the phone is unavailable.

    :param call_status: Status of the recipient's phone (busy, unavailable, etc.).
    :param caller_number: Phone number of the caller.
    :param recipient_number: Phone number of the recipient.
    """
    if call_status in ["busy", "unavailable", "no-answer"]:
        response = VoiceResponse()
        response.say("The person you are calling is unavailable. Transferring you to the AI assistant.")
        # Logic to interact with AI assistant
        message_summary = interact_with_ai(caller_number)
        send_message_summary(recipient_number, message_summary)


def interact_with_ai(caller_number):
    """
    Uses a conversational AI to capture and summarize the caller's message.

    :param caller_number: Phone number of the caller.
    :return: Summarized message from the caller.
    """
    print("Connecting to conversational AI for caller number:", caller_number)
    # Example message collection and summarization logic
    caller_message = "Hello, I need assistance with billing."

    # Interacting with Ollama's local AI endpoint for summarization
    # url = "http://localhost:11434/api/generate"
    url = "http://localhost:11434/api/generate"
    payload = {
        # "model": "llama2",  # Replace with the appropriate Ollama model name
        # "model": "llama3.2",  # Replace with the appropriate Ollama model name
        "model": "llama3.2:latest",  # Replace with the appropriate Ollama model name
        # "prompt": f"Summarize this message: {caller_message}",
        "prompt": caller_message,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print(result)
        # summary = result.get('text', 'Unable to generate summary.')
        summary = "Caller Message : Hello, I need assistance with billing. \n" \
                  "AI Response : "+result.get('response')

    except requests.exceptions.RequestException as e:
        print("Error connecting to Ollama API:", e)
        summary = "Error generating summary. Please check the AI assistant."

    return summary


def send_message_summary(recipient_number, summary):
    """
    Sends a summarized message to the recipient via WhatsApp or Telegram.

    :param recipient_number: Phone number of the recipient.
    :param summary: Summarized message to send.
    """
    print(f"Sending summary to {recipient_number}: {summary}")
    # Retrieve Twilio credentials from environment variables
    # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    # print("Printing account_sid....."+str(account_sid))
    # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    # print("Printing auth_token....."+str(auth_token))
    account_sid = 'twilio_sid'
    auth_token = 'twilio_token'
    
    twilio_whatsapp_number = 'whatsapp:+twilio_whatsapp_number'
    # print("Printing account_sid....." + str(account_sid))
    # print("Printing auth_token....." + str(auth_token))
    client = Client(account_sid, auth_token)

    try:
        client.messages.create(
            from_=f'{twilio_whatsapp_number}',
            body=f"You received a new voicemail summary: {summary}",
            to=f'whatsapp:{recipient_number}'
        )
        print("Message sent successfully.")
    except Exception as e:
        print("Error sending message:", e)


# Example Test Case
if __name__ == "__main__":
    test_call_status = "busy"
    test_caller_number = "+test_caller_number"
    test_recipient_number = "+test_recipient_number"
    handle_incoming_call(test_call_status, test_caller_number, test_recipient_number)
