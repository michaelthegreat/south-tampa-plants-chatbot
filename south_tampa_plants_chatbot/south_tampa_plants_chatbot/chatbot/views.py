from .fb import FB
from .models import Postbacks
from rest_framework.response import Response
from time import sleep
import json
import requests
from rest_framework.decorators import api_view
from rest_framework import generics
from .renderers import PlainTextRenderer
import os

@api_view(['GET','POST'])
def south_tampa_plants(request):
    if request.method == 'GET':
        print (request.body)
        body_unicode = request.body.decode('utf-8')

        return Response("get call made to south_tampa_plants")
    if request.method == 'POST':
        print (request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        fb = FB(body)
        query_json = body['result']['parameters']

        #try:
        if 'postback' in body['originalRequest']['data']:
            # fb_rating = Postbacks(
            #     first_name=fb.userInfo['first_name'],
            #     last_name=fb.userInfo['last_name'],
            #     gender=fb.userInfo['gender'],
            #     postback=str(body['originalRequest']['data']['postback']['payload']),
            #     fb_userId=str(fb.sender_id)
            # )
            # fb_rating.save_to_db()
            postback = body['originalRequest']['data']['postback']['payload']
            print("postback", postback)
            # handle_postback(postback, fb)


            # if "NEW_USER_STARTED" in body['originalRequest']['data']['postback']['payload']:
            #     fb.independantTextMessage(fb.sender_id, "Hey there, Foodie !!! I'm JugheadBot, your friendly neighbourhood Restaurant finding Bot")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "You can ask me following questions:")
            #     fb.independantTextMessage(fb.sender_id, "\"Which are the best Restaurants in Kothrud, Pune\"")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "\"Which are the best Chinese Restaurants in Dadar, Mumbai\"")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "\"What is the review of Blue Nile in Camp Area, Pune\"")
            #     sleep(1)
            # elif "HELP_TEXT" in body['originalRequest']['data']['postback']['payload']:
            #     fb.independantTextMessage(fb.sender_id, "Currently, I understand only the following 3 types of questions")
            #     fb.independantTextMessage(fb.sender_id, "\"Which are the best Restaurants in Kothrud, Pune\"")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "\"Which are the best Chinese Restaurants in Dadar, Mumbai\"")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "\"What is the review of Blue Nile in Camp Area, Pune\"")
            #     sleep(1)
            #     fb,independantTextMessage(fb.sender_id, "And PLEASE remember to specify the Area AND City. For example: \"Manhattan, New York\" or \"Dadar, Mumbai\"")
            #     sleep(1)
            # else:
            #     fb.independantTextMessage(fb.sender_id, "Thanks !! I'll let Raseel know how much you liked me !!")
            return Response("{}")
        # except:
        #         # Not a Postback, so continue
        #         print("Not a Postback, so continue")
        #         pass

        messages = []
        restaurant_list = []

        if "Cuisines" in query_json:
            cuisine = str()
            cuisine = query_json['Cuisines']
            print (cuisine)
            messages = fb.textMessage(messages, "Could not find Restaurants for your specific Cuisine. Could you maybe re-check the spelling and try again?")
        elif "res-name" in query_json:
            print ("This is a query for a Review")
            res_name = query_json['res-name']
            print (res_name)
            restaurant_review = "TODO: delete this review endpoint"
            messages = fb.cardMessage(messages, restaurant_review)
        else:
            # Just get the Top 5 Restaurants in the location
            messages = fb.cardMessage(messages, restaurant_list)

        response = {
            "messages" : messages
        }
        print(response)
        return Response(response)


def handle_postback(postback, fb):
    """
    Handle the postback
    """
    if "NEW_USER_STARTED" in postback:
        greeting_message = "Hello " + fb.userInfo['first_name'] + ", I'm JugheadBot, your friendly neighbourhood Restaurant finding Bot"
        fb.independantTextMessage(fb.sender_id, greeting_message)
        help_message(fb)
    elif "HELP_TEXT" in postback:
        help_message(fb)
    elif "LIKED_JUGHEADBOT" in postback:
        fb.independantTextMessage(fb.sender_id, "Thanks !! I'll let Raseel know how much you liked me !!")
    elif "INTERESTED_IN_JUGHEADBOT" in postback:
        fb.independantTextMessage(fb.sender_id, "Hmm ... I'll try my best to be more helpful and entertaining")
    elif "BORED_WITH_JUGHEADBOT" in postback:
        fb.independantTextMessage(fb.sender_id, "That's too bad :-( But hey, don't blame me, Raseel's the one who's made me Boring")
    else:
        fb.independantTextMessage(fb.sender_id, "I Live to Eat")


def help_message(fb):
    """
    Help for JugheadBot
    """
    fb.independantTextMessage(fb.sender_id, "Currently, I understand only the following 3 types of questions")
    sleep(2)
    fb.independantTextMessage(fb.sender_id, "Best Restaurants : \"Which are the best Restaurants in Kothrud, Pune\"")
    sleep(2)
    fb.independantTextMessage(fb.sender_id, "Best Restaurants by Cuisine : \"Which are the best Chinese Restaurants in Dadar, Mumbai\"")
    sleep(2)
    fb.independantTextMessage(fb.sender_id, "Reviews for a specific Restaurant : \"What is the review of Blue Nile in Camp Area, Pune\"")
    sleep(2)
    fb.independantTextMessage(fb.sender_id, "PLEASE REMEMBER to specify an Area and City. For example : \"Gomti Nagar, Lucknow\" or \"Mahim, Mumbai\" or \"Kothrud, Pune\"")

        # Todo: pull this from env

VERIFY_TOKEN = 'test_token'

class MessengerWebhook(generics.GenericAPIView):
    """Facebook messenger webhook"""
    renderer_classes = [PlainTextRenderer]
    page_access_token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    facebook_message_url = "https://graph.facebook.com/v2.10/me/messages"
    facebook_user_url = "https://graph.facebook.com/v2.10/"
    default_reply = "Hello, this is an automated response. Feel free to place an order or ask a question and a human will be with you shortly. You can see everything available for sale and the quantity available here https://southtampaplants.wemerch.me"
    
    def get(self, request, *args, **kwargs):
        """Verifys facebook messenger token"""
        
        mode = request.GET.get("hub.mode")
        if mode == "subscribe" and request.GET.get('hub.verify_token') == VERIFY_TOKEN:
            return Response(request.GET.get('hub.challenge'))
        else:
            return Response("Verification token mismatch", status=403)

    def post(self, request, *args, **kwargs):
        """Main webhook endpoint"""
        print("in main webhook", request.data)
        object = request.data.get("object")
        if object == 'page':
            entry = request.data.get("entry")
            print("entry", entry)
            for entry in entry:
                try:
                    messaging = entry["messaging"]
                    for m in messaging:
                        sender_id = m['sender']['id']
                        recipient_id = m['recipient']['id']
                        message = m.get("message")
                        print("recieved message", {"sender": sender_id, "recipient": recipient_id, "message":message})
                    
                        self.sendMessage(sender_id, self.default_reply)
                except Exception as e:
                    print("exception occured when parsing messages", e)
                
            return Response('EVENT_RECEIVED')
        
        print("messenger hook called with")
        mode = request.data.get("hub.mode")
        if mode == "subscribe" and request.data.get('hub.verify_token') == VERIFY_TOKEN:
            return Response(request.data.get('hub.challenge'))
        else:
            return Response("Verification token mismatch", status=403)
        
        
    def sendMessage(self, senderId, text):
        """
        Reference independant FB message
        if fb.isFacebook():
           fb.independantTextMessage(fb.sender_id, "I love Burgers !!!")
        """
        headers = {"Content-Type":"application/json"}
        params = {"access_token":self.page_access_token}
        data = json.dumps({"recipient":{"id":senderId}, "message":{"text":text}})

        status = requests.post(self.facebook_message_url,params=params,headers=headers,data=data)
        print("status_code = %s, status_text = %s", status.status_code, status.text)