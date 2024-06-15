import sympy as sp
import numpy as np

class Spring:
    """"
    Class for creating a Spring object.
    First the Spring it self is initialized. After that the inital conditions can be set.
    There are also Methods to compute the related force or the movement of the spring.
    An mehtod for geting the values for each symbolic parameter as a dictionary is also implemented.

    :param stiffness: stifness of the spring in (N/m)
    :type stiffness: int or float
    :param rest_length: the length of the spring in the rest position in (m)
    :type rest_length: int or float
    :param index: index of the spring in the system which is used for the Notation of the symbolic vaules
    :type index: int
    :param type: the type of the spring (linear or cubic), default is "linear"
    :type type: str
    :param color: color of the spring in the animation, default is "black"
    :type color: str
    :param lienwidth: the lienwidth of the spring in the animation, default is 2
    :type lienwidth: int or float

    :ivar stiffness: stiffness of the spring  in (N/m)
    :vartype stiffness: int or float
    :ivar rest_length: the length of the spring in the rest position in (m)
    :vartype rest_length: int or float
    :ivar index: index of the spring which is used for the Notation of the symbolic vaules
    :vartype index: int
    :ivar type: type of the spring (linear or cubic)
    :vartype type: str
    :ivar color: color of the spring in the animation
    :vartype color: str
    :ivar lw: linewidth of the spring in the animation
    :vartype lw: int or float
    :ivar sym_rest_length: symbolic rest length of the spring
    :vartype sym_rest_length: sympy.Symbol
    :ivar sym_stiffness: symbolic stiffness of the spring
    :vartype sym_stiffness: sympy.Symbol
    :ivar sym_Fx: symbolic force in x direction
    :vartype sym_Fx: sympy.Symbol
    :ivar sym_Fy: symbolic force in y direction
    :vartype sym_Fy: sympy.Symbol
    :ivar startingpoint: startingpoint of the spring in (m)
    :vartype startingpoint: list of int or float
    :ivar endpoint: endpoint of the spring in (m)
    :vartype endpoint: list of int or float
    :ivar velocity: starting velocity of the spring in (m/s)
    :vartype velocity: list of float
    :ivar length: current length of the spring in (m)
    :vartype length: float
    :ivar prestretch: prestretch of the spring in (m)
    :vartype prestretch: float
    """
    def __init__(self, stiffness, rest_length, index, type = "linear", color="black", lienwidth=2):
        """
        Initialize the Spring instance.

        :param stiffness: stiffness of the spring in (N/m)
        :type stiffness: int or float
        :param rest_length: rest length of the spring in (m)
        :type rest_length: int or float
        :param index: Index of the spring
        :type index: int
        :param type: Type of the spring, default is "linear"
        :type type: str
        :param color: Color of the spring, default is "black"
        :type color: str
        :param linewidth: Line width of the spring, default is 2
        :type linewidth: int or float
        """
        self.stiffness = stiffness # in (N/m)
        self.rest_length = rest_length # in (m)
        self.index = index
        self.type = type
        self.color = color
        self.lw = lienwidth

        #definiton of symbolic values 
        self.sym_rest_length = sp.Symbol("l"+str(self.index)+"_0")
        self.sym_stiffness = sp.Symbol("k"+str(self.index))
        self.sym_Fx = sp.Symbol("F_x"+str(self.index)) #force
        self.sym_Fy = sp.Symbol("F_y"+str(self.index)) #force
        self.sym_type = f"spring_type{self.index}"
      
    def __repr__(self):
        return str(list(self.__dict__.items()))
    
    def check_attributes(self):
        """
        Method for checking the type of input variable

        :raises AssertionError: if the type of the input variable is wrong
        """
        assert isinstance(self.startingpoint, list)
        assert self.startingpoint.shape == (2,)
        assert isinstance(self.rest_length, (int, float))
        assert isinstance(self.length, (int, float))
        assert isinstance(self.stiffness, (int, float))
        assert isinstance(self.type, str)
        assert isinstance(self.endpoint, list)
        assert self.endpoint.shape == (2,)
        assert isinstance(self.color, str)
        assert isinstance(self.lw, (int,float))
        
    def setInitialConditions(self,top_mass, bottom_mass, velocity):
        """"
        Method for setting the inital conditions of the spring. 
        The user have the choice weather he wants to input a mass point or a steady body as a mass.
        Depending on the type of mass connected to the spring, the start and end point is set differently,
        because the steady body has a dimension and the mass point does not.
        If the inputs aren't correct an assertion error should be raised.

        :param top_mass: the mass on which the spring is attached, if the created spring is the first spring in the system 
            it is usally attached to the origin instead of a mass. Therefore the value should be None in this case.
        :type top_mass: object or None
        :param bottom_mass: the mass which is connected with the endpoint of the spring
        :type bottom_mass: object
        :param velocity: the starting velocity of the spring in (m/s)
        :type velocity: list of int or float
        """
        if top_mass == None:
            self.startingpoint = [0,0]

        elif top_mass.type == "masspoint":
            self.startingpoint = top_mass.position

        elif top_mass.type == "steady body":
            self.startingpoint = [top_mass.position[0], top_mass.position[1] - float(top_mass.y_dim)/2]
        else:
            raise AssertionError("Please insert a mass or None, if the spring is not placed between two masses, as first argument of the method")
            

        if bottom_mass.type == "masspoint":
            self.endpoint = bottom_mass.position

        elif bottom_mass.type == "steady body":
            self.endpoint = [bottom_mass.position[0], bottom_mass.position[1] + float(bottom_mass.y_dim)/2]

        else:
            raise AssertionError("Please insert a mass as second argument of the method")


        self.velocity= velocity
        self.length = np.sqrt((self.endpoint[0]-self.startingpoint[0])**2 + (self.endpoint[1]-self.startingpoint[1])**2)
        self.prestretch =  self.length - self.rest_length


    def force(self, top_mass, bottom_mass):
        """"
        Method for computing the force of the spring in its current position.
        The force of the spring depends on the type of the spring. 
        Also it depends on the type of mass connected to the spring, because the steady body has a dimension and the mass point does not.
        If the inputs aren't correct an assertion error should be raised.

        :param top_mass: the mass on which the spring is attached, if the created spring is the first spring in the system 
            it is usally attached to the origin instead of a mass. Therefore the value should be None in this case.
        :type top_mass: object or None
        :param bottom_mass: the mass which is connected with the endpoint of the spring
        :type bottom_mass: object
        :return: forces of the spring in (N)
        :rtype: list of sympy.Add or sympy.Mul
        """
       
        match self.type:
            case "linear":
                if top_mass== None and bottom_mass.type == "masspoint":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-self.sym_rest_length)
                elif top_mass== None and bottom_mass.type == "steady body":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-bottom_mass.sym_h/2-self.sym_rest_length)
                elif top_mass.type == "masspoint" and bottom_mass.type == "masspoint":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-top_mass.yt-self.sym_rest_length)
                elif top_mass.type == "masspoint" and bottom_mass.type == "steady body":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-bottom_mass.sym_h/2-top_mass.yt-self.sym_rest_length)
                elif top_mass.type == "steady body" and bottom_mass.type == "masspoint":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-top_mass.yt-top_mass.sym_h/2-self.sym_rest_length)
                elif top_mass.type == "steady body" and bottom_mass.type == "steady body":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-bottom_mass.sym_h/2-top_mass.yt-top_mass.sym_h/2-self.sym_rest_length)
                else:
                    raise AssertionError("Please insert a masspoint, a steady body or None as first argument of the method and a masspoint or a steady body as second argument of the method")
            case "cubic":
                if top_mass== None and bottom_mass.type == "masspoint":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-self.sym_rest_length)**3
                elif top_mass== None and bottom_mass.type == "steady body":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-bottom_mass.sym_h/2-self.sym_rest_length)**3
                elif top_mass.type == "masspoint" and bottom_mass.type == "masspoint":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-top_mass.yt-self.sym_rest_length)**3
                elif top_mass.type == "masspoint" and bottom_mass.type == "steady body":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-bottom_mass.sym_h/2-top_mass.yt-self.sym_rest_length)**3
                elif top_mass.type == "steady body" and bottom_mass.type == "masspoint":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-top_mass.yt-top_mass.sym_h/2-self.sym_rest_length)**3
                elif top_mass.type == "steady body" and bottom_mass.type == "steady body":
                    self.sym_Fy = self.sym_stiffness * (bottom_mass.yt-bottom_mass.sym_h/2-top_mass.yt-top_mass.sym_h/2-self.sym_rest_length)**3
                else:
                    raise AssertionError("Please insert a masspoint, a steady body or None as first argument of the method and a masspoint or a steady body as second argument of the method")

        self.sym_Fx=0

        return [self.sym_Fx, self.sym_Fy]
    
    def move(self,top_mass, bottom_mass):
        """
        Method for computing the new start and end point of the spring depending on the positons of the masses.
        The current length is also computed.
        The computation depends on weather the connected mass is a masspoint or a steady body, because steady bodies have a dimension and masspoints do not

        :param top_mass: the mass on which the spring is attached, if the created spring is the first spring in the system 
            it is usally attached to the origin instead of a mass. Therefore the value should be None in this case.
        :type top_mass: object or None
        :param bottom_mass: the mass which is connected with the endpoint of the spring
        :type bottom_mass: object
        :return: current startingpoint and endpoint of the spring in (m)
        :rtype: list of lists of int or float
        """
        if top_mass == None:
            pass
            #self.startingpoint = self.startingpoint

        elif top_mass.type == "masspoint":
            self.startingpoint = top_mass.position

        elif top_mass.type == "steady body":
            self.startingpoint = [top_mass.position[0], top_mass.position[1] - top_mass.y_dim/2]


        if bottom_mass.type == "masspoint":
            self.endpoint = bottom_mass.position

        elif bottom_mass.type == "steady body":
            self.endpoint = [bottom_mass.position[0], bottom_mass.position[1] + bottom_mass.y_dim/2]

        self.length = np.sqrt((self.endpoint[0]-self.startingpoint[0])**2 + (self.endpoint[1]-self.startingpoint[1])**2 )

        return [self.startingpoint,  self.endpoint]
    
    def get_param_values(self):
        """
        Get numeric values for symbolic representations

        :return: dictionary of symbolic parameters and their values
        :rtype: dictionary
        """
        return {self.sym_rest_length: self.rest_length, self.sym_stiffness: self.stiffness, self.sym_type: self.type}

