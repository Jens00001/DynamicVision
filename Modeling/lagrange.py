from sympy import lambdify, Mul, Add, Symbol, trigsimp, Eq, solve
from scipy.integrate import solve_ivp
from numpy import linspace


class Lagrange:
    """
    Class for calculating the equation of motion using Lagrange (symbolic), only second order systems possible

    :param q: generalized coordinate of the system and the derivatives
    :type q: list of lists of sympy.Function (q depends on time q(t)) [[q1,dq1,ddq1],[q2,dq2,ddq2],...]
    :param t: time variable
    :type t: sympy.Symbol
    :param T: kinetic energy
    :type T: sympy.Add or sympy.Mul
    :param U: potential energy
    :type U: sympy.Add or sympy.Mul
    :param F: external force (1-dim force) e.g. constant force or damper
    :type F: list of sympy.Add, sympy.Mul or int/float if the force is constant
    """

    def __init__(self, q, t, T, U, F):
        self.T = T
        self.U = U
        self.q = q
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
        assert isinstance(self.F, (list, Mul, Add, int, float))

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
        :rtype: dict of sympy.Add with second derivative as key and rhs as value
        """
        num_q = len(self.q)

        # get second derivatives
        acc = [self.q[i][-1] for i in range(num_q)]

        # get Lagrange function
        L = self.lagrange_equation()

        # init lists
        L_dq = []
        L_dqd = []
        DL_dqd = []
        eq = []
        eq_rhs = []

        if not isinstance(self.F, list):
            self.F = [self.F, ]

        # compute derivatives of Lagrange function regarding the generalized coordinate
        for i in range(num_q):
            L_dq.append(L.diff(self.q[i][0]))
            L_dqd.append(L.diff(self.q[i][1]))
            DL_dqd.append(L_dqd[i].diff(self.t))
            eq.append(DL_dqd[i] - L_dq[i] - self.F[i])

            # Set up the equation according to the pattern: eq = 0
            eq_rhs.append(Eq(eq[i], 0))

        # return equation rearranged for the second derivative
        return solve(eq_rhs, acc)

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
        L = self.lagrangian()
        num_L = len(L)
        # create list with variables that are needed for the lambdify function: [t,q1,q2,...,dq1,dq2,...]
        q_list = [self.t]
        for j in range(len(self.q[0]) - 1):
            for i in range(num_L):
                q_list.append(self.q[i][j])

        # Convert symbolic functions to a callable functions
        rhs_func = [lambdify(q_list, L[self.q[i][2]], 'numpy') for i in range(num_L)]

        # function to convert second order system to two first order systems
        def sim_fun(t, y):
            y_len = len(y)
            y_half_len = int(y_len/2)

            # create list of parameters
            param_list = [t]
            param_list.extend(y)
            y_dot = []

            # construct the derivative of the state vector
            for n in range(y_len):
                # the first half are the derivatives
                if n < y_half_len:
                    y_dot.append(y[y_half_len + n])
                # the second half are the second derivatives
                else:
                    y_dot.append(rhs_func[n - y_half_len](*param_list))
            return y_dot

        # return solved/simulated problem (solve problem by inserting numerical values)
        return solve_ivp(sim_fun, t_span, init_cond, t_eval=linspace(t_span[0], t_span[1], num_points), rtol=1e-5)

