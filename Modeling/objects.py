import sympy as sp
import numpy as np

class Spring:
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
        xt is the symbolic expression for the change from the rest postion
        """
        # assert isinstance(xt,) TODO
        match self.type:
            case "linear":
                self.sym_U = 1/2 * self.sym_stiffness * xt**2
            
            case "qubic":
                self.sym_U = self.sym_stiffness * xt**3
        
        return self.sym_U
    
    def move(self,x):
        """
        x is the value of the change from the rest positon
        """
        self.length += x
        self.endpoint[1] += x

        return self.length, self.endpoint
    

class Mass:
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

    def enery(self,xt,xdt,g):
        """" 
        xt is the symbolic expression for the change from the rest postion
        xdt is the symbolic expression for the velocity of the change from the rest position
        g is the earth gravity
        """  
        #TODO assert check     
        self.T = 1/2 * self.sym_mass * xdt**2
        self.U = -self.sym_mass * g * xt

        return self.T, self.U
    
    def move(self,x):
        """
        x is the value of the change from the rest positon
        """
        self.position[1] += x

        return self.position