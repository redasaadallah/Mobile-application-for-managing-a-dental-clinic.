from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from collections import OrderedDict
from pymongo import MongoClient
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.datatables import MDDataTable
from hover import HoverIconList
from kivy.metrics import dp
import numpy as np
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.label import Label

Builder.load_string('''
<DataTable>:
    id: main_win

    RecycleView:
        viewclass: 'CustButton'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            #default_size: (None,250)
            #default_size_hint: (1,None)
            size_hint: None,None
            height: self.minimum_height
            width: self.minimum_width
            spacing: 1
<CustButton@Button>:
    #size_hint: None, None
    #size: dp(200), dp(100)  # Adjust the size to fit your layout
    #text_size: self.size  # Enable text wrapping within the button's size
    halign: "center"  # Center the text horizontally
    valign: "middle"  # Center the text vertically
    font_size:11
    bold:True
    multiline: False 
    #bcolor: (1,1,1,1)
    #background_color:app.theme_cls.accent_color
    #canvas.before:
        #Color:
            #rgba: root.background_color
        #Rectangle:
            #size: self.size
            #pos: self.pos
    on_release:app.on_button_click_table(self);app.root.get_screen('asst').on_button_click_table(self)        
''')

class DataTable(BoxLayout):
    def __init__(self,table, **kwargs):
        super().__init__(**kwargs)

         # Access the first button

        rendez_vous = table
        col_titles = [k for k in rendez_vous.keys()]
        rows_len = len(rendez_vous[col_titles[0]])
        self.columns = len(col_titles)

        self.row = rows_len

        # print(rows_len)
        self.table_data = []
        for t in col_titles:
            #self.table_data.append({'text': str(t), 'size_hint_y': None, 'height': 80,'background_color':(1, 0, 0, 1)})
            self.table_data.append(
                {'text': str(t), 'size_hint_y': None, 'size_hint_x': None, 'width': 230, 'height': 30,
                 'background_color': (0, 0, 1, 1)})

        for r in range(rows_len):
            for t in col_titles:
                #self.table_data.append({'text': str(rendez_vous[t][r]), 'size_hint_y': None, 'height': 40, 'id': r,'background_color': (0, 1, 0, 1) })
                self.table_data.append(
                    {'text': str(rendez_vous[t][r]), 'size_hint_y': None, 'size_hint_x': None, 'width': 230,
                     'height': 30, 'id': r, 'background_color': (0/255,204/255,0/255,1)})

        self.table_data_array = np.array(self.table_data)
        self.table_data_array.shape = (rows_len + 1, self.columns)
        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = self.table_data














    def get_patients(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Patients
        _users = OrderedDict(Patients_Number={},Noms={}, Prenoms={}, Dates_de_naissance={}, Telephones={},Adresses={},Antecedents_medicaux={},Emails={},Assurances={})
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
            Adresse.append(user['Adresse'])
            Telephones.append(user['Telephone'])
            Ant.append(user['Antecedents medicaux'])
            email.append(user['Email'])
            pt.append(user['patientNumber'])
            assu.append(user['Assurance'])
        users_length = len(Noms)
        iteration = 0
        while iteration < users_length:
            _users['Noms'][iteration] = Noms[iteration]
            _users['Prenoms'][iteration] = Prenoms[iteration]
            _users['Dates_de_naissance'][iteration] = Dates_de_naissance[iteration]
            _users['Adresses'][iteration] = Adresse[iteration]
            _users['Telephones'][iteration] = Telephones[iteration]
            _users['Antecedents_medicaux'][iteration] = Ant[iteration]
            _users['Emails'][iteration] = email[iteration]
            _users['Patients_Number'][iteration] = pt[iteration]
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
    def click(self):
        print('yasine')

    def get_visites(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Visite_de_la_journee
        _users = OrderedDict(ID_de_la_visite={},PatientNumber={}, Date_visite={}, Heure_visite={}, Traitement_effectué={},Notes_ou_remarques_supplémentaires={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]

        for user in users.find():
            Noms.append(user['ID de la visite'])
            Prenoms.append(user['ID du patient'])
            Dates_de_naissance.append(user['Date de la visite'])
            Telephones.append(user['Heure de la visite'])
            Adresse.append(user['Traitement effectué'])
            Ant.append(user['Notes ou remarques supplémentaires'])

        users_length = len(Noms)
        iteration = 0
        while iteration < users_length:
            _users['ID_de_la_visite'][iteration] = Noms[iteration]
            _users['PatientNumber'][iteration] = Prenoms[iteration]
            _users['Date_visite'][iteration] = Dates_de_naissance[iteration]
            _users['Heure_visite'][iteration] = Telephones[iteration]
            _users['Traitement_effectué'][iteration] = Adresse[iteration]
            _users['Notes_ou_remarques_supplémentaires'][iteration] = Ant[iteration]
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
            Noms.append(user["ID du reflet"])
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
        _users = OrderedDict(ID_Prescription={},PatientNumber={}, Medicament_prescrit={}, Psologie={}, Duree_de_prescription={},Statut_prescription={},Notes_supplementaires={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]
        notes=[]

        for user in users.find():
            Noms.append(user["ID de la prescription"])
            Prenoms.append(user["ID du patient"])
            Dates_de_naissance.append(user["Médicaments prescrits"])
            Telephones.append(user["Posologie"])
            Adresse.append(user["Durée de la prescription"])
            Ant.append(user['Statut de la prescription'])
            notes.append(user['Notes supplémentaires'])

        users_length = len(Noms)
        print(Noms)
        iteration = 0
        while iteration < users_length:
            _users['ID_Prescription'][iteration] = Noms[iteration]
            _users['PatientNumber'][iteration] = Prenoms[iteration]
            _users['Medicament_prescrit'][iteration] = Dates_de_naissance[iteration]
            _users['Psologie'][iteration] = Telephones[iteration]
            _users['Duree_de_prescription'][iteration] = Adresse[iteration]
            _users['Statut_prescription'][iteration] = Ant[iteration]
            _users['Notes_supplementaires'][iteration] = notes[iteration]
            iteration += 1

        return (_users)

    def get_actes(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Actes
        _users = OrderedDict(ID_acte={},Nom_acte={},Description_acte ={}, Coût_acte={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []

        for user in users.find():
            Noms.append(user["ID de l'acte"])
            Prenoms.append(user["Nom de l'acte"])
            Dates_de_naissance.append(user["Description de l'acte"])
            Telephones.append(user["Coût de l'acte"])

        users_length = len(Noms)
        print(Noms)
        iteration = 0
        while iteration < users_length:
            _users['ID_acte'][iteration] = Noms[iteration]
            _users['Nom_acte'][iteration] = Prenoms[iteration]
            _users['Description_acte'][iteration] = Dates_de_naissance[iteration]
            _users['Coût_acte'][iteration] = Telephones[iteration]
            iteration += 1

        return (_users)

    def get_medicament(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Medicaments
        _users = OrderedDict(ID_médicament={},Nom_médicament={}, Description_du_médicament={}, Dosage_médicament={}, Stock_disponible={},Fournisseur={},Date_expiration={})
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
        print(Noms)
        iteration = 0
        while iteration < users_length:

            _users['ID_médicament'][iteration] = Noms[iteration]
            _users['Nom_médicament'][iteration] = Prenoms[iteration]
            _users['Description_du_médicament'][iteration] = Dates_de_naissance[iteration]
            _users['Dosage_médicament'][iteration] = Telephones[iteration]
            _users['Stock_disponible'][iteration] = Adresse[iteration]
            _users['Date_expiration'][iteration] = notes[iteration]
            _users['Fournisseur'][iteration] = Ant[iteration]
            iteration += 1

        return (_users)


    def get_paiement(self):
        client = MongoClient()
        db = client.Admin_cabinet
        users = db.Paiements
        _users = OrderedDict(ID_Transaction={},ID_Patients={}, ID_Actes={}, Montant_payé={}, Montant_reste_a_payer={},Modes_Paiements={},Dates_transaction={},Statut_transaction={},Description_transaction={})
        Noms = []
        Prenoms = []
        Dates_de_naissance = []
        Telephones = []
        Adresse=[]
        Ant=[]
        tr=[]
        dtr=[]
        notes=[]

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
            iteration += 1

        return (_users)
