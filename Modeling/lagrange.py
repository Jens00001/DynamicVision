from sympy import lambdify, Mul, Add, Symbol, trigsimp, Eq, solve
from scipy.integrate import solve_ivp
from numpy import linspace


class Lagrange:
    """
    Class for calculating the equation of motion using Lagrange (symbolic), only second order systems possible

    :param q: generalized coordinate of the system and the derivatives that appear in the equations
    :type q: list of sympy.Function (q depends on time q(t))
    :param t: time variable
    :type t: sympy.Symbol
    :param T: kinetic energy
    :type T: sympy.Add or sympy.Mul
    :param U: potential energy
    :type U: sympy.Add or sympy.Mul
    :param F: external force (1-dim linear force) e.g. constant force or damper
    :type F: sympy.Add, sympy.Mul or int/float if the force is constant
    :param k: kinematic (geometric) equation
    :type k: sympy.Add, sympy.Mul
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
        """
        Method for checking the type of input variable

        :raises AssertionError: if the type of the input variable is wrong
        """
        assert isinstance(self.T, (Mul, Add))
        assert isinstance(self.U, (Mul, Add))
        assert isinstance(self.q, list)
        assert isinstance(self.t, Symbol)
        assert isinstance(self.k, (Mul, Add))
        assert isinstance(self.F, (Mul, Add, int, float))

    def lagrange_equation(self):
        """
        Method for calculating the Lagrange function  L = T - U

        :return: symbolic Lagrange function
        :rtype: sympy.Add (symbolic sum --> Lagrange function)
        """
        L = self.T - self.U
        L = L.expand()          # simplify L
        return trigsimp(L)      # simplify L

    def lagrangian(self):
        """
        Method for computing the analytical Lagrange equations

        :return: right hand side symbolic equation of motion: x'' = a + bx +cx'
        :rtype: sympy.Add (symbolic sum --> equation of motion)
        """
        L = self.lagrange_equation()
        # This function calculates the equation of motion
        L_dq = L.diff(self.q[0])
        L_dqd = L.diff(self.q[1])
        DL_dqd = L_dqd.diff(self.t)
        eq = DL_dqd - L_dq + self.F
        eq = eq.expand()
        eq = trigsimp(eq)
        eq = Eq(eq, 0)
        return solve(eq, self.q[0].diff(self.t, 2))

    def simulate(self, init_cond, t_span, num_points=1001):
        """
        Method to simulate (integrate) the given system

        :param init_cond: initial conditions regarding the system (Initial state)
        :type init_cond: list of int/float
        :param t_span: Interval of integration (start time and end time)
        :type t_span: tuple if int/float
        :param num_points: number of time steps for numerical integration
        :type num_points: int
        :return: See documentation of solve_ivp()
        :rtype: Bunch object
        """
        # get Lagrangian
        L = self.lagrangian()[0]

        # Convert symbolic function to a callable function
        rhs_func = lambdify((self.t, self.q[0], self.q[1]), L.subs(self.q[0].diff(self.t), self.q[1]))

        # function to convert second order system to two first order systems
        def sim_fun(t, y):
            return [y[1], rhs_func(t, y[0], y[1])]

        return solve_ivp(sim_fun, t_span, init_cond, t_eval=linspace(t_span[0], t_span[1], num_points))

    # TODO:
    # implement the possibility for kinematic equations
