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
from datetime import date
import plyer
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
Builder.load_file('Fixer_RDV1.kv')
class FixerApp(Screen):
    def enregistrer(self):
        app = App.get_running_app()

        date = self.ids.fdate.text
        heure = self.ids.ftime.text
        db = app.root.get_screen('loginp').databasef
        if date=='' and heure=='' and app.root.get_screen('Fixer_RDV1').ids.fdate.disabled == False:
            dialog = MDDialog(
                title="OOPS",
                text="Veuillez remplir tous les champs",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()
        elif app.root.get_screen('Fixer_RDV1').ids.fdate.disabled == True:
            dialog = MDDialog(
                title="OOPS",
                text="Vous avez déjà pris un rendez-vous. Veuillez annuler votre rendez-vous actuel pour en prendre un autre.",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

        else:
            i = -1
            j = -2
            k = 1
            d = 1
            app = App.get_running_app()
            patients = app.get_rendez_vous()
            last_ele = list(patients.items())[0]

            p = (last_ele[1])
            new_string = 'P000'
            if not p:
                pass

            else:
                pp = list(p.values())[-1]
                if int(pp[-1]) == 9:
                    pp = 'P0' + str(k + 9)
                    k += 1
                if int(pp[-2:]) == 99:
                    pp = 'P' + str(d + 99)
                    d += 1
                num = int(pp[-1]) + 1
                string_list = list(pp)
                string_list[-1] = str(num)
                new_string = ''.join(string_list)
            collection = db["Fixer_RDV"]
            client1 = MongoClient()
            db2 = client1['Admin_cabinet']
            collection2=db2['Rendez_vous']
            document = {"Date":date , "Heure":heure }
            doc2= {"ID_Rendez_vous":new_string , "ID_Patient":app.ID,"Date":date,"Heure":heure,"Nom_Acte": "-","Statut du rendez-vous": "-","Notes ou instructions supplémentaires": "-"}
            collection.insert_one(document)
            collection2.insert_one(doc2)
            datee='Date: '
            hour='Heure: '
            id='ID: '
            self.verify=True
            dialog = MDDialog(
                title="Confirmation",
                text="Votre rendez-vous a été fixé avec succès.",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            think=False

            noti = db['Notifications']
            plyer.notification.notify(title='Dentiste Amana', message='Rendez vous fixé')
            app.root.get_screen('Notification').ids.avatar.secondary_text="from:Amana@gmail.com\\"+ datetime.now().time().strftime("%H:%M:%S")
            screen = App.get_running_app().root.get_screen('Notification')
            list0 = screen.ids.list0
            list1 = screen.ids.list1

            # Get the current pos_hint values of list0 and list1
            pos_hint_0 = {'center_x':.5,'center_y':.5}
            pos_hint_1 = {'center_x':.5,'center_y':.3}

            # Swap the pos_hint values
            list0.pos_hint = pos_hint_1
            list1.pos_hint = pos_hint_0

            for user in noti.find():
                doc_prec = {"Time_rdv": user['Time_rdv']}
                newvalues = {"$set": {'Time_rdv':datetime.now().time().strftime("%H:%M:%S") }}
                noti.update_one(doc_prec, newvalues)
            if app.root.get_screen('home').ids.card1_button.opacity==0:
                app.root.get_screen('home').ids.card1_button.opacity=1
                app.root.get_screen('Notification').ids.fb.opacity = 1
                for user in noti.find():
                    doc_prec = {"Etat": user['Etat']}
                    newvalues = {"$set": {'Etat': '1'}}
                    noti.update_one(doc_prec, newvalues)
            else:
                app.root.get_screen('home').ids.card1_button.icon = 'numeric-2'
                app.root.get_screen('Notification').ids.fb.opacity = 1
                for user in noti.find():
                    doc_prec = {"Etat": user['Etat']}
                    newvalues = {"$set": {'Etat': '2'}}
                    noti.update_one(doc_prec, newvalues)


            if app.verifyy==True:

                app.parent_layout.remove_widget(app.label)
                for adam in app.removed_widgets_box:
                    app.parent_layout.add_widget(adam)

                for widget in app.removed_widgets_mrdv:
                    app.mrdv.add_widget(widget)

                app.removed_widgets_mrdv.clear()
                app.removed_widgets_box.clear()
                app.verifyy=False


            collection2=db2['Patients']
            collection1=db['signup']

            for user1,user2 in zip(collection1.find(),collection2.find()):
                if user1['Nom']==user2['Nom'] and user1['Prenom']==user2['Prenom']:
                    app.ID=user2['ID_Patient']
            app.root.get_screen('Mes_RDV1').ids.moddate.text=datee
            app.root.get_screen('Mes_RDV1').ids.modclock.text=hour
            app.root.get_screen('Mes_RDV1').ids.op.text=id
            app.root.get_screen('Mes_RDV1').ids.op.text += app.ID
            app.root.get_screen('Mes_RDV1').ids.moddate.text +=app.root.get_screen('Fixer_RDV1').ids.fdate.text
            app.root.get_screen('Mes_RDV1').ids.modclock.text += app.root.get_screen('Fixer_RDV1').ids.ftime.text
            app.root.get_screen('Fixer_RDV1').ids.clock.disabled = True
            app.root.get_screen('Fixer_RDV1').ids.calendar.disabled = True
            app.root.get_screen('Fixer_RDV1').ids.ftime.disabled = True
            app.root.get_screen('Fixer_RDV1').ids.fdate.disabled = True
            app.root.get_screen('Mes_RDV1').ids.md.disabled = False
            app.root.get_screen('Mes_RDV1').ids.sp.disabled = False

            app.root.get_screen('Fixer_RDV1').ids.fdate.text = ''
            app.root.get_screen('Fixer_RDV1').ids.ftime.text = ''
            dialog.open()




    def Time(self):
        app = App.get_running_app()
        cal_time=MDTimePicker()
        default_time=datetime.strptime("19:00:00",'%H:%M:%S')
        cal_time.set_time(default_time)
        app.root.get_screen('Fixer_RDV1').ids.ftime.text = '19:00:00'
        cal_time.bind(on_cancel=self.on_cancel_time,time=self.on_save_time)
        cal_time.open()

    def Date(self):
        cal_date=MDDatePicker()
        cal_date.bind(on_save=self.on_save)
        cal_date.open()


    def on_save(self,instance,value,date_range):

        clientauth = MongoClient()
        heures=['10:00:00','10:30:00','11:00:00','11:30:00','12:00:00','12:30:00','13:00:00','13:30:00','14:00:00','14:30:00','15:00:00']
        collection_names = ['Fixer_RDV','Rendez_vous']
        databases = clientauth.list_database_names()
        flag=False
        po=True
        for database in databases:
            db = clientauth[database]
            for collection_name in collection_names:

                if collection_name in db.list_collection_names():
                    collecton=db[collection_name]
                    for user in collecton.find():

                        if (user['Date'] == value.strftime("%Y-%m-%d") and user['Heure'] in heures)  :
                            heures.remove(user['Heure'])
                            if heures==[]:
                                dialog1 = MDDialog(
                                    title="OOPS",
                                    text="La date choisie est indisponible.Tous les rendez-vous sont remplis pour cette journée.",
                                    buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog1.dismiss())],
                                )
                                dialog1.open()
                                flag = True
                                po = False
                                break


                # Set the flag to True

                                break
                    if po==False:
                        break

                if po == False:
                    break

            if po == False:  # Check the flag after the innermost loop
                break




        if value.weekday() in (5, 6):
            dialog = MDDialog(
            title="OOPS",
            text="Ce jour est ferie.",
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()
            flag = True
            po = False




        if value.strftime("%Y-%m-%d") < date.today().strftime("%Y-%m-%d"):
            dialog1 = MDDialog(
            title="OOPS",
            text="La date choisie est indisponible.Tous les rendez-vous sont remplis pour cette journée.",
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog1.dismiss())],
            )
            dialog1.open()
            flag = True
            po = False

        if flag==False:

            confirm_dialog = MDDialog(
                text=f"Êtes-vous certain de vouloir sélectionner{str(value)}?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm(value, confirm_dialog),
                    ),
                ],
            )
            confirm_dialog.open()




    def on_save_time(self,instance,time):
        current_time = datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute

        po=True
        clientauth = MongoClient()
        collection_names = ['Fixer_RDV', 'Rendez_vous']
        databases = clientauth.list_database_names()
        app = App.get_running_app()
        for database in databases:
            db = clientauth[database]
            for collection_name in collection_names:
                if collection_name in db.list_collection_names():
                    collecton=db[collection_name]
                    for user in collecton.find():


                        if (user['Heure'] == time.strftime('%H:%M:%S') and (user['Date'] == self.date )):
                            dialog = MDDialog(
                                title="OOPS",
                                text="L'heure choisie est indisponible. Veuillez choisir une autre heure.",
                                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                            )
                            dialog.open()

                            po=False
                            break
                    if po==False:
                        break
            if po==False:
                break
        if ((time.minute > 0 and time.minute < 30) and (time.hour == time.hour)) or ((time.minute > 30 and time.minute <= 59) and (time.hour == time.hour))or (time >= tm(15,30) or time <= tm(9,59)):
            dialog = MDDialog(
                title="OOPS",
                text="L'heure choisie est indisponible. Veuillez choisir une autre heure.",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()
            po=False






        if po==True:
            confirm_dialog = MDDialog(
            text=f"Êtes-vous certain de vouloir sélectionner {str(time)}?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                        ),
                    MDFlatButton(
                        text="SELECT",
                                on_release=lambda x: self.on_confirm2(time, confirm_dialog),
                        ),
                    ],
                )

            confirm_dialog.open()



    def on_confirm(self, value, dialog):
        # Perform desired action with selected date
        self.date = value.strftime("%Y-%m-%d")
        dialog.dismiss()
        app = App.get_running_app()
        app.root.get_screen('Fixer_RDV1').ids.fdate.text =str(value)

    def on_cancel_time(self,instance,time):
        app = App.get_running_app()
        if time==None:
            app.root.get_screen('Fixer_RDV1').ids.ftime.text=''




    def on_confirm2(self, time, dialog):
        # Perform desired action with selected date
        app = App.get_running_app()
        app.root.get_screen('Fixer_RDV1').ids.ftime.text =  str(time)
        dialog.dismiss()


    def Fixer_RDV_back(self):
        app = App.get_running_app()
        app.root.current = "home"

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
