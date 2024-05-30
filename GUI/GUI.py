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

# Define the Start Menu with Header, Pictures and Buttons to Switch to Create Model, Open Model, Documentation and Exit the App 
class StartMenu(wx.Panel):
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
        button_run = wx.Button(self, label="Run Simulation", pos=(500, 600))
        button_run.Bind(wx.EVT_BUTTON, self.on_run_simulation)
        

        self.button_run = wx.Button(self, label="Run Simulation", pos=(500, 600))
        self.button_run.Bind(wx.EVT_BUTTON, self.on_run_simulation)
        self.num = 0  # Initialize num
        self.paused = False 
        self.updatetime = 100 # Initialize updatetime
        self.skip_sim_steps = 1 # Intitalize the number of steps which are skiped in the animation

    def on_run_simulation(self, event):
        res, list_of_object_lists,system = main_modeling.run_simulation(simulation_points=50001)
        self.plot_results(res, list_of_object_lists)
        self.canvas.draw()
        # Start animation
        max_simulated_time = res.t[-1]
        num_frames = len(res.t)
        animation_time = max_simulated_time * 1000  # Convert to milliseconds
        # computes the necessary steps that must be skipped to obtain an update time of 110 ms which allows 
        # matching the simulated time in the animation quiet good wtih one spring mass oszillator
        self.skip_sim_steps = round(110 * num_frames / animation_time) 
        print('Skipped Simulation Steps: ' + str(self.skip_sim_steps))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_animation, self.timer)
        self.timer.Start(self.updatetime)  # Update time per frame

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
                self.paused = True
                self.timer.Stop()
                wx.CallLater(2000, self.restart_animation)  # Pause for 2 seconds before restarting

            self.canvas.draw()

    def restart_animation(self):
        self.paused = False
        self.timer.Start(self.updatetime)  # Restart timer
        self.num = 0  # Reset num

    # Create Method to open the Pop-Up 
    def on_open_popup(self,event):
        popup = CreateElement(self)
        popup.Show()

# Create the panel "Open Model"
class OpenModel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,size=(1200,800))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))  # Set background color to white
        text = wx.StaticText(self, label="OpenModel", pos=(50, 50))  # Add a static text to the panel

# Create the Panel "ChooseElement"
class ChooseElement(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))

        # Define Button Size  
        button_size_element = (100,25)

        # Create Button to Switch to the Mass panel
        self.button_mass = wx.Button(self,label="Mass",size=button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_mass,self.button_mass)

        # Create Button to Switch to Spring Panel
        self.button_spring = wx.Button(self,label="Spring",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_spring,self.button_spring)

        # Calculate the positions for the buttons 
        panel_size = self.GetSize()
        x_pos_btn = (panel_size[0]-button_size_element[0])//2
        y_pos_btn = (panel_size[1]-button_size_element[1]*3)//2

        # Set the position of the Buttons in the Center of the Panel 
        self.button_mass.SetPosition((x_pos_btn, y_pos_btn))
        self.button_spring.SetPosition((x_pos_btn, y_pos_btn + button_size_element[1]))
       

    

