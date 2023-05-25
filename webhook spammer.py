import time
import requests

webhook = "your webhook here"
message = "your message here"

def send_webhook_message(url, message):
    data = {
        "content": message
    }
    response = requests.post(url, json=data)
    if response.status_code == 204:
        print("sent")
    else:
        print(f"rate limit, this shouldn't happen more than 5 times in a row")

while True:
    send_webhook_message(webhook, message)
    time.sleep(0.05)  
