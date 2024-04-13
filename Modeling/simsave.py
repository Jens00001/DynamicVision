from h5py import File


def save(file_name="data.hdf5", data_names=None, data=None):
    """
    Method for saving the simulated data

    :param file_name: name of the wanted file (with or without .hdf5)
    :type file_name: string
    :param data_names: names of the corresponding data (like keys for python dictionaries)
    :type data_names: list of strings
    :param data: data to save
    :type data: list of int or float
    """

    # check if ".hdf5" is already in file name
    if ".hdf5" in file_name:
        name_str = file_name
    else:
        name_str = file_name + ".hdf5"

    # open/create file in write mode ("w")
    data_file = File(name_str, "w")

    # write data to file
    for i in range(len(data_names)):
        data_file.create_dataset(data_names[i], data=data[i])


def load(file_name="data.hdf5", num_data=(0,)):
    """
    Method for loading the simulated data in the current workspace

    :param file_name: name of the file you want to load (with or without .hdf5)
    :type file_name: string
    :param num_data: Which data should be loaded?
                     Default value loads all data inside file.
                     One Value loads one column: (0). "x" corresponds to the index of the data you want to load.
                     Two values load data between the values: (x,y).
                        "x" and "y" corresponds to the indices of the data you want to load (and the data between these indices).
    :type num_data: tuple of int
    :return: data loaded from file
    :rtype: list of lists (of int or float)
    """

    # check if ".hdf5" is already in file name
    if ".hdf5" in file_name:
        name_str = file_name
    else:
        name_str = file_name + ".hdf5"

    # open file in read mode ("r")
    data_file = File(name_str, 'r')

    # save data_keys (name of the saved data) --> like keys for python dictionaries
    data_keys = list(data_file.keys())
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
    len_data = len(data)
    data_set = [data_file[data[i]] for i in range(len_data)]    # faster than for-loop

    return data_set
