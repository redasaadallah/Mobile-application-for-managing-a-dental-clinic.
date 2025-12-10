import os
import ssl

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
import smtplib
import random
import string
from email.message  import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
Builder.load_file('oublierr.kv')
class OublierApp(Screen):
        def Envoyer(self):
                app=App
                app.get_running_app()
                cl=MongoClient()
                db=cl['Admin_cabinet']
                col=db['Patients']
                password = self.generate_random_password()
                for user in col.find():

                        if user['Email']==self.ids.em.text:

                                app.email=self.ids.em.text
                                dialog = MDDialog(
                                        title="Confirmation",
                                        text="Veuillez consulter votre boîte de réception Gmail pour trouver votre nouveau mot de passe. Un email contenant les instructions pour accéder à votre compte a été envoyé. Si vous ne trouvez pas l'email dans votre boîte de réception principale, veuillez vérifier votre dossier 'Spam' ou 'Courrier indésirable' ",
                                        buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                                )
                                dialog.open()
                                emailsender = 'amanadentiste234@gmail.com'
                                emailpassword = 'smlcfqjukkbbcyzg'
                                emailreceiver = app.email
                                subject = "Réinitialisation du mot de passe"
                                body = "Bonjour "+" "+user['Nom']+" "+user['Prenom']+",Nous avons réinitialisé avec succès le mot de passe de votre compte.\n\nVeuillez trouver ci-dessous votre nouveau mot de passe :\nNouveau mot de passe : "+password +"\n\nSi vous n'avez pas demandé de réinitialisation de mot de passe, veuillez ignorer cet e-mail,Merci.\n\nCordialement,\n\nDentiste Amana."

                                db5 = cl[user['Prenom']+'_'+user['Nom']]
                                col2=db5['signup']
                                for user2 in col2.find():
                                        doc_prec = {"Password": user2['Password']}
                                        newvalues = {
                                        "$set": {'Password': hashlib.sha256(password.encode()).hexdigest()}}

                                        col2.update_one(doc_prec, newvalues)
                                em = EmailMessage()
                                em['From'] = emailsender
                                em['Subject'] = subject
                                em['To'] = emailreceiver
                                em.set_content(body)
                                context = ssl.create_default_context()
                                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                        smtp.login(emailsender, emailpassword)
                                        smtp.sendmail(emailsender, emailreceiver, em.as_string())
                                break
                        elif self.ids.em.text=='':
                                dialog = MDDialog(
                                        title="OOPS",
                                        text="Veuillez remplir le champs",
                                        buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                                )
                                dialog.open()

                        else:
                                dialog = MDDialog(
                                        title="Erreur",
                                        text="L'email fourni n'a pas été trouvé dans notre système.",
                                        buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                                )
                                dialog.open()

        def generate_random_password(self,length=8):
                length = int(length)
                characters = string.ascii_letters + string.digits + string.punctuation
                password = ''.join(random.choice(characters) for _ in range(length))
                return password


