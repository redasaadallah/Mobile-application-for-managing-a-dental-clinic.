import hashlib

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from datetime import datetime
from kivy.properties import ObjectProperty, BooleanProperty
from kivymd.uix.list import OneLineListItem, TwoLineAvatarIconListItem
from kivymd.uix.pickers import MDTimePicker,MDDatePicker
from datetime import time as tm
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Line
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView

from hover import HoverIconList
from datatable import *



from kivy.metrics import dp
from collections import OrderedDict
from pymongo import MongoClient


Builder.load_file('Infopers.kv')



class ActionApp(Screen):
    def Mes_infos_perso_back(self):
        app=App.get_running_app()
        app.root.current = "home"




    #def Modifier_info(self):

    def enr(self):
        app=App.get_running_app()
        l=[]
        l.append('Nom: ')
        l.append('Prenom: ')
        l.append('Date de naissance: ')
        l.append('Telephone: ')
        l.append('Adresse: ')
        l.append('Email: ')
        l.append('Assurance: ')
        l.append('CIN: ')
        l.append('Mot de passe: ')
        i=0
        t=[]
        t.append(self.ids.nom.text)
        t.append(self.ids.prenom.text)
        t.append(self.ids.dn.text)
        t.append(self.ids.tel.text)
        t.append(self.ids.adr.text)
        t.append(self.ids.ema.text)
        t.append(self.ids.ass.text)
        #t.append(self.ids.CIN.text)
        #t.append(self.ids.motpass.text)
        k=[]
        for widget in t:
            substring = l[i]
            if widget.startswith(substring):
                new_string = widget[len(substring):]
                k.append(new_string)

            i+=1

        app.root.get_screen('save').ids.nom.text=k[0]
        app.root.get_screen('save').ids.prenom.text =k[1]
        app.root.get_screen('save').ids.dn.text =k[2]
        app.root.get_screen('save').ids.tel.text =k[3]
        app.root.get_screen('save').ids.adr.text =k[4]
        app.root.get_screen('save').ids.email.text =k[5]
        app.root.get_screen('save').ids.ass.text =k[6]
        #app.root.get_screen('save').ids.cin.text =k[7]
        #app.root.get_screen('save').ids.passw.text =k[8]
        app.root.current='save'


        
    def deconnecter(self):
        confirm_dialog = MDDialog(
            text="Êtes-vous sûr de vouloir vous déconnecter ?",
            buttons=[
                MDFlatButton(
                    text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDFlatButton(
                    text="SELECT",
                    on_release=lambda x: self.on_confirm11( confirm_dialog),
                ),
            ],
        )

        confirm_dialog.open()
    def on_confirm11(self,dialog):
        app=App.get_running_app()
        dialog.dismiss()
        app.root.current='loginp'
        