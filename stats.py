from kivy.clock import Clock
from kivy.lang import Builder
from pymongo import MongoClient
from kivy.app import App
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
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
Builder.load_file('stats.kv')

class StatsApp(Screen):
    def generate_plot(self):
        # Generate data
        #x = np.linspace(0, 2 * np.pi, 100)
        #y = np.sin(x)
        app=App.get_running_app()
        year_count=app.year_count
        years = list(year_count.keys())
        counts = list(year_count.values())

        fig, ax = plt.subplots()
        ax.bar(years, counts)
        plt.xlabel("Années")
        plt.ylabel("Personnes")
        plt.title("Nombre de nouveaux patient/années")
        # Create the plot
        #fig, ax = plt.subplots()
        #ax.plot(x, y)

        # Create a FigureCanvasKivyAgg instance and add the plot to it
        canvas = FigureCanvasKivyAgg(fig)

        # Add the canvas to the screen
        self.ids.plot_box.add_widget(canvas)


        from mpl_toolkits.mplot3d import Axes3D

        # Define acts and their corresponding patient counts
        acts = []
        CLIENT=MongoClient()
        db=CLIENT['Admin_cabinet']
        col=db['Actes']
        col1=db['Rendez-vous']
        for user in col.find():
            acts.append(user["Nom_Acte"])
        count = {}
        for person in col1.find():
            name_acte = person["Nom_Acte"]
            if  person['Seance']=='1':
                if name_acte in count:
                    count[name_acte] += 1
                else:
                    count[name_acte] = 1
            else:
                pass

        acts = []
        CLIENT = MongoClient()
        db = CLIENT['Admin_cabinet']
        col = db['Actes']
        col1 = db['Visite_de_la_journee']
        for user in col.find():
            acts.append(user["Nom_Acte"])
        count = {}
        for person in col1.find():
            name_acte = person["Nom_Acte"]
            if person['Seance'] == '1':
                if name_acte in count:
                    count[name_acte] += 1
                else:
                    count[name_acte] = 1
                    print('adam',name_acte)
            else:
                pass


        patient_counts = list(count.values())
        print('adam')

        # Example patient counts

        # Calculate total number of patients
        total_patients = sum(patient_counts)
        print(total_patients)

        # Calculate heights based on patient counts
        heights = [countt / total_patients for countt in patient_counts]

        # Calculate gaps between cubes
        gap = 10  # Gap between cubes
        num_cubes = len(heights)
        print('adam',num_cubes,heights)
        total_width = num_cubes + (num_cubes - 1) * gap
        cube_width = 1

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot cubes with proportional heights and gaps
        for i, (height, act) in enumerate(zip(heights, acts)):
            x = i * (cube_width + gap)
            cube_coordinates = [
                (1, 1, height), (1, 1, 0), (1, 0, 0), (1, 0, height),  # Front face
                (0, 1, height), (0, 1, 0), (0, 0, 0), (0, 0, height)  # Back face
            ]
            cube = [(coord[0] + x, coord[1], coord[2]) for coord in cube_coordinates]
            ax.bar3d(x, 0, 0, cube_width*8, cube_width, height, color='b')

            # Add label for each cube
            #ax.text(x + 0.5, 0.5, height + 0.1, act, ha='center', va='center', fontsize=10, color='black')

        # Set axis labels and ticks
        #ax.set_xlabel('Acts')
        ax.set_ylabel('Y')
        ax.set_zlabel('Patient Count')
        ax.set_xticks(range(num_cubes))
        ax.set_xticklabels(acts,ha="right", rotation=45)
        #, rotation = 45, ha = 'right'
        #ax.tick_params(axis='x', labelsize=8, which='both')
        #plt.subplots_adjust(bottom=0.2)



        # Set plot limits to include all cubes
        ax.set_xlim3d(0, total_width)
        ax.set_ylim3d(0, cube_width)
        ax.set_zlim3d(0, max(heights))

        # Show the plot


        # Create a 3D plot
        canvas = FigureCanvasKivyAgg(fig)

        # Add the canvas to the screen
        self.ids.plot_box.add_widget(canvas)




