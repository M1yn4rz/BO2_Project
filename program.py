import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import networkx as nx
import random
import graph as gp
import matplotlib.image as mpimg
import algorithm as ag
import time
import threading
from pubsub import pub
import sys
import time
import pandas as pd
import wx.grid as gridlib
from matplotlib.ticker import MaxNLocator





class MyFrame(wx.Frame):


# ________________ CLASS CONSTRUCTOR ________________ #
    
    def __init__(self, *args, **kw):

        super(MyFrame, self).__init__(*args, **kw)
        self.panel = wx.Panel(self)
        
        self.parameters()
        self.buttons()
        self.variables()
        
        self.window = 'Map'
        self.print_graph()
        
        self.panel.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.SetSize((1280, 756))
        self.SetBackgroundColour(wx.Colour(0, 0, 0))

        self.Show(True)


# ________________ PARAMETERS ________________ #
        
    def parameters(self):

        self.df = pd.read_csv("data/packages.csv")
        self.dt = pd.read_csv("data/data.csv")
        self.dl = pd.read_csv("data/locomotives.csv")
        self.dw = pd.read_csv("data/wagons.csv")

        self.list_min_f = []
        self.list_max_f = []
        self.list_mean_f = []
        self.X = []
        self.best_result = ""
        self.no_text = ""
        self.time_to_the_end = ""
        self.G = gp.Graph()
        self.image = mpimg.imread("data\poland.png")
        self.thread = None
        self.stop_event = threading.Event()


# ________________ BUTTONS ________________ #
        
    def buttons(self):

        self.close_button()
        self.start_button()
        self.stop_button()
        self.graph_button()
        self.chart_button()
        self.result_button()
        self.packages_button()
        self.trains_button()
        self.nexttrain_button_()
        self.previoustrain_button_()
        self.showtrack_button_()
        

# ________________ VARIABLES ________________ #

    def variables(self):

        self.variable_size_population = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_size_population.SetValue("250")
        self.variable_size_population.SetPosition((1100, 250))
        self.label_size_population = wx.StaticText(self.panel, label="Size population")
        self.label_size_population.SetPosition((1100, 233))
        self.label_size_population.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_epochs = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_epochs.SetValue("30")
        self.variable_epochs.SetPosition((1100, 300))
        self.label_epochs = wx.StaticText(self.panel, label="Number of epochs")
        self.label_epochs.SetPosition((1100, 283))
        self.label_epochs.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_previous_population = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_previous_population.SetValue("20")
        self.variable_previous_population.SetPosition((1100, 350))
        self.label_previous_population = wx.StaticText(self.panel, label="Previous population in %")
        self.label_previous_population.SetPosition((1100, 333))
        self.label_previous_population.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_mutate_power = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_mutate_power.SetValue("10")
        self.variable_mutate_power.SetPosition((1100, 400))
        self.label_mutate_power = wx.StaticText(self.panel, label="Mutate power in %")
        self.label_mutate_power.SetPosition((1100, 383))
        self.label_mutate_power.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_number_of_trains = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_number_of_trains.SetValue("8")
        self.variable_number_of_trains.SetPosition((1100, 450))
        self.label_number_of_trains = wx.StaticText(self.panel, label="Number of trains")
        self.label_number_of_trains.SetPosition((1100, 433))
        self.label_number_of_trains.SetForegroundColour(wx.Colour(255, 255, 255))

        city_choices = self.dt['City'].tolist()  # Dodaj własne opcje
        self.variable_city_start = wx.ComboBox(self.panel, value=city_choices[0], choices=city_choices, style=wx.CB_READONLY)
        self.variable_city_start.SetPosition((1100, 500))
        self.variable_city_start.SetSize((110, 23))
        self.label_city_start = wx.StaticText(self.panel, label="Start city ID")
        self.label_city_start.SetPosition((1100, 483))
        self.label_city_start.SetForegroundColour(wx.Colour(255, 255, 255))

        self.label_time_to_end = wx.StaticText(self.panel, label = "Ready to start")
        self.label_time_to_end.SetPosition((1100, 583))
        self.label_time_to_end.SetForegroundColour(wx.Colour(255, 255, 255))

        self.label_result = wx.StaticText(self.panel, label=self.no_text, style=wx.ALIGN_LEFT)
        self.label_result.Wrap(800)
        self.label_result.SetPosition((218, 0))
        self.label_result.SetForegroundColour(wx.Colour(255, 255, 255))

        self.label_track_train = wx.StaticText(self.panel, label=self.no_text, style=wx.ALIGN_LEFT)
        self.label_track_train.Wrap(200)
        self.label_track_train.SetPosition((20, 400))
        self.label_track_train.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_train_number = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        self.variable_train_number.SetValue("1")
        self.variable_train_number.SetPosition((94, 250))
        self.variable_train_number.SetSize((30, 30))
        self.label_train_number = wx.StaticText(self.panel, label="Train number")
        self.label_train_number.SetPosition((54, 233))
        self.label_train_number.SetForegroundColour(wx.Colour(255, 255, 255))


