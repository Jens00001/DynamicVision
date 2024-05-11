import sympy as sp
import numpy as np

class Spring:
    """"
    Class for creating a Spring object

    :param startingpoint: startingpoint of the spring
    :type startingpoint: list of float numbers with two elements [x,y]
    :param rest_length: the length of the spring in the rest position 
    :type rest_length: int or float
    :param length: the current length of the spring in each position 
    :type length: int or float
    :param stiffness: stifness of the spring
    :type stiffness: int or float
    :param type: the type of the spring (linear or cubic), default is linear
    :type type: str
    :param endpoint: endpoint of the spring
    :type endpoint: list of float numbers with two elements [x,y]
    :param color: color of the spring in the visualization, default is black
    :type color: str
    :param sym_rest_length: the length of the spring in the rest position 
    :type sym_rest_length: sympy.Symbol
    :param sym_length: the current length of the spring in each position  
    :type sym_length: sympy.Symbol
    :param sym_stiffness: stifness of the spring
    :type sym_stiffness: sympy.Symbol
    :param sym_U: potential energy of the spring
    :type sym_U: sympy.Add or sympy.Mul
    """
    def __init__(self, startingpoint, rest_length, stiffness, type = "linear", color="black"):
        self.startingpoint = startingpoint
        self.rest_length = rest_length # in m
        self.length = self.rest_length # in m        
        self.stiffness = stiffness
        self.type = type
        self.endpoint = self.startingpoint + [0,self.length]
        self.color = color
        self.sym_rest_length = sp.Symbol("l_0")
        self.sym_length = sp.Symbol("l")
        self.sym_stiffness = sp.Symbol("k")
        self.sym_U = sp.Symbol("U") #potential energy
      
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
        

    def energy(self, xt):
        """"
        Method for computing the energy of the spring in its current position

        :param xt: is the symbolic expression for the change in the y-coordinate of the end point of the spring from the rest position
        :type xt: sympy.Function 
        :return: potential energy of the spring
        :rtype: sympy.Add or sympy.Mul
        """
        # assert isinstance(xt,) TODO
        match self.type:
            case "linear":
                self.sym_U = 1/2 * self.sym_stiffness * xt**2
            
            case "cubic":
                self.sym_U = self.sym_stiffness * xt**3
        
        return self.sym_U
    
    def move(self,x):
        """
        Method for computing the new lenght and y-coordinate of the end point of the spring by a given change x

        :param x: is the value of the change in the y-coordinate of the end point of the spring from the rest position
        :type x: int or float
        :return: current length of the spring and current endpoint of the spring
        :rtype: tuple 
        """
        self.length += x
        self.endpoint[1] += x

        return self.length, self.endpoint
    

class Mass:
    """
    Class for creating a mass object

    :param mass: value of the mass
    :type mass: int or float
    :param sym_mass: mass
    :type sym_mass: sympy.Symbol
    :param position: position of the mass
    :type position: list of float numbers with two elements [x,y]
    :param color: color of the mass in the visualization, default is red
    :type color: str
    :param T: kinetic energy
    :type T: sympy.Add or sympy.Mul
    :param U: potential energy 
    :type U: sympy.Add or sympy.Mul
    """
    def __init__(self, mass, position, color ="red"):
        self.mass = mass
        self.sym_mass = sp.Symbol("m")
        self.position = position
        self.color = color 
        self.sym_T = sp.Symbol("T") # kinetic energy
        self.sym_U = sp.Symbol("U") # potential energy

    def check_attributes(self):
        """
        Method for checking the type of input variable

        :raises AssertionError: if the type of the input variable is wrong
        """
        assert isinstance(self.position, list)
        assert self.position.shape == (2,)
        assert isinstance(self.mass,(int,float))
        assert isinstance(self.color, str)

    def energy(self,xt,xdt,g):
        """" 
        Method for computing the energy of the spring in its current position

        :param xt: is the symbolic expression for the change in the y-coordinate of the position of the mass
        :type xt: sympy.Function
        :param xdt: is the symbolic expression for the velocity of the change in the y-coordinate of the position of the mass
        :type xdt: sympy.function.Derivative
        :param g: earth gravity
        :type g: sympy.Symbol
        :return: kinetic energy and potential energy 
        :rtype: tuple
        """  
        #TODO assert check     
        self.T = 1/2 * self.sym_mass * xdt**2
        self.U = -self.sym_mass * g * xt

        return self.T, self.U
    
    def move(self,x):
        """
        :param x: is the value of the change in the y-coordinate of the position of the mass
        :type x: int or float
        :return: position of the mass
        :rtype: list[(int,float)]
        """
        self.position[1] += x

        return self.position