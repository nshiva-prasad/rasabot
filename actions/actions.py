# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import re
import time
# from typing_extensions import Required
from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from typing import Any, Text, Dict, List, Union
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction, FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet, UserUtteranceReverted, SessionStarted, AllSlotsReset, FollowupAction


class ActionFees(Action):
    def name(self) -> Text:
        return "utter_fees"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='The fees is 500 Rupees')
        return []

# Validating NAME


class ActionAskName(Action):
    def name(self) -> Text:
        return "action_ask_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot("name_invalid") == 'True':
            dispatcher.utter_message(text='Please enter your name.')
            return [SlotSet("name_invalid", 'False')]
        else:
            dispatcher.utter_message(text='May I have your name?')
        return []


class UserNameForm(FormValidationAction):
    def name(self) -> Text:
        return "user_name_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["name"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"name": self.from_text()}


class ValidateUserNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_name_form"

    def validate_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> Dict[Text, Any]:
        print(slot_value)
        a = tracker.get_slot('name_invalid')  # accessing value from the slots
        if a != 'True':
            if (re.search(r"^[a-zA-Z ]*$", slot_value)):
                return {"name": slot_value, "name_counter": 1, "name_invalid": "True"}
            else:
                dispatcher.utter_message(
                    text="Need your Name to move forward.")
                return {"name": None}
        return {"name_counter": tracker.get_slot('name_counter') + 1}

# Validating NUMBER


class ActionAskNumber(Action):
    def name(self) -> Text:
        return "action_ask_number"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot("number_invalid") == 'True':
            dispatcher.utter_message(text='Please enter your number.')
            return [SlotSet("number_invalid", 'False')]
        else:
            dispatcher.utter_message(text='May I have your number?')
        return []


class UserNumberForm(FormValidationAction):
    def name(self) -> Text:
        return "user_number_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["number"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"number": self.from_text()}


class ValidateUserNumberForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_number_form"

    def validate_number(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> Dict[Text, Any]:
        print(slot_value)
        # accessing value from the slots
        a = tracker.get_slot('number_invalid')
        if a != 'True':
            if (re.search(r"^[6-9]\d{9}$", slot_value)):
                return {"number": slot_value, "number_counter": 1, "number_invalid": "True"}
            else:
                dispatcher.utter_message(
                    text="Need your Number to move forward.")
                return {"number": None}
        return {"number_counter": tracker.get_slot('number_counter') + 1}


# Validating EMAIL

class ActionAskEmail(Action):
    def name(self) -> Text:
        return "action_ask_email"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot("email_invalid") == 'True':
            dispatcher.utter_message(text='Please enter your email.')
            return [SlotSet("email_invalid", 'False')]
        else:
            dispatcher.utter_message(text='May I have your email?')
        return []


class UserEmailForm(FormValidationAction):
    def name(self) -> Text:
        return "user_email_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["email"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"email": self.from_text()}


class ValidateUserEmailForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_email_form"

    def validate_email(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> Dict[Text, Any]:
        print(slot_value)
        a = tracker.get_slot('email_invalid')  # accessing value from the slots
        if a != 'True':
            if (re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", slot_value)):
                return {"email": slot_value, "email_counter": 1, "email_invalid": "True"}
            else:
                dispatcher.utter_message(
                    text="Need your Email to move forward.")
                return {"email": None}
        return {"email_counter": tracker.get_slot('email_counter') + 1}

# Checking all the slots values

# Checking for OPD


class ActionSubmitOPD(Action):
    def name(self) -> Text:
        return "action_submit_OPD"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") > 1) and (tracker.get_slot("email_counter") > 1) and (tracker.get_slot("number_counter") > 1) and (tracker.get_slot("website_domain_counter") > 1)):
            dispatcher.utter_message(
                text='We have your details already. Your appointment is booked')
        else:
            dispatcher.utter_message(
                text="Thank you")
        dispatcher.utter_message(
            template="utter_more_help")
        return []

# Asking for OPD details


class ActionSubmitOPDDetails(Action):
    def name(self) -> Text:
        return "action_submit_OPD_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") == 0) and (tracker.get_slot("email_counter") == 0) and (tracker.get_slot("number_counter") == 0) and (tracker.get_slot("website_domain_counter") == 0)):
            dispatcher.utter_message(
                text='We would need the following details:')
        else:
            pass
        return []


# Checking for Skin Care


class ActionSubmitSkinCare(Action):
    def name(self) -> Text:
        return "action_submit_skin_care"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") > 1) and (tracker.get_slot("email_counter") > 1) and (tracker.get_slot("number_counter") > 1)):
            dispatcher.utter_message(
                text='We have your details already. Your appointment is booked')
        else:
            dispatcher.utter_message(
                text="Thank you, We have well experienced skin specialists with vide areas of experiences")
        dispatcher.utter_message(
            template="utter_more_help")
        return []


# Asking for Skin Care details


class ActionSubmitSkinCareDetails(Action):
    def name(self) -> Text:
        return "action_submit_skin_care_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") == 0) and (tracker.get_slot("email_counter") == 0) and (tracker.get_slot("number_counter") == 0)):
            dispatcher.utter_message(
                text='We would need the following details:')
        else:
            pass
        return []

# Checking for Cardiology


class ActionSubmitCardiology(Action):
    def name(self) -> Text:
        return "action_submit_cardiology"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") > 1) and (tracker.get_slot("email_counter") > 1) and (tracker.get_slot("number_counter") > 1)):
            dispatcher.utter_message(
                text='We have your details already. We look farward to see you.')
        else:
            dispatcher.utter_message(
                text="Thank you for choosing Kavya Hospital, We make your recovery fast")
        dispatcher.utter_message(
            template="utter_more_help")
        return []