# ________________ START BUTTON ________________ #

    def on_start_enter(self, event):
        self.start_button.SetBackgroundColour(wx.Colour(255, 165, 0))  # R, G, B
        self.start_button.Refresh()

    def on_start_leave(self, event):
        self.start_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.start_button.Refresh()

    def click_start_button(self, event):

        self.list_min_f = []
        self.list_max_f = []
        self.list_mean_f = []
        self.X = []

        self.destroy_window()
        self.print_chart()
        self.window = 'Chart'
        self.label_time_to_end.SetLabel("Generating first population")
        self.label_time_to_end.SetForegroundColour(wx.Colour(255, 255, 255))

        pub.subscribe(self.update_chart, 'update_chart')
        pub.subscribe(self.time_to_end, 'update_time')
        pub.subscribe(self.wrong_variables, 'update_variables')
        self.thread = threading.Thread(target = self.start_algorithm)
        self.stop_event.clear()
        self.thread.start()

    def start_algorithm(self):

        list_min_f = []
        list_max_f = []
        list_mean_f = []
        X = []

        size_population = int(self.variable_size_population.GetValue())
        epochs = int(self.variable_epochs.GetValue())
        previous_population = int(self.variable_previous_population.GetValue())
        mutate_power = int(self.variable_mutate_power.GetValue())
        number_of_trains = int(self.variable_number_of_trains.GetValue())
        start_city = self.dt[self.dt['City'] == self.variable_city_start.GetValue()].index[0] + 1

        flag_size = False
        flag_epochs = False
        flag_previous = False
        flag_mutate = False
        flag_trains = False

        error = False

        if size_population < 100 or size_population > 1000:
            error = True
            flag_size = True

        if epochs < 5 or epochs > 100:
            error = True
            flag_epochs = True

        if previous_population < 1 or previous_population > 50:
            error = True
            flag_previous = True

        if mutate_power < 1 or mutate_power > 50:
            error = True
            flag_mutate = True

        if number_of_trains < 1 or number_of_trains > 20:
            error = True
            flag_trains = True

        pub.sendMessage('update_variables', flag_size = flag_size, flag_epochs = flag_epochs,
                            flag_previous = flag_previous, flag_mutate = flag_mutate, flag_trains = flag_trains)

        if error:
            pub.sendMessage('update_time', time_ = "ERROR")
            return None

        new_ag = ag.Algorithm(n = number_of_trains)
        
        population, previous, mutate = new_ag.start_AG(
                                size_population = size_population,  
                                previous_population = previous_population,
                                mutate_power = mutate_power,
                                start = start_city)
        
        for i in range(epochs):

            if self.stop_event.is_set():
                break

            start_time = time.time()

            population = new_ag.loop_AG(population, size_population, previous, mutate, start_city)
            goal_functions = [x.f for x in population]

            X.append(i + 1)
            list_min_f.append(min(goal_functions))
            list_max_f.append(max(goal_functions))
            list_mean_f.append(sum(goal_functions)/len(goal_functions))
            
            pub.sendMessage('update_chart', X=X, list_min_f=list_min_f,
                            list_max_f=list_max_f, list_mean_f=list_mean_f)
            
            end_time = time.time()

            time_ = (end_time - start_time) * (epochs - (i + 1))

            pub.sendMessage('update_time', time_ = int(time_))
            
        best_id = goal_functions.index(min(goal_functions))
        self.best_result = population[best_id]
        self.variable_train_number.SetValue(str(1))
        pub.sendMessage('update_time', time_ = int(0))

    def time_to_end(self, time_):
        if type(time_) == str:
            self.time_to_the_end = time_
            self.label_time_to_end.SetForegroundColour(wx.Colour(255, 0, 0))
        else:
            self.time_to_the_end = "Time to end: "
            if time_ >= 3600:
                self.time_to_the_end += str(time_//3600) + " h "
            if time_ >= 60:
                self.time_to_the_end += str((time_ - (time_//3600)*3600)//60) + " min "
            if time_ >= 1:
                self.time_to_the_end += str(time_ - (time_//3600)*3600 - (time_ - (time_//3600)*3600)//60*60) + " s "
            else:
                self.time_to_the_end = "Complete"
        self.label_time_to_end.SetLabel(self.time_to_the_end)
        
    def wrong_variables(self, flag_size = False, flag_epochs = False, flag_previous = False, flag_mutate = False, flag_trains = False):

        if flag_size:
            self.label_size_population.SetForegroundColour(wx.Colour(255, 0, 0))
            self.label_size_population.SetLabel("Size population (100 - 1000)")
        else:
            self.label_size_population.SetForegroundColour(wx.Colour(255, 255, 255))
            self.label_size_population.SetLabel("Size population")

        if flag_epochs:
            self.label_epochs.SetForegroundColour(wx.Colour(255, 0, 0))
            self.label_epochs.SetLabel("Number of epochs (5 - 100)")
        else:
            self.label_epochs.SetForegroundColour(wx.Colour(255, 255, 255))
            self.label_epochs.SetLabel("Number of epochs")

        if flag_previous:
            self.label_previous_population.SetForegroundColour(wx.Colour(255, 0, 0))
            self.label_previous_population.SetLabel("Previous population in % (1 - 50)")
        else:
            self.label_previous_population.SetForegroundColour(wx.Colour(255, 255, 255))
            self.label_previous_population.SetLabel("Previous population in %")

        if flag_mutate:
            self.label_mutate_power.SetForegroundColour(wx.Colour(255, 0, 0))
            self.label_mutate_power.SetLabel("Mutate power in % (1 - 50)")
        else:
            self.label_mutate_power.SetForegroundColour(wx.Colour(255, 255, 255))
            self.label_mutate_power.SetLabel("Mutate power in %")

        if flag_trains:
            self.label_number_of_trains.SetForegroundColour(wx.Colour(255, 0, 0))
            self.label_number_of_trains.SetLabel("Number of trains (1 - 20)")
        else:
            self.label_number_of_trains.SetForegroundColour(wx.Colour(255, 255, 255))
            self.label_number_of_trains.SetLabel("Number of trains")

        self.Refresh()

    def start_button(self):

        self.start_button = wx.Button(self.panel, label = "Start AG", size = (110, 30))
        self.start_button.Bind(wx.EVT_ENTER_WINDOW, self.on_start_enter)
        self.start_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_start_leave)
        self.Bind(wx.EVT_BUTTON, self.click_start_button, self.start_button)
        self.start_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.start_button.SetPosition((1100, 600))

    
# ________________ STOP BUTTON ________________ #
        
    def on_stop_enter(self, event):
        self.stop_button.SetBackgroundColour(wx.Colour(255, 165, 0))  # R, G, B
        self.stop_button.Refresh()

    def on_stop_leave(self, event):
        self.stop_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.stop_button.Refresh()

    def click_stop_button(self, event):
        self.stop_event.set()

    def stop_button(self):

        self.stop_button = wx.Button(self.panel, label = "Stop AG", size = (110, 30))
        self.stop_button.Bind(wx.EVT_ENTER_WINDOW, self.on_stop_enter)
        self.stop_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_stop_leave)
        self.Bind(wx.EVT_BUTTON, self.click_stop_button, self.stop_button)
        self.stop_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.stop_button.SetPosition((1100, 650))


# ________________ CLOSE BUTTON ________________ #
        
    def on_close_enter(self, event):
        self.close_button.SetBackgroundColour(wx.Colour(255, 165, 0))  # R, G, B
        self.close_button.Refresh()

    def on_close_leave(self, event):
        self.close_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.close_button.Refresh()

    def click_close_button(self, event):
        sys.exit()

    def close_button(self):

        self.close_button = wx.Button(self.panel, label = "Close", size = (110, 30))
        self.close_button.Bind(wx.EVT_ENTER_WINDOW, self.on_close_enter)
        self.close_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_close_leave)
        self.Bind(wx.EVT_BUTTON, self.click_close_button, self.close_button)
        self.close_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.close_button.SetPosition((1100, 50))


# ________________ GRAPH BUTTON ________________ #
        
    def on_graph_enter(self, event):
        self.graph_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.graph_button.Refresh()

    def on_graph_leave(self, event):
        self.graph_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.graph_button.Refresh()

    def click_graph_button(self, event):
        self.window = 'Map'
        self.destroy_window()
        self.print_graph()

    def graph_button(self):

        self.graph_button = wx.Button(self.panel, label = "Map", size = (110, 30))
        self.graph_button.Bind(wx.EVT_ENTER_WINDOW, self.on_graph_enter)
        self.graph_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_graph_leave)
        self.Bind(wx.EVT_BUTTON, self.click_graph_button, self.graph_button)
        self.graph_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.graph_button.SetPosition((54, 50))


# ________________ CHART BUTTON ________________ #
        
    def on_chart_enter(self, event):
        self.chart_button.SetBackgroundColour(wx.Colour(255, 165, 0))  # R, G, B
        self.chart_button.Refresh()

    def on_chart_leave(self, event):
        self.chart_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.chart_button.Refresh()

    def click_chart_button(self, event):
        self.destroy_window()
        self.print_chart()
        self.window = 'Chart'

    def chart_button(self):

        self.chart_button = wx.Button(self.panel, label = "Goal chart", size = (110, 30))
        self.chart_button.Bind(wx.EVT_ENTER_WINDOW, self.on_chart_enter)
        self.chart_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_chart_leave)
        self.Bind(wx.EVT_BUTTON, self.click_chart_button, self.chart_button)
        self.chart_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.chart_button.SetPosition((54, 100))


# ________________ RESULT BUTTON ________________ #

    def on_result_enter(self, event):
        self.result_button.SetBackgroundColour(wx.Colour(255, 165, 0))  # R, G, B
        self.result_button.Refresh()

    def on_result_leave(self, event):
        self.result_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.result_button.Refresh()

    def click_result_button(self, event):
        self.destroy_window()
        self.window = 'Result'
        self.label_result.SetLabel(str(self.best_result))

    def result_button(self):

        self.result_button = wx.Button(self.panel, label = "The best result", size = (110, 30))
        self.result_button.Bind(wx.EVT_ENTER_WINDOW, self.on_result_enter)
        self.result_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_result_leave)
        self.Bind(wx.EVT_BUTTON, self.click_result_button, self.result_button)
        self.result_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.result_button.SetPosition((54, 150))


