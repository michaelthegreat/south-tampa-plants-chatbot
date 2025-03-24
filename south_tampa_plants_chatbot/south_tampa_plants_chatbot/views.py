from hotels.fb import FB
from hotels.models import Postbacks

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
