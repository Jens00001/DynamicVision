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
python "PATH_TO_YOUR_DIRECTORY\Dynamic Vision\DynamicVision\GUI\GUI.py"
```

### How to use the program
An example is used to show how to use the app. A double mass oscillator is set up as an example.
* After executing the GUI.py file, the main menu will open.
![MainMenu](/Pictures/MainMenu.png)
* Click **_Create Model_** and then **_Create Element_**.
![CreateElement](/Pictures/CreateElement.png)
* Here you can add **_Masses_** and **_Springs_** to the system. It makes no difference whether you add the springs or the masses first.
* Let's select **_Mass_** first. Click on **_Masspoint_** in the next window.
* There you can enter the mass of the **_Masspoint_**. Let's enter $$\inline 2\,\text{kg}$$.
![Mass2Parameters](/Pictures/Mass2Parameters.png)
* Press **_submit_** and close the **_Create Element_** window.
* Now click on **_Create Element_** ⟶ **_Masses_** ⟶ **_Steady Body_**.
* The steady body needs 4 parameters: **_density_**, **_length_**, **_height_** and **_width_**.
* For example you can enter $$\inline 2710 \, \frac{\text{kg}}{\text{m}^3}$$ for the **_density_**. The **_length_** is $$\inline 0.2\,\text{m}$$, the height can be $$\inline 0.15\,\text{m}$$ and the **_width_** is $$\inline 0.1\,\text{m}$$.
![Mass1Parameters](/Pictures/Mass1Parameters.png)
* Press **_submit_** and close the **_Create Element_** window.
* Now click on **_Create Element_** ⟶ **_Spring_** ⟶ **_Single Spring_**.
* There you have to enter the **_stiffness_** and the **_length_** of the spring. For example we can enter $$\inline 350\, \frac{\text{N}}{\text{m}}$$ and $$\inline 0.1\,\text{m}$$.
![Spring1Parameters](/Pictures/SpringParameters.png)
* Press **_submit_**. Next you can enter the **_stiffness_** and the **_length_** for the second spring. For example $$\inline 550\, \frac{\text{N}}{\text{m}}$$ and $$\inline 0.15\,\text{m}$$.
![Spring2Parameters](/Pictures/Spring2Parameters.png)
* Press **_submit_** and close the **_Create Element_** window.
* Now we created the mechanical system more precisely a **double mass oscillator**.
* Next we have to enter the initial condition. So basically the initial positions and the initial velocities.
* Click on **_I Conditions_**. The **_Initial Conditions_** window will pop up. Regarding the order of the entered masses you have to enter the initial position and initial velocity.
* For the first mass we can use $$\inline -0.2\,\text{m}$$ and $$\inline 0\, \frac{\text{m}}{\text{s}}$$. The second mass can have a inital position of $$\inline -0.6\,\text{m}$$ and a initial velocity of $$\inline 0\, \frac{\text{m}}{\text{s}}$$.
![InitalConditions](/Pictures/IC.png)
* Press **_submit_** and close the **_Initial Condition_** window.
* Now press **_Run Simulation_**. The system will be simulated. Afterwards the results are plotted and an animation of the system will occur. Additionally a new window will pop up that displays the equation of motions. In a third window you can enter a name to save the system and the simulated data.
![Animation](/Pictures/Animation.gif)
![Equations](/Pictures/EquationsOfMotion.png)
* To save the simulation and the system enter the desired name and press **_save_**.
![Save](/Pictures/SaveResults.png)
* Close the **_Save_** window.
* To create a new system, you must restart the program in the current release.

### Additional Information
In addition to single springs, it is also possible to build both parallel and serial springs.


#### Parallel Springs
Mechanically, parallel springs can be represented by a single spring. So if you want to set up parallel springs, the program will automatically compute the resulting single spring.
The resulting spring constant $$ k_{res} $$ is computed by:

$$ k_{res}=\sum_{i=1}^{n}k_{i}. $$

And $$ n $$ represents the number of parallel springs. 
As the parallel springs are the same length, the length of the replacement spring is the same as that of the parallel springs.


#### Serial Springs
Mechanically, serial springs can also be represented by a single spring. So if you want to set up single springs, the program will automatically compute the resulting single spring.
The resulting inverse spring constant $$ k_{inv} $$ is computed by:

$$ {k_{inv}}=\sum_{i=1}^{n}\frac {1}{k_{i}}, $$

with $$ n $$ as the number of serial springs. That means the spring constant $$ k_{res} $$ of the resulting single spring is given by:

$$ k_{res}=\frac {1}{k_{inv}}. $$

In the case of the serial spring, the total length of the replacement spring also changes. Therefore the length of the resulting single spring $$ l_{res} $$ can be computed as:

$$ l_{res}=\sum_{i=1}^{n}l_{i}, $$

with $$ n $$ as the number of serial springs.


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

