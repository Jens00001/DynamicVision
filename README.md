# DynamicVision: Dynamic Model Visualization Tool

The DynamicVision project aids engineers in understanding complex mechanical systems by allowing them to create, model, and simulate systems with a GUI, providing equations of motion, visualizations, and synchronized plots.

## Description

Engineers develop complex systems that often need to be modeled and simulated before the actual system can be created. For this reason, system modeling is a crucial part of engineering. Initially, mechanical systems consist of simple couplings of basic elements like springs, masses, and dampers. Analyzing and simulating these systems is not trivial, especially at the beginning of the engineering studies. This is often due to a lack of system understanding and an unclear idea of how the final system behaves.

The DynamicVision project addresses this issue. Users can use a GUI to create simple mechanical systems from springs and masses, which are then modeled and simulated. Users are provided with the resulting equations of motion for the respective system and a visualization. Additionally, plots synchronized with the visualization are generated.

TODO: step by step description how to use the programm

## Getting Started

### Dependencies

* Python Interpreter (Version >= 3.11)
* sympy
* numpy
* scipy
* matplotlib
* wx
* netCDF4

### Installing

* Clone the git repo: https://github.com/Jens00001/DynamicVision.git

### Executing program

* Download the app (see "Installing")
* Navigate to the directory DynamicVision and open the GUI folder
* Execute (double click) GUI.py
* Alternative: open a CMD promt and enter the following command:
```
python "PATH_TO_YOUR_DIRECTORY\Dynamic Vision\DynamicVision\GUI\GUI.py"
```

## Help

There are two possibilities to open the documentation. First you can start the app and click "Documentation".
The second thing you can do is to navigate into the directory of the app and open a Command Line Window (CMD). Then enter the following command:

```
start Documentation\build\html\index.html
```

## Authors

* Daniel Philippi (https://github.com/Sagittarii-A)
* Jens Rößler (https://github.com/Jens00001/)
* Nicolas Scherer (https://github.com/xiCentauri)

