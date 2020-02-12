# Optimization of Heterogeneous Fleet Vehicle Routing Problem (HVRP) using Google Ortools Solver

**Objective of the model is to create routes such that:**

-	Number of vehicles used are minimized
-	Travel is minimized
-	Cost of not-serving order is minimized

**Subject to constraints such as:**
-	Different end times for vehicles
-	Max waiting for vehicles
-	Different start times for vehicles
-	Different service times for vehicles
-	Different travel times for vehicles
-	Different capacity restrictions for vehicles
-	Different max working hours for vehicles
-	Time windows for orders



## Prerequisites

To run this **Python** program, please install **ortools**, **csv**, **pandas**, **datetime**, and **logging** libraries/packages. 
More details in `src/requirements.txt`



## Structure Of The Project

All the code is in src folder. 
Input data (input excel file) used is in input folder.
Output (csv and log file) from Optimizer is in output folder.

To run the code, please run **routeOptimization.py** (to run from cmd, please enter python.exe routeOptimization.py).