# ________________ PACKAGES BUTTON ________________ #

    def on_packages_enter(self, event):
        self.packages_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.packages_button.Refresh()

    def on_packages_leave(self, event):
        self.packages_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.packages_button.Refresh()

    def click_packages_button(self, event):
        self.destroy_window()
        self.window = 'Packages'
        self.print_packages()

    def packages_button(self):

        self.packages_button = wx.Button(self.panel, label = "Packages", size = (110, 30))
        self.packages_button.Bind(wx.EVT_ENTER_WINDOW, self.on_packages_enter)
        self.packages_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_packages_leave)
        self.Bind(wx.EVT_BUTTON, self.click_packages_button, self.packages_button)
        self.packages_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.packages_button.SetPosition((1100, 100))


# ________________ ADD ROW BUTTON ________________ #
        
    def on_addrow_enter(self, event):
        self.addrow_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.addrow_button.Refresh()

    def on_addrow_leave(self, event):
        self.addrow_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.addrow_button.Refresh()

    def click_addrow_button(self, event):
        self.add_row()

    def addrow_button_(self):

        self.addrow_button = wx.Button(self.panel, label = "Add row", size = (110, 30))
        self.addrow_button.Bind(wx.EVT_ENTER_WINDOW, self.on_addrow_enter)
        self.addrow_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_addrow_leave)
        self.Bind(wx.EVT_BUTTON, self.click_addrow_button, self.addrow_button)
        self.addrow_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.addrow_button.SetPosition((800, 50))


