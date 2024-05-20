import sympy as sp
import numpy as np

class Spring:
    """"
    Class for creating a Spring object

    :param startingpoint: startingpoint of the spring in (m)
    :type startingpoint: list of float numbers with two elements [x,y]
    :param rest_length: the length of the spring in the rest position in (m)
    :type rest_length: int or float
    :param inital_angle: the intital angle of the spring in (°)
    :type inital_angle: int or float
    :param stiffness: stifness of the spring in (N/m)
    :type stiffness: int or float
    :param index: index of the spring in the system
    :type index: int
    :param type: the type of the spring (linear or cubic), default is linear
    :type type: str
    :param endpoint: endpoint of the spring in (m)
    :type endpoint: list of float numbers with two elements [x,y]
    :param color: color of the spring in the animation, default is black
    :type color: str
    :param lienwidth: the lienwidth of the spring in the animation
    :type lienwidth: int or float
    """
    def __init__(self, startingpoint, stiffness, rest_length, index, inital_angle = 0 , type = "linear", color="black", lienwidth=2):
        self.startingpoint = startingpoint # in (m)
        self.rest_length = rest_length # in (m)
        self.length = self.rest_length # in (m) 
        self.index = index
        self.inital_angle = inital_angle # in °
        self.angle = inital_angle      # in ° 
        self.stiffness = stiffness # in (N/m)
        self.type = type
        self.endpoint = [self.startingpoint[0] - self.length*np.sin(self.angle), self.startingpoint[1] - self.length*np.cos(self.angle)] # in (m)
        self.color = color
        self.lw =lienwidth

        #definiton of symbolic values 
        t = sp.Symbol("t")
        self.xt = sp.Function("x"+str(self.index))(t)
        self.xdt = self.xt.diff(t)
        self.xddt = self.xt.diff(t,2)
        self.phit = sp.Function("phi"+str(self.index))(t)
        self.phidt = self.phit.diff(t)
        self.phiddt = self.phit.diff(t,2)
        self.sym_rest_length = sp.Symbol("l"+str(self.index)+"_0")
        self.sym_length = sp.Symbol("l"+str(self.index))
        self.sym_stiffness = sp.Symbol("k"+str(self.index))
        self.sym_F = sp.Symbol("F"+str(self.index)) #force
      
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
        assert isinstance(self.inital_angle, (int, float))
        assert isinstance(self.angle, (int, float))
        assert isinstance(self.stiffness, (int, float))
        assert isinstance(self.type, str)
        assert isinstance(self.endpoint, list)
        assert self.endpoint.shape == (2,)
        assert isinstance(self.color, str)
        assert isinstance(self.lw, (int,float))
        

    def force(self,xt_attached):
        """"
        Method for computing the force of the spring in its current position

        :param xt_attached: is the displacement of the object where the spring is attached
        :type xt_attached: sympy.Function
        :return: force of the spring
        :rtype: sympy.Add or sympy.Mul
        """
       
        match self.type:
            case "linear":
                self.sym_F =  self.sym_stiffness * (self.xt-xt_attached-self.sym_rest_length)
            
            case "rotational":
                self.sym_F = self.sym_stiffness * self.phit
        
        return self.sym_F
    
    def move(self,attached_point, connected_point_below, angle=0):
        """
        Method for computing the new lenght and y-coordinate of the end point of the spring by a given change x

        :param x: is the value of the change of the length
        :type x: int or float
        :param angle: is the value of the change of the angle
        :type angle: int or float
        :param attached_point: is the point where the spring is attached
        :type attached_point: list
        :return: current startingpoint, angle, length and endpoint of the spring 
        :rtype: list 
        """
        self.startingpoint = attached_point
        # self.angle += angle
        # self.length += x
        self.endpoint = connected_point_below

        return [self.startingpoint,  self.endpoint]
    
    def get_param_values(self):
        
        return {self.sym_rest_length: self.rest_length,self.sym_stiffness: self.stiffness}

class Mass:
    """
    Class for creating a mass object

    :param position: position of the mass in (m)
    :type position: list of float numbers with two elements [x,y]
    :param mass: value of the mass in (kg)
    :type mass: int or float
    :param index: index of the mass in the system
    :type index: int
    :param diameter: diameter of the mass in the animation
    :param color: color of the mass in the animation, default is red
    :type color: str
    """
    def __init__(self, position, mass, index, diameter= 0.1, color ="red"):
        self.position = position
        self.mass = mass
        self.index = index
        self.color = color 
        self.diameter = diameter

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

    def force(self):
        """" 
        Method for computing the gravitational force of the mass

        :return: gravitational force
        :rtype: sympy.Add
        """  
             
        self.sym_F = self.sym_mass*self.sym_g

        return self.sym_F
    
    def move(self,x,y):
        """
        :param attached_point: is the point where the mass is attached
        :type attached_point: list
        :return: position of the mass
        :rtype: list
        """
        self.position = [x,y]

        return self.position
    
    def get_param_values(self):
        
        return {self.sym_mass: self.mass}