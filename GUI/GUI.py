import wx
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"\Modeling")
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.animation as animation 
from matplotlib.figure import Figure
import main_test_v2 as main_modeling
import animation_gui as anim
import objects
from additions import eq_to_latex, show_equations_of_motion
from simsave import save_system, tex_save

list_of_springs= []
list_of_mass = []

# Define the Start Menu with Header, Pictures and Buttons to Switch to Create Model, Open Model, Documentation and Exit the App 
class StartMenu(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels.

    :param parent: The Main Frame
    :type parent: wx.Frame
    """
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(1200,800))
        self.SetBackgroundColour(wx.Colour(255,255,255,0))

        # Create Images from the Univeristy Logo and the Logo of Systems Engineering 
        image_left = wx.Image(os.path.dirname(os.path.realpath(__file__))+"\Image_uni.png",wx.BITMAP_TYPE_ANY)   # Load the Image of the Uni Logo
        image_right = wx.Image(os.path.dirname(os.path.realpath(__file__))+"\Image_se.png",wx.BITMAP_TYPE_ANY)   # Load the Image of Systems Engineering
        image_left = image_left.ConvertToBitmap()
        image_right = image_right.ConvertToBitmap()
        self.bitmap_left = wx.StaticBitmap(self,bitmap=image_left,pos=(10,10))
        self.bitmap_right = wx.StaticBitmap(self,bitmap = image_right,pos=(1000,10))

        # Define Button Size  
        button_size = (200,50)

        # Create Button to Switch to the Create Model Panel 
        self.button_create_model = wx.Button(self,label="Create Model",size=button_size)
        self.Bind(wx.EVT_BUTTON,parent.on_switch_create_model,self.button_create_model)

        # Create Button to Switch to Open Model Panel
        self.button_open_model = wx.Button(self,label="Open Model",size = button_size)
        self.Bind(wx.EVT_BUTTON,parent.on_switch_open_model,self.button_open_model)

        # Create Button to get to the documentation 
        self.button_documentation = wx.Button(self,label="Open Documentation",size = button_size)

        # Create Button to close the App 
        self.close_button = wx.Button(self,label="Close Dynamic Vision",size = button_size)
        self.Bind(wx.EVT_BUTTON,parent.on_close_app,self.close_button)

        # Calculate the positions for the buttons 
        panel_size = self.GetSize()
        x_pos_btn = (panel_size[0]-button_size[0])//2
        y_pos_btn = (panel_size[1]-button_size[1]*4)//2

        # Set the position of the Buttons in the Center of the Panel 
        self.button_create_model.SetPosition((x_pos_btn, y_pos_btn))
        self.button_open_model.SetPosition((x_pos_btn, y_pos_btn + button_size[1]))
        self.button_documentation.SetPosition((x_pos_btn,y_pos_btn+2*button_size[1]))
        self.close_button.SetPosition((x_pos_btn, y_pos_btn + 3*button_size[1]))

        # Create a Header 
        header_font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # Define font for header
        self.header_text = wx.StaticText(self, label="DynamicVision")  # Create StaticText widget for header
        self.header_text.SetFont(header_font)  # Apply font to header text
        self.header_text.SetForegroundColour(wx.Colour(0, 0, 255))  # Set text color to blue
        header_size = self.header_text.GetSize()
        x_pos_header = (panel_size[0]-header_size[0])//2
        self.header_text.SetPosition((x_pos_header,70))

        # Create Text which shows the Authors
        self.author_text = wx.StaticText(self,label="Created by Daniel Philippi, Jens Rößler and Nicolas Scherer")
        author_size = self.author_text.GetSize()
        x_pos_author = (panel_size[0]-author_size[0])//2
        y_pos_author = (panel_size[1]-5*author_size[1])//1
        self.author_text.SetForegroundColour(wx.Colour(0, 0, 255))  # Set text color to blue
        self.author_text.SetPosition((x_pos_author,y_pos_author))



# Create the Panel "Create Model" 
class CreateModel(wx.Panel):
    """
    Class to create the panel on which one can create the model. 
    This panel is contained within the main frame.
    It opens when the button "create model" ist clicked on.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Main Frame
    :type parent: wx.Frame
    """
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(1200,800))
        self.SetBackgroundColour(wx.Colour(255,255,255))

        # Create a Matplotlib canvas to display the figure
        self.figure=Figure(figsize=(10,4))
        self.ax1 = self.figure.add_subplot(1,2,1)
        self.ax2 = self.figure.add_subplot(1,2,2)
        self.canvas = FigureCanvas(self, -1, self.figure)
        
        # Create a button to open the pop-up window to create a Element 
        self.button_create_element = wx.Button(self,label="Create Element")
        self.Bind(wx.EVT_BUTTON,self.on_open_popup,self.button_create_element)             

        # Add the button to the sizer (also maybe imporve after the whole layout is done)
        self.button_create_element.SetPosition((1000,500))

        #Create a button to start the simultion
        self.button_run = wx.Button(self, label="Run Simulation", pos=(400, 600))
        self.button_run.Bind(wx.EVT_BUTTON, self.on_run_simulation)

        self.button_IC = wx.Button(self, label="Set Inital Conditions", pos=(600, 600))
        self.button_IC.Bind(wx.EVT_BUTTON, self.on_open_IC)
        
        self.num = 0  # Initialize num
        self.paused = False 
        self.updatetime = 100 # Initialize updatetime
        self.skip_sim_steps = 1 # Intitalize the number of steps which are skiped in the animation
        self.timer = wx.Timer(self)

    def on_run_simulation(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        #list_of_object_lists = main_modeling.create_objects()
        list_of_object_lists = [list_of_springs, list_of_mass]
        self.res, self.system = main_modeling.run_simulation(list_of_object_lists, simulation_points=25001)
        self.plot_results(self.res, list_of_object_lists)
        self.show_equations(self.system)
        self.canvas.draw()
        # Start animation
        max_simulated_time = self.res.t[-1]
        num_frames = len(self.res.t)
        animation_time = max_simulated_time * 1000  # Convert to milliseconds
        # computes the necessary steps that must be skipped to obtain an update time of 110 ms which allows 
        # matching the simulated time in the animation quiet good wtih one spring mass oszillator
        self.skip_sim_steps = round(110 * num_frames / animation_time) 
        print('Skipped Simulation Steps: ' + str(self.skip_sim_steps))

        #self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_animation, self.timer)
        self.timer.Start(self.updatetime)  # Update time per frame

        folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"\Modeling\data"
 
        # Create a save file dialog
        with wx.FileDialog(self, "Save Simulation data", defaultDir=folder_path,
                           wildcard="All files (*.*)|*.*",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as save_dialog:
 
            # Show the dialog and get the response
            if save_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the dialog
 
            # Get the path for saving the file
            save_file_path = save_dialog.GetPath()
 
            # Call your custom save function with the selected file path 
            print(save_file_path)
            save_system(save_file_path, self.res ,self.system)
            print("Data saved.")  


    def show_equations(self, system):
        """
        Method to switch between the start menu and the "create model" menu
        """
        # plot/show equations of motion
        main_modeling.generate_latex(system)

    def plot_results(self, res, list_of_object_lists):
        """
        Method to switch between the start menu and the "create model" menu
        """
        # Plot results in ax1
        main_modeling.plot_results(res, self.ax1)
        self.animation = anim.Animation(res, list_of_object_lists, self.ax2)

    def update_animation(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        if not self.paused:
            # Update animation with appropriate frame number
            self.animation.update_frame(self.num)
            self.num += self.skip_sim_steps  # Increment num for the next frame

            # If num exceeds the length of y_pos, pause for a moment and restart
            y = -self.animation.sol.y
            pos = y[0:int(len(y)/2)]
            y_pos = pos[1::2]
            if self.num >= len(y_pos[0]):
                #make sure that the animation stops at the last simulated point
                self.num = len(y_pos[0])-1
                self.animation.update_frame(self.num)

                self.paused = True
                self.timer.Stop()
                wx.CallLater(2000, self.restart_animation)  # Pause for 2 seconds before restarting

            self.canvas.draw()

    def restart_animation(self):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.paused = False
        self.timer.Start(self.updatetime)  # Restart timer
        self.num = 0  # Reset num

    # Create Method to open the Pop-Up 
    def on_open_popup(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """

        global list_of_springs 
        global list_of_mass 
        
        list_of_springs = []
        list_of_mass = []

        self.timer.Stop()
        self.ax1.cla()  # clear axis 1
        self.ax2.cla()  # clear axis 2
        self.canvas.draw()  # refresh the canvas

        popup = CreateElement(self)
        popup.Show()


    def on_open_IC(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        IC_popup = InitialCondition(self)
        IC_popup.Show()

# Create the panel "Open Model"
class OpenModel(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Main Frame
    :type parent: wx.Frame
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,size=(1200,800))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))  # Set background color to white
        text = wx.StaticText(self, label="OpenModel", pos=(50, 50))  # Add a label to the panel

        # Create a Matplotlib canvas to display the figure
        self.figure=Figure(figsize=(10,4))
        self.ax1 = self.figure.add_subplot(1,2,1)
        self.ax2 = self.figure.add_subplot(1,2,2)
        self.canvas = FigureCanvas(self, -1, self.figure)
        
        # Create a button to open the pop-up window to create a Element 
        self.button_load_model = wx.Button(self,label="Load Model")
        self.Bind(wx.EVT_BUTTON,self.on_load_model,self.button_load_model)             
        self.button_load_model.SetPosition((1000,500))

        self.num = 0  # Initialize num
        self.paused = False 
        self.updatetime = 100 # Initialize updatetime
        self.skip_sim_steps = 1 # Intitalize the number of steps which are skiped in the animation
        self.timer = wx.Timer(self)

    def on_load_model(self,event):

        self.timer.Stop()
        self.ax1.cla()  # clear axis 1
        self.ax2.cla()  # clear axis 2
        self.canvas.draw()  # refresh the canvas
        
        folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"\Modeling\data"

        # Create a file dialog
        with wx.FileDialog(self, "Select the file to be loaded ", defaultDir=folder_path,
                           wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:

            # Show the dialog and get the response
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the dialog

            # Get the selected file path
            selected_file_path = file_dialog.GetPath()
            loaded_list_of_object_lists = main_modeling.load_list(selected_file_path)
            self.loaded_res = main_modeling.load_sys(selected_file_path)
            self.loaded_system = self.loaded_res.loaded_system

            self.plot_results(self.loaded_res, loaded_list_of_object_lists)
            self.show_equations(self.loaded_system)
            self.canvas.draw()
            # Start animation
            max_simulated_time = self.loaded_res.t[-1]
            num_frames = len(self.loaded_res.t)
            animation_time = max_simulated_time * 1000  # Convert to milliseconds
            # computes the necessary steps that must be skipped to obtain an update time of 110 ms which allows 
            # matching the simulated time in the animation quiet good wtih one spring mass oszillator
            self.skip_sim_steps = round(110 * num_frames / animation_time)

            self.Bind(wx.EVT_TIMER, self.update_animation, self.timer)
            self.timer.Start(self.updatetime)  # Update time per frame

    def show_equations(self, system):
        # plot/show equations of motion
        main_modeling.generate_latex(system)

    def plot_results(self, res, list_of_object_lists):
        # Plot results in ax1
        main_modeling.plot_results(res, self.ax1)
        self.animation = anim.Animation(res, list_of_object_lists, self.ax2)

    def update_animation(self, event):
        if not self.paused:
            # Update animation with appropriate frame number
            self.animation.update_frame(self.num)
            self.num += self.skip_sim_steps  # Increment num for the next frame

            # If num exceeds the length of y_pos, pause for a moment and restart
            y = -self.animation.sol.y
            pos = y[0:int(len(y)/2)]
            y_pos = pos[1::2]
            if self.num >= len(y_pos[0]):
                #make sure that the animation stops at the last simulated point
                self.num = len(y_pos[0])-1
                self.animation.update_frame(self.num)

                self.paused = True
                self.timer.Stop()
                wx.CallLater(2000, self.restart_animation)  # Pause for 2 seconds before restarting

            self.canvas.draw()

    def restart_animation(self):
        self.paused = False
        self.timer.Start(self.updatetime)  # Restart timer
        self.num = 0  # Reset num

# Create the Panel "ChooseElement"
class ChooseElement(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Create Element Frame
    :type parent: wx.Frame
    """
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))

        # Define Button Size  
        button_size_element = (300,25)

        # Create Button to Switch to the Mass panel
        self.button_mass = wx.Button(self,label="Mass",size=button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_mass,self.button_mass)

        # Create Button to Switch to Spring Panel
        self.button_spring = wx.Button(self,label="Spring",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_spring,self.button_spring)

        # Create Button to Switch to Spring Panel
        self.button_finish = wx.Button(self,label="Finish",size = (button_size_element[0]/2,button_size_element[1]))
        self.Bind(wx.EVT_BUTTON,parent.on_finish,self.button_finish)

        # Calculate the positions for the buttons 
        panel_size = self.GetSize()
        x_pos_btn = (panel_size[0]-button_size_element[0])//2
        y_pos_btn = (panel_size[1]-button_size_element[1]*3)//2

        # Set the position of the Buttons in the Center of the Panel 
        self.button_mass.SetPosition((x_pos_btn, y_pos_btn))
        self.button_spring.SetPosition((x_pos_btn, y_pos_btn + button_size_element[1]))
        self.button_finish.SetPosition((panel_size[0]-100,panel_size[1]-(75)))
       

    

# Create the Panel "Mass"
class MassElement(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Create Element Frame
    :type parent: wx.Frame
    """
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.text_mass = wx.StaticText(self, label="Mass")  # Add a static text to the panel
        text_mass_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # Define font for header
        self.text_mass.SetFont(text_mass_font) 
        mass_size = self.text_mass.GetSize()
        panel_size = self.GetSize()
        x_pos_mass = (panel_size[0]-mass_size[0])//2
        y_pos_mass = (2*mass_size[1])//1
        self.text_mass.SetPosition((x_pos_mass,y_pos_mass))



        # Define Button Size  
        button_size_element = (200,25)

        # Create Button to Switch to the Mass panel
        self.button_mass_point = wx.Button(self,label="Mass Point",size=button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_mass_point,self.button_mass_point)

        # Create Button to Switch to Spring Panel
        self.button_steady_body = wx.Button(self,label="Steady Body",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_mass_steady,self.button_steady_body)

        # Create Button to get back to the choose element panel 
        self.button_back = wx.Button(self,label="Back",size = (button_size_element[0]/2,button_size_element[1]))
        self.Bind(wx.EVT_BUTTON,self.on_back,self.button_back)

        # Calculate the positions for the buttons 
        panel_size = self.GetSize()
        x_pos_btn = (panel_size[0]-button_size_element[0])//2
        y_pos_btn = (panel_size[1]-button_size_element[1]*3)//2

        # Set the position of the Buttons in the Center of the Panel 
        self.button_mass_point.SetPosition((x_pos_btn, y_pos_btn))
        self.button_steady_body.SetPosition((x_pos_btn, y_pos_btn + button_size_element[1]))
        self.button_back.SetPosition((panel_size[0]-100,panel_size[1]-(75)))

        self.choose_element = parent.choose_element

    def on_back(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.Hide()
        self.choose_element.Show()

class MassPoint(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Create Element Frame
    :type parent: wx.Frame
    """    
    def __init__(self, parent):
        wx.Panel.__init__(self,parent,size=(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.mass_point_text = wx.StaticText(self, label="Mass Point")  # Add a static text to the panel
        self.mass_label = wx.StaticText(self,label = "What is the mass of the Mass Point:")
        text_mass_point_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # Define font for header
        self.mass_point_text.SetFont(text_mass_point_font) 
        mass_point_size = self.mass_point_text.GetSize()
        panel_size = self.GetSize()
        x_pos_mass_point = (panel_size[0]-mass_point_size[0])//2
        y_pos_mass_point = (2*mass_point_size[1])//1
        self.mass_point_text.SetPosition((x_pos_mass_point,y_pos_mass_point))

        mass_point_label_size = self.mass_label.GetSize()
        x_pos_mass_point_label = (panel_size[0]-1*mass_point_label_size[0])//2
        y_pos_mass_point_label = (panel_size[1]-15*mass_point_label_size[1])//1
        self.mass_label.SetPosition((x_pos_mass_point_label,y_pos_mass_point_label))

        self.mass = wx.TextCtrl(self, pos=(x_pos_mass_point_label,y_pos_mass_point_label+1*mass_point_label_size[1]), size=(200, -1))
        self.input_mass = None

        button_size_element = (100,25)

        # Create submit Button
        self.button_steady_body_submit= wx.Button(self,label="submit",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,self.on_submit,self.button_steady_body_submit)
        self.button_steady_body_submit.SetPosition((300,325))

        # Create Button to get back to the choose element panel 
        self.button_back = wx.Button(self,label="Back",size = (button_size_element[0]/2,button_size_element[1]))
        self.Bind(wx.EVT_BUTTON,self.on_back,self.button_back)
        self.button_back.SetPosition((panel_size[0]-100,panel_size[1]-(75)))

    
        self.choose_element = parent.choose_element
        self.mass_element = parent.mass_element

    def on_back(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.Hide()
        self.mass_element.Show()

    def on_submit(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        # Process the list of spring lengths
        if self.mass:
            self.mass_mass_point = 0
            self.mass_mass_point = float(self.mass.GetValue())
            #wx.MessageBox(f"{self.mass_mass_point}")
            m = objects.Masspoint(mass=self.mass_mass_point, index = (len(list_of_mass)+1))
            list_of_mass.append(m)

            self.mass.Clear()

            self.Hide()
            self.choose_element.Show()

        else:
            wx.MessageBox("No spring lengths to submit.", "Warning", wx.OK | wx.ICON_WARNING)

class SteadyBody(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Create Element Frame
    :type parent: wx.Frame
    """
    def __init__(self, parent):
        wx.Panel.__init__(self,parent,size=(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.steady_body_text = wx.StaticText(self, label="SteadyBody", pos=(50, 50))  # Add a static text to the panel
        text_steady_body_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.steady_body_text.SetFont(text_steady_body_font) 
        steady_body_size = self.steady_body_text.GetSize()
        panel_size = self.GetSize()
        x_pos_steady_body = (panel_size[0]-1*steady_body_size[0])//2
        y_pos_steady_body = (panel_size[1]-15*steady_body_size[1])//1
        self.steady_body_text.SetPosition((x_pos_steady_body,y_pos_steady_body))

        self.density_label = wx.StaticText(self,label = "What is the density of the Steady Body:")
        density_label_size = self.density_label.GetSize()
        x_pos_density_label = (panel_size[0]-2*density_label_size[0])//2
        y_pos_density_label = (panel_size[1]-20*density_label_size[1])//1
        self.density_label.SetPosition((x_pos_density_label,y_pos_density_label))
        self.density_input = wx.TextCtrl(self, pos=(x_pos_density_label, y_pos_density_label+1*density_label_size[1]), size=(200, -1))

        self.length_label = wx.StaticText(self,label = "What is the length of the Steady Body:")
        length_label_size = self.length_label.GetSize()
        x_pos_length_label = (panel_size[0]-2*length_label_size[0])//2
        y_pos_length_label = (panel_size[1]-16*length_label_size[1])//1
        self.length_label.SetPosition((x_pos_length_label,y_pos_length_label))
        self.length_input = wx.TextCtrl(self, pos=(x_pos_length_label, y_pos_length_label+1*length_label_size[1]), size=(200, -1))

        self.height_label = wx.StaticText(self,label = "What is the height of the Steady Body:")
        height_label_size = self.height_label.GetSize()
        x_pos_height_label = (panel_size[0]-2*height_label_size[0])//2
        y_pos_height_label = (panel_size[1]-12*height_label_size[1])//1
        self.height_label.SetPosition((x_pos_height_label,y_pos_height_label))
        self.height_input = wx.TextCtrl(self, pos=(x_pos_height_label, y_pos_height_label+1*height_label_size[1]), size=(200, -1))

        self.width_label = wx.StaticText(self,label = "What is the width of the Steady Body:")
        width_label_size = self.width_label.GetSize()
        x_pos_width_label = (panel_size[0]-2*width_label_size[0])//2
        y_pos_width_label = (panel_size[1]-8*width_label_size[1])//1
        self.width_label.SetPosition((x_pos_width_label,y_pos_width_label))
        self.width_input = wx.TextCtrl(self, pos=(x_pos_width_label, y_pos_width_label+1*width_label_size[1]), size=(200, -1))

        button_size_element = (100,25)

        # Create submit Button
        self.button_steady_body_submit= wx.Button(self,label="submit",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,self.on_submit,self.button_steady_body_submit)
        self.button_steady_body_submit.SetPosition((300,325))

        # Create Button to get back to the choose element panel 
        self.button_back = wx.Button(self,label="Back",size = (button_size_element[0]/2,button_size_element[1]))
        self.Bind(wx.EVT_BUTTON,self.on_back,self.button_back)
        self.button_back.SetPosition((panel_size[0]-100,panel_size[1]-(75)))

        self.choose_element = parent.choose_element
        self.mass_element = parent.mass_element

    def on_back(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.Hide()
        self.mass_element.Show()

    
    def on_submit(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        # Process the list of spring lengths
        if self.density_input:
            self.mass_steady_body = 0
            self.density = float(self.density_input.GetValue())
            self.width = float(self.width_input.GetValue())
            self.height = float(self.height_input.GetValue())
            self.length = float(self.length_input.GetValue())
            self.mass_steady_body = self.height*self.width*self.length*self.density
            m = objects.SteadyBody(self.length,self.height,self.width,self.density, index = (len(list_of_mass)+1))
            list_of_mass.append(m)
            #wx.MessageBox(f"{self.mass_steady_body}")

            self.height_input.Clear()
            self.width_input.Clear()
            self.length_input.Clear()
            self.density_input.Clear()

            self.Hide()
            self.choose_element.Show()
            

        else:
            wx.MessageBox("No spring lengths to submit.", "Warning", wx.OK | wx.ICON_WARNING)


# Create the Panel "Spring"
class SpringElement(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Create Element Frame
    :type parent: wx.Frame
    """
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        #text = wx.StaticText(self, label="Spring", pos=(50, 50))  # Add a static text to the panel

        # Define Button Size  
        button_size_element = (200,25)

        # Create Button to Switch to the Single Spring
        self.button_spring_single = wx.Button(self,label="Single Spring",size=button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_spring_single,self.button_spring_single)

        # Create Button to Switch to Parallel Springs
        self.button_spring_parallel= wx.Button(self,label="Several Paralell Springs",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_spring_parallel,self.button_spring_parallel)

        # Create Button to Switch to Series Springs
        self.button_spring_series = wx.Button(self,label="Several Springs in Series",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_spring_series,self.button_spring_series)

        # Calculate the positions for the buttons 
        panel_size = self.GetSize()
        x_pos_btn = (panel_size[0]-button_size_element[0])//2
        y_pos_btn = (panel_size[1]-button_size_element[1]*3)//2

        # Set the position of the Buttons in the Center of the Panel 
        self.button_spring_single.SetPosition((x_pos_btn, y_pos_btn))
        self.button_spring_parallel.SetPosition((x_pos_btn, y_pos_btn + button_size_element[1]))
        self.button_spring_series.SetPosition((x_pos_btn, y_pos_btn + 2*button_size_element[1]))

        # Create Button to get back to the choose element panel 
        self.button_back = wx.Button(self,label="Back",size = (button_size_element[0]/2,button_size_element[1]))
        self.Bind(wx.EVT_BUTTON,self.on_back,self.button_back)
        self.button_back.SetPosition((panel_size[0]-100,panel_size[1]-(75)))

        self.choose_element = parent.choose_element

    def on_back(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.Hide()
        self.choose_element.Show()



class SingleSpring(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Create Element Frame
    :type parent: wx.Frame
    """
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))

        panel_size = self.GetSize()
        self.single_spring_text = wx.StaticText(self, label="Single Spring", pos=(50, 50))  # Add a static text to the panel
        text_single_spring_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.single_spring_text.SetFont(text_single_spring_font) 
        single_spring_size = self.single_spring_text.GetSize()
        x_pos_parallel_spring = (panel_size[0]-1*single_spring_size[0])//2
        y_pos_parallel_spring = (panel_size[1]-15*single_spring_size[1])//1
        self.single_spring_text.SetPosition((x_pos_parallel_spring,y_pos_parallel_spring))

        self.stiffness_label = wx.StaticText(self,label = "What is the stiffness of the Spring:")
        stiffness_label_size = self.stiffness_label.GetSize()
        x_pos_stiffness_label = (panel_size[0]-2*stiffness_label_size[0])//2
        y_pos_stiffness_label = (panel_size[1]-20*stiffness_label_size[1])//1
        self.stiffness_label.SetPosition((x_pos_stiffness_label,y_pos_stiffness_label))
        self.stiffness_spring_single = wx.TextCtrl(self, pos=(x_pos_stiffness_label, y_pos_stiffness_label+1*stiffness_label_size[1]), size=(200, -1))
     

        self.length_label = wx.StaticText(self,label = "What is the length of the Spring:")
        length_label_size = self.length_label.GetSize()
        x_pos_length_label = (panel_size[0]-2*length_label_size[0])//2
        y_pos_length_label = (panel_size[1]-16*length_label_size[1])//1
        self.length_label.SetPosition((x_pos_length_label,y_pos_length_label))
        self.length_spring_single = wx.TextCtrl(self, pos=(x_pos_length_label, y_pos_length_label+1*length_label_size[1]), size=(200, -1))
        
    
        button_size_element = (100,25)

        # Create submit Button
        self.button_spring_single_submit= wx.Button(self,label="submit",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,self.on_submit,self.button_spring_single_submit)
        self.button_spring_single_submit.SetPosition((300,325))

        # Create Button to get back to the choose element panel 
        self.button_back = wx.Button(self,label="Back",size = (button_size_element[0]/2,button_size_element[1]))
        self.Bind(wx.EVT_BUTTON,self.on_back,self.button_back)
        self.button_back.SetPosition((panel_size[0]-100,panel_size[1]-(75)))

        self.choose_element = parent.choose_element
        self.spring_element = parent.spring_element

    def on_back(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.Hide()
        self.spring_element.Show()
    
    def on_submit(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        # Process the list of spring lengths
        if self.length_spring_single:
            self.spring_length = 0
            self.spring_length = float(self.length_spring_single.GetValue())
            #wx.MessageBox(f"{self.spring_length}")

            self.spring_stiffness = 0
            self.spring_stiffness = float(self.stiffness_spring_single.GetValue())
           

            s = objects.Spring(rest_length = self.spring_length,stiffness=self.spring_stiffness,index =(len(list_of_springs)+1))
            list_of_springs.append(s)
            #wx.MessageBox(f"{list_of_springs}")
            
            self.length_spring_single.Clear()
            self.stiffness_spring_single.Clear()

            self.Hide()
            self.choose_element.Show()
            
        else:
            wx.MessageBox("No spring lengths to submit.", "Warning", wx.OK | wx.ICON_WARNING)

class ParallelSpring(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Create Element Frame
    :type parent: wx.Frame
    """
    def __init__(self,parent,*args):
        wx.Panel.__init__(self,parent,size=(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.spring_lengths_parallel = []
        self.spring_stiffness_parallel = []

        self.parallel_spring_text = wx.StaticText(self, label="Parallel Spring", pos=(50, 50))  # Add a static text to the panel
        text_parallel_spring_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.parallel_spring_text.SetFont(text_parallel_spring_font) 
        parallel_spring_size = self.parallel_spring_text.GetSize()
        panel_size = self.GetSize()
        x_pos_parallel_spring = (panel_size[0]-1*parallel_spring_size[0])//2
        y_pos_parallel_spring = (panel_size[1]-15*parallel_spring_size[1])//1
        self.parallel_spring_text.SetPosition((x_pos_parallel_spring,y_pos_parallel_spring))

        self.stiffness_label = wx.StaticText(self,label = "What is the stiffness of the Spring:")
        stiffness_label_size = self.stiffness_label.GetSize()
        x_pos_stiffness_label = (panel_size[0]-2*stiffness_label_size[0])//2
        y_pos_stiffness_label = (panel_size[1]-20*stiffness_label_size[1])//1
        self.stiffness_label.SetPosition((x_pos_stiffness_label,y_pos_stiffness_label))
        self.stiffness_spring_parallel = wx.TextCtrl(self, pos=(x_pos_stiffness_label, y_pos_stiffness_label+1*stiffness_label_size[1]), size=(200, -1))

        self.length_label = wx.StaticText(self,label = "What is the length of the Spring:")
        length_label_size = self.length_label.GetSize()
        x_pos_length_label = (panel_size[0]-2*length_label_size[0])//2
        y_pos_length_label = (panel_size[1]-16*length_label_size[1])//1
        self.length_label.SetPosition((x_pos_length_label,y_pos_length_label))
        self.length_spring_parallel = wx.TextCtrl(self, pos=(x_pos_length_label, y_pos_length_label+1*length_label_size[1]), size=(200, -1))
    
        button_size_element = (100,25)

        # Create add Button
        self.button_spring_parallel_add= wx.Button(self,label="add",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,self.on_add,self.button_spring_parallel_add)
        self.button_spring_parallel_add.SetPosition((300,300))

        # Create submit Button
        self.button_spring_parallel_submit= wx.Button(self,label="submit",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,self.on_submit,self.button_spring_parallel_submit)
        self.button_spring_parallel_submit.SetPosition((300,325))

        # Create Button to get back to the choose element panel 
        self.button_back = wx.Button(self,label="Back",size = (button_size_element[0]/2,button_size_element[1]))
        self.Bind(wx.EVT_BUTTON,self.on_back,self.button_back)
        self.button_back.SetPosition((panel_size[0]-100,panel_size[1]-(75)))

        self.choose_element = parent.choose_element
        self.spring_element = parent.spring_element

    def on_back(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.Hide()
        self.spring_element.Show()

    def on_add(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        length = float(self.length_spring_parallel.GetValue())
        if length:
            self.spring_lengths_parallel.append(length)
            self.length_spring_parallel.Clear()
        stiffness = float(self.stiffness_spring_parallel.GetValue())
        if stiffness:
            self.spring_stiffness_parallel.append(stiffness)
            self.stiffness_spring_parallel.Clear()
    
    def on_submit(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        # Process the list of spring lengths
        if self.spring_lengths_parallel:
            self.spring_length = 0
            for length in self.spring_lengths_parallel:
                self.spring_length +=length
            self.spring_length = self.spring_length/len(self.spring_lengths_parallel) 
            #wx.MessageBox(f"{list_of_springs_length}")

            self.spring_stiffness = 0
            for stiffness in self.spring_stiffness_parallel:
                self.spring_stiffness +=stiffness
            #wx.MessageBox(f"{list_of_springs_stiffness}")

            s = objects.Spring(rest_length = self.spring_length,stiffness=self.spring_stiffness,index =(len(list_of_springs)+1))
            list_of_springs.append(s)

            self.stiffness_spring_parallel.Clear()
            self.length_spring_parallel.Clear()

            self.Hide()
            self.choose_element.Show()
            
        else:
            wx.MessageBox("No spring lengths to submit.", "Warning", wx.OK | wx.ICON_WARNING)


class SeriesSpring(wx.Panel):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 

    :param parent: The Create Element Frame
    :type parent: wx.Frame
    """
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.spring_lengths_series =[]
        self.spring_stiffness_series = []

        self.series_spring_text = wx.StaticText(self, label="Series of Springs", pos=(50, 50))  # Add a static text to the panel
        text_series_spring_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.series_spring_text.SetFont(text_series_spring_font) 
        series_spring_size = self.series_spring_text.GetSize()
        panel_size = self.GetSize()
        x_pos_series_spring = (panel_size[0]-1*series_spring_size[0])//2
        y_pos_series_spring = (panel_size[1]-15*series_spring_size[1])//1
        self.series_spring_text.SetPosition((x_pos_series_spring,y_pos_series_spring))

        self.stiffness_label = wx.StaticText(self,label = "What is the stiffness of the Spring:")
        stiffness_label_size = self.stiffness_label.GetSize()
        x_pos_stiffness_label = (panel_size[0]-2*stiffness_label_size[0])//2
        y_pos_stiffness_label = (panel_size[1]-20*stiffness_label_size[1])//1
        self.stiffness_label.SetPosition((x_pos_stiffness_label,y_pos_stiffness_label))
        self.stiffness_spring_series = wx.TextCtrl(self, pos=(x_pos_stiffness_label, y_pos_stiffness_label+1*stiffness_label_size[1]), size=(200, -1))
      

        self.length_label = wx.StaticText(self,label = "What is the length of the Spring:")
        length_label_size = self.length_label.GetSize()
        x_pos_length_label = (panel_size[0]-2*length_label_size[0])//2
        y_pos_length_label = (panel_size[1]-16*length_label_size[1])//1
        self.length_label.SetPosition((x_pos_length_label,y_pos_length_label))
        self.length_spring_series = wx.TextCtrl(self, pos=(x_pos_length_label, y_pos_length_label+1*length_label_size[1]), size=(200, -1))

        button_size_element = (100,25)

        # Create add Button
        self.button_spring_parallel_add= wx.Button(self,label="add",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,self.on_add,self.button_spring_parallel_add)
        self.button_spring_parallel_add.SetPosition((300,300))

        # Create submit Button
        self.button_spring_parallel_submit= wx.Button(self,label="submit",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,self.on_submit,self.button_spring_parallel_submit)
        self.button_spring_parallel_submit.SetPosition((300,325))

        # Create Button to get back to the choose element panel 
        self.button_back = wx.Button(self,label="Back",size = (button_size_element[0]/2,button_size_element[1]))
        self.Bind(wx.EVT_BUTTON,self.on_back,self.button_back)
        self.button_back.SetPosition((panel_size[0]-100,panel_size[1]-(75)))

        self.choose_element = parent.choose_element
        self.spring_element = parent.spring_element

    def on_back(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.Hide()
        self.spring_element.Show()

    def on_add(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        length = float(self.length_spring_series.GetValue())
        if length:
            self.spring_lengths_series.append(length)
            self.length_spring_series.Clear()
        stiffness = float(self.stiffness_spring_series.GetValue())
        if stiffness:
            self.spring_stiffness_series.append(stiffness)
            self.stiffness_spring_series.Clear()
    
    def on_submit(self, event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        # Process the list of spring lengths
        if self.spring_lengths_series:
            self.spring_length = 0
            for length in self.spring_lengths_series:
                self.spring_length +=length
            #wx.MessageBox(f"{list_of_springs_length}")

            self.spring_stiffness = 0
            for stiffness in self.spring_stiffness_series:
                self.spring_stiffness += (1/stiffness)
            self.spring_stiffness = (1/self.spring_stiffness)
            #wx.MessageBox(f"{list_of_springs_stiffness}")

            s = objects.Spring(rest_length = self.spring_length,stiffness=self.spring_stiffness,index =(len(list_of_springs)+1))
            list_of_springs.append(s)

            self.Hide()
            self.choose_element.Show()
            
        else:
            wx.MessageBox("No spring lengths to submit.", "Warning", wx.OK | wx.ICON_WARNING)
        

class InitialCondition(wx.Frame):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 
    """
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,title="Initial Conditions", size =(600,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        panel_size = self.GetSize()
        self.i = 0
            
        self.position_label = wx.StaticText(self,label = "What is inital Position of the mass:")
        position_label_size = self.position_label.GetSize()
        x_pos_position_label = (panel_size[0]-2*position_label_size[0])//2
        y_pos_position_label = (panel_size[1]-20*position_label_size[1])//1
        self.position_label.SetPosition((x_pos_position_label,y_pos_position_label))
        self.position_input = wx.TextCtrl(self, pos=(x_pos_position_label, y_pos_position_label+1*position_label_size[1]), size=(200, -1))

        self.velocity_label = wx.StaticText(self,label = "What is inital Velocity of the mass:")
        velocity_label_size = self.velocity_label.GetSize()
        x_pos_velocity_label = (panel_size[0]-2*velocity_label_size[0])//2
        y_pos_velocity_label = (panel_size[1]-16*velocity_label_size[1])//1
        self.velocity_label.SetPosition((x_pos_velocity_label,y_pos_velocity_label))
        self.velocity_input = wx.TextCtrl(self, pos=(x_pos_velocity_label, y_pos_velocity_label+1*velocity_label_size[1]), size=(200, -1))

        # Create submit Button
        self.button_IC_submit= wx.Button(self,label="submit",size = (100,25))
        self.button_IC_submit.SetPosition((300,325))
        self.Bind(wx.EVT_BUTTON,self.on_submit_IC,self.button_IC_submit)

    def on_submit_IC(self,event):
        """
        Method to switch between the start menu and the "create model" menu
        """
        self.position = 0
        self.velocity = 0
        self.position = float(self.position_input.GetValue())
        self.velocity = float(self.velocity_input.GetValue())

    
        list_of_mass[self.i].setInitialConditions([0,self.position],[0,self.velocity])
        if self.i == 0:
            list_of_springs[self.i].setInitialConditions(None,list_of_mass[self.i],[0,0])
        else: 
            list_of_springs[self.i].setInitialConditions(list_of_mass[self.i-1],list_of_mass[self.i],[0,0])

        self.position_input.Clear()
        self.velocity_input.Clear()

        self.i += 1 

        if self.i >= len(list_of_mass):
            self.Close()


# Create The Frame for the Create Element 
class CreateElement(wx.Frame):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 
    """
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,title="Create Element",size=(600,400))

        self.choose_element = ChooseElement(self)
        self.mass_element = MassElement(self)
        self.spring_element = SpringElement(self)
        self.mass_point = MassPoint(self)
        self.mass_steady_body = SteadyBody(self)
        self.spring_single = SingleSpring(self)
        self.spring_parallel = ParallelSpring(self)
        self.spring_series = SeriesSpring(self)

        self.choose_element.Show()
        self.mass_element.Hide()
        self.spring_element.Hide()
        self.mass_point.Hide()
        self.mass_steady_body.Hide() 
        self.spring_single.Hide()
        self.spring_parallel.Hide() 
        self.spring_series.Hide() 
        

    # Method to switch to Create Mass 
    def on_mass(self,event):
        """
        Method to switch between the "choose element" panel and the "mass element" panel.
        """
        self.choose_element.Hide()
        self.mass_element.Show() 
        self.Layout()

    # Method to switch to Mass Point 
    def on_mass_point(self,event):
        """
        Method to switch between the "mass element" panel and the "mass point" panel.
        """        
        self.mass_element.Hide() 
        self.mass_point.Show()
        self.Layout()

    # Method to switch to Steady Body
    def on_mass_steady(self,event):
        """
        Method to switch between the "mass element" panel and the "steady body" panel.
        """        
        self.mass_element.Hide() 
        self.mass_steady_body.Show()
        self.Layout()     

    # Method to switch to Create Spring 
    def on_spring(self,event):
        """
        Method to switch between the "choose element" panel and the "spring element" panel. 
        """        
        self.choose_element.Hide()
        self.spring_element.Show()
        self.Layout()

        # Method to switch to Single Springs 
    def on_spring_single(self,event):
        """
        Method to switch between the "spring element" panel and the "singel spring" panel.
        """        
        self.spring_element.Hide()
        self.spring_single.Show()
        self.Layout()

        # Method to switch to Parallel Springs
    def on_spring_parallel(self,event):
        """
        Method to switch between the "spring element" panel and the "several parallel springs" panel.
        """        
        self.spring_element.Hide()
        self.spring_parallel.Show()
        self.Layout()

        # Method to switch to Springs in Series
    def on_spring_series(self,event):
        """
        Method to switch between the "spring element" panel and the "several springs in series" panel.
        """        
        self.spring_element.Hide()
        self.spring_series.Show()
        self.Layout()

    def on_finish(self,event):
        """
        Method to close the application by exiting the main loop which starts when starting the application.
        """
        global list_of_mass
        global list_of_springs

        if len(list_of_mass) == len(list_of_springs):
            self.Close()
        else: 
            wx.MessageBox(f"There are {len(list_of_springs)} springs and {len(list_of_mass)} masses. In this version of DynamicVision, there have to be an equal amount of both elements. Please check and try again")    
        




# Create the Main Frame 
class MainFrame(wx.Frame):
    """
    Class to create the panel, which contains the start menu. 
    This panel is contained within the main frame.
    It opens when the application is started.
    It contains two logos, one header and the names of the authors. 
    It contains 4 buttons ("Create Model","Open Model","Open Documentation","Close Application")
    Here the positions and labels of the buttons are set.
    The buttons are binded to events which allow to open the other panels. 
    """
    def __init__(self):
        wx.Frame.__init__(self,None,title="DynamicVision",size =(1200,800))
        self.SetBackgroundColour(wx.Colour(255,255,255))

        self.start_menu = StartMenu(self)
        self.create_model = CreateModel(self)
        self.open_model = OpenModel(self)

        self.create_model.Hide()
        self.open_model.Hide()
        self.start_menu.Show()

    # Method to Switch to create Model 
    def on_switch_create_model(self,event):
        """
        Method to switch between the start menu and the "create model" panel.
        """
        self.start_menu.Hide()
        self.create_model.Show()
        self.Layout()

    # Method to Switch to open Model 
    def on_switch_open_model(self,event):
        """
        Method to switch between the start menu and the "open model" panel.
        """
        self.start_menu.Hide()
        self.open_model.Show()
        self.Layout()

    # Create the Method that closes the App 
    def on_close_app(self,event):
        """
        Method to close the application by exiting the main loop which starts when starting the application.
        """
        wx.GetApp().ExitMainLoop()
        
# Entry point of the application
if __name__ == "__main__":
    app = wx.App(False)  # Create an instance of the application
    frame = MainFrame()  # Create an instance of the main frame
    frame.Show()  # Show the frame
    app.MainLoop()  # Start the event loop to handle events