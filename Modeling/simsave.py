from netCDF4 import Dataset
from sympy import latex

def save(file_name="data.nc", data=None, names=None):
    """
    Method for saving the simulated data (and symbolic equation)

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


def load(file_name="data.nc", num_data=(0,)):
    """
    Method for loading the simulated data in the current workspace

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


def tex_save(file_name="tex_equation.txt", data=None):
    """
    Method for saving the symbolic equation in latex format

    :param file_name: name of the wanted file (with or without .txt)
    :type file_name: string
    :param data: data to save (equation)
    :type data: list of symbolic equations
    """

    # check if ".txt" is already in file name
    if ".txt" in file_name:
        name_str = file_name
    else:
        name_str = file_name + ".txt"

    # open and create file
    file = open(name_str, "w")

    # check for one or more equations
    if isinstance(data, list):
        for d in data:
            file.write(latex(d) + "\n")
    else:
        file.write(latex(data))

    # close file
    file.close()
