import json
import re
import random_responses
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from datetime import datetime
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivymd.uix.list import OneLineListItem, TwoLineAvatarIconListItem
from kivymd.uix.pickers import MDTimePicker,MDDatePicker

from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Line
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from hover import HoverIconList
from datetime import datetime, time
from oublierr import *
from datatable import *
from sinscrire import *
from Infopers import *
from loginp import  *
from home import *
from Fixer_RDV1 import *
from Mes_RDV1 import *

Window
from kivy.metrics import dp
from collections import OrderedDict
from pymongo import MongoClient
from asst import *
from datetime import date
Builder.load_file('Messagerie.kv')


class ChatbotApp(Screen):
    chat_area = ObjectProperty()
    message = ObjectProperty()

    def __init__(self):
        super(ChatbotApp, self).__init__()
        self.response_data = self.load_json("data.json")



    def send_message(self):
        self.user_input = self.ids.message.text
        self.ids.message.text = ""
        length = len(self.user_input)

        if length >= 40:
            self.ids.chat_area.add_widget(
                PatientInput(text=self.user_input, font_size=17, height=length)
            )
        else:
            self.ids.chat_area.add_widget(
                PatientInput(text=self.user_input, font_size=17)
            )

    def bot_response(self):
        response = self.get_response(self.user_input)
        length = len(str(response))

        if length >= 40:
            self.ids.chat_area.add_widget(
                Reponse(text="{}".format(response), font_size=17, height=length)
            )
        else:
            self.ids.chat_area.add_widget(
                Reponse(text="{}".format(response), font_size=17)
            )

    def load_json(self,file):
        with open(file) as bot_responses:

            return json.load(bot_responses)

    # Store JSON data


    def get_response(self,input_string):
        split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
        score_list = []

        # Check all the responses
        for response in self.response_data:
            response_score = 0
            required_score = 0
            required_words = response["required_words"]

            # Check if there are any required words
            if required_words:
                for word in split_message:
                    if word in required_words:
                        required_score += 1

            # Amount of required words should match the required score
            if required_score == len(required_words):
                # print(required_score == len(required_words))
                # Check each word the user has typed
                for word in split_message:
                    # If the word is in the response, add to the score
                    if word in response["user_input"]:
                        response_score += 1

            # Add score to list
            score_list.append(response_score)
            # Debugging: Find the best phrase
            # print(response_score, response["user_input"])

        # Find the best response and return it if they're not all 0
        best_response = max(score_list)
        response_index = score_list.index(best_response)

        # Check if input is empty
        if input_string == "":
            return "Veuillez taper quelque chose pour que nous puissions discuter  :("

        # If there is no good response, return a random one.
        if best_response != 0:
            return self.response_data[response_index]["bot_response"]

        return random_responses.random_string()


class PatientInput(MDCard):
    text=StringProperty()
    font_size = NumericProperty()

class Reponse(MDCard):
    text = StringProperty()
    font_size = NumericProperty()