# Asking for Cardiology details


class ActionSubmitCardiologyDetails(Action):
    def name(self) -> Text:
        return "action_submit_cardiology_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") == 0) and (tracker.get_slot("email_counter") == 0) and (tracker.get_slot("number_counter") == 0)):
            dispatcher.utter_message(
                text='Great! Please share the following details:')
        else:
            pass
        return []

# Checking for Pulmonology


class ActionSubmitPulmonology(Action):
    def name(self) -> Text:
        return "action_submit_pulmonology"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") > 1) and (tracker.get_slot("email_counter") > 1) and (tracker.get_slot("number_counter") > 1)):
            dispatcher.utter_message(
                text='We have your details already. Please visit the hospital on the appointment date')
        else:
            dispatcher.utter_message(
                text="Thank you, your appointment with us is booked")
        dispatcher.utter_message(
            template="utter_more_help")
        return []

# Asking for Pulmonology details


class ActionSubmitPulmonologyDetails(Action):
    def name(self) -> Text:
        return "action_submit_pulmonology_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") == 0) and (tracker.get_slot("email_counter") == 0) and (tracker.get_slot("number_counter") == 0)):
            dispatcher.utter_message(
                text="Please share the following details:")
        else:
            pass
        return []

# Checking for Oncology


class ActionSubmitOncology(Action):
    def name(self) -> Text:
        return "action_submit_oncology"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") > 1) and (tracker.get_slot("email_counter") > 1) and (tracker.get_slot("number_counter") > 1)):
            dispatcher.utter_message(
                text='We have your details already.')
        else:
            dispatcher.utter_message(
                text="Thank you, Please visit the hospital for a detailed review")
        dispatcher.utter_message(
            template="utter_more_help")
        return []

# Asking for Oncology details


class ActionSubmitOncologyDetails(Action):
    def name(self) -> Text:
        return "action_submit_oncology_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") == 0) and (tracker.get_slot("email_counter") == 0) and (tracker.get_slot("number_counter") == 0)):
            dispatcher.utter_message(
                text="Please share the following details:")
        else:
            pass
        return []

# Checking for Pediatrics


class ActionSubmitDigitalSuite(Action):
    def name(self) -> Text:
        return "action_submit_pediatrics"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") > 1) and (tracker.get_slot("email_counter") > 1) and (tracker.get_slot("number_counter") > 1)):
            dispatcher.utter_message(
                text='We have your details already.')
        else:
            dispatcher.utter_message(
                text="Thank you, Please visit the hopsital immediately in case or emergency or call us on 108")
        dispatcher.utter_message(
            template="utter_more_help")
        return []

# Asking for Pediatrics details


class ActionSubmitAffiliateMarketingDetails(Action):
    def name(self) -> Text:
        return "action_submit_pediatrics_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if ((tracker.get_slot("name_counter") == 0) and (tracker.get_slot("email_counter") == 0) and (tracker.get_slot("number_counter") == 0)):
            dispatcher.utter_message(
                text="Please share the following details:")
        else:
            pass
        return []


def getTime():
    current_hour = time.strptime(time.ctime(time.time())).tm_hour

    if current_hour < 12:
        return "Good Morning!"
    elif current_hour == 12:
        return "Good Noon!"
    elif current_hour > 12 and current_hour < 16:
        return "Good AfterNoon!"
    elif current_hour >= 16:
        return "Good Evening!"


class ActionGetStarted(Action):
    def name(self) -> Text:
        return "action_get_started"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        wish = getTime()
        dispatcher.utter_message(
            text=f"{wish}, welcome to Bavyesh Digital Media - Hyderabad's leading digital marketing agency.")
        dispatcher.utter_message(template="utter_greet")
        return []


# class user_registration_form(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_user_registration_form"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             required_slots = ["name", "number", "email"]
#             # buttons = [
#             #     {"payload":"SEO", "title":"SEO"},
#             #     {"payload":"Website development", "title":"Website development"},
#             #     {"payload":"Digital Marketing", "title":"Digital Marketing"},
#             #     {"payload":"Social Media Marketing", "title":"Social Media Marketing"},
#             #     {"payload":"Digital Suite", "title":"Digital Suite"},
#             #     {"payload":"Affiliate marketing", "title":"Affiliate marketing"},
#             # ]

#         dispatcher.utter_message(template="utter_response")

#         return []

##################################################################################

#
# class UserRegistrationForm(FormValidationAction):
#     def name(self) -> Text:
#         print("activataed")
#         return "user_registration_form"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["name", "number", "email"]

#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         return {"name": self.from_text(), "number": self.from_text(), "email": self.from_text()}


# class ValidateUserRegistrationForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_user_registration_form"

#     def validate_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> Dict[Text, Any]:
#         print(slot_value)
#         # a = tracker.get_slot('name') // accessing value from the slots
#         if (re.search(r"^[a-zA-Z ]*$", slot_value)):
#             return {"name": slot_value}
#         else:
#             dispatcher.utter_message(
#                 text="Need your Name to move forward.")
#             return {"name": None}

#     def validate_number(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> Dict[Text, Any]:
#         print(slot_value)
#         if (re.search(r"^[6-9]\d{9}$", slot_value)):
#             return {"number": slot_value}
#         else:
#             dispatcher.utter_message(
#                 text="Need your Number to move forward.")
#             return {"number": None}

#     def validate_email(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> Dict[Text, Any]:
#         print(slot_value)
#         if (re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", slot_value)):
#             return {"email": slot_value}
#         else:
#             dispatcher.utter_message(
#                 text="Need your Email to move forward.")
#             return {"email": None}
#
