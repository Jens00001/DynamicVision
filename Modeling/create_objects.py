import objects
import ast

def create_objects(eq_sytle):
    """
    eq_style defines if the energy equations are with symbolic or numeric values
    """
    while True:
        
        object_type = input("Please enter the name of the object you want to insert: ")
        
        match object_type:
            case "Spring":
                list_of_springs = []
                startingpoint= ast.literal_eval(input("Please enter the startingpoint of the spring: "))
                rest_length = float(input("Please enter the rest length of the spring: "))
                stiffness = float(input("Please enter the stiffness of the spring: "))
                list_of_springs.append(objects.Spring(startingpoint,stiffness, rest_length))
            
            case "Mass":
                list_of_mass = []
                position = ast.literal_eval(input("Please enter the position of the mass: "))
                mass = float(input("Please enter weight of the mass: "))
                list_of_mass.append(objects.Mass(position, mass))

            case "stop":
                break

    return [list_of_springs, list_of_mass]
