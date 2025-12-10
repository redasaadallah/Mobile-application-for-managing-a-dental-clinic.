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
import hashlib

from kivy.metrics import dp
from collections import OrderedDict
from pymongo import MongoClient

Builder.load_file('sinscrire.kv')



class PatientApp(Screen):

    def Creation_DATABASE_signup_auth(self, **kwargs):
        Nom=self.ids.nom.text
        Prenom=self.ids.prenom.text
        dn=self.ids.dn.text
        tel=self.ids.tel.text
        CIN=self.ids.cin.text
        Adresse=self.ids.adr.text
        email=self.ids.email.text
        ass=self.ids.ass.text
        passw=self.ids.passw.text
        clientsignup=MongoClient()
        databases = clientsignup.list_database_names()
        collection_name = 'signup'
        verify=True
        if Nom=='' or  Prenom=='' or dn=='' or tel=='' or Adresse=='' or email=='' or ass=='' or passw=='':
            dialog = MDDialog(
                title="OOPS",
                text="Veuillez remplir tous les champs",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()
        else:
            for database in databases:
                db=clientsignup[database]
                if collection_name in db.list_collection_names():
                    for user in db.signup.find():
                        if user['Email']==email:
                            dialog = MDDialog(
                                title="OOPS",
                                text="L'adresse e-mail que vous avez fournie est déjà associée à un compte existant. Veuillez utiliser une autre adresse e-mail.",
                                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                            )
                            dialog.open()
                            verify = False
                            break


                        elif user['CIN']==hashlib.sha256(CIN.encode()).hexdigest():
                            dialog = MDDialog(
                                title="OOPS",
                                text="La CIN que vous avez fournie est déjà associée à un compte existant. Veuillez utiliser une autre CIN.",
                                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                            )
                            dialog.open()
                            verify = False
                            break



                    if verify == False:  # Check the flag after the innermost loop
                        break
                if verify == False:  # Check the flag after the innermost loop
                    break


            if verify:
                app = App.get_running_app()
                dialog = MDDialog(
                    title="Succès",
                    text="Votre compte a été créé avec succès.",
                    buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                )
                dialog.open()
                self.ids.nom.text = ''
                self.ids.prenom.text = ''
                self.ids.cin.text = ''
                self.ids.tel.text = ''
                self.ids.adr.text = ''
                self.ids.dn.text = ''
                self.ids.email.text = ''
                self.ids.ass.text = ''
                self.ids.cin.text = ''
                self.ids.passw.text = ''
                app.root.current = 'loginp'
                i = -1
                j = -2
                k = 1
                d = 1
                app=App.get_running_app()
                patients = app.get_patients()
                last_ele = list(patients.items())[0]

                p = (last_ele[1])
                new_string = 'P000'
                if not p:
                    pass

                else:
                    pp = list(p.values())[-1]
                    if int(pp[-1]) == 9:
                        pp = 'P0'+str(k+9)
                        k += 1
                    if int(pp[-2:]) == 99:
                        pp='P' + str(d + 99)
                        d += 1
                    num = int(pp[-1]) + 1
                    string_list = list(pp)
                    string_list[-1] = str(num)
                    new_string = ''.join(string_list)
                client = MongoClient()
                db = client[Prenom+'_'+Nom]
                db2=client['Admin_cabinet']
                signup = db["signup"]
                patient=db2['Patients']
                notif=db['Notifications']


                hashed_password = hashlib.sha256(passw.encode()).hexdigest()
                hashed_CIN=hashlib.sha256(CIN.encode()).hexdigest()
                currenttime=datetime.now().time()
                document = {"Nom": Nom, "Prenom":Prenom,'Date de naissance':dn,'Telephone':tel,'Adresse':Adresse,'Email':email,'Assurance':ass,'CIN':hashed_CIN,'Password':hashed_password}
                doc2={'ID_Patient':new_string,'Nom':Nom,'Prenom':Prenom,'Date de naissance':dn,'Telephone':tel,'Adresse':Adresse,'Antecedents medicaux':"-",'Email':email,'Assurance':ass}
                doc3={'Etat':'Never clicked','duo':'bienvenue','first_connexion':currenttime.strftime("%H:%M:%S"),'Time_rdv':'-'}

                signup.insert_one(document)
                patient.insert_one(doc2)
                notif.insert_one(doc3)
                #app=App.get_running_app()
                #app.ID=new_string

    def switch_to_screen(self):
        app = App.get_running_app()
        app.root.current = 'loginp'

    def focus_next_text_inputs(self, instance):

        if instance.hint_text =='Nom':
            self.ids.prenom.focus = True
        if instance.hint_text =='Prenom':
            self.ids.dn.focus = True
        if instance.hint_text =='Date de naissance':
            self.ids.tel.focus = True
        if instance.hint_text =='Telephone':
            self.ids.adr.focus = True
        if instance.hint_text =='Adresse':
            self.ids.email.focus = True
        if instance.hint_text =='Email':
            self.ids.ass.focus = True
        if instance.hint_text =='Assurance':
            self.ids.cin.focus = True
        if instance.hint_text =='CIN':
            self.ids.passw.focus = True