# Program for Calculation and Display Info on Workouts from Sensors Data #

### Description ###
Basic task of this project was formulated as a program realisation of calculation and display info from data received from sensors. This code handles prearranged workouts data from 'sensors' via 3 classes inherited from basic Workout class. All classes have inherited and original methods for calculations (kcal spent, average speed etc.). Also there are class with method for returning info message on workouts and function for validating and extracting data from data packages. 

### Features ###
- Type hints and docstrings
- @dataclasses with ClassVars for avoiding manual filling of ```__init__```
- Errors handling with ```raise``` syntax

### Classes and Methods ###
Basic ```class Workout``` has 3 inheritors: ```class Running```, ```class SportsWalking``` and ```class Swimming```. All child classes have own class attributes and variables. All of them use different formulas in ```get_spent_calories``` method, ```class Swimming``` also has it's own realisation of ```get_mean_speed``` method. For creation and returning info message on workouts there is ```class InfoMessage```