# ________________ DELETE ROWS BUTTON ________________ #

    def on_deleterow_enter(self, event):
        self.deleterow_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.deleterow_button.Refresh()

    def on_deleterow_leave(self, event):
        self.deleterow_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.deleterow_button.Refresh()

    def click_deleterow_button(self, event):
        self.delete_rows()

    def deleterows_button_(self):

        self.deleterow_button = wx.Button(self.panel, label = "Delete rows", size = (110, 30))
        self.deleterow_button.Bind(wx.EVT_ENTER_WINDOW, self.on_deleterow_enter)
        self.deleterow_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_deleterow_leave)
        self.Bind(wx.EVT_BUTTON, self.click_deleterow_button, self.deleterow_button)
        self.deleterow_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.deleterow_button.SetPosition((800, 100))


# ________________ RANDOM PACKAGES BUTTON ________________ #
        
    def on_randompackages_enter(self, event):
        self.randompackages_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.randompackages_button.Refresh()

    def on_randompackages_leave(self, event):
        self.randompackages_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.randompackages_button.Refresh()

    def click_randompackages_button(self, event):
        number_rows = int(self.variable_number_rows.GetValue())
        min_packages = int(self.variable_min_packages.GetValue())
        max_packages = int(self.variable_max_packages.GetValue())

        data = {'From ID' : [],'From city' : [],'To ID' : [],'To city' : [],'How many' : []}
        new_df = pd.DataFrame(data)

        for _ in range(number_rows):
            from_city = random.randint(0, len(self.dt) - 1)
            to_city = random.randint(0, len(self.dt) - 1)
            while from_city == to_city:
                to_city = random.randint(0, len(self.dt) - 1)
            packages = random.randint(min_packages, max_packages)
            new_row = {'From ID' : self.dt['ID'][from_city],'From city' : self.dt['City'][from_city],'To ID' : self.dt['ID'][to_city],'To city' : self.dt['City'][to_city],'How many' : packages}
            new_df = new_df._append(new_row, ignore_index=True)

        new_df.to_csv("data/packages.csv", index=False)
        self.df = pd.read_csv("data/packages.csv")
        self.destroy_window()
        self.print_packages()

    def randompackages_button_(self):

        self.randompackages_button = wx.Button(self.panel, label = "Random packages", size = (110, 30))
        self.randompackages_button.Bind(wx.EVT_ENTER_WINDOW, self.on_randompackages_enter)
        self.randompackages_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_randompackages_leave)
        self.Bind(wx.EVT_BUTTON, self.click_randompackages_button, self.randompackages_button)
        self.randompackages_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.randompackages_button.SetPosition((800, 500))


# ________________ TRAINS BUTTON ________________ #
        
    def on_trains_enter(self, event):
        self.trains_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.trains_button.Refresh()

    def on_trains_leave(self, event):
        self.trains_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.trains_button.Refresh()

    def click_trains_button(self, event):
        self.destroy_window()
        self.window = 'Trains'
        self.print_trains()

    def trains_button(self):
        self.trains_button = wx.Button(self.panel, label = "Trains", size = (110, 30))
        self.trains_button.Bind(wx.EVT_ENTER_WINDOW, self.on_trains_enter)
        self.trains_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_trains_leave)
        self.Bind(wx.EVT_BUTTON, self.click_trains_button, self.trains_button)
        self.trains_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.trains_button.SetPosition((1100, 150))


