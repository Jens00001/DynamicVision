import sympy as sp
from sympy import lambdify
from scipy.integrate import solve_ivp
from numpy import linspace
class Lagrange:
    """
    Class for calculating the equation of motion using Lagrange (symbolic)

    :param q: generalized coordinate of the system and the derivatives that appear in the equations
    :type q: list of sympy.Function (q depends on time q(t))
    :param t: time variable
    :type t: sympy.Symbol
    :param T: kinetic energy
    :type T: sympy.Add or sympy.Mul
    :param U: potential energy
    :type U: sympy.Add or sympy.Mul
    :param F: external force (1-dim linear force)
    :type F: sympy.Add, sympy.Mul or int if the force is constant
    :param k: kinematic (geometric) equation
    :type k: sympy.Add, sympy.Mul or int if the kinematic equation is constant
    :raises Lagrange.InvalidCoordError: If the generalized coordinate is invalid
    :raises Lagrange.InvalidEnergyError: If the energies is invalid
    :raises Lagrange.InvalidKinematicError: If the kinematic equation is invalid
    """

    def __init__(self, q, t, T, U, F, k):
        self.T = T
        self.U = U
        self.q = q
        self.k = k
        self.t = t
        self.F = F

    def __repr__(self):
        return str(list(self.__dict__.items()))

    def check_attributes(self):
        assert isinstance(self.T, (sp.Mul, sp.Add))
        assert isinstance(self.U, (sp.Mul, sp.Add))
        assert isinstance(self.q, list)
        assert isinstance(self.k, (sp.Mul, sp.Add, int))

    def lagrange_equation(self):
        # This function calculates the lagrangian
        L = self.T - self.U
        L = L.expand()
        return sp.trigsimp(L)

    def lagrangian(self):
        """
        Function for computing the analytical Lagrange equations

        :return: symbolic equation of motion
        :rtype: sympy.Add (symbolic sum --> equation of motion)
        """
        L = self.lagrange_equation()
        # This function calculates the equation of motion
        L_dq = L.diff(self.q[0])
        L_dqd = L.diff(self.q[1])
        DL_dqd = L_dqd.diff(self.t)
        eq = DL_dqd - L_dq - self.F
        eq = eq.expand()
        eq = sp.trigsimp(eq)
        eq = sp.Eq(eq, 0)
        return sp.solve(eq, self.q[0].diff(self.t, 2))

    def simulate(self, init_cond, t_span, num_points=1001):
        """
        Function for computing the numerical equation of motion for simulation

        :return: list of first order differential equations
        :rtype: list
        """
        # get Lagrangian
        L = self.lagrangian()[0]

        # Convert symbolic function to a callable function
        rhs_func = lambdify((self.t, self.q[0]), L.subs(self.q[0].diff(self.t), self.q[1]))

        # function to convert second order system to two first order system
        def second_to_one(t, y):
            return [y[1], rhs_func(t, y[0])]

        return solve_ivp(second_to_one, t_span, init_cond, t_eval=linspace(t_span[0], t_span[1], num_points))

    # TODO:
    # extend check_attribute method
    # implement more than only second order systems
    # implement the possibility for kinematic equations --> e.x. pre-strech of spring
    # insert documentation for every method
