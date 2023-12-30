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





class MyFrame(wx.Frame):


# ________________ CLASS CONSTRUCTOR ________________ #
    
    def __init__(self, *args, **kw):

        super(MyFrame, self).__init__(*args, **kw)
        self.panel = wx.Panel(self)

        self.df = pd.read_csv("data/packages.csv")
        self.dt = pd.read_csv("data/data.csv")
        self.list_min_f = []
        self.list_max_f = []
        self.list_mean_f = []
        self.X = []
        self.best_result = ""
        self.no_text = ""
        self.time_to_the_end = ""

        self.window = 'Map'
        self.print_graph()
        self.buttons()
        self.variables()
        
        self.panel.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.SetSize((1280, 756))
        self.SetBackgroundColour(wx.Colour(0, 0, 0))

        self.Show(True)


# ________________ BUTTONS ________________ #
        
    def buttons(self):

        self.close_button()
        self.start_button()
        self.graph_button()
        self.chart_button()
        self.result_button()
        self.packages_button()


# ________________ VARIABLES ________________ #

    def variables(self):

        self.variable_size_population = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_size_population.SetValue("100")
        self.variable_size_population.SetPosition((1100, 350))
        self.label_size_population = wx.StaticText(self.panel, label="Size population")
        self.label_size_population.SetPosition((1100, 333))
        self.label_size_population.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_epochs = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_epochs.SetValue("100")
        self.variable_epochs.SetPosition((1100, 400))
        self.label_epochs = wx.StaticText(self.panel, label="Number of epochs")
        self.label_epochs.SetPosition((1100, 383))
        self.label_epochs.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_previous_population = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_previous_population.SetValue("1")
        self.variable_previous_population.SetPosition((1100, 450))
        self.label_previous_population = wx.StaticText(self.panel, label="Previous population in %")
        self.label_previous_population.SetPosition((1100, 433))
        self.label_previous_population.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_mutate_power = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_mutate_power.SetValue("5")
        self.variable_mutate_power.SetPosition((1100, 500))
        self.label_mutate_power = wx.StaticText(self.panel, label="Mutate power in %")
        self.label_mutate_power.SetPosition((1100, 483))
        self.label_mutate_power.SetForegroundColour(wx.Colour(255, 255, 255))

        self.variable_number_of_trains = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.variable_number_of_trains.SetValue("6")
        self.variable_number_of_trains.SetPosition((1100, 550))
        self.label_number_of_trains = wx.StaticText(self.panel, label="Number of trains")
        self.label_number_of_trains.SetPosition((1100, 533))
        self.label_number_of_trains.SetForegroundColour(wx.Colour(255, 255, 255))

        self.label_time_to_end = wx.StaticText(self.panel, label = "Ready to start")
        self.label_time_to_end.SetPosition((1100, 633))
        self.label_time_to_end.SetForegroundColour(wx.Colour(255, 255, 255))

        self.label_result = wx.StaticText(self.panel, label=self.no_text, style=wx.ALIGN_LEFT)
        self.label_result.Wrap(827)
        self.label_result.SetPosition((218, 0))
        self.label_result.SetForegroundColour(wx.Colour(255, 255, 255))


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
        self.label_time_to_end.SetLabel("Generating start population")

        pub.subscribe(self.update_chart, 'update_chart')
        pub.subscribe(self.time_to_end, 'update_time')
        thread = threading.Thread(target = self.start_algorithm)
        thread.start()

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

        SL =[[50, 4], 
            [35, 2], 
            [45, 3]]
    
        SW =   [[30, 30, 100],
                [20, 15, 50],
                [15, 20, 30]]

        new_ag = ag.Algorithm(SL, SW, n = number_of_trains)
        
        population, previous, mutate = new_ag.start_AG(
                                size_population = size_population,  
                                previous_population = previous_population,
                                mutate_power = mutate_power)
        
        for i in range(epochs):

            start_time = time.time()

            population = new_ag.loop_AG(population, size_population, previous, mutate)
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
        self.best_result = str(population[best_id])

    def time_to_end(self, time_):
        self.time_to_the_end = ""
        if time_ >= 3600:
            self.time_to_the_end += str(time_//3600) + " h "
        if time_ >= 60:
            self.time_to_the_end += str((time_ - (time_//3600)*3600)//60) + " min "
        if time_ >= 1:
            self.time_to_the_end += str(time_ - (time_//3600)*3600 - (time_ - (time_//3600)*3600)//60*60) + " s "
        else:
            self.time_to_the_end = "Complete"
        self.label_time_to_end.SetLabel(self.time_to_the_end)

    def start_button(self):

        self.start_button = wx.Button(self.panel, label = "Start", size = (110, 30))
        self.start_button.Bind(wx.EVT_ENTER_WINDOW, self.on_start_enter)
        self.start_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_start_leave)
        self.Bind(wx.EVT_BUTTON, self.click_start_button, self.start_button)
        self.start_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.start_button.SetPosition((1100, 650))

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
        self.label_result.SetLabel(self.best_result)

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
        self.packages_button.SetPosition((1100, 150))


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
        self.print_packages()

    def randompackages_button_(self):

        self.randompackages_button = wx.Button(self.panel, label = "Random packages", size = (110, 30))
        self.randompackages_button.Bind(wx.EVT_ENTER_WINDOW, self.on_randompackages_enter)
        self.randompackages_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_randompackages_leave)
        self.Bind(wx.EVT_BUTTON, self.click_randompackages_button, self.randompackages_button)
        self.randompackages_button.SetBackgroundColour(wx.Colour(0, 128, 255))
        self.randompackages_button.SetPosition((800, 500))


# ________________ GRAPH ________________ #

    def print_graph(self):

        G = gp.Graph()
        image = mpimg.imread("data\poland.png")
        self.figure, self.ax = plt.subplots()
        plt.imshow(image)
        pos = nx.get_node_attributes(G.G, 'coordinates')
        nx.draw(G.G, ax=self.ax, pos = pos, with_labels=True, font_weight='bold')
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
        self.ax.set_title('Genetic Algorithm chart', color='white')
        self.ax.legend()
        self.ax.grid()
        self.figure.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.title.set_color('white')
        self.ax.tick_params(axis='both', colors='white')
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

        

# ________________ DESTROY WINDOW ________________ #

    def destroy_window(self):
        self.label_result.SetLabel(self.no_text)
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





# ________________ MAIN FUNCTION ________________ #

if __name__ == '__main__':

    app = wx.App(False)
    frame = MyFrame(None, title = 'Genetics Algorithm')

    app.MainLoop()