# ________________ ADD ROW LOC BUTTON ________________ #
        
    def on_addrowloc_enter(self, event):
        self.addrowloc_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.addrowloc_button.Refresh()

    def on_addrowloc_leave(self, event):
        self.addrowloc_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.addrowloc_button.Refresh()

    def click_addrowloc_button(self, event):
        self.add_row_loc()

    def addrowloc_button_(self):
        self.addrowloc_button = wx.Button(self.panel, label = "Add row", size = (110, 30))
        self.addrowloc_button.Bind(wx.EVT_ENTER_WINDOW, self.on_addrowloc_enter)
        self.addrowloc_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_addrowloc_leave)
        self.Bind(wx.EVT_BUTTON, self.click_addrowloc_button, self.addrowloc_button)
        self.addrowloc_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.addrowloc_button.SetPosition((800, 50))


# ________________ DELETE ROWS LOC BUTTON ________________ #

    def on_deleterowloc_enter(self, event):
        self.deleterowloc_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.deleterowloc_button.Refresh()

    def on_deleterowloc_leave(self, event):
        self.deleterowloc_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.deleterowloc_button.Refresh()

    def click_deleterowloc_button(self, event):
        self.delete_rows_loc()

    def deleterowsloc_button_(self):
        self.deleterowloc_button = wx.Button(self.panel, label = "Delete rows", size = (110, 30))
        self.deleterowloc_button.Bind(wx.EVT_ENTER_WINDOW, self.on_deleterowloc_enter)
        self.deleterowloc_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_deleterowloc_leave)
        self.Bind(wx.EVT_BUTTON, self.click_deleterowloc_button, self.deleterowloc_button)
        self.deleterowloc_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.deleterowloc_button.SetPosition((800, 100))


# ________________ ADD ROW WAG BUTTON ________________ #
        
    def on_addrowwag_enter(self, event):
        self.addrowwag_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.addrowwag_button.Refresh()

    def on_addrowwag_leave(self, event):
        self.addrowwag_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.addrowwag_button.Refresh()

    def click_addrowwag_button(self, event):
        self.add_row_wag()

    def addrowwag_button_(self):
        self.addrowwag_button = wx.Button(self.panel, label = "Add row", size = (110, 30))
        self.addrowwag_button.Bind(wx.EVT_ENTER_WINDOW, self.on_addrowwag_enter)
        self.addrowwag_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_addrowwag_leave)
        self.Bind(wx.EVT_BUTTON, self.click_addrowwag_button, self.addrowwag_button)
        self.addrowwag_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.addrowwag_button.SetPosition((800, 410))


# ________________ DELETE ROWS WAG BUTTON ________________ #

    def on_deleterowwag_enter(self, event):
        self.deleterowwag_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.deleterowwag_button.Refresh()

    def on_deleterowwag_leave(self, event):
        self.deleterowwag_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.deleterowwag_button.Refresh()

    def click_deleterowwag_button(self, event):
        self.delete_rows_wag()

    def deleterowswag_button_(self):
        self.deleterowwag_button = wx.Button(self.panel, label = "Delete rows", size = (110, 30))
        self.deleterowwag_button.Bind(wx.EVT_ENTER_WINDOW, self.on_deleterowwag_enter)
        self.deleterowwag_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_deleterowwag_leave)
        self.Bind(wx.EVT_BUTTON, self.click_deleterowwag_button, self.deleterowwag_button)
        self.deleterowwag_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.deleterowwag_button.SetPosition((800, 460))


# ________________ NEXT TRAIN BUTTON ________________ #

    def on_nexttrain_enter(self, event):
        self.nexttrain_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.nexttrain_button.Refresh()

    def on_nexttrain_leave(self, event):
        self.nexttrain_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.nexttrain_button.Refresh()

    def click_nexttrain_button(self, event):
        train_number = int(self.variable_train_number.GetValue())
        try:
            if train_number + 1 <= len(self.best_result.DT):
                self.variable_train_number.SetValue(str(train_number + 1))
        except:
            pass

    def nexttrain_button_(self):

        self.nexttrain_button = wx.Button(self.panel, label = "+", size = (40, 30))
        self.nexttrain_button.Bind(wx.EVT_ENTER_WINDOW, self.on_nexttrain_enter)
        self.nexttrain_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_nexttrain_leave)
        self.Bind(wx.EVT_BUTTON, self.click_nexttrain_button, self.nexttrain_button)
        self.nexttrain_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.nexttrain_button.SetPosition((124, 250))