# Create the Panel "Mass"
class MassElement(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        #text = wx.StaticText(self, label="Mass", pos=(50, 50))  # Add a static text to the panel

        # Define Button Size  
        button_size_element = (100,25)

        # Create Button to Switch to the Mass panel
        self.button_mass_point = wx.Button(self,label="Mass Point",size=button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_mass_point,self.button_mass_point)

        # Create Button to Switch to Spring Panel
        self.button_steady_body = wx.Button(self,label="Steady Body",size = button_size_element)
        self.Bind(wx.EVT_BUTTON,parent.on_mass_steady,self.button_steady_body)

        # Calculate the positions for the buttons 
        panel_size = self.GetSize()
        x_pos_btn = (panel_size[0]-button_size_element[0])//2
        y_pos_btn = (panel_size[1]-button_size_element[1]*3)//2

        # Set the position of the Buttons in the Center of the Panel 
        self.button_mass_point.SetPosition((x_pos_btn, y_pos_btn))
        self.button_steady_body.SetPosition((x_pos_btn, y_pos_btn + button_size_element[1]))

class MassPoint(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        text = wx.StaticText(self, label="MassPoint", pos=(50, 50))  # Add a static text to the panel
        self.mass_label = wx.StaticText(self,label = "What is the mass of the Mass Point:",pos=(10,10))
        self.mass = wx.TextCtrl(self, pos=(10, 30), size=(200, -1))
        self.input_mass = None

class SteadyBody(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        text = wx.StaticText(self, label="SteadyBody", pos=(50, 50))  # Add a static text to the panel

        self.density_label = wx.StaticText(self,label = "What is the density of the Steady Body:",pos=(10,10))
        self.density = wx.TextCtrl(self, pos=(10, 30), size=(200, -1))
        self.input_density = None

        self.length_label = wx.StaticText(self,label = "What is the length of the Steady Body:",pos=(10,10))
        self.length = wx.TextCtrl(self, pos=(10, 30), size=(200, -1))
        self.input_length = None 

        self.height_label = wx.StaticText(self,label = "What is the height of the Steady Body:",pos=(10,10))
        self.height = wx.TextCtrl(self, pos=(10, 30), size=(200, -1))
        self.input_height = None

        self.width_label = wx.StaticText(self,label = "What is the width of the Steady Body:",pos=(10,10))
        self.width = wx.TextCtrl(self, pos=(10, 30), size=(200, -1))
        self.input_width = None


# Create the Panel "Spring"
class SpringElement(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        #text = wx.StaticText(self, label="Spring", pos=(50, 50))  # Add a static text to the panel

        # Define Button Size  
        button_size_element = (100,25)

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

class SingleSpring(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        text = wx.StaticText(self, label="Single Spring", pos=(50, 50))  # Add a static text to the panel

        self.length_spring_label = wx.StaticText(self,label = "What is the length of the spring:",pos=(10,10))
        self.length_spring = wx.TextCtrl(self, pos=(10, 30), size=(200, -1))
        self.input_length_spring = None

        self.stiffness_spring_label = wx.StaticText(self,label = "What is the stiffness of the spring:",pos=(10,10))
        self.stiffness_spring = wx.TextCtrl(self, pos=(10, 30), size=(200, -1))
        self.input_stiffness_spring = None

class ParallelSpring(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        text = wx.StaticText(self, label="Sveral parallel springs", pos=(50, 50))  # Add a static text to the panel

        self.length_spring_label = wx.StaticText(self,label = "What is the length of the spring:",pos=(10,10))
        self.length_spring = wx.TextCtrl(self, pos=(10, 30), size=(200, -1))
        self.input_length_spring = None

class SeriesSpring(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        text = wx.StaticText(self, label="Several springs in series", pos=(50, 50))  # Add a static text to the panel



# Create The Frame for the Create Element 
class CreateElement(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,title="Create Element",size=(400,200))

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
        self.choose_element.Hide()
        self.mass_element.Show() 
        self.Layout()

    # Method to switch to Mass Point 
    def on_mass_point(self,event):
        self.mass_element.Hide() 
        self.mass_point.Show()
        self.Layout()

    # Method to switch to Steady Body
    def on_mass_steady(self,event):
        self.mass_element.Hide() 
        self.mass_steady_body.Show()
        self.Layout()     

    # Method to switch to Create Spring 
    def on_spring(self,event):
        self.choose_element.Hide()
        self.spring_element.Show()
        self.Layout()

        # Method to switch to Single Springs 
    def on_spring_single(self,event):
        self.spring_element.Hide()
        self.spring_single.Show()
        self.Layout()

        # Method to switch to Parallel Springs
    def on_spring_parallel(self,event):
        self.spring_element.Hide()
        self.spring_parallel.Show()
        self.Layout()

        # Method to switch to Springs in Series
    def on_spring_series(self,event):
        self.spring_element.Hide()
        self.spring_series.Show()
        self.Layout()

# Create the Main Frame 
class MainFrame(wx.Frame):
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
        self.start_menu.Hide()
        self.create_model.Show()
        self.Layout()

    # Method to Switch to open Model 
    def on_switch_open_model(self,event):
        self.start_menu.Hide()
        self.open_model.Show()
        self.Layout()

    # Create the Method that closes the App 
    def on_close_app(self,event):
        wx.GetApp().ExitMainLoop()
        
# Entry point of the application
if __name__ == "__main__":
    app = wx.App(False)  # Create an instance of the application
    frame = MainFrame()  # Create an instance of the main frame
    frame.Show()  # Show the frame
    app.MainLoop()  # Start the event loop to handle events