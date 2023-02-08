# from flask import Flask, request, abort

# app = Flask(__name__)

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         print(request.json)
#         return 'success', 200
#     else:
#         abort(400)
        
# @app.route('/webhook', methods=['GET'])
# def webhookGet():
#     if request.method == 'GET':
#         print(request.json)
#         return 'success', 200
#     else:
#         abort(400)

# if __name__ == '__main__':
#     app.run()

# app/whatsapp_client.py

import os
import requests

import json

# import time
# import random
# from chat_bot import chatbot_response


class WhatsAppWrapper:

    API_URL = "https://graph.facebook.com/v13.0/"
    BOT_URL = "https://chat-bot-responder-ox6yxlojcq-tl.a.run.app/"
    API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    NUMBER_ID = os.environ.get("WHATSAPP_NUMBER_ID")

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.NUMBER_ID

    def send_template_message(self, template_name, language_code, phone_number):

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"

        return response.status_code
    
    def send_message(self, message, phone_number):
        print(message)
        print(phone_number)
        # bot_response = chatbot_response(message)
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"

        return response.status_code
    
    
    def mark_message_as_read(self, message_id):
        
        payload = json.dumps({
            'messaging_product': 'whatsapp',
            'status': 'read',
            'message_id': message_id,
        })
        response = requests.request(
            "POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"
        return response.status_code
    
    
    def ask_response_to_the_bot(self, message):
        
        print(message)
        
        payload = json.dumps({
            "message": message
        })
        response = requests.request(
            "GET", f"{self.BOT_URL}/get_response", headers=self.headers, data=payload)

        assert response.status_code == 201, "Error sending message"
        return response
    
    

    def process_webhook_notification(self, data):
        """_summary_: Process webhook notification
        For the moment, this will mark the message as read and return the type of notification
        """

        response = []

        for entry in data["entry"]:

            # self.mark_as_read(message_id=entry["id"])
            for change in entry["changes"]:
                response.append(
                    {
                        "type": change["field"],
                        "from": change["value"]["metadata"]["display_phone_number"],
                    }
                )
                for message in change["value"]["messages"]:
                    # print(change["value"])
                    # random_sleeper = random.randint(0, 30)
                    # time.sleep(random_sleeper)
                    message_id = message["id"]
                    self.mark_message_as_read(message_id=message_id)
                    # self.send_message(self, message, response["from"])
                    sended_message = message["text"]["body"]
                    print(sended_message)
                    res = self.ask_response_to_the_bot(self, message=sended_message)
                    if True:
                        received_message = res.content
                        print(received_message)
                        self.send_message("received_message", "237698509488")
                    # else:
                    #     self.send_message("An error occured", response["from"])
                    # print(message["contacts"]["wa_id"])
                    # Do whatever with the response
        return response