# ________________ PREVIOUS TRAIN BUTTON ________________ #

    def on_previoustrain_enter(self, event):
        self.previoustrain_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.previoustrain_button.Refresh()

    def on_previoustrain_leave(self, event):
        self.previoustrain_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.previoustrain_button.Refresh()

    def click_previoustrain_button(self, event):
        train_number = int(self.variable_train_number.GetValue())
        try:
            if train_number - 1 >= 1:
                self.variable_train_number.SetValue(str(train_number - 1))
        except:
            pass

    def previoustrain_button_(self):

        self.previoustrain_button = wx.Button(self.panel, label = "-", size = (40, 30))
        self.previoustrain_button.Bind(wx.EVT_ENTER_WINDOW, self.on_previoustrain_enter)
        self.previoustrain_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_previoustrain_leave)
        self.Bind(wx.EVT_BUTTON, self.click_previoustrain_button, self.previoustrain_button)
        self.previoustrain_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.previoustrain_button.SetPosition((54, 250))


# ________________ SHOW TRACK BUTTON ________________ #

    def on_showtrack_enter(self, event):
        self.showtrack_button.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.showtrack_button.Refresh()

    def on_showtrack_leave(self, event):
        self.showtrack_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.showtrack_button.Refresh()

    def click_showtrack_button(self, event):
        self.destroy_window()
        
        try:
            track = self.best_result.DT[int(self.variable_train_number.GetValue()) - 1]
            self.print_graph_track(track)
            text = ""
            i = 0
            for elem in track:
                text += "(" + str(int(elem[0])) + ")" + " " + str(self.dt['City'][elem[0] - 1]) + " -> "
                if i == 1:
                    text += "\n"
                    i = 0
                else:
                    i += 1
            text += "(" + str(int(track[-1][1])) + ")" + " " + str(self.dt['City'][track[-1][1] - 1])
            self.label_track_train.SetLabel(text)
        except:
            pass 

    def showtrack_button_(self):

        self.showtrack_button = wx.Button(self.panel, label = "Show track", size = (110, 30))
        self.showtrack_button.Bind(wx.EVT_ENTER_WINDOW, self.on_showtrack_enter)
        self.showtrack_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_showtrack_leave)
        self.Bind(wx.EVT_BUTTON, self.click_showtrack_button, self.showtrack_button)
        self.showtrack_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.showtrack_button.SetPosition((54, 300))


# ________________ GRAPH ________________ #

    def print_graph(self):

        self.figure, self.ax = plt.subplots()
        plt.imshow(self.image)
        pos = nx.get_node_attributes(self.G.G, 'coordinates')
        #edge_labels = {(u, v): d['weight'] for u, v, d in self.G.G.edges(data=True)}
        node_sizes = [self.G.G.nodes[node]['size'] for node in self.G.G.nodes]
        nx.draw(self.G.G, ax=self.ax, pos = pos, with_labels=True, font_weight='bold', node_size = node_sizes)
        #nx.draw_networkx_edge_labels(self.G.G, pos = pos, edge_labels = edge_labels, font_color = 'red', font_size = 7)
        self.ax.set_position([0, 0, 1, 1])
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        self.canvas.SetSize(218, 0, 827, 720)

    def print_graph_track(self, way):

        self.figure, self.ax = plt.subplots()
        plt.imshow(self.image)
        pos = nx.get_node_attributes(self.G.G, 'coordinates')
        node_sizes = [self.G.G.nodes[node]['size'] for node in self.G.G.nodes]
        nx.draw(self.G.G, ax=self.ax, pos = pos, with_labels=True, font_weight='bold', node_size = node_sizes)
        nx.draw_networkx_edges(self.G.G, pos = pos, edgelist = way, width = 3, edge_color = 'red')
        self.ax.set_position([0, 0, 1, 1])
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        self.canvas.SetSize(218, 0, 827, 720)
        

# ________________ CHART ________________ #
        
    def print_chart(self):

        self.figure, self.ax = plt.subplots()
        self.ax.set_position([0.1, 0.1, 0.8, 0.8])
        self.ax.plot(self.X, self.list_min_f, label = "Min goal function in epoch")
        self.ax.plot(self.X, self.list_max_f, label = "Max goal function in epoch")
        self.ax.plot(self.X, self.list_mean_f, label = "Mean goal function in epoch")
        self.ax.set_xlabel('Number of epoch', color = 'white')
        self.ax.set_ylabel('Goal function value', color = 'white')
        self.ax.set_title('Genetic Algorithm chart', color = 'white')
        self.ax.legend()
        self.ax.grid()
        self.figure.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.title.set_color('white')
        self.ax.tick_params(axis='both', colors='white')
        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        self.canvas.SetSize(218, 0, 827, 720)

    def update_chart(self, X, list_min_f, list_max_f, list_mean_f):

        self.X = X
        self.list_min_f = list_min_f
        self.list_max_f = list_max_f
        self.list_mean_f = list_mean_f

        if self.window == 'Chart':
            self.ax.clear()
            self.ax.set_position([0.1, 0.1, 0.8, 0.8])
            self.ax.plot(self.X, self.list_min_f, label="Min goal function in epoch")
            self.ax.plot(self.X, self.list_max_f, label="Max goal function in epoch")
            self.ax.plot(self.X, self.list_mean_f, label="Mean goal function in epoch")
            self.ax.set_xlabel('Number of epoch', color='white')
            self.ax.set_ylabel('Goal function value', color='white')
            self.ax.set_title('Genetic Algorithm chart', color='white')
            self.ax.legend()
            self.ax.grid()
            self.figure.patch.set_facecolor('black')
            self.ax.set_facecolor('black')
            self.ax.title.set_color('white')
            self.ax.tick_params(axis='both', colors='white')
            self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            self.canvas.draw()


