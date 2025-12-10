from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
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
from datetime import datetime, time

from datatable import *
from sinscrire import *
from Infopers import *
from loginp import  *
from home import *
from Fixer_RDV1 import *
from Mes_RDV1 import *
from datetime import date



from kivy.metrics import dp
from collections import OrderedDict
from pymongo import MongoClient
Builder.load_file('asst.kv')



class AsisstantApp(Screen):
    def __init__(self):
        super().__init__()
        self.rm = []
        self.ID = None
        self.verifyy = False
        self.mesrdv = RDVApp()
        self.verify = True
        self.test = True
        self.etat = 0
        client = MongoClient()
        db = client.Admin_cabinet
        self.patients = db.Patients
        table_patients = self.get_patients()
        self.DataTable_patients = DataTable(table=table_patients)
        self.l_past = []
        self.champs_patient = ["ID_Patient", "Nom", "Prenom", "Date de naissance", 'Telephone', "Adresse",
                               "Antecedents medicaux", "Email", "Assurance"]
        self.rdvs = db.Rendez_vous
        self.table_rdv = self.get_rendez_vous()
        self.DataTable_rdv = DataTable(table=self.table_rdv)
        self.l_past_rdv = []
        self.champs_rdv = ["ID_Rendez_vous", "ID_Patient", "Date", "Heure", "Nom_Acte",
                           "Statut du rendez-vous", "Notes ou instructions supplémentaires"]
        self.visites = db.Visite_de_la_journee
        self.table_visites = self.get_visites()
        print(self.table_visites)
        self.DataTable_visites = DataTable(table=self.table_visites)
        self.l_past_visite = []
        self.champs_visite = ["ID_Visite", "ID_Patient", "Date de la visite", "Heure de la visite", "Nom_Acte" ,'Seance',
                              "Notes ou remarques supplémentaires"]
        self.salle = db.Reflet_salle
        self.table_salle = self.get_salle()
        print(self.table_salle)
        self.DataTable_salle = DataTable(table=self.table_salle)
        self.l_past_salle = []
        self.champs_salle = ["ID_Reflet", "Date du reflet", " Heure du reflet", "Nombre de patients en attente",
                             "Statut des patients",
                             "Remarques ou informations supplémentaires"]
        self.presc = db.Prescriptions
        self.table_presc = self.get_prescription()
        self.DataTable_presc = DataTable(table=self.table_presc)
        self.l_past_presc = []
        self.champs_presc = ["ID_Prescription", "ID_Patient", "Nom du medicament", "Posologie",
                             'Durée de la prescription', "Statut de la prescription",
                             "Notes supplémentaires"]
        self.actes = db.Actes
        self.table_actes = self.get_actes()
        self.DataTable_actes = DataTable(table=self.table_actes)
        self.l_past_actes = []
        self.champs_actes = ["ID_Acte", "Nom_Acte", "Coût de l'acte"]

        self.med = db.Medicaments
        self.table_med = self.get_medicament()
        self.DataTable_med = DataTable(table=self.table_med)
        self.l_past_med = []
        self.champs_med = ["ID_Médicament", "Nom du médicament", "Description du médicament",
                           "Dosage/forme du médicament",
                           'Stock disponible', "Fournisseur", "Date d'expiration"]

        self.paie = db.Paiements
        self.table_paie = self.get_paiement()
        self.DataTable_paie = DataTable(table=self.table_paie)
        self.l_past_paie = []
        self.champs_paie = ["ID_Transaction", "ID_Patient", 'ID_Acte','Seance', "Montant payé", 'Montant reste a payer',
                            'Date de la transaction',
                            'Mode de paiement', 'Statut de la transaction', 'Description de la transaction']

        self.signup = PatientApp()
        self.databasef = None
        patients = self.get_paiement()
        self.TD_paiements = DataTable(table=patients).table_data_array



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







    def on_cancelll(self,instance,time):

        if time==None:
            self.ids.text4_rdv.text=''

    def Time(self):
        cal_time=MDTimePicker()
        default_time=datetime.strptime("10:00:00",'%H:%M:%S')
        cal_time.set_time(default_time)
        self.ids.text4_rdv.text = '10:00:00'
        cal_time.bind(on_cancel=self.on_cancelll,time=self.on_save_time)
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




                        elif value.strftime("%Y-%m-%d")<date.today().strftime("%Y-%m-%d"):
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
            print(type(user['Heure']))
            confirm_dialog = MDDialog(
                text=f"Are you sure you want to select {str(value)}?",
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








    def on_confirm(self, value, dialog):
        # Perform desired action with selected date
        self.date=value.strftime("%Y-%m-%d")
        self.ids.text3_rdv.text = str(value)
        print(self.date)
        dialog.dismiss()


    def on_save_time(self,instance,time):
        current_time = datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute
        print(time)
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
                        print(user['Date'],self.date,user['Heure'],time.strftime('%H:%M:%S'))

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
        self.ids.text4_rdv.text = str(time)
        dialog.dismiss()

    def update_second_text(self, instance):
        self.ids.text4_p.text = instance.text

    def update_third_text(self, instance):
        self.ids.text3_p.text = instance.text

    def check_inputsy(self):
        print('adam')
        montant_paye = self.ids.text4_p.text.strip()
        id_acte = self.ids.text3_p.text.strip()
        montant_restant=self.ids.text5_p.text
        print(montant_paye)
        print(type(id_acte))
        client=MongoClient()
        db=client['Admin_cabinet']
        col=db['Actes']
        for user in col.find():
            print(type(user['ID_Acte']))
            if user['ID_Acte']==id_acte:
                if montant_paye and id_acte:
                    try:
                        montant_restant = int(user["Coût de l'acte"]) - int(montant_paye)
                        self.ids.text5_p.text = str(montant_restant)
                    except ValueError:
                        # Handle the case when the input values cannot be converted to integers
                        self.ids.text5_p.text = ""
                else:
                    # Clear the text field if any of the input fields are empty
                    self.ids.text5_p.text = ""













    def switch_to_screen(self,name):
        if name=='display_rendez_vous':
            self.ids.scm_cases.current='display_RDV_cases'
            self.ids.scm.current='display_rendez_vous'
            self.ids.scm_button_cases.current = 'display_rdv_button_cases'
            self.ids.lp.text = "Listes des rendez-vous:"


        elif name=='display_patients':
            self.ids.scm.current ='display_patients'
            self.ids.scm_cases.current = 'display_patients_cases'
            self.ids.scm_button_cases.current = 'display_patients_button_cases'
            self.ids.lp.text = "Listes des patients:"
        elif name=='display_visites':
            self.ids.scm.current ='display_visite'
            self.ids.scm_cases.current = 'display_visite_cases'
            self.ids.scm_button_cases.current = 'display_vst_button_cases'
            self.ids.lp.text = "Listes des visites:"
        elif name=='display_salle':
            self.ids.scm.current ='display_salle'
            self.ids.scm_cases.current = 'display_salle_cases'
            self.ids.scm_button_cases.current = 'display_salle_button_cases'
            self.ids.lp.text = "Listes des reflets de la salle:"
        elif name=='display_presc':
            self.ids.scm.current ='display_presc'
            self.ids.scm_cases.current = 'display_presc_cases'
            self.ids.scm_button_cases.current = 'display_prescription_button_cases'
            self.ids.lp.text = "Listes des prescriptions:"
        elif name=='display_actes':
            self.ids.scm.current ='display_actes'
            self.ids.scm_cases.current = 'display_actes_cases'
            self.ids.scm_button_cases.current = 'display_actes_button_cases'
            self.ids.lp.text = "Listes des actes:"
        elif name=='display_med':
            self.ids.scm.current ='display_med'
            self.ids.scm_cases.current = 'display_med_cases'
            self.ids.scm_button_cases.current = 'display_med_button_cases'
            self.ids.lp.text = "Listes des medicaments:"
        elif name=='display_paiement':
            self.ids.scm.current ='display_paiement'
            self.ids.scm_cases.current = 'display_paiement_cases'
            self.ids.scm_button_cases.current = 'display_pmt_button_cases'
            self.ids.lp.text = "Listes des paiements:"



    def get_patients(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Patients
        _users = OrderedDict(ID_Patients={},Noms={}, Prenoms={}, Dates_de_naissance={}, Telephones={},Adresses={},Antecedents_medicaux={},Emails={},Assurances={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]
        email=[]
        pt=[]
        assu=[]
        for user in users.find():
            Noms.append(user['Nom'])
            Prenoms.append(user['Prenom'])
            Dates_de_naissance.append(user['Date de naissance'])
            Telephones.append(user['Telephone'])
            Adresse.append(user['Adresse'])
            Ant.append(user['Antecedents medicaux'])
            email.append(user['Email'])
            pt.append(user['ID_Patient'])
            assu.append(user['Assurance'])
        users_length = len(Noms)
        iteration = 0
        while iteration < users_length:
            _users['Noms'][iteration] = Noms[iteration]
            _users['Prenoms'][iteration] = Prenoms[iteration]
            _users['Dates_de_naissance'][iteration] = Dates_de_naissance[iteration]
            _users['Telephones'][iteration] = Telephones[iteration]
            _users['Adresses'][iteration] = Adresse[iteration]
            _users['Antecedents_medicaux'][iteration] = Ant[iteration]
            _users['Emails'][iteration] = email[iteration]
            _users['ID_Patients'][iteration] = pt[iteration]
            _users['Assurances'][iteration] = assu[iteration]
            iteration += 1

        return (_users)




    def get_rendez_vous(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Rendez_vous
        _rdv = OrderedDict(ID_Rendez_vous={},ID_Patients={},Dates_RDV={}, Heures_RDV={}, Nom_Actes={}, Statuts_RDV={},Notes_Supp={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        traitement=[]
        statut=[]
        notes=[]

        for user in users.find():
            Prenoms.append(user['ID_Patient'])
            Dates_de_naissance.append(user["Date"])
            Telephones.append(user['Heure'])
            traitement.append(user['Nom_Acte'])
            statut.append(user["Statut du rendez-vous"])
            notes.append(user["Notes ou instructions supplémentaires"])
            Noms.append(user['ID_Rendez_vous'])
        users_length = len(Noms)
        iteration = 0
        while iteration < users_length:
            _rdv['ID_Rendez_vous'][iteration] = Noms[iteration]
            _rdv['ID_Patients'][iteration] = Prenoms[iteration]
            _rdv['Dates_RDV'][iteration] = Dates_de_naissance[iteration]
            _rdv['Heures_RDV'][iteration] = Telephones[iteration]
            _rdv['Nom_Actes'][iteration] = traitement[iteration]
            _rdv['Statuts_RDV'][iteration] = statut[iteration]
            _rdv['Notes_Supp'][iteration] = notes[iteration]
            iteration += 1

        return (_rdv)


    def get_visites(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Visite_de_la_journee
        _users = OrderedDict(ID_Visites={},ID_Patients={}, Date_visites={}, Heure_visites={}, Nom_Actes={},Seances={},Notes_ou_remarques_supplémentaires={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]
        seance = []

        for user in users.find():
            Noms.append(user['ID_Visite'])
            Prenoms.append(user['ID_Patient'])
            Dates_de_naissance.append(user['Date de la visite'])
            Telephones.append(user['Heure de la visite'])
            Adresse.append(user['Nom_Acte'])
            Ant.append(user['Notes ou remarques supplémentaires'])
            seance.append(user['Seance'])

        users_length = len(Noms)
        print(Noms)
        iteration = 0
        while iteration < users_length:
            _users['ID_Visites'][iteration] = Noms[iteration]
            _users['ID_Patients'][iteration] = Prenoms[iteration]
            _users['Date_visites'][iteration] = Dates_de_naissance[iteration]
            _users['Heure_visites'][iteration] = Telephones[iteration]
            _users['Nom_Actes'][iteration] = Adresse[iteration]
            _users['Notes_ou_remarques_supplémentaires'][iteration] = Ant[iteration]
            _users['Seances'][iteration] = seance[iteration]
            iteration += 1

        return (_users)

    def get_salle(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Reflet_salle
        _users = OrderedDict(ID_de_Reflet={},Date_de_Reflet={}, Heure_de_Reflet={}, Nombre_patient_en_attente={}, Statut_patients={},Remarques_ou_informations_supplémentaires={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]

        for user in users.find():
            Noms.append(user["ID_Reflet"])
            Prenoms.append(user["Date du reflet"])
            Dates_de_naissance.append(user[" Heure du reflet"])
            Telephones.append(user["Nombre de patients en attente"])
            Adresse.append(user["Statut des patients"])
            Ant.append(user['Remarques ou informations supplémentaires'])

        users_length = len(Noms)
        print(Noms)
        iteration = 0
        while iteration < users_length:
            _users['ID_de_Reflet'][iteration] = Noms[iteration]
            _users['Date_de_Reflet'][iteration] = Prenoms[iteration]
            _users['Heure_de_Reflet'][iteration] = Dates_de_naissance[iteration]
            _users['Nombre_patient_en_attente'][iteration] = Telephones[iteration]
            _users['Statut_patients'][iteration] = Adresse[iteration]
            _users['Remarques_ou_informations_supplémentaires'][iteration] = Ant[iteration]
            iteration += 1

        return (_users)

    def get_prescription(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Prescriptions
        _users = OrderedDict(ID_Prescription={},ID_Patients={}, Noms_Medicaments={}, Psologies={}, Duree_des_prescriptions={},Statut_prescriptions={},Notes_supplementaires={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]
        notes=[]

        for user in users.find():
            Noms.append(user["ID_Prescription"])
            Prenoms.append(user["ID_Patient"])
            Dates_de_naissance.append(user["Nom du medicament"])
            Telephones.append(user["Posologie"])
            Adresse.append(user["Durée de la prescription"])
            Ant.append(user['Statut de la prescription'])
            notes.append(user['Notes supplémentaires'])

        users_length = len(Noms)
        print(Noms)
        iteration = 0
        while iteration < users_length:
            _users['ID_Prescription'][iteration] = Noms[iteration]
            _users['ID_Patients'][iteration] = Prenoms[iteration]
            _users['Noms_Medicaments'][iteration] = Dates_de_naissance[iteration]
            _users['Psologies'][iteration] = Telephones[iteration]
            _users['Duree_des_prescriptions'][iteration] = Adresse[iteration]
            _users['Statut_prescriptions'][iteration] = Ant[iteration]
            _users['Notes_supplementaires'][iteration] = notes[iteration]
            iteration += 1

        return (_users)


    def get_actes(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Actes
        _users = OrderedDict(ID_Actes={},Noms_Actes={}, Coûts_Actes={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []

        for user in users.find():
            Noms.append(user["ID_Acte"])
            Prenoms.append(user["Nom_Acte"])
            Telephones.append(user["Coût de l'acte"])

        users_length = len(Noms)

        iteration = 0
        while iteration < users_length:
            _users['ID_Actes'][iteration] = Noms[iteration]
            _users['Noms_Actes'][iteration] = Prenoms[iteration]
            _users['Coûts_Actes'][iteration] = Telephones[iteration]
            iteration += 1

        return (_users)

    def get_medicament(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Medicaments
        _users = OrderedDict(ID_Médicaments={},Nom_Médicaments={}, Description_des_médicaments={}, Dosage_médicaments={}, Stock_disponible={},Fournisseurs={},Dates_expiration={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]
        notes=[]

        for user in users.find():
            Noms.append(user["ID_Médicament"])
            Prenoms.append(user["Nom du médicament"])
            Dates_de_naissance.append(user["Description du médicament"])
            Telephones.append(user["Dosage/forme du médicament"])
            Adresse.append(user["Stock disponible"])
            Ant.append(user["Fournisseur"])
            notes.append(user["Date d'expiration"])

        users_length = len(Noms)

        iteration = 0
        while iteration < users_length:

            _users['ID_Médicaments'][iteration] = Noms[iteration]
            _users['Nom_Médicaments'][iteration] = Prenoms[iteration]
            _users['Description_des_médicaments'][iteration] = Dates_de_naissance[iteration]
            _users['Dosage_médicaments'][iteration] = Telephones[iteration]
            _users['Stock_disponible'][iteration] = Adresse[iteration]
            _users['Dates_expiration'][iteration] = notes[iteration]
            _users['Fournisseurs'][iteration] = Ant[iteration]
            iteration += 1

        return (_users)
    def get_paiement(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Paiements
        _users = OrderedDict(ID_Transaction={},ID_Patients={}, ID_Actes={},Seances={} ,Montant_payé={}, Montant_reste_a_payer={},Modes_Paiements={},Dates_transaction={},Statut_transaction={},Description_transaction={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]
        tr=[]
        dtr=[]
        notes=[]
        seance = []
        for user in users.find():
            Noms.append(user["ID_Transaction"])
            Prenoms.append(user["ID_Patient"])
            notes.append(user["ID_Acte"])
            Dates_de_naissance.append(user["Montant payé"])
            Telephones.append(user["Montant reste a payer"])
            Adresse.append(user["Date de la transaction"])
            Ant.append(user["Mode de paiement"])
            tr.append(user["Statut de la transaction"])
            dtr.append(user["Description de la transaction"])
            seance.append(user['Seance'])


        users_length = len(Noms)

        iteration = 0
        while iteration < users_length:

            _users['ID_Transaction'][iteration] = Noms[iteration]
            _users['ID_Patients'][iteration] = Prenoms[iteration]
            _users['ID_Actes'][iteration] = notes[iteration]
            _users['Montant_payé'][iteration] = Dates_de_naissance[iteration]
            _users['Montant_reste_a_payer'][iteration] = Telephones[iteration]
            _users['Modes_Paiements'][iteration] = Ant[iteration]
            _users['Dates_transaction'][iteration] = Adresse[iteration]
            _users['Statut_transaction'][iteration] = tr[iteration]
            _users['Description_transaction'][iteration] = dtr[iteration]
            _users['Seances'][iteration] = seance[iteration]
            iteration += 1

        return (_users)


    def on_button_click_table(self,button):
        self.row_id=int(button.id)+1
        print(self.row_id)
        screen=self.ids.scm_cases
        l = []
        rdv = []
        visite=[]
        salle=[]
        if screen.current=='display_patients_cases':
            try:
                patients=self.get_patients()
                self.TD_patients = DataTable(table=patients).table_data_array

                for i in self.TD_patients[self.row_id]:
                    l.append(i['text'])
                self.ids.text1.text = l[0]
                self.ids.text2.text = l[1]
                self.ids.text3.text = l[2]
                self.ids.text4.text = l[3]
                self.ids.text5.text = l[4]
                self.ids.text6.text = l[5]
                self.ids.text7.text = l[6]
                self.ids.text8.text = l[7]
                self.ids.text9.text = l[8]
                self.ids.text1.readonly = True
                self.ids.text2.readonly=True
                self.ids.text3.readonly = True
                self.ids.text4.readonly=True
                self.ids.text5.readonly = True
                self.ids.text6.readonly = True
                self.ids.text7.readonly = True
                self.ids.text8.readonly = True
                self.ids.text9.readonly = True
                l.clear()
            except Exception as e:
                pass
        elif screen.current=='display_RDV_cases':
            try:
                patients = self.get_rendez_vous()
                self.TD_rdv = DataTable(table=patients).table_data_array
                for i in self.TD_rdv[self.row_id]:
                    rdv.append(i['text'])
                self.ids.text1_rdv.text = rdv[0]
                self.ids.text2_rdv.text = rdv[1]
                self.ids.text3_rdv.text = rdv[2]
                self.ids.text4_rdv.text = rdv[3]
                self.ids.text5_rdv.text = rdv[4]
                self.ids.text6_rdv.text = rdv[5]
                self.ids.text7_rdv.text = rdv[6]
                self.ids.text1_rdv.readonly = True
                self.ids.text2_rdv.readonly = True
                self.ids.text3_rdv.readonly = True
                self.ids.text4_rdv.readonly = True
                self.ids.text5_rdv.readonly = True
                self.ids.text6_rdv.readonly = True
                self.ids.text7_rdv.readonly = True
                rdv.clear()
            except Exception as e:
                pass
        elif screen.current == 'display_visite_cases':
            try:
                patients = self.get_visites()
                self.TD_visite = DataTable(table=patients).table_data_array

                for i in self.TD_visite[self.row_id]:
                    visite.append(i['text'])
                self.ids.text1_visite.text = visite[0]
                self.ids.text2_visite.text = visite[1]
                self.ids.text3_visite.text = visite[2]
                self.ids.text4_visite.text = visite[3]
                self.ids.text5_visite.text = visite[4]
                self.ids.text6_visite.text = visite[6]
                self.ids.text7_visite.text = visite[5]
                self.ids.text1_visite.readonly = True
                self.ids.text2_visite.readonly = True
                self.ids.text3_visite.readonly = True
                self.ids.text4_visite.readonly = True
                self.ids.text5_visite.readonly = True
                self.ids.text6_visite.readonly = True
                self.ids.text7_visite.readonly = True
                visite.clear()
            except Exception as e:
                pass
        elif screen.current=='display_salle_cases':
            try:
                patients = self.get_salle()
                self.TD_salle = DataTable(table=patients).table_data_array

                for i in self.TD_salle[self.row_id]:
                    salle.append(i['text'])
                self.ids.text1_salle.text = salle[0]
                self.ids.text2_salle.text = salle[1]
                self.ids.text3_salle.text = salle[2]
                self.ids.text4_salle.text = salle[3]
                self.ids.text5_salle.text = salle[4]
                self.ids.text6_salle.text = salle[5]
                self.ids.text1_salle.readonly = True
                self.ids.text2_salle.readonly=True
                self.ids.text3_salle.readonly = True
                self.ids.text4_salle.readonly=True
                self.ids.text5_salle.readonly = True
                self.ids.text6_salle.readonly = True
                salle.clear()
            except Exception as e:
                pass
        elif screen.current=='display_presc_cases':
            try:
                patients = self.get_prescription()
                self.TD_presc = DataTable(table=patients).table_data_array

                for i in self.TD_presc[self.row_id]:
                    salle.append(i['text'])
                self.ids.text1_presc.text = salle[0]
                self.ids.text2_presc.text = salle[1]
                self.ids.text3_presc.text = salle[2]
                self.ids.text4_presc.text = salle[3]
                self.ids.text5_presc.text = salle[4]
                self.ids.text6_presc.text = salle[5]
                self.ids.text7_presc.text = salle[6]
                self.ids.text1_presc.readonly = True
                self.ids.text2_presc.readonly=True
                self.ids.text3_presc.readonly = True
                self.ids.text4_presc.readonly=True
                self.ids.text5_presc.readonly = True
                self.ids.text6_presc.readonly = True
                self.ids.text7_presc.readonly = True
                salle.clear()
            except Exception as e:
                pass


        elif screen.current=='display_actes_cases':
            try:
                patients = self.get_actes()
                self.TD_actes = DataTable(table=patients).table_data_array

                for i in self.TD_actes[self.row_id]:
                    salle.append(i['text'])
                self.ids.text1_actes.text = salle[0]
                self.ids.text2_actes.text = salle[1]
                self.ids.text4_actes.text = salle[2]
                self.ids.text1_actes.readonly = True
                self.ids.text2_actes.readonly=True
                self.ids.text4_actes.readonly=True
                salle.clear()
            except Exception as e:
                pass
        elif screen.current=='display_med_cases':
            try:
                patients = self.get_medicament()
                self.TD_med = DataTable(table=patients).table_data_array

                for i in self.TD_med[self.row_id]:
                    salle.append(i['text'])
                self.ids.text1_med.text = salle[0]
                self.ids.text2_med.text = salle[1]
                self.ids.text3_med.text = salle[2]
                self.ids.text4_med.text = salle[3]
                self.ids.text5_med.text = salle[4]
                self.ids.text6_med.text = salle[5]
                self.ids.text7_med.text = salle[6]
                self.ids.text1_med.readonly = True
                self.ids.text2_med.readonly=True
                self.ids.text3_med.readonly = True
                self.ids.text4_med.readonly=True
                self.ids.text5_med.readonly = True
                self.ids.text6_med.readonly = True
                self.ids.text7_med.readonly = True
                salle.clear()
            except Exception as e:
                pass
        if screen.current=='display_paiement_cases':
            try:
                patients=self.get_paiement()
                self.TD_paiements = DataTable(table=patients).table_data_array

                for i in self.TD_paiements[self.row_id]:
                    l.append(i['text'])
                self.ids.text1_p.text = l[0]
                self.ids.text2_p.text = l[1]
                self.ids.text3_p.text = l[2]
                self.ids.text4_p.text = l[4]
                self.ids.text5_p.text = l[5]
                self.ids.text6_p.text = l[6]
                self.ids.text7_p.text = l[7]
                self.ids.text8_p.text = l[8]
                self.ids.text9_p.text = l[9]
                self.ids.text10_p.text = l[3]
                self.ids.text1_p.readonly = True
                self.ids.text2_p.readonly=True
                self.ids.text3_p.readonly = True
                self.ids.text4_p.readonly=True
                self.ids.text5_p.readonly = True
                self.ids.text6_p.readonly = True
                self.ids.text7_p.readonly = True
                self.ids.text8_p.readonly = True
                self.ids.text9_p.readonly = True
                self.ids.text10_p.readonly = True
                l.clear()
            except Exception as e:
                pass


    def delete_table(self):
        screen = self.ids.scm_cases
        if screen.current == 'display_patients_cases':
            self.ids.text1.readonly = True
            self.ids.text2.readonly = True
            self.ids.text3.readonly = True
            self.ids.text4.readonly = True
            self.ids.text5.readonly = True
            self.ids.text6.readonly = True
            self.ids.text7.readonly = True
            self.ids.text8.readonly = True
            self.ids.text9.readonly = True
            confirm_dialog = MDDialog(
                text=f"Voulez-vous supprimer ce patient?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm_table(confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()
        elif screen.current == 'display_RDV_cases':
            self.ids.text1_rdv.readonly = True
            self.ids.text2_rdv.readonly = True
            self.ids.text3_rdv.readonly = True
            self.ids.text4_rdv.readonly = True
            self.ids.text5_rdv.readonly = True
            self.ids.text6_rdv.readonly = True
            self.ids.text7_rdv.readonly = True
            confirm_dialog = MDDialog(
                text=f"Voulez-vous supprimer ce rendz-vous?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm_table(confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()
        elif screen.current == 'display_visite_cases':
            self.ids.text1_visite.readonly = True
            self.ids.text2_visite.readonly = True
            self.ids.text3_visite.readonly = True
            self.ids.text4_visite.readonly = True
            self.ids.text5_visite.readonly = True
            self.ids.text6_visite.readonly = True
            self.ids.text7_visite.readonly = True
            confirm_dialog = MDDialog(
                text=f"Voulez-vous supprimer cette visite?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm_table(confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()
        elif screen.current == 'display_salle_cases':
            self.ids.text1_salle.readonly = True
            self.ids.text2_salle.readonly = True
            self.ids.text3_salle.readonly = True
            self.ids.text4_salle.readonly = True
            self.ids.text5_salle.readonly = True
            self.ids.text6_salle.readonly = True
            confirm_dialog = MDDialog(
                text=f"Voulez-vous supprimer cet reflet de la salle?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm_table(confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()

        elif screen.current == 'display_presc_cases':
            self.ids.text1_presc.readonly = True
            self.ids.text2_presc.readonly = True
            self.ids.text3_presc.readonly = True
            self.ids.text4_presc.readonly = True
            self.ids.text5_presc.readonly = True
            self.ids.text6_presc.readonly = True
            self.ids.text7_presc.readonly = True
            confirm_dialog = MDDialog(
                text=f"Voulez-vous supprimer cette prescription?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm_table(confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()
        elif screen.current == 'display_actes_cases':
            self.ids.text1_actes.readonly = True
            self.ids.text2_actes.readonly = True
            self.ids.text4_actes.readonly = True
            confirm_dialog = MDDialog(
                text=f"Voulez-vous supprimer cette acte?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm_table(confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()


        elif screen.current == 'display_med_cases':
            self.ids.text1_med.readonly = True
            self.ids.text2_med.readonly = True
            self.ids.text3_med.readonly = True
            self.ids.text4_med.readonly = True
            self.ids.text5_med.readonly = True
            self.ids.text6_med.readonly = True
            self.ids.text7_med.readonly = True
            confirm_dialog = MDDialog(
                text=f"Voulez-vous supprimer ce medicament?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm_table(confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()
        elif screen.current == 'display_paiement_cases':
            self.ids.text1_p.readonly = True
            self.ids.text2_p.readonly = True
            self.ids.text3_p.readonly = True
            self.ids.text4_p.readonly = True
            self.ids.text5_p.readonly = True
            self.ids.text6_p.readonly = True
            self.ids.text7_p.readonly = True
            self.ids.text8_p.readonly = True
            self.ids.text9_p.readonly = True
            self.ids.text10_p.readonly = True
            confirm_dialog = MDDialog(
                text=f"Voulez-vous supprimer cette transaction?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm_table(confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()

    def on_confirm_table(self,dialog):
        j=0
        screen = self.ids.scm_cases
        if screen.current == 'display_patients_cases':
            dialog.dismiss()
            self.ids.text1.text=''
            self.ids.text2.text=''
            self.ids.text3.text=''
            self.ids.text4.text = ''
            self.ids.text5.text = ''
            self.ids.text6.text = ''
            self.ids.text7.text = ''
            self.ids.text8.text = ''
            self.ids.text9.text = ''

            document = self.patients.find().skip(self.row_id - 1).limit(1)[0]
            self.patients.delete_one({"_id": document["_id"]})

            self.ids.display_patients.clear_widgets()
            patients = self.get_patients()
            patientstable = DataTable(table=patients)
            content = self.ids.display_patients
            content.add_widget(patientstable)
            self.ids.text1.readonly = False
            self.ids.text2.readonly = False
            self.ids.text3.readonly = False
            self.ids.text4.readonly = False
            self.ids.text5.readonly = False
            self.ids.text6.readonly = False
            self.ids.text7.readonly = False
            self.ids.text8.readonly = False
            self.ids.text9.readonly = False
        elif screen.current == 'display_RDV_cases':
            dialog.dismiss()
            self.ids.text1_rdv.text = ''
            self.ids.text2_rdv.text = ''
            self.ids.text3_rdv.text = ''
            self.ids.text4_rdv.text = ''
            self.ids.text5_rdv.text = ''
            self.ids.text6_rdv.text = ''
            self.ids.text7_rdv.text = ''
            document = self.rdvs.find().skip(self.row_id - 1).limit(1)[0]
            self.rdvs.delete_one({"_id": document["_id"]})

            self.ids.display_rendez_vous.clear_widgets()
            rdvs = self.get_rendez_vous()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_rendez_vous
            content.add_widget(rdvstable)
            self.ids.text1_rdv.readonly = False
            self.ids.text2_rdv.readonly = False
            self.ids.text3_rdv.readonly = False
            self.ids.text4_rdv.readonly = False
            self.ids.text5_rdv.readonly = False
            self.ids.text6_rdv.readonly = False
            self.ids.text7_rdv.readonly = False

        elif screen.current == 'display_visite_cases':
            dialog.dismiss()
            self.ids.text1_visite.text = ''
            self.ids.text2_visite.text = ''
            self.ids.text3_visite.text = ''
            self.ids.text4_visite.text = ''
            self.ids.text5_visite.text = ''
            self.ids.text6_visite.text = ''
            self.ids.text7_visite.text = ''
            document = self.visites.find().skip(self.row_id - 1).limit(1)[0]
            self.visites.delete_one({"_id": document["_id"]})

            self.ids.display_visite.clear_widgets()
            rdvs = self.get_visites()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_visite
            content.add_widget(rdvstable)
            self.ids.text1_visite.readonly = False
            self.ids.text2_visite.readonly = False
            self.ids.text3_visite.readonly = False
            self.ids.text4_visite.readonly = False
            self.ids.text5_visite.readonly = False
            self.ids.text6_visite.readonly = False
            self.ids.text7_visite.readonly = False
        elif screen.current == 'display_salle_cases':
            dialog.dismiss()
            self.ids.text1_salle.text = ''
            self.ids.text2_salle.text = ''
            self.ids.text3_salle.text = ''
            self.ids.text4_salle.text = ''
            self.ids.text5_salle.text = ''
            self.ids.text6_salle.text = ''
            document = self.salle.find().skip(self.row_id - 1).limit(1)[0]
            self.salle.delete_one({"_id": document["_id"]})

            self.ids.display_salle.clear_widgets()
            rdvs = self.get_salle()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_salle
            content.add_widget(rdvstable)
            self.ids.text1_salle.readonly = False
            self.ids.text2_salle.readonly = False
            self.ids.text3_salle.readonly = False
            self.ids.text4_salle.readonly = False
            self.ids.text5_salle.readonly = False
            self.ids.text6_salle.readonly = False
        elif screen.current == 'display_presc_cases':
            dialog.dismiss()
            self.ids.text1_presc.text = ''
            self.ids.text2_presc.text = ''
            self.ids.text3_presc.text = ''
            self.ids.text4_presc.text = ''
            self.ids.text5_presc.text = ''
            self.ids.text6_presc.text = ''
            self.ids.text7_presc.text = ''
            document = self.presc.find().skip(self.row_id - 1).limit(1)[0]
            self.presc.delete_one({"_id": document["_id"]})

            self.ids.display_presc.clear_widgets()
            rdvs = self.get_prescription()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_presc
            content.add_widget(rdvstable)
            self.ids.text1_presc.readonly = False
            self.ids.text2_presc.readonly = False
            self.ids.text3_presc.readonly = False
            self.ids.text4_presc.readonly = False
            self.ids.text5_presc.readonly = False
            self.ids.text6_presc.readonly = False
            self.ids.text7_presc.readonly = False

        elif screen.current == 'display_actes_cases':
            dialog.dismiss()
            self.ids.text1_actes.text = ''
            self.ids.text2_actes.text = ''
            self.ids.text4_actes.text = ''
            document = self.actes.find().skip(self.row_id - 1).limit(1)[0]
            self.actes.delete_one({"_id": document["_id"]})

            self.ids.display_actes.clear_widgets()
            rdvs = self.get_actes()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_actes
            content.add_widget(rdvstable)
            self.ids.text1_actes.readonly = False
            self.ids.text2_actes.readonly = False

            self.ids.text4_actes.readonly = False

        elif screen.current == 'display_med_cases':
            dialog.dismiss()
            self.ids.text1_med.text = ''
            self.ids.text2_med.text = ''
            self.ids.text3_med.text = ''
            self.ids.text4_med.text = ''
            self.ids.text5_med.text = ''
            self.ids.text6_med.text = ''
            self.ids.text7_med.text = ''
            document = self.med.find().skip(self.row_id - 1).limit(1)[0]
            self.med.delete_one({"_id": document["_id"]})

            self.ids.display_med.clear_widgets()
            rdvs = self.get_medicament()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_med
            content.add_widget(rdvstable)
            self.ids.text1_med.readonly = False
            self.ids.text2_med.readonly = False
            self.ids.text3_med.readonly = False
            self.ids.text4_med.readonly = False
            self.ids.text5_med.readonly = False
            self.ids.text6_med.readonly = False
            self.ids.text7_med.readonly = False

        if screen.current == 'display_paiement_cases':
            dialog.dismiss()
            self.ids.text1_p.text=''
            self.ids.text2_p.text=''
            self.ids.text3_p.text=''
            self.ids.text4_p.text = ''
            self.ids.text5_p.text = ''
            self.ids.text6_p.text = ''
            self.ids.text7_p.text = ''
            self.ids.text8_p.text = ''
            self.ids.text9_p.text = ''
            self.ids.text10_p.text = ''

            document = self.paie.find().skip(self.row_id - 1).limit(1)[0]
            self.paie.delete_one({"_id": document["_id"]})

            self.ids.display_paiement.clear_widgets()
            patients = self.get_paiement()
            patientstable = DataTable(table=patients)
            content = self.ids.display_paiement
            content.add_widget(patientstable)
            self.ids.text1_p.readonly = False
            self.ids.text2_p.readonly = False
            self.ids.text3_p.readonly = False
            self.ids.text4_p.readonly = False
            self.ids.text5_p.readonly = False
            self.ids.text6_p.readonly = False
            self.ids.text7_p.readonly = False
            self.ids.text8_p.readonly = False
            self.ids.text9_p.readonly = False
            self.ids.text10_p.readonly = False

    def add_table(self):
        self.previous_action = 'add'
        screen = self.ids.scm_cases
        if screen.current == 'display_patients_cases':
            try:
                i = -1
                j = -2
                k = 1
                d = 1
                app = App.get_running_app()
                patients = self.get_patients()
                last_ele = list(patients.items())[0]
                print(last_ele)
                p = (last_ele[1])
                new_string = 'P000'
                if not p:
                    self.ids.text1_p.text = 'P000'

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
            except Exception as e:
                pass
            self.ids.text1.text = new_string
            self.ids.text2.text = ''
            self.ids.text3.text = ''
            self.ids.text4.text = ''
            self.ids.text5.text = ''
            self.ids.text6.text = ''
            self.ids.text7.text = ''
            self.ids.text8.text = ''
            self.ids.text9.text=''
            self.ids.text1.readonly = False
            self.ids.text2.readonly = False
            self.ids.text3.readonly = False
            self.ids.text4.readonly = False
            self.ids.text5.readonly = False
            self.ids.text6.readonly = False
            self.ids.text7.readonly = False
            self.ids.text8.readonly = False
            self.ids.text9.readonly = False


        elif screen.current == 'display_RDV_cases':
            try:
                i = -1
                j = -2
                k = 1
                d = 1
                app = App.get_running_app()
                patients = self.get_rendez_vous()
                last_ele = list(patients.items())[0]
                print(last_ele)
                p = (last_ele[1])
                new_string = 'RDV000'
                if not p:
                    self.ids.text1_rdv.text = 'RDV000'

                else:
                    pp = list(p.values())[-1]
                    if int(pp[-1]) == 9:
                        pp = 'RDV0' + str(k + 9)
                        k += 1
                    if int(pp[-2:]) == 99:
                        pp = 'RDV' + str(d + 99)
                        d += 1
                    num = int(pp[-1]) + 1
                    string_list = list(pp)
                    string_list[-1] = str(num)
                    new_string = ''.join(string_list)
            except Exception as e:
                pass


            self.ids.text1_rdv.text = new_string
            self.ids.text2_rdv.text = ''
            self.ids.text3_rdv.text = ''
            self.ids.text4_rdv.text = ''
            self.ids.text5_rdv.text = ''
            self.ids.text6_rdv.text = ''
            self.ids.text7_rdv.text = ''
            self.ids.text1_rdv.readonly = False
            self.ids.text2_rdv.readonly = False
            self.ids.text3_rdv.readonly = False
            self.ids.text4_rdv.readonly = False
            self.ids.text5_rdv.readonly = False
            self.ids.text6_rdv.readonly = False
            self.ids.text7_rdv.readonly = False

        elif screen.current == 'display_visite_cases':
            try:
                i = -1
                j = -2
                k = 1
                d = 1
                app = App.get_running_app()
                patients = self.get_visites()
                last_ele = list(patients.items())[0]
                print(last_ele)
                p = (last_ele[1])
                new_string = 'VST000'
                if not p:
                    self.ids.text1_p.text = 'VST000'

                else:
                    pp = list(p.values())[-1]
                    if int(pp[-1]) == 9:
                        pp = 'VST0' + str(k + 9)
                        k += 1
                    if int(pp[-2:]) == 99:
                        pp = 'VST' + str(d + 99)
                        d += 1
                    num = int(pp[-1]) + 1
                    string_list = list(pp)
                    string_list[-1] = str(num)
                    new_string = ''.join(string_list)
            except Exception as e:
                pass
            self.ids.text1_visite.text = new_string
            self.ids.text2_visite.text = ''
            self.ids.text3_visite.text = ''
            self.ids.text4_visite.text = ''
            self.ids.text5_visite.text = ''
            self.ids.text6_visite.text = ''
            self.ids.text7_visite.text = ''
            self.ids.text1_visite.readonly = False
            self.ids.text2_visite.readonly = False
            self.ids.text3_visite.readonly = False
            self.ids.text4_visite.readonly = False
            self.ids.text5_visite.readonly = False
            self.ids.text6_visite.readonly = False
            self.ids.text7_visite.readonly = False

        elif screen.current == 'display_salle_cases':
            try:
                i = -1
                j = -2
                k = 1
                d = 1
                app = App.get_running_app()
                patients = self.get_salle()
                last_ele = list(patients.items())[0]
                print(last_ele)
                p = (last_ele[1])
                new_string = 'SALLE000'
                if not p:
                    self.ids.text1_p.text = 'SALLE000'

                else:
                    pp = list(p.values())[-1]
                    if int(pp[-1]) == 9:
                        pp = 'SALLE0' + str(k + 9)
                        k += 1
                    if int(pp[-2:]) == 99:
                        pp = 'SALLE' + str(d + 99)
                        d += 1
                    num = int(pp[-1]) + 1
                    string_list = list(pp)
                    string_list[-1] = str(num)
                    new_string = ''.join(string_list)
            except Exception as e:
                pass
            self.ids.text1_salle.text = new_string
            self.ids.text2_salle.text = ''
            self.ids.text3_salle.text = ''
            self.ids.text4_salle.text = ''
            self.ids.text5_salle.text = ''
            self.ids.text6_salle.text = ''
            self.ids.text1_salle.readonly = False
            self.ids.text2_salle.readonly = False
            self.ids.text3_salle.readonly = False
            self.ids.text4_salle.readonly = False
            self.ids.text5_salle.readonly = False
            self.ids.text6_salle.readonly = False

        elif screen.current == 'display_presc_cases':
            try:
                i = -1
                j = -2
                k = 1
                d = 1
                app = App.get_running_app()
                patients = self.get_prescription()
                last_ele = list(patients.items())[0]
                print(last_ele)
                p = (last_ele[1])
                new_string = 'Presc000'
                if not p:
                    self.ids.text1_p.text = 'Presc000'

                else:
                    pp = list(p.values())[-1]
                    if int(pp[-1]) == 9:
                        pp = 'PRESC0' + str(k + 9)
                        k += 1
                    if int(pp[-2:]) == 99:
                        pp = 'PRESC' + str(d + 99)
                        d += 1
                    num = int(pp[-1]) + 1
                    string_list = list(pp)
                    string_list[-1] = str(num)
                    new_string = ''.join(string_list)
            except Exception as e:
                pass
            self.ids.text1_presc.text = new_string
            self.ids.text2_presc.text = ''
            self.ids.text3_presc.text = ''
            self.ids.text4_presc.text = ''
            self.ids.text5_presc.text = ''
            self.ids.text6_presc.text = ''
            self.ids.text7_presc.text = ''
            self.ids.text1_presc.readonly = False
            self.ids.text2_presc.readonly = False
            self.ids.text3_presc.readonly = False
            self.ids.text4_presc.readonly = False
            self.ids.text5_presc.readonly = False
            self.ids.text6_presc.readonly = False
            self.ids.text7_presc.readonly = False

        elif screen.current == 'display_actes_cases':
            try:
                i = -1
                j = -2
                k = 1
                d = 1
                app = App.get_running_app()
                patients = self.get_actes()
                last_ele = list(patients.items())[0]
                print(last_ele)
                p = (last_ele[1])
                new_string = 'ACT000'
                if not p:
                    self.ids.text1_p.text = 'ACT000'

                else:
                    pp = list(p.values())[-1]
                    if int(pp[-1]) == 9:
                        pp = 'ACT0' + str(k + 9)
                        k += 1
                    if int(pp[-2:]) == 99:
                        pp = 'ACT' + str(d + 99)
                        d += 1
                    num = int(pp[-1]) + 1
                    string_list = list(pp)
                    string_list[-1] = str(num)
                    new_string = ''.join(string_list)
            except Exception as e:
                pass
            self.ids.text1_actes.text = new_string
            self.ids.text2_actes.text = ''
            self.ids.text4_actes.text = ''
            self.ids.text1_actes.readonly = False
            self.ids.text2_actes.readonly = False
            self.ids.text4_actes.readonly = False

        elif screen.current == 'display_med_cases':
            try:
                i = -1
                j = -2
                k = 1
                d = 1
                app = App.get_running_app()
                patients = self.get_medicament()
                last_ele = list(patients.items())[0]
                print(last_ele)
                p = (last_ele[1])
                new_string = 'MED000'
                if not p:
                    self.ids.text1_p.text = 'MED000'

                else:
                    pp = list(p.values())[-1]
                    if int(pp[-1]) == 9:
                        pp = 'MED' + str(k + 9)
                        k += 1
                    if int(pp[-2:]) == 99:
                        pp = 'MED' + str(d + 99)
                        d += 1
                    num = int(pp[-1]) + 1
                    string_list = list(pp)
                    string_list[-1] = str(num)
                    new_string = ''.join(string_list)
            except Exception as e:
                pass
            self.ids.text1_med.text = new_string
            self.ids.text2_med.text = ''
            self.ids.text3_med.text = ''
            self.ids.text4_med.text = ''
            self.ids.text5_med.text = ''
            self.ids.text6_med.text = ''
            self.ids.text7_med.text = ''
            self.ids.text1_med.readonly = False
            self.ids.text2_med.readonly = False
            self.ids.text3_med.readonly = False
            self.ids.text4_med.readonly = False
            self.ids.text5_med.readonly = False
            self.ids.text6_med.readonly = False
            self.ids.text7_med.readonly = False


        if screen.current == 'display_paiement_cases':
            try:
                i = -1
                j = -2
                k = 1
                d = 1
                app = App.get_running_app()
                patients = self.get_paiement()
                last_ele = list(patients.items())[0]
                print(last_ele)
                p = (last_ele[1])
                new_string = 'Paiem000'
                if not p:
                    self.ids.text1_p.text = 'Paiem000'

                else:
                    pp = list(p.values())[-1]
                    if int(pp[-1]) == 9:
                        pp = 'Paiem0' + str(k + 9)
                        k += 1
                    if int(pp[-2:]) == 99:
                        pp = 'Paiem' + str(d + 99)
                        d += 1
                    num = int(pp[-1]) + 1
                    string_list = list(pp)
                    string_list[-1] = str(num)
                    new_string = ''.join(string_list)
            except Exception as e:
                pass
            self.ids.text1_p.text = new_string
            self.ids.text2_p.text = ''
            self.ids.text3_p.text = ''
            self.ids.text4_p.text = ''
            self.ids.text5_p.text = ''
            self.ids.text6_p.text = ''
            self.ids.text7_p.text = ''
            self.ids.text8_p.text = ''
            self.ids.text9_p.text=''
            self.ids.text10_p.text = ''
            self.ids.text1_p.readonly = False
            self.ids.text2_p.readonly = False
            self.ids.text3_p.readonly = False
            self.ids.text4_p.readonly = False
            self.ids.text5_p.readonly = False
            self.ids.text6_p.readonly = False
            self.ids.text7_p.readonly = False
            self.ids.text8_p.readonly = False
            self.ids.text9_p.readonly = False
            self.ids.text10_p.readonly = False




    previous_action = None
    def update_table(self):
        j=0
        self.previous_action = 'update'
        screen = self.ids.scm_cases
        if screen.current=='display_patients_cases':
            self.ids.text1.readonly=False
            self.ids.text2.readonly=False
            self.ids.text3.readonly=False
            self.ids.text4.readonly=False
            self.ids.text5.readonly = False
            self.ids.text6.readonly = False
            self.ids.text7.readonly = False
            self.ids.text8.readonly = False
            self.ids.text9.readonly = False

            for i in self.TD_patients[self.row_id]:
                myquery ={self.champs_patient[j]:i['text']}
                self.l_past.append(myquery)
                j+=1
        elif screen.current == 'display_RDV_cases':
            self.ids.text1_rdv.readonly = False
            self.ids.text2_rdv.readonly = False
            self.ids.text3_rdv.readonly = False
            self.ids.text4_rdv.readonly = False
            self.ids.text5_rdv.readonly = False
            self.ids.text6_rdv.readonly = False
            self.ids.text7_rdv.readonly = False
            for i in self.TD_rdv[self.row_id]:
                myquery ={self.champs_rdv[j]:i['text']}
                j+=1
                self.l_past_rdv.append(myquery)

        elif screen.current == 'display_visite_cases':
            self.ids.text1_visite.readonly = False
            self.ids.text2_visite.readonly = False
            self.ids.text3_visite.readonly = False
            self.ids.text4_visite.readonly = False
            self.ids.text5_visite.readonly = False
            self.ids.text6_visite.readonly = False
            self.ids.text7_visite.readonly = False
            print(self.TD_visite)
            for i in self.TD_visite[self.row_id]:
                myquery ={self.champs_visite[j]:i['text']}
                j+=1
                self.l_past_visite.append(myquery)
            print(self.l_past_visite)
        elif screen.current == 'display_salle_cases':
            self.ids.text1_salle.readonly = False
            self.ids.text2_salle.readonly = False
            self.ids.text3_salle.readonly = False
            self.ids.text4_salle.readonly = False
            self.ids.text5_salle.readonly = False
            self.ids.text6_salle.readonly = False
            for i in self.TD_salle[self.row_id]:
                myquery ={self.champs_salle[j]:i['text']}
                j+=1
                self.l_past_salle.append(myquery)
        elif screen.current == 'display_presc_cases':
            self.ids.text1_presc.readonly = False
            self.ids.text2_presc.readonly = False
            self.ids.text3_presc.readonly = False
            self.ids.text4_presc.readonly = False
            self.ids.text5_presc.readonly = False
            self.ids.text6_presc.readonly = False
            self.ids.text7_presc.readonly = False
            for i in self.TD_presc[self.row_id]:
                myquery ={self.champs_presc[j]:i['text']}
                j+=1
                self.l_past_presc.append(myquery)
        elif screen.current == 'display_actes_cases':
            self.ids.text1_actes.readonly = False
            self.ids.text2_actes.readonly = False
            self.ids.text4_actes.readonly = False
            for i in self.TD_actes[self.row_id]:
                myquery ={self.champs_actes[j]:i['text']}
                j+=1
                self.l_past_actes.append(myquery)

        elif screen.current == 'display_med_cases':
            self.ids.text1_med.readonly = False
            self.ids.text2_med.readonly = False
            self.ids.text3_med.readonly = False
            self.ids.text4_med.readonly = False
            self.ids.text5_med.readonly = False
            self.ids.text6_med.readonly = False
            self.ids.text7_med.readonly = False
            for i in self.TD_med[self.row_id]:
                myquery ={self.champs_med[j]:i['text']}
                j+=1
                self.l_past_med.append(myquery)
        if screen.current=='display_paiement_cases':
            self.ids.text1_p.readonly=False
            self.ids.text2_p.readonly=False
            self.ids.text3_p.readonly=False
            self.ids.text4_p.readonly=False
            self.ids.text5_p.readonly = False
            self.ids.text6_p.readonly = False
            self.ids.text7_p.readonly = False
            self.ids.text8_p.readonly = False
            self.ids.text9_p.readonly = False
            self.ids.text10_p.readonly = False

            for i in self.TD_paiements[self.row_id]:
                myquery ={self.champs_paie[j]:i['text']}
                self.l_past_paie.append(myquery)
                j+=1


    def enregistrer_modification_table(self):
        j=0
        l=[]
        screen = self.ids.scm_cases
        if screen.current == 'display_patients_cases':
            l.append(self.ids.text1.text)
            l.append(self.ids.text2.text)
            l.append(self.ids.text3.text)
            l.append(self.ids.text4.text)
            l.append(self.ids.text5.text)
            l.append(self.ids.text6.text)
            l.append(self.ids.text7.text)
            l.append(self.ids.text8.text)
            l.append(self.ids.text9.text)




            for i in range(len(self.TD_patients[self.row_id])):
                newvalues ={"$set": {  self.champs_patient[j]:l[i]}}
                myquery=self.l_past[j]
                self.patients.update_one(myquery, newvalues)
                j+=1



            self.ids.display_patients.clear_widgets()
            patients = self.get_patients()

            patientstable =DataTable(table=patients)
            content = self.ids.display_patients
            content.add_widget(patientstable)
            self.ids.text1.text = ''
            self.ids.text2.text = ''
            self.ids.text3.text = ''
            self.ids.text4.text = ''
            self.ids.text5.text = ''
            self.ids.text6.text = ''
            self.ids.text7.text = ''
            self.ids.text8.text = ''
            self.ids.text9.text = ''
        elif screen.current == 'display_RDV_cases':
            l.append(self.ids.text1_rdv.text)
            l.append(self.ids.text2_rdv.text)
            l.append(self.ids.text3_rdv.text)
            l.append(self.ids.text4_rdv.text)
            l.append(self.ids.text5_rdv.text)
            l.append(self.ids.text6_rdv.text)
            l.append(self.ids.text7_rdv.text)

            for i in range(len(self.TD_rdv[self.row_id])):
                newvalues ={"$set": {  self.champs_rdv[j]:l[i]}}
                myquery=self.l_past_rdv[j]
                self.rdvs.update_one(myquery, newvalues)
                j+=1


            self.ids.display_rendez_vous.clear_widgets()
            rdvs = self.get_rendez_vous()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_rendez_vous
            content.add_widget(rdvstable)
            self.ids.text1_rdv.text = ''
            self.ids.text2_rdv.text = ''
            self.ids.text3_rdv.text = ''
            self.ids.text4_rdv.text = ''
            self.ids.text5_rdv.text = ''
            self.ids.text6_rdv.text = ''
            self.ids.text7_rdv.text = ''
        elif screen.current == 'display_visite_cases':
            l.append(self.ids.text1_visite.text)
            l.append(self.ids.text2_visite.text)
            l.append(self.ids.text3_visite.text)
            l.append(self.ids.text4_visite.text)
            l.append(self.ids.text5_visite.text)
            l.append(self.ids.text7_visite.text)
            l.append(self.ids.text6_visite.text)
            for i in range(len(self.TD_visite[self.row_id])):
                newvalues ={"$set": {  self.champs_visite[j]:l[i]}}
                myquery=self.l_past_visite[j]
                self.visites.update_one(myquery, newvalues)
                j+=1
            self.ids.display_visite.clear_widgets()
            rdvs = self.get_visites()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_visite
            content.add_widget(rdvstable)
            self.ids.text1_visite.text=''
            self.ids.text2_visite.text=''
            self.ids.text3_visite.text=''
            self.ids.text4_visite.text=''
            self.ids.text5_visite.text=''
            self.ids.text6_visite.text=''
            self.ids.text7_visite.text = ''
        elif screen.current == 'display_salle_cases':
            l.append(self.ids.text1_salle.text)
            l.append(self.ids.text2_salle.text)
            l.append(self.ids.text3_salle.text)
            l.append(self.ids.text4_salle.text)
            l.append(self.ids.text5_salle.text)
            l.append(self.ids.text6_salle.text)
            for i in range(len(self.TD_salle[self.row_id])):
                newvalues ={"$set": {  self.champs_salle[j]:l[i]}}
                myquery=self.l_past_salle[j]
                self.salle.update_one(myquery, newvalues)
                j+=1

            self.ids.display_salle.clear_widgets()
            rdvs = self.get_salle()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_salle
            content.add_widget(rdvstable)
            self.ids.text1_salle.text = ''
            self.ids.text2_salle.text = ''
            self.ids.text3_salle.text = ''
            self.ids.text4_salle.text = ''
            self.ids.text5_salle.text = ''
            self.ids.text6_salle.text = ''

        elif screen.current == 'display_presc_cases':
            l.append(self.ids.text1_presc.text)
            l.append(self.ids.text2_presc.text)
            l.append(self.ids.text3_presc.text)
            l.append(self.ids.text4_presc.text)
            l.append(self.ids.text5_presc.text)
            l.append(self.ids.text6_presc.text)
            l.append(self.ids.text7_presc.text)
            for i in range(len(self.TD_presc[self.row_id])):
                newvalues ={"$set": {  self.champs_presc[j]:l[i]}}
                myquery=self.l_past_presc[j]
                self.presc.update_one(myquery, newvalues)
                j+=1

            self.ids.display_presc.clear_widgets()
            rdvs = self.get_prescription()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_presc
            content.add_widget(rdvstable)
            self.ids.text1_presc.text = ''
            self.ids.text2_presc.text = ''
            self.ids.text3_presc.text = ''
            self.ids.text4_presc.text = ''
            self.ids.text5_presc.text = ''
            self.ids.text6_presc.text = ''
            self.ids.text7_presc.text = ''

        elif screen.current == 'display_actes_cases':
            l.append(self.ids.text1_actes.text)
            l.append(self.ids.text2_actes.text)
            l.append(self.ids.text4_actes.text)
            for i in range(len(self.TD_actes[self.row_id])):
                newvalues ={"$set": {  self.champs_actes[j]:l[i]}}
                myquery=self.l_past_actes[j]
                self.actes.update_one(myquery, newvalues)
                j+=1

            self.ids.display_actes.clear_widgets()
            rdvs = self.get_actes()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_actes
            content.add_widget(rdvstable)
            print(self.row_id)
            self.ids.text1_actes.text = ''
            self.ids.text2_actes.text = ''
            self.ids.text4_actes.text = ''
        elif screen.current == 'display_med_cases':
            l.append(self.ids.text1_med.text)
            l.append(self.ids.text2_med.text)
            l.append(self.ids.text3_med.text)
            l.append(self.ids.text4_med.text)
            l.append(self.ids.text5_med.text)
            l.append(self.ids.text6_med.text)
            l.append(self.ids.text7_med.text)
            for i in range(len(self.TD_med[self.row_id])):
                newvalues ={"$set": {  self.champs_med[j]:l[i]}}
                myquery=self.l_past_med[j]
                self.med.update_one(myquery, newvalues)
                j+=1


            self.ids.display_med.clear_widgets()
            rdvs = self.get_medicament()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_med
            content.add_widget(rdvstable)
            self.ids.text1_med.text = ''
            self.ids.text2_med.text = ''
            self.ids.text3_med.text = ''
            self.ids.text4_med.text = ''
            self.ids.text5_med.text = ''
            self.ids.text6_med.text = ''
            self.ids.text7_med.text = ''

        if screen.current == 'display_paiement_cases':
            l.append(self.ids.text1_p.text)
            l.append(self.ids.text2_p.text)
            l.append(self.ids.text3_p.text)
            l.append(self.ids.text10_p.text)
            l.append(self.ids.text4_p.text)
            l.append(self.ids.text5_p.text)
            l.append(self.ids.text6_p.text)
            l.append(self.ids.text7_p.text)
            l.append(self.ids.text8_p.text)
            l.append(self.ids.text9_p.text)




            for i in range(len(self.TD_paiements[self.row_id])):
                newvalues ={"$set": {  self.champs_paie[j]:l[i]}}
                myquery=self.l_past_paie[j]
                self.paie.update_one(myquery, newvalues)
                j+=1



            self.ids.display_paiement.clear_widgets()
            patients = self.get_paiement()

            patientstable =DataTable(table=patients)
            content = self.ids.display_paiement
            content.add_widget(patientstable)
            self.ids.text1_p.text = ''
            self.ids.text2_p.text = ''
            self.ids.text3_p.text = ''
            self.ids.text4_p.text = ''
            self.ids.text5_p.text = ''
            self.ids.text6_p.text = ''
            self.ids.text7_p.text = ''
            self.ids.text8_p.text = ''
            self.ids.text9_p.text = ''
            self.ids.text10_p.text = ''

    def enregistrer_ajouter(self):
        screen = self.ids.scm_cases
        print(screen.current)
        if screen.current == 'display_patients_cases':
            target1 = self.ids.text1.text
            target2 = self.ids.text2.text
            target3 = self.ids.text3.text
            target4 = self.ids.text4.text
            target5 = self.ids.text5.text
            target6 = self.ids.text6.text
            target7 = self.ids.text7.text
            target8 = self.ids.text8.text
            target9 = self.ids.text9.text
            self.patients.insert_one({self.champs_patient[0]: target1, self.champs_patient[1]: target2,
                                   self.champs_patient[2]:target3, self.champs_patient[3]: target4,self.champs_patient[4]: target5,self.champs_patient[5]: target6,self.champs_patient[6]: target7,self.champs_patient[7]: target8,self.champs_patient[8]: target9,})

            self.ids.display_patients.clear_widgets()
            patients = self.get_patients()
            patientstable = DataTable(table=patients)
            content = self.ids.display_patients
            content.add_widget(patientstable)
            self.ids.text1.text = ''
            self.ids.text2.text = ''
            self.ids.text3.text = ''
            self.ids.text4.text = ''
            self.ids.text5.text = ''
            self.ids.text6.text = ''
            self.ids.text7.text = ''
            self.ids.text8.text = ''
            self.ids.text9.text = ''
        elif screen.current == 'display_RDV_cases':
            target1 = self.ids.text1_rdv.text
            target2 = self.ids.text2_rdv.text
            target3 = self.ids.text3_rdv.text
            target4 = self.ids.text4_rdv.text
            target5 = self.ids.text5_rdv.text
            target6 = self.ids.text6_rdv.text
            target7 = self.ids.text7_rdv.text
            self.rdvs.insert_one({self.champs_rdv[0]: target1, self.champs_rdv[1]: target2,
                                  self.champs_rdv[2]: target3, self.champs_rdv[3]: target4, self.champs_rdv[4]: target5, self.champs_rdv[5]: target6, self.champs_rdv[6]: target7})

            self.ids.display_rendez_vous.clear_widgets()
            rdvs = self.get_rendez_vous()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_rendez_vous
            content.add_widget(rdvstable)
            self.ids.text1_rdv.text = ''
            self.ids.text2_rdv.text = ''
            self.ids.text3_rdv.text = ''
            self.ids.text4_rdv.text = ''
            self.ids.text5_rdv.text = ''
            self.ids.text6_rdv.text = ''
            self.ids.text7_rdv.text = ''
        elif screen.current == 'display_visite_cases':
            target1 = self.ids.text1_visite.text
            target2 = self.ids.text2_visite.text
            target3 = self.ids.text3_visite.text
            target4 = self.ids.text4_visite.text
            target5 = self.ids.text5_visite.text
            target6 = self.ids.text6_visite.text
            target7 = self.ids.text7_visite.text
            self.visites.insert_one({self.champs_visite[0]: target1, self.champs_visite[1]: target2,
                                  self.champs_visite[2]: target3, self.champs_visite[3]: target4, self.champs_visite[4]: target5,
                                  self.champs_visite[6]: target6,self.champs_visite[5]: target7})

            self.ids.display_visite.clear_widgets()
            rdvs = self.get_visites()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_visite
            content.add_widget(rdvstable)
            self.ids.text1_visite.text=''
            self.ids.text2_visite.text=''
            self.ids.text3_visite.text=''
            self.ids.text4_visite.text=''
            self.ids.text5_visite.text=''
            self.ids.text6_visite.text=''
            self.ids.text7_visite.text = ''
        elif screen.current == 'display_salle_cases':
            target1 = self.ids.text1_salle.text
            target2 = self.ids.text2_salle.text
            target3 = self.ids.text3_salle.text
            target4 = self.ids.text4_salle.text
            target5 = self.ids.text5_salle.text
            target6 = self.ids.text6_salle.text
            self.salle.insert_one({self.champs_salle[0]: target1, self.champs_salle[1]: target2,
                                  self.champs_salle[2]: target3, self.champs_salle[3]: target4, self.champs_salle[4]: target5,
                                  self.champs_salle[5]: target6})

            self.ids.display_salle.clear_widgets()
            rdvs = self.get_salle()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_salle
            content.add_widget(rdvstable)
            self.ids.text1_salle.text=''
            self.ids.text2_salle.text=''
            self.ids.text3_salle.text=''
            self.ids.text4_salle.text=''
            self.ids.text5_salle.text=''
            self.ids.text6_salle.text=''

        elif screen.current == 'display_presc_cases':
            target1 = self.ids.text1_presc.text
            target2 = self.ids.text2_presc.text
            target3 = self.ids.text3_presc.text
            target4 = self.ids.text4_presc.text
            target5 = self.ids.text5_presc.text
            target6 = self.ids.text6_presc.text
            target7 = self.ids.text7_presc.text
            self.presc.insert_one({self.champs_presc[0]: target1, self.champs_presc[1]: target2,
                                  self.champs_presc[2]: target3, self.champs_presc[3]: target4, self.champs_presc[4]: target5,
                                  self.champs_presc[5]: target6,self.champs_presc[6]: target7})

            self.ids.display_presc.clear_widgets()
            rdvs = self.get_prescription()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_presc
            content.add_widget(rdvstable)
            self.ids.text1_presc.text=''
            self.ids.text2_presc.text=''
            self.ids.text3_presc.text=''
            self.ids.text4_presc.text=''
            self.ids.text5_presc.text=''
            self.ids.text6_presc.text=''
            self.ids.text7_presc.text = ''
        elif screen.current == 'display_actes_cases':
            target1 = self.ids.text1_actes.text
            target2 = self.ids.text2_actes.text
            target4 = self.ids.text4_actes.text
            self.actes.insert_one({self.champs_actes[0]: target1, self.champs_actes[1]: target2,
                                  self.champs_actes[2]: target4})

            self.ids.display_actes.clear_widgets()
            rdvs = self.get_actes()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_actes
            content.add_widget(rdvstable)
            self.ids.text1_actes.text=''
            self.ids.text2_actes.text=''
            self.ids.text4_actes.text=''
        elif screen.current == 'display_med_cases':
            target1 = self.ids.text1_med.text
            target2 = self.ids.text2_med.text
            target3 = self.ids.text3_med.text
            target4 = self.ids.text4_med.text
            target5 = self.ids.text5_med.text
            target6 = self.ids.text6_med.text
            target7 = self.ids.text7_med.text
            self.med.insert_one({self.champs_med[0]: target1, self.champs_med[1]: target2,
                                  self.champs_med[2]: target3, self.champs_med[3]: target4, self.champs_med[4]: target5,
                                  self.champs_med[5]: target6,self.champs_med[6]: target7})

            self.ids.display_med.clear_widgets()
            rdvs = self.get_medicament()
            rdvstable = DataTable(table=rdvs)
            content = self.ids.display_med
            content.add_widget(rdvstable)
            self.ids.text1_med.text=''
            self.ids.text2_med.text=''
            self.ids.text3_med.text=''
            self.ids.text4_med.text=''
            self.ids.text5_med.text=''
            self.ids.text6_med.text=''
            self.ids.text7_med.text = ''

        if screen.current == 'display_paiement_cases':
            target1 = self.ids.text1_p.text
            target2 = self.ids.text2_p.text
            target3 = self.ids.text3_p.text
            target4 = self.ids.text4_p.text
            target5 = self.ids.text5_p.text
            target6 = self.ids.text6_p.text
            target7 = self.ids.text7_p.text
            target8 = self.ids.text8_p.text
            target9 = self.ids.text9_p.text
            target10 = self.ids.text10_p.text
            self.paie.insert_one({self.champs_paie[0]: target1, self.champs_paie[1]: target2,
                                   self.champs_paie[2]:target3, self.champs_paie[3]: target10,self.champs_paie[4]: target4,self.champs_paie[5]: target5,self.champs_paie[6]: target6,self.champs_paie[7]: target7,self.champs_paie[8]: target8,self.champs_paie[9]: target9})

            self.ids.display_paiement.clear_widgets()
            patients = self.get_paiement()
            patientstable = DataTable(table=patients)
            content = self.ids.display_paiement
            content.add_widget(patientstable)
            self.ids.text1_p.text = ''
            self.ids.text2_p.text = ''
            self.ids.text3_p.text = ''
            self.ids.text4_p.text = ''
            self.ids.text5_p.text = ''
            self.ids.text6_p.text = ''
            self.ids.text7_p.text = ''
            self.ids.text8_p.text = ''
            self.ids.text9_p.text = ''
            self.ids.text10_p.text = ''



    is_button_disabled = BooleanProperty(True)


    def check_inputs(self):
        input1 = self.ids.text1.text.strip()
        input2 = self.ids.text2.text.strip()
        input3 = self.ids.text3.text.strip()
        input4 = self.ids.text4.text.strip()


        if input1 == '' and input2 == '' and input3 == '' and input4 == '':
            self.is_button_disabled = True
        else:
            self.is_button_disabled = False

    def on_save_button_release(self):
        p1 = self.ids.text1.text
        p2 = self.ids.text2.text
        p3 = self.ids.text3.text
        p4 = self.ids.text4.text
        p5 = self.ids.text5.text
        p6 = self.ids.text6.text
        p7 = self.ids.text7.text
        p8 = self.ids.text8.text
        p9 = self.ids.text9.text
        pa1 = self.ids.text1_p.text
        pa2 = self.ids.text2_p.text
        pa3 = self.ids.text3_p.text
        pa4 = self.ids.text4_p.text
        pa5 = self.ids.text5_p.text
        pa6 = self.ids.text6_p.text
        pa7 = self.ids.text7_p.text
        pa8 = self.ids.text8_p.text
        pa9 = self.ids.text9_p.text
        pa10 = self.ids.text10_p.text
        r1 = self.ids.text1_rdv.text
        r2 = self.ids.text2_rdv.text
        r3 = self.ids.text3_rdv.text
        r4 = self.ids.text4_rdv.text
        r5 = self.ids.text5_rdv.text
        r6 = self.ids.text6_rdv.text
        r7 = self.ids.text7_rdv.text
        v1 = self.ids.text1_visite.text
        v2 = self.ids.text2_visite.text
        v3 = self.ids.text3_visite.text
        v4 = self.ids.text4_visite.text
        v5 = self.ids.text5_visite.text
        v6 = self.ids.text6_visite.text
        v7 = self.ids.text7_visite.text
        s1 = self.ids.text1_salle.text
        s2 = self.ids.text2_salle.text
        s3 = self.ids.text3_salle.text
        s4 = self.ids.text4_salle.text
        s5 = self.ids.text5_salle.text
        s6 = self.ids.text6_salle.text
        pr1 = self.ids.text1_presc.text
        pr2 = self.ids.text2_presc.text
        pr3 = self.ids.text3_presc.text
        pr4 = self.ids.text4_presc.text
        pr5 = self.ids.text5_presc.text
        pr6 = self.ids.text6_presc.text
        pr7 = self.ids.text7_presc.text
        a1 = self.ids.text1_actes.text
        a2 = self.ids.text2_actes.text
        a4 = self.ids.text4_actes.text
        m1 = self.ids.text1_med.text
        m2 = self.ids.text2_med.text
        m3 = self.ids.text3_med.text
        m4 = self.ids.text4_med.text
        m5 = self.ids.text5_med.text
        m6 = self.ids.text6_med.text
        m7 = self.ids.text7_med.text
        if (self.ids.scm_cases.current == 'display_patients_cases'and (p1 == '' or p2 == '' or p3 == '' or p4 == '' or p5 == '' or p6 == '' or p7 == '' or p8 == '' or p9 == '')) or  (self.ids.scm_cases.current == 'display_RDV_cases' and  (r1 == '' or r2 == '' or r3 == '' or r4 == '' or r5 == '' or r6 == '' or r7 == '') )or  (self.ids.scm_cases.current == 'display_visite_cases' and (v1 == '' or v2 == '' or v3 == '' or v4 == '' or v5 == '' or v6 == '' or v7=='')) or  (self.ids.scm_cases.current == 'display_salle_cases'and (s1 == '' or s2 == '' or s3 == '' or s4 == '' or s5 == '' or s6 == '')) or  (self.ids.scm_cases.current == 'display_presc_cases' and (pr1 == '' or pr2 == '' or pr3 == '' or pr4 == '' or pr5 == '' or pr6 == '' or pr7 == ''))or  (self.ids.scm_cases.current == 'display_actes_cases' and (a1 == '' or a2 == ''  or a4 == '')) or  (self.ids.scm_cases.current == 'display_med_cases' and (m1 == '' or m2 == '' or m3 == '' or m4 == '' or m5 == '' or m6 == '' or m7 == '')) or (self.ids.scm_cases.current == 'display_paiement_cases'and (pa1 == '' or pa2 == '' or pa3 == '' or pa4 == '' or pa5 == '' or pa6 == '' or pa7 == '' or pa8 == '' or pa9 == '' or pa10=='')):
            dialog = MDDialog(
                title="OOPS",
                text="Champs non remplis.",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

        else:
            if self.previous_action == 'add':
                self.enregistrer_ajouter()
            elif self.previous_action == 'update':
                self.enregistrer_modification_table()
                self.ids.text1.readonly = True
                self.ids.text2.readonly = True
                self.ids.text3.readonly = True
                self.ids.text4.readonly = True
                self.ids.text5.readonly = True
                self.ids.text6.readonly = True
                self.ids.text7.readonly = True
                self.ids.text8.readonly = True
                self.ids.text9.readonly = True
                self.ids.text1_p.readonly = True
                self.ids.text2_p.readonly = True
                self.ids.text3_p.readonly = True
                self.ids.text4_p.readonly = True
                self.ids.text5_p.readonly = True
                self.ids.text6_p.readonly = True
                self.ids.text7_p.readonly = True
                self.ids.text8_p.readonly = True
                self.ids.text9_p.readonly = True
                self.ids.text10_p.readonly = True
                self.ids.text1_rdv.readonly = True
                self.ids.text2_rdv.readonly = True
                self.ids.text3_rdv.readonly = True
                self.ids.text4_rdv.readonly = True
                self.ids.text5_rdv.readonly = True
                self.ids.text6_rdv.readonly = True
                self.ids.text7_rdv.readonly = True
                self.ids.text1_visite.readonly = True
                self.ids.text2_visite.readonly = True
                self.ids.text3_visite.readonly = True
                self.ids.text4_visite.readonly = True
                self.ids.text5_visite.readonly = True
                self.ids.text6_visite.readonly = True
                self.ids.text7_visite.readonly = True
                self.ids.text1_salle.readonly = True
                self.ids.text2_salle.readonly = True
                self.ids.text3_salle.readonly = True
                self.ids.text4_salle.readonly = True
                self.ids.text5_salle.readonly = True
                self.ids.text6_salle.readonly = True
                self.ids.text1_presc.readonly = True
                self.ids.text2_presc.readonly = True
                self.ids.text3_presc.readonly = True
                self.ids.text4_presc.readonly = True
                self.ids.text5_presc.readonly = True
                self.ids.text6_presc.readonly = True
                self.ids.text7_presc.readonly = True
                self.ids.text1_actes.readonly = True
                self.ids.text2_actes.readonly = True
                self.ids.text4_actes.readonly = True
                self.ids.text1_med.readonly = True
                self.ids.text2_med.readonly = True
                self.ids.text3_med.readonly = True
                self.ids.text4_med.readonly = True
                self.ids.text5_med.readonly = True
                self.ids.text6_med.readonly = True
                self.ids.text7_med.readonly = True

    def Date1(self):
        cal_date = MDDatePicker()
        cal_date.bind(on_save=self.on_save1)
        cal_date.open()

    def Time1(self):
        cal_time = MDTimePicker()
        default_time = datetime.strptime("19:00:00", '%H:%M:%S')
        cal_time.set_time(default_time)
        # self.root.get_screen('Fixer_RDV').ids.ftime.text = '19:00:00'
        cal_time.bind(on_cancel=self.on_cancel_time1, time=self.on_save_time1)
        cal_time.open()

    def on_save1(self, instance, value, date_range):
        if value.weekday() in (5, 6):
            dialog = MDDialog(
                title="OOPS",
                text="Ce jour est ferie.",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()



        else:
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
        dialog.dismiss()
        if self.ids.scm_cases.current == 'display_visite_cases':
            # Perform desired action with selected date
            self.ids.text3_visite.text = str(value)
        elif self.ids.scm_cases.current == 'display_salle_cases':
            self.ids.text2_salle.text = str(value)
        elif self.ids.scm_cases.current == 'display_patients_cases':
            self.ids.text4.text = str(value)
        elif self.ids.scm_cases.current == 'display_med_cases':
            self.ids.text7_med.text = str(value)
        elif self.ids.scm_cases.current == 'display_paiement_cases':
            self.ids.text6_p.text = str(value)

        # Time

    def on_cancel_time1(self, instance, time):
        if time == None:
            if self.ids.scm_cases.current == 'display_visite_cases':
                self.ids.text4_visite.text = ''
            else:
                self.ids.text3_salle.text = ''

    def on_save_time1(self, instance, time):

        if tm(15, 30) <= time <= tm(0, 0) or tm(0, 0) <= time <= tm(9, 59):
            dialog = MDDialog(
                title="OOPS",
                text="l'heure choisie n'est pas disponible.",
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()


        else:

            # Create confirmation dialog
            confirm_dialog = MDDialog(
                text=f"Êtes-vous certain de vouloir sélectionner {str(time)}?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="SELECT",
                        on_release=lambda x: self.on_confirm3(time, confirm_dialog),
                    ),
                ],
            )

            confirm_dialog.open()

    def on_confirm3(self, time, dialog):
        if self.ids.scm_cases.current == 'display_visite_cases':
            self.ids.text4_visite.text = str(time)
        else:
            self.ids.text3_salle.text = str(time)
        dialog.dismiss()






    def rechercher(self,valeur):
        print(valeur)
        if self.ids.scm.current =='display_patients':
            print('fdhfjhfj')

            app = App.get_running_app()
            nom_patient = self.ids.rech.text.strip()
            print(nom_patient)


            if nom_patient:  # Search for the patient name
                _users = OrderedDict(ID_Patients={}, Noms={}, Prenoms={}, Dates_de_naissance={}, Telephones={},
                                     Adresses={}, Antecedents_medicaux={}, Emails={}, Assurances={})

                client = MongoClient()
                db = client['Admin_cabinet']
                col = db['Patients']
                i = 0
                if valeur=='nom':

                    for user in col.find():
                        print(user['Nom'], nom_patient)
                        #print(user['Prenom'], nom_patient)
                        if user['Nom'] == nom_patient:
                            try:
                                _users['Noms'][i] = user['Nom']
                                _users['Prenoms'][i] = user['Prenom']
                                _users['Dates_de_naissance'][i] = user['Date de naissance']
                                _users['Telephones'][i] = user['Telephone']
                                _users['Adresses'][i] = user['Adresse']
                                _users['Antecedents_medicaux'][i] = user['Antecedents medicaux']
                                _users['Emails'][i] = user['Email']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Assurances'][i] = user['Assurance']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur=='prenom':
                    for user in col.find():
                        print(user['Prenom'],nom_patient)
                        if user['Prenom'] == nom_patient:
                            try:
                                _users['Noms'][i] = user['Nom']
                                _users['Prenoms'][i] = user['Prenom']
                                _users['Dates_de_naissance'][i] = user['Date de naissance']
                                _users['Telephones'][i] = user['Telephone']
                                _users['Adresses'][i] = user['Adresse']
                                _users['Antecedents_medicaux'][i] = user['Antecedents medicaux']
                                _users['Emails'][i] = user['Email']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Assurances'][i] = user['Assurance']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur=='telephone':
                    for user in col.find():
                        if user['Telephone'] == nom_patient:
                            try:
                                _users['Noms'][i] = user['Nom']
                                _users['Prenoms'][i] = user['Prenom']
                                _users['Dates_de_naissance'][i] = user['Date de naissance']
                                _users['Telephones'][i] = user['Telephone']
                                _users['Adresses'][i] = user['Adresse']
                                _users['Antecedents_medicaux'][i] = user['Antecedents medicaux']
                                _users['Emails'][i] = user['Email']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Assurances'][i] = user['Assurance']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur=='email':
                    for user in col.find():
                        if user['Email'] == nom_patient:
                            try:
                                _users['Noms'][i] = user['Nom']
                                _users['Prenoms'][i] = user['Prenom']
                                _users['Dates_de_naissance'][i] = user['Date de naissance']
                                _users['Telephones'][i] = user['Telephone']
                                _users['Adresses'][i] = user['Adresse']
                                _users['Antecedents_medicaux'][i] = user['Antecedents medicaux']
                                _users['Emails'][i] = user['Email']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Assurances'][i] = user['Assurance']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""


                if i > 0:  # Display search results
                    self.ids.display_patients.clear_widgets()
                    content1 = self.ids.display_patients
                    rdvs = _users
                    rdvstable = DataTable(table=rdvs)
                    content1.add_widget(rdvstable)
                else:  # No search results found
                    # Display a message or perform any desired action
                    pass
            else:  # Empty search field, restore the original table
                self.ids.display_patients.clear_widgets()
                content1 = self.ids.display_patients
                original_table_widget = self.get_patients()
                rdvstable1 = DataTable(table=original_table_widget)# Replace with the actual widget class
                content1.add_widget(rdvstable1)




        elif self.ids.scm.current =='display_rendez_vous':
            print('oui')
            app = App.get_running_app()
            nom_patient = self.ids.rech.text.strip()
            print(nom_patient)
            if nom_patient:  # Search for the patient name
                _users = OrderedDict(ID_Rendez_vous={},ID_Patients={},Dates_RDV={}, Heures_RDV={}, Nom_Actes={}, Statuts_RDV={},Notes_Supp={})

                client = MongoClient()
                db = client['Admin_cabinet']
                col = db['Rendez_vous']
                i = 0
                if valeur == 'ID_Patient':
                    for user in col.find():
                        if user['ID_Patient'] == nom_patient:
                            try:
                                _users['ID_Rendez_vous'][i] = user['ID_Rendez_vous']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Dates_RDV'][i] = user['Date']
                                _users['Heures_RDV'][i] = user['Heure']
                                _users['Nom_Actes'][i] = user['Nom_Acte']
                                _users['Statuts_RDV'][i] = user['Statut du rendez-vous']
                                _users['Notes_Supp'][i] = user['Notes ou instructions supplémentaires']

                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'date':
                    print('adam')
                    for user in col.find():
                        print(user)
                        print(user['Date'])
                        if user['Date'] == nom_patient:
                            try:
                                _users['ID_Rendez_vous'][i] = user['ID_Rendez_vous']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Dates_RDV'][i] = user['Date']
                                _users['Heures_RDV'][i] = user['Heure']
                                _users['Nom_Actes'][i] = user['Nom_Acte']
                                _users['Statuts_RDV'][i] = user['Statut du rendez-vous']
                                _users['Notes_Supp'][i] = user['Notes ou instructions supplémentaires']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'heure':
                    for user in col.find():
                        if user['Heure'] == nom_patient:
                            try:
                                _users['ID_Rendez_vous'][i] = user['ID_Rendez_vous']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Dates_RDV'][i] = user['Date']
                                _users['Heures_RDV'][i] = user['Heure']
                                _users['Nom_Actes'][i] = user['Nom_Acte']
                                _users['Statuts_RDV'][i] = user['Statut du rendez-vous']
                                _users['Notes_Supp'][i] = user['Notes ou instructions supplémentaires']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'acte':
                    for user in col.find():
                        if user['Nom_Acte'] == nom_patient:
                            try:
                                _users['ID_Rendez_vous'][i] = user['ID_Rendez_vous']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Dates_RDV'][i] = user['Date']
                                _users['Heures_RDV'][i] = user['Heure']
                                _users['Nom_Actes'][i] = user['Nom_Acte']
                                _users['Statuts_RDV'][i] = user['Statut du rendez-vous']
                                _users['Notes_Supp'][i] = user['Notes ou instructions supplémentaires']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""

                if i > 0:  # Display search results
                    self.ids.display_rendez_vous.clear_widgets()
                    content1 = self.ids.display_rendez_vous
                    rdvs = _users
                    rdvstable = DataTable(table=rdvs)
                    content1.add_widget(rdvstable)
                else:  # No search results found
                    # Display a message or perform any desired action
                    pass
            else:  # Empty search field, restore the original table
                self.ids.display_rendez_vous.clear_widgets()
                content1 = self.ids.display_rendez_vous
                original_table_widget = self.get_rendez_vous()
                rdvstable1 = DataTable(table=original_table_widget)  # Replace with the actual widget class
                content1.add_widget(rdvstable1)
        elif self.ids.scm.current =='display_visite':
            app = App.get_running_app()
            nom_patient = self.ids.rech.text.strip()


            if nom_patient:  # Search for the patient name
                _users = OrderedDict(ID_Visites={},ID_Patients={}, Date_visite={}, Heure_visite={}, Traitement_effectué={},Notes_ou_remarques_supplémentaires={})

                client = MongoClient()
                db = client['Admin_cabinet']
                col = db['Visite_de_la_journee']
                i = 0
                if valeur == 'ID_Patient_visite':
                    for user in col.find():
                        if user['ID_Patient'] == nom_patient:
                            try:
                                _users['ID_Visites'][i] = user['ID de la visite']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Date_visite'][i] = user['Date de la visite']
                                _users['Heure_visite'][i] = user['Heure de la visite']
                                _users['Nom_Actes'][i] = user['Nom_Acte']
                                _users['Notes_ou_remarques_supplémentaires'][i] = user['Notes ou remarques supplémentaires']


                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'datev':
                    for user in col.find():
                        if user['Date de la visite'] == nom_patient:
                            try:
                                _users['ID_Visites'][i] = user['ID de la visite']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Date_visite'][i] = user['Date de la visite']
                                _users['Heure_visite'][i] = user['Heure de la visite']
                                _users['Nom_Actes'][i] = user['Nom_Acte']
                                _users['Notes_ou_remarques_supplémentaires'][i] = user['Notes ou remarques supplémentaires']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'heurev':
                    for user in col.find():
                        if user['Heure de la visite'] == nom_patient:
                            try:
                                _users['ID_Visites'][i] = user['ID de la visite']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Date_visite'][i] = user['Date de la visite']
                                _users['Heure_visite'][i] = user['Heure de la visite']
                                _users['Nom_Actes'][i] = user['Nom_Acte']
                                _users['Notes_ou_remarques_supplémentaires'][i] = user[
                                    'Notes ou remarques supplémentaires']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'actev':
                    for user in col.find():
                        if user['Nom_Acte'] == nom_patient:
                            try:
                                _users['ID_Visites'][i] = user['ID de la visite']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Date_visite'][i] = user['Date de la visite']
                                _users['Heure_visite'][i] = user['Heure de la visite']
                                _users['Nom_Actes'][i] = user['Nom_Acte']
                                _users['Notes_ou_remarques_supplémentaires'][i] = user['Notes ou remarques supplémentaires']
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""

                if i > 0:  # Display search results
                    self.ids.display_visite.clear_widgets()
                    content1 = self.ids.display_visite
                    rdvs = _users
                    rdvstable = DataTable(table=rdvs)
                    content1.add_widget(rdvstable)
                else:  # No search results found
                    # Display a message or perform any desired action
                    pass
            else:  # Empty search field, restore the original table
                self.ids.display_visite.clear_widgets()
                content1 =self.ids.display_visite
                original_table_widget = self.get_visites()
                rdvstable1 = DataTable(table=original_table_widget)  # Replace with the actual widget class
                content1.add_widget(rdvstable1)




        elif self.ids.scm.current =='display_salle':
            app = App.get_running_app()
            nom_patient = self.ids.rech.text.strip()


            if nom_patient:  # Search for the patient name
                _users = OrderedDict(ID_de_Reflet={},Date_de_Reflet={}, Heure_de_Reflet={}, Nombre_patient_en_attente={}, Statut_patients={},Remarques_ou_informations_supplémentaires={})

                client = MongoClient()
                db = client['Admin_cabinet']
                col = db['Reflet_salle']
                i = 0
                if valeur == 'datesa':
                    for user in col.find():
                        if user['Date du reflet'] == nom_patient:
                            try:
                                _users['ID_de_Reflet'][i] = user['ID de la visite']
                                _users['Date_de_Reflet'][i] = user['Date du reflet']
                                _users['Heure_de_Reflet'][i] = user['Heure du reflet ']
                                _users['Nombre_patient_en_attente'][i] = user['Nombre de patients en attente']
                                _users['Statut_patients'][i] = user['Statut des patients']
                                _users['Remarques_ou_informations_supplémentaires'][i] = user['Remarques ou informations supplémentaires']


                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'heuresa':
                    for user in col.find():
                        if user[' Heure du reflet'] == nom_patient:
                            try:
                                _users['ID_de_Reflet'][i] = user['ID_Reflet']
                                _users['Date_de_Reflet'][i] = user['Date du reflet']
                                _users['Heure_de_Reflet'][i] = user[' Heure du reflet']
                                _users['Nombre_patient_en_attente'][i] = user['Nombre de patients en attente']
                                _users['Statut_patients'][i] = user['Statut des patients']
                                _users['Remarques_ou_informations_supplémentaires'][i] = user[ 'Remarques ou informations supplémentaires']

                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""


                if i > 0:  # Display search results
                    self.ids.display_salle.clear_widgets()
                    content1 = self.ids.display_salle
                    rdvs = _users
                    rdvstable = DataTable(table=rdvs)
                    content1.add_widget(rdvstable)
                else:  # No search results found
                    # Display a message or perform any desired action
                    pass
            else:  # Empty search field, restore the original table
                self.ids.display_salle.clear_widgets()
                content1 = self.ids.display_salle
                original_table_widget = self.get_salle()
                rdvstable1 = DataTable(table=original_table_widget)  # Replace with the actual widget class
                content1.add_widget(rdvstable1)
        elif self.ids.scm.current == 'display_presc':
            app = App.get_running_app()
            nom_patient = self.ids.rech.text.strip()


            if nom_patient:  # Search for the patient name
                _users =OrderedDict(ID_Prescription={},ID_Patients={}, Noms_Medicaments={}, Posologies={}, Duree_des_prescriptions={},Statut_prescriptions={},Notes_supplementaires={})

                client = MongoClient()
                db = client['Admin_cabinet']
                col = db['Prescriptions']
                i = 0
                if valeur == 'idppresc':
                    for user in col.find():
                        if user['ID_Patient'] == nom_patient:
                            try:
                                _users['ID_Prescription'][i] = user['ID_Prescription']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Noms_Medicaments'][i] = user['Nom du medicament']
                                _users['Posologies'][i] = user['Posologie']
                                _users['Duree_des_prescriptions'][i] = user['Durée de la prescription']
                                _users['Statut_prescriptions'][i] = user['Statut de la prescription']
                                _users['Notes_supplementaires'][i]=user['Notes supplémentaires']

                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'nomdumed':
                    for user in col.find():
                        if user['Nom du medicament'] == nom_patient:
                            try:
                                _users['ID_Prescription'][i] = user['ID_Prescription']
                                _users['ID_Patients'][i] = user['ID_Patient']
                                _users['Noms_Medicaments'][i] = user['Nom du medicament']
                                _users['Posologies'][i] = user['Posologie']
                                _users['Duree_des_prescriptions'][i] = user['Durée de la prescription']
                                _users['Statut_prescriptions'][i] = user['Statut de la prescription']
                                _users['Notes_supplementaires'][i] = user['Notes supplémentaires']

                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""

                if i > 0:  # Display search results
                    self.ids.display_presc.clear_widgets()
                    content1 = self.ids.display_presc
                    rdvs = _users
                    rdvstable = DataTable(table=rdvs)
                    content1.add_widget(rdvstable)
                else:  # No search results found
                    # Display a message or perform any desired action
                    pass
            else:  # Empty search field, restore the original table
                self.ids.display_presc.clear_widgets()
                content1=self.ids.display_presc
                original_table_widget = self.get_prescription()
                rdvstable1 = DataTable(table=original_table_widget)  # Replace with the actual widget class
                content1.add_widget(rdvstable1)
        elif self.ids.scm.current == 'display_actes':
            app = App.get_running_app()
            nom_patient = self.ids.rech.text.strip()


            if nom_patient:  # Search for the patient name
                _users =OrderedDict(ID_Actes={},Noms_Actes={}, Coûts_Actes={})

                client = MongoClient()
                db = client['Admin_cabinet']
                col = db['Actes']
                i = 0
                if valeur == 'nomacte':
                    for user in col.find():
                        if user['Nom_Acte'] == nom_patient:
                            try:
                                _users['ID_Actes'][i] = user['ID_Acte']
                                _users['Noms_Actes'][i] = user['Nom_Acte']
                                _users['Coûts_Actes'][i] = user["Coût de l'acte"]


                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'coutacte':
                    for user in col.find():
                        if user["Coût de l'acte"] == nom_patient:
                            try:
                                _users['ID_Actes'][i] = user['ID_Acte']
                                _users['Noms_Actes'][i] = user['Nom_Acte']
                                _users['Coûts_Actes'][i] = user["Coût de l'acte"]

                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""

                if i > 0:  # Display search results
                    self.ids.display_actes.clear_widgets()
                    content1 = self.ids.display_actes
                    rdvs = _users
                    rdvstable = DataTable(table=rdvs)
                    content1.add_widget(rdvstable)
                else:  # No search results found
                    # Display a message or perform any desired action
                    pass
            else:  # Empty search field, restore the original table
                self.ids.display_actes.clear_widgets()
                content1 = self.ids.display_actes
                original_table_widget = self.get_actes()
                rdvstable1 = DataTable(table=original_table_widget)  # Replace with the actual widget class
                content1.add_widget(rdvstable1)



        elif self.ids.scm.current == 'display_med':
            app = App.get_running_app()
            nom_patient = self.ids.rech.text.strip()


            if nom_patient:  # Search for the patient name
                _users =OrderedDict(ID_Médicaments={},Nom_Médicaments={}, Description_des_médicaments={}, Dosage_médicaments={}, Stock_disponible={},Fournisseurs={},Dates_expiration={})

                client = MongoClient()
                db = client['Admin_cabinet']
                col = db['Medicaments']
                print(col)
                i = 0
                if valeur == 'fourniss':
                    for user in col.find():
                        print(user)
                        if user['Fournisseur'] == nom_patient:
                            try:
                                _users['ID_Médicaments'][i] = user["ID_Médicament"]
                                _users['Nom_Médicaments'][i] = user["Nom du médicament"]
                                _users['Description_des_médicaments'][i] = user["Description du médicament"]
                                _users['Dosage_médicaments'][i] = user["Dosage/forme du médicament"]
                                _users['Stock_disponible'][i] = user["Stock disponible"]
                                _users['Dates_expiration'][i] = user["Date d'expiration"]
                                _users['Fournisseurs'][i] = user["Fournisseur"]


                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'nommedi':
                    for user in col.find():
                        if user["Nom du médicament"] == nom_patient:
                            try:
                                    _users['ID_Médicaments'][i]=user["ID_Médicament"]
                                    _users['Nom_Médicaments'][i]=user["Nom du médicament"]
                                    _users['Description_des_médicaments'][i]=user["Description du médicament"]
                                    _users['Dosage_médicaments'][i]=user["Dosage/forme du médicament"]
                                    _users['Stock_disponible'][i]=user["Stock disponible"]
                                    _users['Dates_expiration'][i]=user["Date d'expiration"]
                                    _users['Fournisseurs'][i]=user["Fournisseur"]
                                    i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'dateexp':
                    for user in col.find():
                        if user["Date d'expiration"] == nom_patient:
                            try:
                                _users['ID_Médicaments'][i] = user["ID_Médicament"]
                                _users['Nom_Médicaments'][i] = user["Nom du médicament"]
                                _users['Description_des_médicaments'][i] = user["Description du médicament"]
                                _users['Dosage_médicaments'][i] = user["Dosage/forme du médicament"]
                                _users['Stock_disponible'][i] = user["Stock disponible"]
                                _users['Dates_expiration'][i] = user["Date d'expiration"]
                                _users['Fournisseurs'][i] = user['Fournisseur']


                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""

                if i > 0:  # Display search results
                    self.ids.display_med.clear_widgets()
                    content1 = self.ids.display_med
                    rdvs = _users
                    rdvstable = DataTable(table=rdvs)
                    content1.add_widget(rdvstable)
                else:  # No search results found
                    # Display a message or perform any desired action
                    pass
            else:  # Empty search field, restore the original table
                self.ids.display_med.clear_widgets()
                content1 = self.ids.display_med
                original_table_widget = self.get_medicament()
                rdvstable1 = DataTable(table=original_table_widget)  # Replace with the actual widget class
                content1.add_widget(rdvstable1)
        elif self.ids.scm.current == 'display_paiement':
            app = App.get_running_app()
            nom_patient = self.ids.rech.text.strip()
            copy_tableau = self.ids.display_paiement.children[0].__self__

            if nom_patient:  # Search for the patient name
                _users =OrderedDict(ID_Transaction={},ID_Patients={}, ID_Actes={}, Montant_payé={}, Montant_reste_a_payer={},Modes_Paiements={},Dates_transaction={},Statut_transaction={},Description_transaction={})

                client = MongoClient()
                db = client['Admin_cabinet']
                col = db['Paiements']
                i = 0
                if valeur == 'datetransa':

                    for user in col.find():
                        if user['Date de la transaction'] == nom_patient:
                            try:
                                _users['ID_Transaction'][i] = user["ID_Transaction"]
                                _users['ID_Patients'][i] = user["ID_Patient"]
                                _users['ID_Actes'][i] = user["ID_Acte"]
                                _users['Montant_payé'][i] = user["Montant payé"]
                                _users['Montant_reste_a_payer'][i] = user["Montant reste a payer"]
                                _users['Modes_Paiements'][i] = user["Mode de paiement"]
                                _users['Dates_transaction'][i] = user["Date de la transaction"]
                                _users['Statut_transaction'][i] = user["Statut de la transaction"]
                                _users['Description_transaction'][i] = user["Description de la transaction"]
                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'idactepaie':
                    for user in col.find():
                        if user["ID_Acte"] == nom_patient:
                            try:
                                _users['ID_Transaction'][i] = user["ID_Transaction"]
                                _users['ID_Patients'][i] = user["ID_Patient"]
                                _users['ID_Actes'][i] = user["ID_Acte"]
                                _users['Montant_payé'][i] = user["Montant payé"]
                                _users['Montant_reste_a_payer'][i] = user["Montant reste a payer"]
                                _users['Modes_Paiements'][i] = user["Mode de paiement"]
                                _users['Dates_transaction'][i] = user["Date de la transaction"]
                                _users['Statut_transaction'][i] = user["Statut de la transaction"]
                                _users['Description_transaction'][i] = user["Description de la transaction"]

                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'idpatientpaiem':
                    for user in col.find():
                        if user["ID_Patient"] == nom_patient:
                            try:
                                _users['ID_Transaction'][i] = user["ID_Transaction"]
                                _users['ID_Patients'][i] = user["ID_Patient"]
                                _users['ID_Actes'][i] = user["ID_Acte"]
                                _users['Montant_payé'][i] = user["Montant payé"]
                                _users['Montant_reste_a_payer'][i] = user["Montant reste a payer"]
                                _users['Modes_Paiements'][i] = user["Mode de paiement"]
                                _users['Dates_transaction'][i] = user["Date de la transaction"]
                                _users['Statut_transaction'][i] = user["Statut de la transaction"]
                                _users['Description_transaction'][i] = user["Description de la transaction"]


                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""
                elif valeur == 'modepaie':
                    for user in col.find():
                        if user["Mode de paiement"] == nom_patient:
                            try:
                                _users['ID_Transaction'][i] = user["ID_Transaction"]
                                _users['ID_Patients'][i] = user["ID_Patient"]
                                _users['ID_Actes'][i] = user["ID_Acte"]
                                _users['Montant_payé'][i] = user["Montant payé"]
                                _users['Montant_reste_a_payer'][i] = user["Montant reste a payer"]
                                _users['Modes_Paiements'][i] = user["Mode de paiement"]
                                _users['Dates_transaction'][i] = user["Date de la transaction"]
                                _users['Statut_transaction'][i] = user["Statut de la transaction"]
                                _users['Description_transaction'][i] = user["Description de la transaction"]


                                i += 1
                            except ValueError:
                                # Handle the case when the input values cannot be converted to integers
                                self.ids.rech.text = ""

                if i > 0:  # Display search results
                    self.ids.display_paiement.clear_widgets()
                    content1 = self.ids.display_paiement
                    rdvs = _users
                    rdvstable = DataTable(table=rdvs)
                    content1.add_widget(rdvstable)
                else:  # No search results found
                    # Display a message or perform any desired action
                    pass
            else:  # Empty search field, restore the original table
                self.ids.display_paiement.clear_widgets()
                content1 = self.ids.display_paiement
                original_table_widget = self.get_paiement()
                rdvstable1 = DataTable(table=original_table_widget)  # Replace with the actual widget class
                content1.add_widget(rdvstable1)

    def show_dialogs(self):
        if self.ids.scm.current == 'display_patients':
            textfields = []
            labels = ["Nom", "Prenom", "Telephone", "Email"]
            i = 0
            for label in labels:
                textfield = MDRaisedButton(text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1

            dialog = MDDialog(
                title="Processus de Recherche",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

            textfields[0].bind(on_release=lambda instance: self.gerer('nom',dialog))
            textfields[1].bind(on_release=lambda instance: self.gerer('prenom', dialog))
            textfields[2].bind(on_release=lambda instance: self.gerer('telephone', dialog))
            textfields[3].bind(on_release=lambda instance: self.gerer('email', dialog))


        elif self.ids.scm.current == 'display_rendez_vous':
            textfields = []
            labels = ["ID_Patient", "Date du rendez-vous", "Heure du rendez-vous", "Nom de l'acte"]
            i = 0
            for label in labels:
                textfield = MDRaisedButton(text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1

            dialog = MDDialog(
                title="Processus de Recherche",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

            textfields[0].bind(on_release=lambda instance: self.gerer('ID_Patient', dialog))
            textfields[1].bind(on_release=lambda instance: self.gerer('date', dialog))
            textfields[2].bind(on_release=lambda instance: self.gerer('heure', dialog))
            textfields[3].bind(on_release=lambda instance: self.gerer('acte', dialog))

        elif self.ids.scm.current == 'display_visite':
            textfields = []
            labels = ['ID_Patient','Date de la visite','Heure de la visite','Nom de lacte']
            i = 0
            for label in labels:
                textfield = MDRaisedButton(text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1

            dialog = MDDialog(
                title="Processus de Recherche",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

            textfields[0].bind(on_release=lambda instance: self.gerer('ID_Patient_visite', dialog))
            textfields[1].bind(on_release=lambda instance: self.gerer('datev', dialog))
            textfields[2].bind(on_release=lambda instance: self.gerer('heurev', dialog))
            textfields[3].bind(on_release=lambda instance: self.gerer('actev', dialog))

        elif self.ids.scm.current == 'display_salle':
            textfields = []
            labels = ['Date de reflet','Heure de reflet']
            i = 0
            for label in labels:
                textfield = MDRaisedButton(text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1

            dialog = MDDialog(
                title="Processus de Recherche",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

            textfields[0].bind(on_release=lambda instance: self.gerer('datesa', dialog))
            textfields[1].bind(on_release=lambda instance: self.gerer('heuresa', dialog))


        elif self.ids.scm.current == 'display_presc':
            textfields = []
            labels = ['ID_Patient','Nom du medicament']
            i = 0
            for label in labels:
                textfield = MDRaisedButton(text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1

            dialog = MDDialog(
                title="Processus de Recherche",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

            textfields[0].bind(on_release=lambda instance: self.gerer('idppresc', dialog))
            textfields[1].bind(on_release=lambda instance: self.gerer('nomdumed', dialog))


        elif self.ids.scm.current == 'display_actes':
            textfields = []
            labels = ["Nom de l'acte","cout de l'acte "]
            i = 0
            for label in labels:
                textfield = MDRaisedButton(text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1

            dialog = MDDialog(
                title="Processus de Recherche",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

            textfields[0].bind(on_release=lambda instance: self.gerer('nomacte', dialog))
            textfields[1].bind(on_release=lambda instance: self.gerer('coutacte', dialog))



        elif self.ids.scm.current == 'display_med':
            textfields = []
            labels = ["Fournisseur", "Nom du medicament", "Date d'expiration"]
            i = 0
            for label in labels:
                textfield = MDRaisedButton(text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1

            dialog = MDDialog(
                title="Processus de Recherche",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

            textfields[0].bind(on_release=lambda instance: self.gerer('fourniss', dialog))
            textfields[1].bind(on_release=lambda instance: self.gerer('nommedi', dialog))
            textfields[2].bind(on_release=lambda instance: self.gerer('dateexp', dialog))



        elif self.ids.scm.current == 'display_paiement':
            textfields = []
            labels = ["Date de transaction", "ID_Acte", "ID_Patient", "Mode de paiement"]
            i = 0
            for label in labels:
                textfield = MDRaisedButton(text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1

            dialog = MDDialog(
                title="Processus de Recherche",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

            textfields[0].bind(on_release=lambda instance: self.gerer('datetransa', dialog))
            textfields[1].bind(on_release=lambda instance: self.gerer('idactepaie', dialog))
            textfields[2].bind(on_release=lambda instance: self.gerer('idpatientpaiem', dialog))
            textfields[3].bind(on_release=lambda instance: self.gerer('modepaie', dialog))

    def gerer(self,par,dialog):
        dialog.dismiss()
        self.ids.rech.disabled = False
        self.change=par
        #self.root.get_screen('admin').ids.rech.on_text =  self.rechercher(par)

    def choix(self,tp):
        print(tp)
        if  tp=='idpatientrdv' and hasattr(self, 'dialog') and self.dialog:
            #Dialog instance already exists, so just open it
            self.dialog.open()
            return
        elif  tp=='acterdv' and hasattr(self, 'dialog1') and self.dialog1:
            self.dialog1.open()
            return
        elif tp == 'med' and hasattr(self, 'dialog2') and self.dialog2:
            self.dialog2.open()
            return
        elif  tp == 'idacte' and hasattr(self, 'dialog3') and self.dialog3:
            self.dialog3.open()
            return
        elif tp == 'modpaie' and hasattr(self, 'dialog4') and self.dialog4:
            self.dialog4.open()
            return
        textfields = []
        buttons = []
        cl6 = MongoClient()
        db6 = cl6['Admin_cabinet']
        col6 = db6['Patients']
        col7 = db6['Actes']
        col8 = db6['Medicaments']
        j = 0
        for user in col6.find():
            textfield = MDRaisedButton(text=user['ID_Patient'], id='t' + str(j))
            textfield.size_hint_x = 1
            textfield.bind(on_release=lambda instance, tf=textfield: (self.gerer_choix(tf.text, 'idpatientrdv'),self.dialog.dismiss()))
            textfields.append(textfield)
            j += 1

        self.dialog = MDDialog(
            title="Processus de choix",
            type="custom",
            content_cls=DialogContent1(textfields),
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: self.dialog.dismiss())],
        )

        j = 0
        textfields = []
        buttons = []
        for user in col7.find():
            textfield = MDRaisedButton(text=user['Nom_Acte'], id='t' + str(j))
            textfield.bind(on_release=lambda instance, tf=textfield: (self.gerer_choix(tf.text, 'acterdv'),self.dialog1.dismiss()))
            textfield.size_hint_x = 1
            buttons.append(textfield)
            j += 1
        self.dialog1 = MDDialog(
            title="Processus de choix",
            type="custom",
            content_cls=DialogContent1(buttons),
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: self.dialog1.dismiss())],
        )

        textfields = []
        buttons = []
        i = 0
        for user in col8.find():
            textfield = MDRaisedButton(text=user['Nom du médicament'], id='t' + str(i))
            textfield.bind(on_release=lambda instance, tf=textfield: (self.gerer_choix(tf.text, 'med'),self.dialog2.dismiss()))
            textfield.size_hint_x = 1
            buttons.append(textfield)
            i += 1
        self.dialog2 = MDDialog(
            title="Processus de choix",
            type="custom",
            content_cls=DialogContent1(buttons),
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: self.dialog2.dismiss())],
        )
        textfields = []
        buttons = []
        i = 0
        for user in col7.find():
            textfield = MDRaisedButton(text=user['ID_Acte'], id='t' + str(i))
            textfield.bind(on_release=lambda instance, tf=textfield: (self.gerer_choix(tf.text, 'idacte'),self.dialog3.dismiss()))
            textfield.size_hint_x = 1
            buttons.append(textfield)
            i += 1
        self.dialog3 = MDDialog(
            title="Processus de choix",
            type="custom",
            content_cls=DialogContent1(buttons),
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: self.dialog3.dismiss())],
        )
        textfields = []
        buttons = []
        i = 0
        labels = ['Especes', 'Cheques']
        for label in labels:
            textfield = MDRaisedButton(text=label, id='t' + str(i))
            textfield.bind(on_release=lambda instance, tf=textfield: (self.gerer_choix(tf.text, 'modpaie'),self.dialog4.dismiss()))
            textfield.size_hint_x = 1
            buttons.append(textfield)
            i += 1
        self.dialog4 = MDDialog(
            title="Processus de choix",
            type="custom",
            content_cls=DialogContent1(buttons),
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: self.dialog4.dismiss())],
        )



    def gerer_choix(self,textt,cls):

        if cls=='idpatientrdv' and self.ids.scm.current == 'display_rendez_vous':
            self.ids.text2_rdv.text=textt
            self.dialog.dismiss()
        elif cls=='idpatientrdv' and self.ids.scm.current == 'display_visite':
            self.ids.text2_visite.text=textt
            self.dialog.dismiss()
        elif cls=='idpatientrdv' and self.ids.scm.current == 'display_paiement':
            self.ids.text2_p.text=textt
            self.dialog.dismiss()
        elif cls=='idpatientrdv' and self.ids.scm.current == 'display_presc':
            self.ids.text2_presc.text=textt
            self.dialog.dismiss()
        elif cls== 'acterdv' and self.ids.scm.current == 'display_rendez_vous':
            self.ids.text5_rdv.text=textt
            self.dialog.dismiss()
        elif cls== 'acterdv' and self.ids.scm.current == 'display_visite':
            self.ids.text5_visite.text=textt
            self.dialog.dismiss()
        elif cls== 'med':
            self.ids.text3_presc.text=textt
            self.dialog.dismiss()
        elif cls== 'idacte':
            self.ids.text3_p.text=textt
            self.dialog.dismiss()
        elif cls== 'modpaie':
            self.root.get_screen('admin').ids.text7_p.text=textt
            self.dialog.dismiss()








    def Dossier(self):
        textfields = []
        labels = ["Informations personnelles du patient", 'Historique des visites']
        i = 0
        for label in labels :
            textfield = MDRaisedButton(text=label, id='t' + str(i))
            textfield.size_hint_x = 1
            textfields.append(textfield)
            i += 1

        dialog = MDDialog(
            title="Dossier du patient",
            type="custom",
            content_cls=DialogContent1(textfields),
            buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
        )
        dialog.open()
        textfields[0].bind(on_release=lambda instance: self.dossier_info('info',dialog))
        textfields[1].bind(on_release=lambda instance: self.dossier_info('historique', dialog))


    def dossier_info(self,button,dialog):
        if button == 'info':
            textfields = []
            labels = ["Nom", 'Prenom','Date de naissance','Telephone','Adresse','Antecedents medicaux','Email','Assurance']
            i = 0
            for label in labels:
                textfield = MDTextField(hint_text=label, id='t' + str(i))
                textfield.size_hint_x = 1
                textfields.append(textfield)
                i += 1
            textfields[0].text=self.ids.text2.text
            textfields[1].text=self.ids.text3.text
            textfields[2].text=self.ids.text4.text
            textfields[3].text=self.ids.text5.text
            textfields[4].text=self.ids.text6.text
            textfields[5].text=self.ids.text7.text
            textfields[6].text=self.ids.text8.text
            textfields[7].text=self.ids.text9.text
            for j in range(8):
                textfields[j].disabled=True
            dialog = MDDialog(
                title="Dossier du patient",
                type="custom",
                content_cls=DialogContent1(textfields),
                buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
            )
            dialog.open()

        else:
            t=0
            _users = OrderedDict(Dates_des_visites_précédentes={},Seances={},Nom_Actes={},Couts_Actes={},Montants_payes={},Montants_reste_a_payer={},Nom_du_medicament_prescrit={},Dates_Transaction={})
            cl7=MongoClient()
            db = cl7['Admin_cabinet']
            col=db['Paiements']
            col1=db['Rendez_vous']
            col2=db['Actes']
            col3=db['Prescriptions']
            i=0
            for user0 in col1.find():
                if user0['ID_Patient'] == self.ids.text1.text:
                    _users['Dates_des_visites_précédentes'][i]=user0['Date']
                    _users['Nom_Actes'][i]=user0['Nom_Acte']


                    t+=1
                    for user3 in col2.find():
                        idacte=user3['ID_Acte']
                        for user4 in col3.find():
                            med=user4['Nom du medicament']
                            for user in col.find():
                                if user['ID_Patient']==self.ids.text1.text and idacte==user['ID_Acte']and (user['Date de la transaction'] ==_users['Dates_des_visites_précédentes'][i]) and (user['ID_Patient']==user4['ID_Patient']):
                                    t+=1

                                    _users['Montants_payes'][i]=user['Montant payé']
                                    _users['Montants_reste_a_payer'][i]=user['Montant reste a payer']
                                    _users['Dates_Transaction'][i] =_users['Dates_des_visites_précédentes'][i]
                                    _users['Couts_Actes'][i] = str(int(user['Montant payé'])+int(user['Montant reste a payer']))
                                    _users['Nom_du_medicament_prescrit'][i] = med
                                    _users['Seances'][i] = user['Seance']


                i+=1
            if t%2==0 and t!=0:
                app=App.get_running_app()
                original_table_widget =_users
                print(original_table_widget)
                print('adsm')
                rdvstable1 = DataTable(table=original_table_widget)
                print(rdvstable1)
                content = MDBoxLayout(orientation="vertical", size_hint=(1, 0.998), padding="10dp", spacing="10dp",
                                      pos_hint={'center_x': 0.5, 'center_y': 0.6})
                content.add_widget(rdvstable1)
                app.root.get_screen('historique').add_widget(content)
                app.root.current='historique'
            else:
                dialog = MDDialog(
                    title="OOPS",
                    text="Manque de donnees.",
                    buttons=[MDFlatButton(text="Close", on_release=lambda *args: dialog.dismiss())],
                )
                dialog.open()

class DialogContent1(ScrollView):
        def __init__(self, textfields, **kwargs):
            super().__init__(**kwargs)
            self.orientation = "vertical"
            self.size_hint = (1, None)
            self.bar_width = "6dp"
            self.do_scroll_x = False

            content = MDBoxLayout(orientation="vertical", size_hint=(1, None), padding="10dp", spacing="10dp")
            content.bind(minimum_height=content.setter("height"))
            for textfield in textfields:
                content.add_widget(textfield)

            self.add_widget(content)


class DialogContent2(ScrollView):
        def __init__(self, table, **kwargs):
            super().__init__(**kwargs)
            self.orientation = "vertical"
            self.size_hint = (1, None)
            self.bar_width = "6dp"
            self.do_scroll_x = False

            content = MDBoxLayout(orientation="vertical", size_hint=(1, None), padding="30dp", spacing="10dp")
            # content.bind(minimum_height=content.setter("height"))
            content.add_widget(table)

            self.add_widget(content)




