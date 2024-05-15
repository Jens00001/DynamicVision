import wx
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.animation as animation 
from matplotlib.figure import Figure
import os

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
        y_pos_btn = (panel_size[1]-button_size[1]*3)//2

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

        ## This Plot is a placeholder for the future plot 
        ##

        # Create a Matplotlib canvas to display the figure
        self.figure=Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        
        # Generate initial data for the plot
        self.x = np.linspace(0, 10, 100)
        self.y = np.sin(self.x)
        
        # Plot the initial data and store the line object
        self.line, = self.axes.plot(self.x, self.y)
        
        # Create an animation that updates the plot at regular intervals
        self.animation = animation.FuncAnimation(self.figure, self.update_plot, frames=100, interval=100)
        
        # Set up the layout using a sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        ##
        ##
        # Create a button to open the pop-up window to create a Element 
        self.button_create_element = wx.Button(self,label="Create Element")
        self.Bind(wx.EVT_BUTTON,self.on_open_popup,self.button_create_element)             

        # Add the button to the sizer (also maybe imporve after the whole layout is done)
        self.button_create_element.SetPosition((1000,500))

        self.SetSizer(self.sizer)

    # Method to update the plot
    def update_plot(self, i):
        self.axes.clear()  # Clear the previous plot
        
        # Update the data for the plot (in this example, animate a sine wave)
        self.y = np.sin(self.x + 0.1 * i)
        
        # Plot the updated data and store the line object
        self.line, = self.axes.plot(self.x, self.y)
        
        # Redraw the canvas with the updated plot
        self.canvas.draw()

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
        text = wx.StaticText(self, label="Mass", pos=(50, 50))  # Add a static text to the panel

# Create the Panel "Spring"
class SpringElement(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(400,200))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        text = wx.StaticText(self, label="Spring", pos=(50, 50))  # Add a static text to the panel

# Create The Frame for the Create Element 
class CreateElement(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,title="Create Element",size=(400,200))

        self.choose_element = ChooseElement(self)
        self.mass_element = MassElement(self)
        self.spring_element = SpringElement(self)

        self.choose_element.Show()
        self.mass_element.Hide()
        self.spring_element.Hide()

    # Method to switch to Create Mass 
    def on_mass(self,event):
        self.choose_element.Hide()
        self.mass_element.Show() 
        self.Layout()

    # Method to switch to Create Spring 
    def on_spring(self,event):
        self.choose_element.Hide()
        self.spring_element.Show()
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