# ________________ Packages ________________ #

    def print_packages(self):

        self.grid = gridlib.Grid(self.panel)
        self.grid.CreateGrid(self.df.shape[0], self.df.shape[1])
        for col in range(self.df.shape[1]):
            self.grid.SetColLabelValue(col, str(self.df.columns[col]))
        for row in range(self.df.shape[0]):
            for col in range(self.df.shape[1]):
                self.grid.SetCellValue(row, col, str(self.df.iloc[row, col]))
        self.grid.EnableEditing(True)
        self.locked_columns = [0, 2]
        self.choice_columns = [1, 3]
        self.editable_column = 4
        self.grid.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChanged)
        self.grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.on_cell_left_click)
        self.setup_columns()
        self.grid.SetPosition((218, 0))
        self.grid.SetSize((499, 720))
        self.addrow_button_()
        self.deleterows_button_()
        self.randompackages_button_()
        self.packages_variables()

    def setup_columns(self):
        for col in range(self.df.shape[1]):
            if col in self.locked_columns:
                self.grid.SetReadOnly(0, col, isReadOnly=True)
            elif col in self.choice_columns:
                self.setup_choice_column(col)

    def setup_choice_column(self, col):
        choices = sorted(self.dt['City'].unique())
        self.grid.SetCellEditor(0, col, gridlib.GridCellChoiceEditor(choices, allowOthers=False))

    def OnCellChanged(self, event):
        row = event.GetRow()
        col = event.GetCol()
        value = self.grid.GetCellValue(row, col)
        if col == self.editable_column:
            self.df.iloc[row, col] = int(value)
            self.df.to_csv('data/packages.csv', index=False)

    def on_cell_left_click(self, event):
        row = event.GetRow()
        col = event.GetCol()

        if col == self.editable_column:
            if not self.grid.IsReadOnly(row, col):
                self.grid.SetGridCursor(row, col)
        elif col in self.choice_columns:
            self.show_choice_dialog(row, col)
        else:
            self.grid.DisableCellEditControl()

    def show_choice_dialog(self, row, col):
        column_name = self.df.columns[col]
        cell_value = str(self.df.iloc[row, col])
        choices = sorted(self.dt['City'].unique())

        dlg = wx.SingleChoiceDialog(
            self,
            f'Wybierz wartość dla {column_name}',
            'Edytuj wartość',
            choices,
            wx.CHOICEDLG_STYLE
        )

        initial_selection = choices.index(cell_value) if cell_value in choices else 0
        dlg.SetSelection(initial_selection)

        if dlg.ShowModal() == wx.ID_OK:
            new_value = dlg.GetStringSelection()
            self.df.at[row, column_name] = new_value
            new_value_ID = self.dt.loc[self.dt['City'] == new_value, 'ID'].values[0]
            self.df.iloc[row, col - 1] = int(new_value_ID)
            self.grid.SetCellValue(row, col, str(new_value))
            self.grid.SetCellValue(row, col - 1, str(new_value_ID))
            self.df.to_csv('data/packages.csv', index=False)

        dlg.Destroy()

    def add_row(self):
        new_row = pd.Series(['', '', '', '', ''], index=self.df.columns)
        self.df = self.df._append(new_row, ignore_index=True)
        num_rows, num_cols = self.grid.GetNumberRows(), self.grid.GetNumberCols()
        self.grid.AppendRows(1)
        for col, value in enumerate(new_row):
            self.grid.SetCellValue(num_rows, col, str(value))
        self.df.to_csv('data/packages.csv', index=False)

    def delete_rows(self):

        self.df = self.df.dropna()
        self.destroy_window()
        self.df.to_csv('data/packages.csv', index=False)
        self.df = pd.read_csv('data/packages.csv')
        self.df = self.df.dropna()
        self.df.to_csv('data/packages.csv', index=False)
        self.print_packages()

    def packages_variables(self):

        self.variable_number_rows = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_number_rows.SetValue("50")
        self.variable_number_rows.SetPosition((800, 300))
        self.label_number_rows = wx.StaticText(self.panel, label="Number of rows")
        self.label_number_rows.SetPosition((800, 283))
        self.label_number_rows.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_min_packages = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_min_packages.SetValue("30")
        self.variable_min_packages.SetPosition((800, 350))
        self.label_min_packages = wx.StaticText(self.panel, label="Min packages")
        self.label_min_packages.SetPosition((800, 333))
        self.label_min_packages.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_max_packages = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_max_packages.SetValue("150")
        self.variable_max_packages.SetPosition((800, 400))
        self.label_max_packages = wx.StaticText(self.panel, label="Max packages")
        self.label_max_packages.SetPosition((800, 383))
        self.label_max_packages.SetForegroundColour(wx.Colour(255, 255, 255))


