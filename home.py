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
from hover import HoverIconList
from datatable import *



from kivy.metrics import dp
from collections import OrderedDict
from pymongo import MongoClient
Builder.load_file('home.kv')

class OpenApp(Screen):

    def Mes_infos_perso(self):
            #app.root.get_screen('Infopers').ids.CIN.text += user['CIN']
            #app.root.get_screen('Infopers').ids.motpass.text += user['Password']
        app = App.get_running_app()
        app.root.current = "Infopers"

    def Contact(self):
        app = App.get_running_app()
        app.root.current = "Contactn"


    def Mes_RDV(self):
        app = App.get_running_app()
        app.root.current = "Mes_RDV1"


    def Notification(self):
        app = App.get_running_app()
        list=app.root.get_screen('Notification').ids.list1
        papa=app.root.get_screen('Notification').ids.pere
        papa = app.root.get_screen('Notification').ids.avatar


        k=0

        if len(app.root.get_screen('Mes_RDV1').ids.moddate.text)<=6 :
            if k==0:
                for child_widget in list.children:
                    app.removed_widgets.append(child_widget)
                    list.remove_widget(child_widget)
                k+=1
            app.root.current = "Notification"
        else:

            if len(app.removed_widgets)!=0:
                for i in app.removed_widgets:
                    list.add_widget(i)
                    app.removed_widgets.remove(i)
            app.root.current = "Notification"



    def Fixer_RDV(self):
        app = App.get_running_app()
        db = app.root.get_screen('loginp').databasef
        app.root.current = "Fixer_RDV1"
        collecton = db['Fixer_RDV']
        count = collecton.count_documents({})
        if count == 0:
            app.root.get_screen('Fixer_RDV1').ids.clock.disabled = False
            app.root.get_screen('Fixer_RDV1').ids.calendar.disabled = False
            app.root.get_screen('Fixer_RDV1').ids.ftime.disabled = False
            app.root.get_screen('Fixer_RDV1').ids.fdate.disabled = False
            #app.root.get_screen('Mes_RDV1').ids.mrdv.add_widget(app.child)
            #parent_layout = app.root.get_screen('Mes_RDV1').ids.box1
            #app.root.get_screen('Mes_RDV1').ids.pr.add_widget(parent_layout)
            #app.root.get_screen('Mes_RDV1').ids.mrdv.add_widget(app.mdf)
            #app.root.get_screen('Mes_RDV1').ids.mrdv.add_widget(app.supp)



    def Messagerie(self):
        app = App.get_running_app()
        app.root.current = "Messagerie"


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