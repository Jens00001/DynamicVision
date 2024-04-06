from sympy import sin, cos, Function
import sympy as sp
import sys

class Lagrange:
    """
    Class for calculating the equation of motion using Lagrange (symbolic)

    :param q: generalized coordinate of the system
    :type q: sympy.Function (q depends on time q(t))
    :param t: time variable
    :type t: sympy.Symbol
    :param T: kinetic energy
    :type T: sympy.Add or sympy.Mul
    :param U: potential energy
    :type U: sympy.Add or sympy.Mul
    :param k: kinematic (geometric) equation
    :type k: sympy.Add, sympy.Mul or int if there is no kinematic equation
    :raises Lagrange.InvalidCoordError: If the generalized coordinate is invalid
    :raises Lagrange.InvalidEnergyError: If the energies is invalid
    :raises Lagrange.InvalidKinematicError: If the kinematic equation is invalid
    :return: symbolic equation of motion
    :rtype: sympy.Add (symbolic sum --> equation of motion)
    """

    def __init__(self, q, t, T, U, k):
        self.T = T      # kinetic energy
        self.U = U      # potential energy
        self.q = q      # generalized coordinate
        self.k = k      # kinetic
        self.t = t      # time variable

    def __repr__(self):
        return str(list(self.__dict__.items()))

    def check_attributes(self):
        assert isinstance(self.T, (sp.Mul, sp.Add))          # kinetic energy is either a single term or a sum
        assert isinstance(self.U, (sp.Mul, sp.Add))          # potential energy is either a single term or a sum
        assert isinstance(self.q, sp.Function)               # generalized coordinate is a function of time
        assert isinstance(self.k, (sp.Mul, sp.Add, int))     # kinematic equation is either a single term, a sum or 0 (int)

    def lagrange_equation(self):
        L = self.T - self.U
        L = L.expand()
        L = sp.trigsimp(L)
        self.L = L
        return self.L

    def equation_of_motion(self):
        L_dq = self.L.diff(self.q)
        L_dqd = self.L.diff(self.q.diff(self.t))
        DL_dqd = L_dqd.diff(self.t)
        eq = DL_dqd - L_dq
        eq = eq.expand()
        eq = sp.trigsimp(eq)
        self.eq = eq
        return self.eq


    # TODO:
    # implement translatoric external force
    # implement multiple generalized coordinates