# ________________ TRAINS ________________ # 
        
    def print_trains(self):
        self.print_locomotives()
        self.print_wagons()
        self.addrowloc_button_()
        self.deleterowsloc_button_()
        self.addrowwag_button_()
        self.deleterowswag_button_()


# ________________ LOCOMOTIVES ________________ #
        
    def print_locomotives(self):
        self.grid_l = gridlib.Grid(self.panel)
        self.grid_l.CreateGrid(self.dl.shape[0], self.dl.shape[1])
        for col in range(self.dl.shape[1]):
            self.grid_l.SetColLabelValue(col, str(self.dl.columns[col]))
        for row in range(self.dl.shape[0]):
            for col in range(self.dl.shape[1]):
                self.grid_l.SetCellValue(row, col, str(self.dl.iloc[row, col]))
        self.grid_l.EnableEditing(True)
        self.grid_l.SetPosition((218, 0))
        self.grid_l.SetSize((499, 360))
        self.grid_l.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.on_grid_cell_changed_locomotives)

    def on_grid_cell_changed_locomotives(self, event):
        row = event.GetRow()
        col = event.GetCol()
        new_value = self.grid_l.GetCellValue(row, col)
        self.dl.iloc[row, col] = int(new_value)
        self.dl.to_csv("data/locomotives.csv", index=False)

    def add_row_loc(self):
        new_row = pd.Series(['', ''], index=self.dl.columns)
        self.dl = self.dl._append(new_row, ignore_index=True)
        num_rows, num_cols = self.grid_l.GetNumberRows(), self.grid_l.GetNumberCols()
        self.grid_l.AppendRows(1)
        for col, value in enumerate(new_row):
            self.grid_l.SetCellValue(num_rows, col, str(value))
        self.dl.to_csv('data/locomotives.csv', index=False)

    def delete_rows_loc(self):
        self.dl = self.dl.dropna()
        self.destroy_window()
        self.dl.to_csv('data/locomotives.csv', index=False)
        self.dl = pd.read_csv('data/locomotives.csv')
        self.dl = self.dl.dropna()
        self.dl.to_csv('data/locomotives.csv', index=False)
        self.print_trains()
        

# ________________ WAGONS ________________ #

    def print_wagons(self):
        self.grid_w = gridlib.Grid(self.panel)
        self.grid_w.CreateGrid(self.dw.shape[0], self.dw.shape[1])
        for col in range(self.dw.shape[1]):
            self.grid_w.SetColLabelValue(col, str(self.dw.columns[col]))
        for row in range(self.dw.shape[0]):
            for col in range(self.dw.shape[1]):
                self.grid_w.SetCellValue(row, col, str(self.dw.iloc[row, col]))
        self.grid_w.EnableEditing(True)
        self.grid_w.SetPosition((218, 360))
        self.grid_w.SetSize((499, 360))
        self.grid_w.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.on_grid_cell_changed_wagons)

    def on_grid_cell_changed_wagons(self, event):
        row = event.GetRow()
        col = event.GetCol()
        new_value = self.grid_w.GetCellValue(row, col)
        self.dw.iloc[row, col] = int(new_value)
        self.dw.to_csv("data/wagons.csv", index=False)

    def add_row_wag(self):
        new_row = pd.Series(['', '', ''], index=self.dw.columns)
        self.dw = self.dw._append(new_row, ignore_index=True)
        num_rows, num_cols = self.grid_w.GetNumberRows(), self.grid_w.GetNumberCols()
        self.grid_w.AppendRows(1)
        for col, value in enumerate(new_row):
            self.grid_w.SetCellValue(num_rows, col, str(value))
        self.dw.to_csv('data/wagons.csv', index=False)

    def delete_rows_wag(self):
        self.dw = self.dw.dropna()
        self.destroy_window()
        self.dw.to_csv('data/wagons.csv', index=False)
        self.dw = pd.read_csv('data/wagons.csv')
        self.dw = self.dw.dropna()
        self.dw.to_csv('data/wagons.csv', index=False)
        self.print_trains()


# ________________ DESTROY WINDOW ________________ #

    def destroy_window(self):
        self.label_result.SetLabel(self.no_text)
        self.label_track_train.SetLabel(self.no_text)
        try:
            self.canvas.Destroy()
        except:
            pass
        try:
            self.grid.Destroy()
            self.addrow_button.Destroy()
            self.deleterow_button.Destroy()
            self.randompackages_button.Destroy()
            self.variable_max_packages.Destroy()
            self.variable_min_packages.Destroy()
            self.variable_number_rows.Destroy()
            self.label_max_packages.Destroy()
            self.label_min_packages.Destroy()
            self.label_number_rows.Destroy()
        except:
            pass
        try:
            self.grid_l.Destroy()
            self.grid_w.Destroy()
            self.addrowloc_button.Destroy()
            self.deleterowloc_button.Destroy()
            self.addrowwag_button.Destroy()
            self.deleterowwag_button.Destroy()
        except:
            pass





# ________________ MAIN FUNCTION ________________ #

if __name__ == '__main__':

    app = wx.App(False)
    frame = MyFrame(None, title = 'Genetics Algorithm')

    app.MainLoop()