class Mass:
    """
    Base class for different types of masses.
    
    :param index: index of the mass in the system which is used for the Notation of the symbolic vaules
    :type index: int
    :param color: color of the mass in the animation, default is "red"
    :type color: str

    :ivar index: index of the mass in the system which is used for the Notation of the symbolic vaules
    :vartype index: int
    :ivar color: color of the mass
    :vartype color: str
    :ivar yt: symbolic function for the position of the mass over the time
    :vartype yt: sympy.Function
    :ivar ydt: symbolic first derivative the position of the mass over the time
    :vartype ydt: sympy.Basic
    :ivar yddt: symbolic second derivative of the position of the mass over the time
    :vartype yddt: sympy.Basic
    :ivar sym_mass: symbolic mass
    :vartype sym_mass: sympy.Symbol
    :ivar sym_g: symbolic gravitational acceleration
    :vartype sym_g: sympy.Symbol
    :ivar sym_F: symbolic force
    :vartype sym_F: sympy.Symbol
    :ivar position: position of the mass in (m)
    :vartype position: list of int or float
    :ivar velocity: velocity of the mass in (m/s)
    :vartype velocity: list of int or float
    """
    def __init__(self, index, color ="red"):
        """
        Initialize the Mass instance

        :param index: index of the mass in the system which is used for the Notation of the symbolic vaules
        :type index: int
        :param color: color of the mass in the animation, default is red
        :type color: str
        """
        self.index = index
        self.color = color 
        

        # definition of symbolic values
        t = sp.Symbol("t")
        self.yt = sp.Function("y"+str(self.index))(t)
        self.ydt = self.yt.diff(t)
        self.yddt = self.yt.diff(t,2)
        self.sym_mass = sp.Symbol("m"+str(self.index))
        self.sym_g = sp.Symbol("g")
        self.sym_F = sp.Symbol("F"+str(self.index))

    def check_attributes(self):
        """
        Method for checking the type of input variable

        :raises AssertionError: if the type of the input variable is wrong
        """
        assert isinstance(self.position, list)
        assert self.position.shape == (2,)
        assert isinstance(self.mass,(int,float))
        assert isinstance(self.diameter,(int,float))
        assert isinstance(self.color, str)

    def setInitialConditions(self, position, velocity):
        """"
        Method for setting the intial conditions for the mass.

        :param position: the position of the mass point or the center of mass of a steady body in (m)
        :type position: list of int or float values
        :param velocity: the starting velocity of the mass point or the center of mass of a steady body in (m/s)
        :type velocity: list of int or float values
        """
        self.position = position
        self.velocity = velocity

    def force(self):
        """" 
        Method for computing the gravitational force of the mass

        :return: gravitational force in (N)
        :rtype: sympy.Add
        """  
             
        self.sym_F = self.sym_mass*self.sym_g

        return self.sym_F
    
    def move(self,x,y):
        """
        Move the mass to a new position

        :param x: x-coordinate of the new position in (m)
        :type x: int or float
        :param y: y-coordinate of the new position in (m)
        :type y: int or float
        :return: new position of the mass in (m)
        :rtype: list of int or float
        """
        self.position = [x,y]

        return self.position
    
    def get_param_values(self):
        """
        Get numeric values for symbolic representations

        :return: dictionary of symbolic parameters and their values
        :rtype: dict
        """

        return {self.sym_mass: self.mass}
    
