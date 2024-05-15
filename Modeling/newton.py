from sympy import lambdify, Mul, Add, Symbol, trigsimp, solve, pprint
from scipy.integrate import solve_ivp
from numpy import linspace, zeros_like

class mechanics:
    """
    Class for calculating the equation of motion using Newton (symbolic) in 2 dimensions

    :param force: forces resulting from the current free-body principle/principle of intersection at every mass
    :type force: list of lists of sp.Mul
    :param mass: masses of the corresponding forces
    :type mass: list of sp.Symbols
    :param coordinate: coordinate direction of the corresponding forces
    :type coordinate: list of coordinate direction in which the force acts
    :param angle: angle between the force and the y coordinates
    :type angle: list of lists of integers or list of lists of floats
    """

    def __init__(self, force, mass, coordinate, angle):
        self.force = force
        self.mass = mass
        self.coordinate = coordinate
        self.angle = angle

    def check_attributes(self):
        """
        Method for checking the type of input variable

        :raises AssertionError: if the type of the input variable is wrong
        """
        assert isinstance(self.force, list)
        assert isinstance(self.coordinate, list)
        assert isinstance(self.angle, list)

    def sum_of_force(self):
        """
        Method for computing the sum of the forces regarding the directions x and y

        :return: symbolic sum of forces regarding F_sum = 0
        :rtype: sympy.Add
        """
        sum_of_force_x = []
        for i in range(len(self.force)):
            sum_of_force_x.append(sum(self.force[i]))

        return sum_of_force_x

    def equation_of_motion(self):
        t = Symbol("t")

        # right hand side of the equation of motion (multiplied by the corresponding mass)
        rhs = self.sum_of_force()
        num_eq = len(rhs)

        # acceleration
        acc = [self.coordinate[i].diff(t, 2) for i in range(num_eq)]

        # left hand side of the equation of motion (mass * acceleration)
        lhs = [self.mass[i] * acc[i] for i in range(num_eq)]

        # equation of motion:  acceleration * mass - sum of forces = 0
        eom = [lhs[i] - rhs[i] for i in range(num_eq)]

        return eom

    def get_eom(self, eom):
        t = Symbol("t")
        # acceleration
        acc = [self.coordinate[i].diff(t, 2) for i in range(len(eom))]
        return solve(eom, acc)

    def simulate(self, eom, init_cond, t_span, num_points=1001):
        """
        Method to simulate (integrate) the given system

        :param eom: equation of motion with substituted parameters
        :type eom: list of sympy.Add
        :param init_cond: initial conditions regarding the system (Initial state)
        :type init_cond: list of int/float
        :param t_span: Interval of integration (start time and end time)
        :type t_span: tuple if int/float
        :param num_points: number of time steps for numerical integration
        :type num_points: int
        :return: See documentation of solve_ivp()
        :rtype: Bunch object
        """

        # get equation of motion
        func = self.get_eom(eom)
        num_eom = len(func)

        # create list with variables that are needed for the lambdify function: [q1,q2,...,dq1,dq2,...]
        t = Symbol("t")
        acc = [self.coordinate[i].diff(t, 2) for i in range(num_eom)]
        coord = self.coordinate
        dcoord = [self.coordinate[i].diff(t) for i in range(num_eom)]
        var_list = coord + dcoord
        # Convert symbolic functions to a callable functions
        rhs_func = [lambdify(var_list, func[acc[i]], 'numpy') for i in range(num_eom)]

        # Lambdify the accelerations
        # accelerations = [lambdify((t, x1, x2, v1, v2), a, modules='numpy') for a in [a1, a2]]


        # function to convert second order system to first order systems
        def sim_fun(t, y):
            pos = y[::2]
            velocity = y[1::2]
            # Compute accelerations
            a = [accel(*y) for accel in rhs_func]

            # Initialize state
            y_dot = zeros_like(y)
            y_dot[::2] = velocity
            y_dot[1::2] = a
            return y_dot

        # return solved/simulated problem
        return solve_ivp(sim_fun, t_span, init_cond, t_eval=linspace(t_span[0], t_span[1], num_points), rtol=1e-6)
