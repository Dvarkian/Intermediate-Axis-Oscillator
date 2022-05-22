Intermidate Axis Oscillator (v1.3.1)
====================================

This software is designed to simulate and graph the motion of a rotating object in free fall, as governed by [Euler's rotation equations](https://github.com/Mblizzard/Intermediate-Axis-Oscillator/blob/main/Numerical%20solution%20of%20Euler%E2%80%99s%20rotation%20equations.pdf).

![Simulator Screenshot](https://github.com/Mblizzard/Intermediate-Axis-Oscillator/blob/main/screenshots/Simulation.png)

Additionally, this simulator can be used to compare experimental angular velocity data collected using [Phyphox](https://phyphox.org/) to the numerically determined theorectical predictions of Euler's rotation equations. The simulator will then make calculations to determine the peried of off axis oscillation caused by the [tennis racquet effect](https://en.wikipedia.org/wiki/Tennis_racket_theorem).

![Data Analysis Screenshot]([https://github.com/Mblizzard/Intermediate-Axis-Oscillator/blob/main/screenshots/Simulation.png](https://github.com/Mblizzard/Intermediate-Axis-Oscillator/blob/main/screenshots/Dataset%201.png))


Installing and using this simulator.
----------------------------------------------------------

**Step 1 - Install Python:** 

Install python 3.10 using `sudo apt install python3` (Linux), or by downloading and running the installer from [python.org](www.python.org) (Windows). This software should work fine on other versions of Python 3.x, although this is untested.

**Step 2 - Download the simulator**: 

Download the simulator by cloning the GitHub repository into your home folder using `git clone https://github.com/Mblizzard/Intermediate-Axis-Oscillator`. This can be done either with the command line, or using GitHub Desktop.

**Step 3 - Running The simulator:** 

Go ahead and run `python3.10 ~/Intermediate-Axis-Oscillator/simulator.py` (Linux), or oopen `simulator.py` using Python 3 (Windows).

The program will start, and you will be able to enter siimulation parameters at the to op the window, as shown in the screenshot.

**Step 4 - Analysing Data:**
 
The software will automatically attept to conduct data analysis on any `.csv` file found in the `/data` directory. By default, this directory contains the data we acquired in our experiment. You may wish to delete this before using the simulator to analyse your own data.
 

Planned Features
----------------

No further development is currently planned for this project. Users are encoraged to edit `simulator.py` to implement any features that they wish to add, and create a pull request if you believe that your functionality would be of use to others who wish to utilise this software.


License
-------

    Intermidate Axis Oscillator: Numerically soulving Euler's rotation equations to analyse the intermediate axis effect.
    Copyright (C) 2022  Murray Jones

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
