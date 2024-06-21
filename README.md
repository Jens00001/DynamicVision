# DynamicVision: Dynamic Model Visualization Tool

The DynamicVision project aids engineers in understanding complex mechanical systems by allowing them to create, model, and simulate systems with a GUI, providing equations of motion, visualizations, and synchronized plots.

## Description

Engineers develop complex systems that often need to be modeled and simulated before the actual system can be created. For this reason, system modeling is a crucial part of engineering. Initially, mechanical systems consist of simple couplings of basic elements like springs, masses, and dampers. Analyzing and simulating these systems is not trivial, especially at the beginning of the engineering studies. This is often due to a lack of system understanding and an unclear idea of how the final system behaves.

The DynamicVision project addresses this issue. Users can use a GUI to create simple mechanical systems from springs and masses, which are then modeled and simulated. Users are provided with the resulting equations of motion for the respective system and a visualization. Additionally, plots synchronized with the visualization are generated.


## Getting Started

### Dependencies

* Python Interpreter (Version >= 3.11)
* sympy
* numpy
* scipy
* matplotlib
* wx
* netCDF4
* Tested with Windows 11

### Installing

* Clone the git repo: https://github.com/Jens00001/DynamicVision.git

### Executing program

* Download the app (see "Installing")
* Navigate to the directory DynamicVision and open the GUI folder
* Execute (double click) GUI.py
* Alternative: open a CMD promt and enter the following command:
```
python "PATH_TO_YOUR_DIRECTORY\DynamicVision\GUI\GUI.py"
```

### How to use the program
An example is used to show how to use the app. A double mass oscillator is set up as an example.
* After executing the GUI.py file, the main menu will open.
![MainMenu](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/MainMenu.png)
* Click **_Create Model_** and then **_Create Element_**.
![CreateElement](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/CreateElement.png)
* Here you can add **_Masses_** and **_Springs_** to the system. It makes no difference whether you add the springs or the masses first.
* Let's select **_Mass_** first. Click on **_Masspoint_** in the next window.
* There you can enter the mass of the **_Masspoint_** and an external force acting on that mass. Let's enter $2 \ \text{kg}$ for the mass and $0 \ \text{N}$ for the external force.
![Mass2Parameters](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/Mass2Parameters.png)
* Press **_submit_**. The program returns to the **_Create Element_** window.
* Now click on **_Mass_** ⟶ **_Steady Body_**.
* The steady body needs 4 parameters: **_density_**, **_length_**, **_height_** and **_width_**. Additionally you can add an external force.
* For example you can enter $2710 \ \frac{\text{kg}}{\text{m}^3}$ for the **_density_**. The **_length_** is $0.2 \ \text{m}$, the height can be $0.15 \ \text{m}$ and the **_width_** is $0.1 \ \text{m}$. The external force can be set to $0 \ \text{N}$.
![Mass1Parameters](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/Mass1Parameters.png)
* Press **_submit_**. The program returns to the **_Create Element_** window.
* Now click on **_Spring_** ⟶ **_Single Spring_**.
* There you have to enter the **_stiffness_** and the **_length_** of the spring. We can also choose between a **_linear_** or a **_cubic_** spring. For example we can enter $250 \  \frac{\text{N}}{\text{m}}$ and $0.2 \ \text{m}$. Select a **_linear_** spring.
![Spring1Parameters](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/SpringParameters.png)
* Press **_submit_**. We will return to the **_Create Element_** window.
* Click on **_Spring_** ⟶ **_Single Spring_**.
* Next you can enter the **_stiffness_** and the **_length_** for the second spring. For example $400 \  \frac{\text{N}}{\text{m}}$ and $0.15 \ \text{m}$. We use a linear spring again.
![Spring2Parameters](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/Spring2Parameters.png)
* Press **_submit_** and **_Finish_** to close the **_Create Element_** window.
* Now we created the mechanical system more precisely a **double mass oscillator**.
* Next we have to enter the initial condition. So basically the initial positions and the initial velocities.
* Click on **_Set Initial Conditions_**. The **_Initial Conditions_** window will pop up. Regarding the order of the entered masses you have to enter the initial position and initial velocity.
* For the first mass we can use $-0.3 \ \text{m}$ and $0 \  \frac{\text{m}}{\text{s}}$. After pressing **_submit_** we can enter the initial conditions for the second mass. The second mass can have a inital position of $-0.6 \ \text{m}$ and a initial velocity of $0 \  \frac{\text{m}}{\text{s}}$.
![InitalConditions](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/IC.png)
* Press **_submit_**. The **_Initial Condition_** window will close automatically.
* Now press **_Run Simulation_**. The system will be simulated. Afterwards the results are plotted and an animation of the system will occur. Additionally a new window will pop up that displays the equation of motions. In a third window you can enter a name and a directory to save the system and the simulated data.
![Animation](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/Animation.gif)
![Equations](https://github.com/Jens00001/DynamicVision/blob/dev/Pictures/EquationsOfMotion.png)
* To create a new system, just click on create Element and the current system is resetted.

### Additional Information
In addition to single springs, it is also possible to build both parallel and serial springs.


#### Parallel Springs
Mechanically, parallel springs can be represented by a single spring. So if you want to set up parallel springs, the program will automatically compute the resulting single spring.
The resulting spring constant $k_{res}$ is computed by:

$$ k_{res}=\sum_{i=1}^{n}k_{i}. $$

And $n$ represents the number of parallel springs. 
As the parallel springs are the same length, the length of the replacement spring is the same as that of the parallel springs.


#### Serial Springs
Mechanically, serial springs can also be represented by a single spring. So if you want to set up single springs, the program will automatically compute the resulting single spring.
The resulting inverse spring constant $k_{inv}$ is computed by:

$$ {k_{inv}}=\sum_{i=1}^{n}\frac {1}{k_{i}}, $$

with $n$ as the number of serial springs. That means the spring constant $k_{res}$ of the resulting single spring is given by:

$$ k_{res}=\frac {1}{k_{inv}}. $$

In the case of the serial spring, the total length of the replacement spring also changes. Therefore the length of the resulting single spring $l_{res}$ is computed as:

$$ l_{res}=\sum_{i=1}^{n}l_{i}, $$

with $n$ as the number of serial springs.


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
