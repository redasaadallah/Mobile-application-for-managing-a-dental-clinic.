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
from hover import HoverIconList
from datatable import *
import plyer


from kivy.metrics import dp
from collections import OrderedDict
from pymongo import MongoClient
from kivymd.toast import toast
Builder.load_file('loginp.kv')



class OwnApp(Screen):
    def focus_next_text_input(self):
        self.ids.password_field.focus = True

    def check_credentials(self):
        username = self.ids.username_field.text
        password = self.ids.password_field.text
        client1 = MongoClient()
        db2 = client1['Admin_cabinet']
        collection2 = db2['Patients']
        clientauth = MongoClient()
        collection_name = 'signup'
        databases = clientauth.list_database_names()
        app = App.get_running_app()
        for database in databases:
            db = clientauth[database]
            if collection_name in db.list_collection_names():
                for user in db.signup.find():

                    if user['Email'] == username and hashlib.sha256(password.encode()).hexdigest()== user['Password']:


                        nom=user['Nom']
                        prenom=user['Prenom']
                        app.root.get_screen('Infopers').ids.nom.text +=user['Nom']
                        app.root.get_screen('Infopers').ids.prenom.text +=user['Prenom']
                        app.root.get_screen('Infopers').ids.dn.text +=user['Date de naissance']
                        app.root.get_screen('Infopers').ids.tel.text +=user['Telephone']
                        app.root.get_screen('Infopers').ids.adr.text +=user['Adresse']
                        app.root.get_screen('Infopers').ids.ema.text +=user['Email']
                        app.root.get_screen('Infopers').ids.ass.text +=user['Assurance']
                        app.root.get_screen('home').ids.userup.text=nom+' '+prenom
                        app.root.get_screen('home').ids.flname.text=nom+' '+prenom
                        app.root.get_screen('email').ids.flname.text = nom + ' ' + prenom
                        app.root.get_screen('Fixer_RDV1').ids.flname.text = nom + ' ' + prenom
                        app.root.get_screen('Infopers').ids.flname.text = nom + ' ' + prenom
                        app.root.get_screen('Mes_RDV1').ids.flname.text = nom + ' ' + prenom
                        app.root.get_screen('Messagerie').ids.flname.text = nom + ' ' + prenom
                        app.root.get_screen('Contactn').ids.flname.text = nom + ' ' + prenom
                        app.root.get_screen('Notification').ids.flname.text = nom + ' ' + prenom
                        app.root.get_screen('bvn').ids.flname.text = nom + ' ' + prenom
                        app.root.get_screen('save').ids.flname.text = nom + ' ' + prenom
                        for user2 in collection2.find():
                            if  nom== user2['Nom'] and  prenom== user2['Prenom']:
                                app.ID=user2['ID_Patient']

                        col3 = db['Notifications']
                        for user3 in col3.find():
                            app.root.get_screen(
                                'Notification').ids.avatar.secondary_text = "from:Amana@gmail.com\\" + user3['Time_rdv']
                            app.root.get_screen(
                                'Notification').ids.avatar1.secondary_text = "from:Amana@gmail.com\\" + user3[
                                'first_connexion']
                            if user3['Etat']=='Never clicked':
                                plyer.notification.notify(title='Dentiste Amana', message='Bienvenue chez Dentiste Amana')
                            if user3['Etat']=='0':
                                app.root.get_screen('Notification').ids.fb.opacity=0
                                app.root.get_screen('home').ids.card1_button.opacity=0
                                app.root.get_screen('Notification').ids.fb1.opacity=0
                            elif user3['Etat']=='2':
                                app.root.get_screen('home').ids.card1_button.icon = 'numeric-2'
                            elif user3['Etat']=='1' and user3['duo']=='bienvenue':
                               app.root.get_screen('Notification').ids.fb1.opacity=0
                            else:
                               app.root.get_screen('Notification').ids.fb.opacity=0




                        collecton = db['Fixer_RDV']
                        count = collecton.count_documents({})
                        for user in collecton.find():
                            if count != 0:
                                app.root.get_screen('Fixer_RDV1').ids.clock.disabled = True
                                app.root.get_screen('Fixer_RDV1').ids.calendar.disabled = True
                                app.root.get_screen('Fixer_RDV1').ids.ftime.disabled = True
                                app.root.get_screen('Fixer_RDV1').ids.fdate.disabled = True
                                app.root.get_screen('Mes_RDV1').ids.op.text += app.ID
                                app.root.get_screen('Mes_RDV1').ids.modclock.text += user['Date']
                                app.root.get_screen('Mes_RDV1').ids.moddate.text += user['Heure']
                                app.root.get_screen('Mes_RDV1').ids.md.disabled = False
                                app.root.get_screen('Mes_RDV1').ids.sp.disabled = False
                            else:
                                app.root.get_screen('Mes_RDV1').ids.md.disabled=True
                                app.root.get_screen('Mes_RDV1').ids.sp.disabled=True
                        self.ids.username_field.text=''
                        self.ids.password_field.text=''
                        app.root.current = 'home'
                        self.databasef = db







                        return True


        if username == "admin" and password == "admin":
            app.root.current = "home"
            self.ids.username_field.text = ''
            self.ids.password_field.text = ''
        elif username=='amanadentiste234@gmail.com' and password=='ZinebHEFFOUDHIamana432':
            #app.root.get_screen('admin').ids.modife.disabled = True
            self.ids.username_field.text = ''
            self.ids.password_field.text = ''
            content = app.root.get_screen('admin').ids.display_patients
            patients = app.get_patients()
            patientstable = DataTable(table=patients)
            content.add_widget(patientstable)
            content1 = app.root.get_screen('admin').ids.display_rendez_vous
            rdvs = app.get_rendez_vous()
            rdvstable = DataTable(table=rdvs)
            content1.add_widget(rdvstable)
            content2 = app.root.get_screen('admin').ids.display_visite
            rdvss = app.get_visites()
            rdvstables = DataTable(table=rdvss)
            content2.add_widget(rdvstables)
            content3 = app.root.get_screen('admin').ids.display_salle
            salle = app.get_salle()
            salletables = DataTable(table=salle)
            content3.add_widget(salletables)
            content4 = app.root.get_screen('admin').ids.display_presc
            presc = app.get_prescription()
            presctables = DataTable(table=presc)
            content4.add_widget(presctables)
            content5 = app.root.get_screen('admin').ids.display_actes
            actes = app.get_actes()
            actestables = DataTable(table=actes)
            content5.add_widget(actestables)
            content6 = app.root.get_screen('admin').ids.display_med
            med = app.get_medicament()
            medtables = DataTable(table=med)
            content6.add_widget(medtables)
            content7 = app.root.get_screen('admin').ids.display_paiement
            paie = app.get_paiement()
            medtabless = DataTable(table=paie)
            content7.add_widget(medtabless)
            app.root.current='admin'
            app.root.get_screen('admin').ids.text1.readonly = True
            app.root.get_screen('admin').ids.text2.readonly = True
            app.root.get_screen('admin').ids.text3.readonly = True
            app.root.get_screen('admin').ids.text4.readonly = True
            app.root.get_screen('admin').ids.text5.readonly = True
            app.root.get_screen('admin').ids.text6.readonly = True
            app.root.get_screen('admin').ids.text7.readonly = True
            app.root.get_screen('admin').ids.text8.readonly = True
            app.root.get_screen('admin').ids.text9.readonly = True
            app.root.get_screen('admin').ids.text1_rdv.readonly = True
            app.root.get_screen('admin').ids.text2_rdv.readonly = True
            app.root.get_screen('admin').ids.text3_rdv.readonly = True
            app.root.get_screen('admin').ids.text4_rdv.readonly = True
            app.root.get_screen('admin').ids.text5_rdv.readonly = True
            app.root.get_screen('admin').ids.text6_rdv.readonly = True
            app.root.get_screen('admin').ids.text7_rdv.readonly = True
            app.root.get_screen('admin').ids.text1_visite.readonly = True
            app.root.get_screen('admin').ids.text2_visite.readonly = True
            app.root.get_screen('admin').ids.text3_visite.readonly = True
            app.root.get_screen('admin').ids.text4_visite.readonly = True
            app.root.get_screen('admin').ids.text5_visite.readonly = True
            app.root.get_screen('admin').ids.text6_visite.readonly = True
            app.root.get_screen('admin').ids.text7_visite.readonly = True
            app.root.get_screen('admin').ids.text1_salle.readonly = True
            app.root.get_screen('admin').ids.text2_salle.readonly = True
            app.root.get_screen('admin').ids.text3_salle.readonly = True
            app.root.get_screen('admin').ids.text4_salle.readonly = True
            app.root.get_screen('admin').ids.text5_salle.readonly = True
            app.root.get_screen('admin').ids.text6_salle.readonly = True
            app.root.get_screen('admin').ids.text1_presc.readonly = True
            app.root.get_screen('admin').ids.text2_presc.readonly = True
            app.root.get_screen('admin').ids.text3_presc.readonly = True
            app.root.get_screen('admin').ids.text4_presc.readonly = True
            app.root.get_screen('admin').ids.text5_presc.readonly = True
            app.root.get_screen('admin').ids.text6_presc.readonly = True
            app.root.get_screen('admin').ids.text7_presc.readonly = True
            app.root.get_screen('admin').ids.text1_actes.readonly = True
            app.root.get_screen('admin').ids.text2_actes.readonly = True
            app.root.get_screen('admin').ids.text4_actes.readonly = True
            app.root.get_screen('admin').ids.text1_med.readonly = True
            app.root.get_screen('admin').ids.text2_med.readonly = True
            app.root.get_screen('admin').ids.text3_med.readonly = True
            app.root.get_screen('admin').ids.text4_med.readonly = True
            app.root.get_screen('admin').ids.text5_med.readonly = True
            app.root.get_screen('admin').ids.text6_med.readonly = True
            app.root.get_screen('admin').ids.text7_med.readonly = True
            app.root.get_screen('admin').ids.text1_p.readonly = True
            app.root.get_screen('admin').ids.text2_p.readonly = True
            app.root.get_screen('admin').ids.text3_p.readonly = True
            app.root.get_screen('admin').ids.text4_p.readonly = True
            app.root.get_screen('admin').ids.text5_p.readonly = True
            app.root.get_screen('admin').ids.text6_p.readonly = True
            app.root.get_screen('admin').ids.text7_p.readonly = True
            app.root.get_screen('admin').ids.text8_p.readonly = True
            app.root.get_screen('admin').ids.text9_p.readonly = True
            app.root.get_screen('admin').ids.text10_p.readonly = True

        elif username=='amanadentiste234@gmail.com' and password=='Assistanteamana432':
            self.ids.username_field.text = ''
            self.ids.password_field.text = ''
            content = app.root.get_screen('asst').ids.display_patients
            patients = app.get_patients()
            patientstable = DataTable(table=patients)
            content.add_widget(patientstable)
            content1 = app.root.get_screen('asst').ids.display_rendez_vous
            rdvs = app.get_rendez_vous()
            rdvstable = DataTable(table=rdvs)
            content1.add_widget(rdvstable)
            content2 = app.root.get_screen('asst').ids.display_visite
            rdvss = app.get_visites()
            rdvstables = DataTable(table=rdvss)
            content2.add_widget(rdvstables)
            content3 = app.root.get_screen('asst').ids.display_salle
            salle = app.get_salle()
            salletables = DataTable(table=salle)
            content3.add_widget(salletables)
            content4 = app.root.get_screen('asst').ids.display_presc
            presc = app.get_prescription()
            presctables = DataTable(table=presc)
            content4.add_widget(presctables)
            content5 = app.root.get_screen('asst').ids.display_actes
            actes = app.get_actes()
            actestables = DataTable(table=actes)
            content5.add_widget(actestables)
            content6 = app.root.get_screen('asst').ids.display_med
            med = app.get_medicament()
            medtables = DataTable(table=med)
            content6.add_widget(medtables)
            content7 = app.root.get_screen('asst').ids.display_paiement
            paie = app.get_paiement()
            medtabless = DataTable(table=paie)
            content7.add_widget(medtabless)
            app.root.current='asst'
            app.root.get_screen('asst').ids.text1.readonly = True
            app.root.get_screen('asst').ids.text2.readonly = True
            app.root.get_screen('asst').ids.text3.readonly = True
            app.root.get_screen('asst').ids.text4.readonly = True
            app.root.get_screen('asst').ids.text5.readonly = True
            app.root.get_screen('asst').ids.text6.readonly = True
            app.root.get_screen('asst').ids.text7.readonly = True
            app.root.get_screen('asst').ids.text8.readonly = True
            app.root.get_screen('asst').ids.text9.readonly = True
            app.root.get_screen('asst').ids.text1_rdv.readonly = True
            app.root.get_screen('asst').ids.text2_rdv.readonly = True
            app.root.get_screen('asst').ids.text3_rdv.readonly = True
            app.root.get_screen('asst').ids.text4_rdv.readonly = True
            app.root.get_screen('asst').ids.text5_rdv.readonly = True
            app.root.get_screen('asst').ids.text6_rdv.readonly = True
            app.root.get_screen('asst').ids.text7_rdv.readonly = True
            app.root.get_screen('asst').ids.text1_visite.readonly = True
            app.root.get_screen('asst').ids.text2_visite.readonly = True
            app.root.get_screen('asst').ids.text3_visite.readonly = True
            app.root.get_screen('asst').ids.text4_visite.readonly = True
            app.root.get_screen('asst').ids.text5_visite.readonly = True
            app.root.get_screen('asst').ids.text6_visite.readonly = True
            app.root.get_screen('asst').ids.text7_visite.readonly = True
            app.root.get_screen('asst').ids.text1_salle.readonly = True
            app.root.get_screen('asst').ids.text2_salle.readonly = True
            app.root.get_screen('asst').ids.text3_salle.readonly = True
            app.root.get_screen('asst').ids.text4_salle.readonly = True
            app.root.get_screen('asst').ids.text5_salle.readonly = True
            app.root.get_screen('asst').ids.text6_salle.readonly = True
            app.root.get_screen('asst').ids.text1_presc.readonly = True
            app.root.get_screen('asst').ids.text2_presc.readonly = True
            app.root.get_screen('asst').ids.text3_presc.readonly = True
            app.root.get_screen('asst').ids.text4_presc.readonly = True
            app.root.get_screen('asst').ids.text5_presc.readonly = True
            app.root.get_screen('asst').ids.text6_presc.readonly = True
            app.root.get_screen('asst').ids.text7_presc.readonly = True
            app.root.get_screen('asst').ids.text1_actes.readonly = True
            app.root.get_screen('asst').ids.text2_actes.readonly = True
            app.root.get_screen('asst').ids.text4_actes.readonly = True
            app.root.get_screen('asst').ids.text1_med.readonly = True
            app.root.get_screen('asst').ids.text2_med.readonly = True
            app.root.get_screen('asst').ids.text3_med.readonly = True
            app.root.get_screen('asst').ids.text4_med.readonly = True
            app.root.get_screen('asst').ids.text5_med.readonly = True
            app.root.get_screen('asst').ids.text6_med.readonly = True
            app.root.get_screen('asst').ids.text7_med.readonly = True
            app.root.get_screen('asst').ids.text1_p.readonly = True
            app.root.get_screen('asst').ids.text2_p.readonly = True
            app.root.get_screen('asst').ids.text3_p.readonly = True
            app.root.get_screen('asst').ids.text4_p.readonly = True
            app.root.get_screen('asst').ids.text5_p.readonly = True
            app.root.get_screen('asst').ids.text6_p.readonly = True
            app.root.get_screen('asst').ids.text7_p.readonly = True
            app.root.get_screen('asst').ids.text8_p.readonly = True
            app.root.get_screen('asst').ids.text9_p.readonly = True
            app.root.get_screen('asst').ids.text10_p.readonly = True

        else:
            dialog = MDDialog(
                title="Login failed",
                text="Incorrect username or password.",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()



    def Inscrire(self):
        app = App.get_running_app()
        app.root.current = "sinscrire"