class Masspoint(Mass):
    """
    Class for creating a masspoint

    :param mass: mass of the masspoint in (kg)
    :type mass: int or float
    :param index: index of the masspoint in the system which is used for the Notation of the symbolic vaules
    :type index: int

    :ivar mass: mass of the masspoint in (kg)
    :vartype mass: int or float
    :ivar type: type of the mass is "masspoint". It is used to differentiate between a masspoint and a steady body in the rest of the Code.
    :vartype type: str
    :ivar diameter: diameter of the masspoint in the animation
    :vartype diameter: float
    """
    def __init__(self, mass, index):
        """
        Initialize the Masspoint instance

        :param mass: mass of the masspoint in (kg)
        :type mass: int or float
        :param index: index of the masspoint in the system which is used for the Notation of the symbolic vaules
        :type index: int
        """
        self.mass = mass
        self.type = "masspoint"
        Mass.__init__(self, index)

    def set_diameter(self,y_range):
        """
        Set the diameter of the masspoint based on the y-axis range in the subplot of the figure where the animation is shown

        :param y_range: Range of the y-axis
        :type y_range: int or float
        """
        base_diameter = 0.04
        exponent = 0.5
        self.diameter = base_diameter * (y_range**exponent)

class SteadyBody(Mass):
    """
    Class for creating a steady body

    :param x_dim: dimension of the steady body along the x-axis in (m)
    :type x_dim: int or float
    :param y_dim: dimension of the steady body along the y-axis in (m)
    :type y_dim: int or float
    :param z_dim: dimension of the steady body along the z-axis in (m)
    :type z_dim: int or float
    :param density: density of the material of the steady body in (kg/m^3)
    :type density: int or float
    :param index: index of the steady body in the system which is used for the Notation of the symbolic vaules
    :type index: int

    :ivar x_dim: dimension of the steady body along the x-axis in (m)
    :vartype x_dim: int or float
    :ivar y_dim: dimension of the steady body along the y-axis in (m)
    :vartype y_dim: int or float
    :ivar z_dim: dimension of the steady body along the z-axis in (m)
    :vartype z_dim: int or float
    :ivar density: density of the material of the steady body in (kg/m^3)
    :vartype density: int or float
    :ivar volume: volume of the body in (m^3)
    :vartype volume: int or float
    :ivar mass: mass of the body in (kg)
    :vartype mass: int or float
    :ivar position: position of the center of mass, only x- and y-dimension is set in (m)
    :vartype position: list of int or float
    :ivar type: type of the mass is "steady body". It is used to differentiate between a masspoint and a steady body in the rest of the Code.
    :vartype type: str
    :ivar sym_h: symbolic height of the steady body
    :vartype sym_h: sympy.Symbol
    :ivar sym_l: symbolic length of the steady body
    :vartype sym_l: sympy.Symbol
    :ivar sym_w: symbolic width of the steady body
    :vartype sym_w: sympy.Symbol
    """
    def __init__(self, x_dim, y_dim, z_dim, density, index):
        """
        Initialize the SteadyBody instance

        :param x_dim: dimension of the steady body along the x-axis in (m)
        :type x_dim: int or float
        :param y_dim: dimension of the steady body along the y-axis in (m)
        :type y_dim: int or float
        :param z_dim: dimension of the steady body along the z-axis in (m)
        :type z_dim: int or float
        :param density: density of the material of the steady body in (kg/m^3)
        :type density: int or float
        :param index: index of the steady body in the system which is used for the Notation of the symbolic vaules
        :type index: int
        """    
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim
        self.density = density
        self.volume = self.x_dim*self.y_dim*self.z_dim
        self.mass = self.volume*self.density
        self.position = [] # is the position of the center of mass
        self.type = "steady body"
        self.sym_h = sp.Symbol("h_"+str(index))
        self.sym_l = sp.Symbol("l_"+str(index))
        self.sym_w = sp.Symbol("w_"+str(index))

        Mass.__init__(self, index)
    
    def get_param_values(self):
        """
        Get numeric values for the symbolic representations

        :return: dictionary of symbolic parameters and their values
        :rtype: dict
        """    
        return {self.sym_mass: self.mass, self.sym_l: self.x_dim ,self.sym_h: self.y_dim, self.sym_w: self.z_dim}

