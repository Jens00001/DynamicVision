from netCDF4 import Dataset
from sympy import sympify
from numpy import array
from os import path, remove
from additions import eq_to_latex

def save(file_name="data.nc", data=None, names=None):
    """
    Method for saving the simulated data (and symbolic equation). To save data it uses the netCDF4 library
    that is based on HDF5. HDF5 is uses optimized structures and algorithms to allow an efficient saving
    and reading of one- and multidimensional tables.
    The data is saved in a binary format. So it is machine-independent and the possibility of compression enables an
    easy and efficient way to save data.
    The given input data is appended to list which is saved in a binary table.

    :param file_name: name of the wanted file (with or without .nc)
    :type file_name: string
    :param data: data to save
    :type data: list of int or list of float or list of str
    :param names: names of the corresponding data (like keys for python dictionaries)
    :type names: list of strings
    """

    # check if ".nc" is already in file name
    if ".nc" in file_name:
        name_str = file_name
    else:
        name_str = file_name + ".nc"

    # check if names is empty, if so create default data names
    if names is None:
        data_names = [f'{"res"}{i}' for i in range(len(data))]
    else:
        data_names = names

    # open/create file in write mode ("w")
    data_file = Dataset(name_str, "w")

    # define data dimensions
    data_dim = []
    for i in range(len(data_names)):
        data_dim.append(data_file.createDimension(data_names[i], size=None))

    # define data variables
    data_var = []
    for n, d, di in zip(data_names, data, data_dim):
        data_var.append(data_file.createVariable(n, datatype=d.dtype, dimensions=(di,)))

    # write data to file
    for n, d in zip(data_names, data):
        data_file.variables[n][:] = d[:]

    # close file
    data_file.close()


def save_system(file_name="data.nc", sim_res=None, system=None,  names=None):
    """
    Method for saving the simulated data and the mechanical system. This method is based on the save() function
    that uses the netCDF4 library. It is optimized to save simulation data and the simulated system itself.
    It takes the simulated data and the important properties of the mechanical system
    (that are needed to reconstruct the system) and saves the data by creating a list that is passed to the save() function.

    :param file_name: name of the wanted file (with or without .nc)
    :type file_name: string
    :param sim_res: simulation results
    :type sim_res: string
    :param system: mechanical system
    :type system: Newton System
    :param names: names of the corresponding data (like keys for python dictionaries)
    :type names: list of strings
    """

    # get masses to save forces
    masses = [str(system.parameters[key]['mass']) for key in system.parameters]
    forces = [system.forces.get(mass, []) for mass in masses]
    # save system
    sym_data = array(
        [str(system.param_values), str(system.parameters), str(system.coordinates),
         str(system.velocities), str(system.accelerations), str(forces), str(system.constraints)])

    # save time
    save_data = [sim_res.t]
    # save simulation result
    save_data.extend(sim_res.y)
    save_data.append(sym_data)

    save(file_name, save_data, names)


def load(file_name="data.nc", num_data=(0,)):
    """
    Method for loading the simulated data in the current workspace. The file to be loaded must be saved in .nc format.
    To save data you can use the netCDF4 library that is based on HDF5. HDF5 is uses optimized structures
    and algorithms to allow an efficient saving and reading of one- and multidimensional tables.
    The data is saved in a binary format. So it is machine-independent and the possibility of compression enables an
    easy and efficient way to save data. As long as this criterion is met, the data can be loaded with the load() function.
    The method loads each column in sequence and saves them in a list.

    :param file_name: name of the file you want to load (with or without .nc)
    :type file_name: string
    :param num_data: Which data should be loaded?
                     Default value loads all data inside file.
                     One Value loads one column: (x,). "x" corresponds to the index of the data you want to load.
                     Two values load data between the values: (x,y).
                     "x" and "y" corresponds to the indices of the data you want to load (and the data between these indices).
    :type num_data: tuple of int
    :return: data loaded from file
    :rtype: list of lists (of int, float or string)
    """

    # check if ".nc" is already in file name
    if ".nc" in file_name:
        name_str = file_name
    else:
        name_str = file_name + ".nc"

    # open file in read mode ("r")
    data_file = Dataset(name_str, 'r')

    # get data_keys (name of the saved data) --> like keys for python dictionaries
    data_keys = data_file.variables.keys()

    data = []

    '''
    check for second method parameter num_data:
    - if there are two values inside the tuple num_data, save the data keys starting from the first value 
      in num_data up to the second value(included) in num_data in variable "data". 
      e.g. num_data=(0, 1): data = [data_keys[0], data_keys[1]]
    - if there is only one value in num_data unequal to zero, 
      save the data key corresponding to the value in variable "data". 
      e.g. num_data=(2,): data = [data_keys[2]]
    - if there is only one value in num_data equal to zero (default), save all data keys in variable "data".
      e.g. num_data=(0,): data = [data_keys[0], ..., data_keys[-1]] 
    '''
    if len(num_data) > 1:
        data = [data_keys[i] for i in range(num_data[-1] + 1)]
    elif len(num_data) == 1 and num_data[0] > 0:
        data.append(data_keys[num_data[0]])
    else:
        data = data_keys

    # save data regarding the data keys in variable "data_set" and return it as a list of lists
    data_set = [data_file.variables[n] for n in data]  # faster than for-loop

    return data_set


def load_system(file_name="data.nc"):
    """
    Method for loading the simulation results and the simulated system.
    This method is based on the load() function that uses the netCDF4 library.
    It is optimized to load simulation data and the simulated system itself. It exports the simulated results
    and the properties of mechanical system to a dictionary for an easy access. After that the simulation results
    can be plotted and the mechanical system can be reconstructed.

    :param file_name: name of the file you want to load (with or without .nc)
    :type file_name: string
    :return: data loaded from file {time,results,system}
    :rtype: dictionary
    """

    data = load(file_name, num_data=(0,))
    loaded_data = {'time': data[0][:],
                   'results': [d[:] for d in data[1:-1]],
                   'system': {'param_values': sympify(data[9][0]),
                              'masses': list(sympify(data[9][1]).keys()),
                              'coordinates': sympify(data[9][2]),
                              'velocities': sympify(data[9][3]),
                              'accelerations': sympify(data[9][4]),
                              'forces': sympify(data[9][5]),
                              'constraints': sympify(data[9][6])
                              }
                   }
    return loaded_data


def tex_save(file_name="tex_equation.txt", system=None):
    """
    Method for saving the symbolic equation in latex format. It takes a mechanical system as an input and saves its
    equation of motion in LaTex format to a .txt file. It uses the eq_to_latex() function of the addition library
    to convert the equations of motion of the given system into LaTeX notion.

    :param file_name: name of the wanted file (with or without .txt)
    :type file_name: string
    :param system: system to save (equations of motions)
    :type system: newton.Mechanics Class
    """

    # check if ".txt" is already in file name
    if ".txt" in file_name:
        name_str = file_name
    else:
        name_str = file_name + ".txt"

    # check if file already exits and delete it
    if path.exists(name_str):
        remove(name_str)

    # open and create a new file
    file = open(name_str, "w")

    # get latex expression of equation of motion and remove dollar sign
    equation = eq_to_latex(system).replace("$", "")

    # write to file
    file.write(equation)

    # close file
    file.close()
