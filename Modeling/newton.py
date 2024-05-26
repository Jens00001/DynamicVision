from sympy import Function, Eq, symbols, lambdify, pprint
from scipy.integrate import solve_ivp
from numpy import linspace, concatenate
from re import search


class Mechanics:
    """
    Class for calculating the equation of motion using Newton in 2 dimensions

    :param parameters: store mass parameter needed for free-body principle/principle of intersection
    :type parameters: dictionary
    :param coordinates: coordinate of every mass
    :type coordinates: dictionary
    :param velocities: velocities of every mass
    :type velocities: dictionary
    :param accelerations: accelerations of every mass
    :type accelerations: dictionary
    :param forces: sum of force at every mass resulting the free-body principle/principle of intersection
    :type forces: dictionary
    :param param_values: Values of parameters like k, m, g,...
    :type param_values: dictionary
    :param t: time variable
    :type t: sympy.Symbols
    """

    def __init__(self):
        self.parameters = {}
        self.coordinates = {}
        self.velocities = {}
        self.accelerations = {}
        self.forces = {}
        self.constraints = {}
        self.param_values = {}
        self.t = symbols("t")

    def add_mass(self, name, mass):
        """
        Method for adding masses and computing their corresponding coordinates, velocities and accelerations

        :param name: name of the mass. Eg: m1, m2, m3,...
        :type name: string
        :param mass: symbol of the mass. Eg: m1, m2, m3,...
        :type mass: sympy.symbols()
        """

        # define mass
        self.parameters[name] = {'mass': mass}

        # regular expression to find the integer at the end (number of the mass)
        integer = search(r'\d+', name)
        name_int = int(integer.group())

        # define coordinates and their derivatives for x and y directions (2-dimensional)
        x = Function(f'x{name_int}')(self.t)
        y = Function(f'y{name_int}')(self.t)
        xdot = x.diff(self.t)
        ydot = y.diff(self.t)
        xddot = x.diff(self.t, 2)
        yddot = y.diff(self.t, 2)

        # save coordinates and derivatives in dictionary
        self.coordinates[name] = {'x': x, 'y': y}
        self.velocities[name] = {'x': xdot, 'y': ydot}
        self.accelerations[name] = {'x': xddot, 'y': yddot}

    def add_force(self, mass, force):
        """
        Method for adding forces that act on the corresponding mass

        :param mass: Mass on which the forces act
        :type mass: string
        :param force: forces that act on the corresponding mass
        :type force: sympy.Add()
        """

        # for first mass added to the system we need to initialize the list
        if mass not in self.forces:
            self.forces[mass] = []
        self.forces[mass].append(force)


    def sum_of_force(self, name, dir):
        """
        Method for computing the sum of the forces regarding the directions x and y

        :param name: Mass on which the forces act
        :type name: string
        :param dir: direction of the sum of forces acting on the corresponding mass
        :type dir: sympy.Add()
        :return: symbolic sum of forces
        :rtype: sympy.Add()
        """
        # list of (force, direction) tuples
        forces_with_directions = self.forces.get(name, [])

        total_force = 0
        # loop through each (force, direction) tuple
        for force, direction in forces_with_directions:
            # sum up the force if the direction matches accordingly
            if direction == dir:
                total_force += force

        return total_force

    def generate_constraint(self, constraint_type, start_point, end_point, dimension):
        """
        Method for generating geometric relationships between two points/masses

        :param constraint_type: type of constraint. Eg. "link"
        :type constraint_type: string
        :param start_point: starting point to define constraint. Eg. mass1.
        :type start_point: string
        :param end_point: ending point to define constraint. Eg. mass2.
            If start = end: The function computes relationship between end_point and coordinate origin.
        :type end_point: string
        :param dimension: For link type: distance between start and end point
        :type dimension: sympy.Symbols
        """

        '''
        TODO:
            Only two kinds of constraints exit for a 2-dimensional system. "Links" (eg. spring) and "angles" (eg. pendulum).
            --> "angle" constraint type will be implemented at a later time.
        '''
        if constraint_type == "link":
            # check if user wants to generate geometric relationship between mass and coordinate origin
            if start_point == end_point:
                link_from_x = 0
                link_from_y = 0
            else:
                link_from_x = self.coordinates[start_point]['x']
                link_from_y = self.coordinates[start_point]['y']

            link_to_x = self.coordinates[end_point]['x']
            link_to_y = self.coordinates[end_point]['y']
            link_length = dimension

            # define link constraint
            constraint_expr = Eq((link_to_x - link_from_x) ** 2 + (link_to_y - link_from_y) ** 2, link_length ** 2)
            self.constraints[start_point + '->' + end_point] = {"constraint type": constraint_type, "constraint": constraint_expr}

    def generate_equations(self):
        """
        Method for computing the equations of motion for every mass and direction

        :return: symbolic equations of motion
        :rtype: list of sympy.Add()
        """

        equations = []
        for name in self.parameters:
            # current mass
            m = self.parameters[name]['mass']

            # accelerations for x and y directions
            xddot = self.accelerations[name]['x']
            yddot = self.accelerations[name]['y']

            # sum of forces in x and y directions (sum of all applied forces)
            F_sum_x = self.sum_of_force(name, 'x')
            F_sum_y = self.sum_of_force(name, 'y')

            # Newton's second law: F=ma <=> a=F/m
            eq_x = Eq(xddot, F_sum_x / m)
            eq_y = Eq(yddot, F_sum_y / m)

            # alternately append equations regarding x and y direction
            equations.append(eq_x)
            equations.append(eq_y)

        return equations

    def substitute_parameters(self, equations, param):
        """
        Method for substituting the parameters of the system (masses, spring constants, etc.)

        :param equations: Equations in which the parameters are substituted (list of equations)
        :type equations: list of sympy.Add()
        :param param: Parameter values. The keys are the name of the parameters.
        :type param: dictionary
        :return: equations with substituted parameters
        :rtype: list of sympy.Add()
        """
        return [eq.subs(param) for eq in equations]

    def rhs_of_equation(self, equations):
        """
        Method for computing the right hand side of the equations

        :param equations: (Substituted) equations of motion
        :type equations: list of sympy.Add()
        :return: right hand side of the equations
        :rtype: list of sympy.Add()
        """
        return [eq.rhs for eq in equations]

    def simulate(self, param_values, init_cond, t_span, num_points=1001):
        """
        Method to simulate (integrate) the given system

        :param param_values: parameter of the given system. For example masses, spring constants,...)
        :type param_values: dictionary
        :param init_cond: initial conditions regarding the system (Initial state)
        :type init_cond: list of int/float
        :param t_span: Interval of integration (start time and end time)
        :type t_span: tuple if int/float
        :param num_points: number of time steps for numerical integration
        :type num_points: int
        :return: See documentation of solve_ivp()
        :rtype: Bunch object
        """
        # get the equations of motion, substitute the parameters and store the right hand side of the equation
        eq = self.generate_equations()
        sub_equations = self.substitute_parameters(eq, param_values)
        eq_rhs = self.rhs_of_equation(sub_equations)

        # init lists for coordinates and velocities
        coord = []
        vel = []

        # construct lists of coordinates and velocities that are needed for the lambdify function
        for name in self.parameters:
            x = self.coordinates[name]['x']
            y = self.coordinates[name]['y']
            xdot = self.velocities[name]['x']
            ydot = self.velocities[name]['y']
            coord.extend([x, y])
            vel.extend([xdot, ydot])

        # Lambdify: transform the symbolic equation of motion to numeric equation of motion
        rhs_funcs = [lambdify(coord + vel, rhs) for rhs in eq_rhs]

        # function to convert a second order system to a first order system
        def sim_fun(t, z):
            half = len(z) // 2
            positions = z[:half]
            velocities = z[half:]

            # evaluate the lambdified function at the current position and velocity ("*" unpacks lists into positional arguments)
            rhs_evals = [f(*positions, *velocities) for f in rhs_funcs]

            # return state vector
            return concatenate((velocities, rhs_evals))

        # define the time points where the solution is computed
        t_eval = linspace(t_span[0], t_span[1], num_points)

        return solve_ivp(sim_fun, t_span, init_cond, t_eval=t_eval, rtol=1e-6)
