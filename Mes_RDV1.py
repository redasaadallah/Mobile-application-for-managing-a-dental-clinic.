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
Builder.load_file('Mes_RDV1.kv')
class RDVApp(Screen):
    def show_modification(self):
            self.dialog=MDDialog(
                    title='procesuss de modification',
                    type='custom',
                    content_cls=Dialogue_modifer(),
                )
            self.dialog.open()


    def Mes_RDV_back(self):
        app=App.get_running_app()
        app.root.current = "home"


    def supp_RDV(self):
        confirm_dialog = MDDialog(
            text=f"Êtes-vous sur d'annuler votre rendez-vous?",
            buttons=[
                MDFlatButton(
                    text="NON", on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDFlatButton(
                    text="OUI",
                    on_release=lambda x: self.supp_RDV2(confirm_dialog),
                ),
            ],
        )

        confirm_dialog.open()




    def supp_RDV2(self,dialog):
        app = App.get_running_app()
        db = app.root.get_screen('loginp').databasef
        #first_document = db.signup.find_one()
        collecton=db['Fixer_RDV']
        client2=MongoClient()
        db2=client2['Admin_cabinet']
        collecton2=db2['Rendez_vous']
        for user in collecton.find():
            collecton.delete_one({"Date":user['Date']})
            collecton.delete_one({"Heure":user['Heure']})
        for user2 in collecton2.find():
            if user2['ID_Patient']==app.ID:

                doc2 = {"ID_Rendez_vous": user2['ID_Rendez_vous'], "ID_Patient":user2["ID_Patient"] , "Date": user2["Date"], "Heure":user2["Heure"], "Nom_Acte": user2["Nom_Acte"],
                    "Statut du rendez-vous": user2["Statut du rendez-vous"], "Notes ou instructions supplémentaires": user2["Notes ou instructions supplémentaires"]}
                collecton2.delete_one(doc2)
                break
        # Clear the list of removed widgets
        app.removed_widgets_mrdv = []
        app.removed_widgets_box = []
        app.new_widgets=[]
        app.mrdv=self.ids.mrdv
        app.mdf=self.ids.md
        app.supp=self.ids.sp
        app.dte=self.ids.moddate
        app.id=self.ids.op
        app.hr=self.ids.modclock
        #app.child=app.mrdv.children[1]
        #app.removed_widgets.append(app.mrdv.children[1])
        #app.mrdv.remove_widget(app.mrdv.children[1])
        app.parent_layout=self.ids.box1
        #app.removed_widgets.append(app.parent_layout)
        app.removed_widgets_box.append(app.id.__self__)
        app.removed_widgets_box.append(app.dte.__self__)
        app.removed_widgets_box.append(app.hr.__self__)
        app.parent_layout.remove_widget(app.id.__self__)
        app.parent_layout.remove_widget(app.dte.__self__)
        app.parent_layout.remove_widget(app.hr.__self__)
        app.removed_widgets_mrdv.append(app.mdf.__self__)
        self.ids.mrdv.remove_widget(app.mdf.__self__)
        app.removed_widgets_mrdv.append(app.supp.__self__)
        self.ids.mrdv.remove_widget(app.supp.__self__)
        xc=MDLabel(text='Veuillez Fixer Un Rendez-vous', font_style='H4', font_size='190sp',
                pos_hint={'center_x': .58, 'center_y': .5})
        app.parent_layout.add_widget(xc)
        app.label=(xc)
        app.verifyy=True
        dialog.dismiss()
        #app.verifyy=False
        db0=app.root.get_screen('loginp').databasef
        noti = db0['Notifications']
        for user3 in noti.find():
            if app.root.get_screen('home').ids.card1_button.icon == 'numeric-2' and user3['duo'] == 'bienvenue':
                app.root.get_screen('Notification').ids.fb1.opacity = 0
                app.root.get_screen('home').ids.card1_button.icon = 'numeric-1'


            elif app.root.get_screen('home').ids.card1_button.icon == 'numeric-1' and user3['duo'] == 'bienvenue':
                app.root.get_screen('Notification').ids.fb1.opacity = 0
                app.root.get_screen('home').ids.card1_button.opacity=0

            elif app.root.get_screen('home').ids.card1_button.icon == 'numeric-2' and user3['duo'] == 'bienvenue':
                app.root.get_screen('Notification').ids.fb.opacity = 0
                app.root.get_screen('home').ids.card1_button.icon = 'numeric-1'


            else:

                app.root.get_screen('Notification').ids.fb.opacity = 0
                app.root.get_screen('home').ids.card1_button.opacity = 0
                doc_prec = {"duo": user3['duo']}
                newvalues = {"$set": {'duo':'rdv'}}
                noti.update_one(doc_prec, newvalues)

    def on_cancell(self):
        self.dialog.dismiss()
class Dialogue_modifer(MDBoxLayout):

    saved_value_time=None
    saved_value_date=None
    def show_date_picker(self):
        datedialog=MDDatePicker()
        datedialog.bind(on_save=self.on_save)
        datedialog.open()


    def on_cancell(self, dialog,**kwargs):
        self.dd.dismiss()


    def Enregistrer_modification(self):
        app=App.get_running_app()
        self.dd=app.root.get_screen('Mes_RDV1').dialog
        if self.ids.mdf_date.text =='' or self.ids.mdf_clock.text == '':
            dialog2 = MDDialog(
                title="OOPS",
                text="Champs non rempli.",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog2.dismiss())],
            )
            dialog2.open()
        else:
            confirm_dialog = MDDialog(
            text=f"Êtes-vous sure d'enregistrer votre modification ",
            buttons=[
                MDFlatButton(
                    text="NON", on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDFlatButton(
                    text="OUI",
                    on_release=lambda x: self.on_confirm( confirm_dialog,self.dd),
                ),
             ],
            )

            confirm_dialog.open()






    def on_confirm(self, dialoge,ins):
        # Perform desired action with selected date
        #self.date = value.strftime("%Y-%m-%d")

        app = App.get_running_app()
        dialoge.dismiss()
        app.root.get_screen('Mes_RDV1').ids.modclock.text='Date: '
        app.root.get_screen('Mes_RDV1').ids.moddate.text='Heure: '
        app.root.get_screen('Mes_RDV1').ids.modclock.text += str(self.temps)
        app.root.get_screen('Mes_RDV1').ids.moddate.text += str(self.date)
        ins.dismiss()

        app=App.get_running_app()
        db = app.root.get_screen('loginp').databasef
        client1=MongoClient()
        db2=client1['Admin_cabinet']
        collection2=db2['Rendez_vous']
        collecton=db['Fixer_RDV']
        for user in collecton.find():
            doc_prec={"Date":user['Date']  }
            newvalues={"$set": { 'Date':self.date},}

            collecton.update_one(doc_prec, newvalues)
            doc_prec = {"Heure": user['Heure']}
            newvalues = {"$set": {'Heure': self.temps}}
            collecton.update_one(doc_prec, newvalues)
        for user2 in collection2.find():

            if user2['ID_Patient']==app.ID:
                doc_prec = {"Date": user2['Date']}
                newvalues = {"$set": {'Date':self.date }}
                collection2.update_one(doc_prec, newvalues)
                doc_prec = {"Heure": user2['Heure']}
                newvalues = {"$set": {'Heure':self.temps }}
                collection2.update_one(doc_prec, newvalues)





        dialog2 = MDDialog(
            title="Confirmation",
            text="Operation avec succees.",
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog2.dismiss())],
            )
        dialog2.open()







    def on_cancel_time(self,instance,time):
        if time==None:
            self.ids.mdf_clock.text=''



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

                        if user['Date'] == value.strftime("%Y-%m-%d") and user['Heure'] in heures  :
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



                        elif value.strftime("%Y-%m-%d") < date.today().strftime("%Y-%m-%d"):
                            dialog1 = MDDialog(
                                    title="OOPS",
                                    text="La date choisie est indisponible.Tous les rendez-vous sont remplis pour cette journée.",
                                    buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog1.dismiss())],
                                )
                            dialog1.open()
                            flag = True
                            po = False
                            break





                        elif value.weekday() in (5,6):
                                dialog = MDDialog(
                                title="OOPS",
                                text="Ce jour est ferie.",
                                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                                )
                                dialog.open()
                                flag = True
                                po=False# Set the flag to True

                                break
                    if po==False:
                        break

                if po == False:
                    break

            if po == False:  # Check the flag after the innermost loop
                break


        if flag==False:

            confirm_dialog = MDDialog(
                text=f"Are you sure you want to select {str(value)}?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm1(value, confirm_dialog),
                    ),
                ],
            )
            confirm_dialog.open()

    def on_confirm1(self, value, dialog):
        # Perform desired action with selected date
        self.date=value.strftime("%Y-%m-%d")
        self.ids.mdf_date.text = str(value)

        dialog.dismiss()




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


                        if user['Heure'] == time.strftime('%H:%M:%S') and (user['Date'] == self.date )or ((time.minute > 0 and time.minute < 30) and (time.hour == time.hour)) or ((time.minute > 30 and time.minute <= 59) and (time.hour == time.hour))or (time >= tm(15,30) or time <= tm(9,59)):
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

    def on_confirm2(self, time, dialog):
        # Perform desired action with selected date
        self.ids.mdf_clock.text = str(time)
        self.temps=str(time)
        dialog.dismiss()



    def dismiss_dialog(self, *args):
        self.button.state = "normal"


    def Time_modification(self):
        cal_time=MDTimePicker()
        default_time=datetime.strptime("19:00:00",'%H:%M:%S')
        cal_time.set_time(default_time)
        self.ids.mdf_clock.text = '19:00:00'
        self.saved_value_time='19:00:00'
        cal_time.bind(on_cancel=self.on_cancel_time,time=self.on_save_time)
        cal_time.open()


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
        dialog.dismiss()
        self.root.current='loginp'