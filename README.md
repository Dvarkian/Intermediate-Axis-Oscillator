Metricify (v1.0.1)
==================

Metricify is a command line Python script designed to scan through a PDF file and replace all imperial units with metric ones. 

![UI Screenshot](https://github.com/Mblizzard/metricify/blob/main/Screenshot.png)

The below tutorial explains how to set up and use this software to convert a PDF of the Dungeons and Dragons Players Handbook (`phb.pdf`) to the metric system.

Note that this tutorial is designed for and tested on Ubuntu Linux. I have included a windows tutorial (scroll down), but please be aware that this is untested, and will almost certainly require basic python programming ability in order to resoulve any compatibility errors.


How to convert a PDF to the Metric System: Linux tutorial.
----------------------------------------------------------

**Step 1 - Update repositories:** 

Update apt package repositories using `sudo apt update` to ensure that the apt package manager has access to the latest versions of the below dependencies.

**Step 2 - Install APT dependencies:** 

First, install Python 3 by running `sudo apt install python3.10` in a terminal. Metricify is tested on python 3.10, but any 3.x version should (probably) also work just fine.

Next, install the optical content recognition algorithm using `sudo apt install ocrmypdf`, then install ghostscript using `sudo apt install ghostscript*`.

**Step 3 - Download Metricify**: 

Download Metricify by cloning the GitHub repository into your home folder using `git clone https://github.com/Mblizzard/metricify`.

**Step 4 - Install Python dependencies:** 

Open a terminal inside the `metricify` application folder, or navigate using `cd ~/metricify/`. Now run `sudo pip3 install -r requirements.txt`. Note that some systems may use `pip` in place of `pip3`.

**Step 5 - Running Metricify:** 

Go ahead and run `python3.10 ~/metricify/metricify.py`. A window will appear prompting you to select a input file (eg. `phb.pdf`), then Metricify will commence converting the units in your pdf to metric ones. This process will take several hours, I suggest that you leave it running overnight.

As Metricify applies edits to you PDF file, it will produce an output file named <page><input>-metric.pdf, where <page> is the number of pages that the software has processed. You can view this file when the at any point during the process to check that everything is working correctly. You may find that you need to go into the code edit the font of font size depending on the resolution and fonts of your input pdf. Note that the font size for edits must be smaller than that of the original pdf, as the word 'metres' is longer than the word 'feet'.
 
Any .ttf font can be used by Metricify. The default font is `BOD_CB.TTF`, size 33. This is easily editable within the `metricify.py` code file.

**Step 6 - Compressing the PDF:**
 
There's every chance that this process has created a very large pdf file. This may be a struggle for your PDF viewer to open, and takes up quite a bit of space on the disk. To make it smaller, run `ghostscript -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf`, where where input.pdf is the file produced by Metricify (eg. `355phb-metric.pdf`), and output.pdf is a filename of your choice, such as `355phb-metric-ghost.pdf`.
 
If this still is not small enough for you, have a read of [this thread](https://gist.github.com/FutureDrivenDev/6390547) to find some commands that will redece the size of the pdf further, but may cause a substantial loss of quality.
 
**Step 7 - Making the pdf searchable:**
 
At this stage our PDF is just a series of images. To make the text searchable again, run `ocrmypdf input.pdf output.pdf`, where input.pdf is the file produced by Ghostscript (eg. `355phb-metric-ghost.pdf`), and output.pdf is a filename of your choice, such as `355phb-metric-ghost-ocr.pdf`.

**Step 8 - Adding Bookmarks for each chapter:**

First, create a .bmk bookmarks file using `pdf-bookmark -p input.pdf`, where `input.pdf` is the original pdf file with imperial units (eg. `phb.pdf`).
 
Now, insert these bookmarks into our new pdf using `pdf-bookmark -p input.pdf -b bookmark.bmk -o output.pdf`, where input.pdf is the metric OCR'ed PDF file produced by the optical content recocognition algorithm (eg. `355phb-metric-ghost-ocr.pdf`), bookmark.bmk is the `.bmk` bookmarks file we have just created, and output.pdf will be the new file with bookmarks (eg. `355phb-metric-ghost-ocr-bmk.pdf`). You can now delete the `.bmk` bookmarks file if you want to.

And that's it! Tada! Enjoy your lovely no-longer-imperial PDF file.
 
 
How to convert a PDF to the Metric System: Windows tutorial.
------------------------------------------------------------

*Please be aware that this winown tutorial is **entirely untested**. There will almost certainly be a few compatibility errors. You will need at least a basic level of python programming experience to make this work.*

**Step 1 - Install Linux**: 

Just kidding. Mostly. You should probably just go ahead and move on to step 2.
 
**Step 2 - Install Python**: 

Download and install the latest version of python from [python.org](https://www.python.org/). Make sure you click the options to install all the extras as well, especially IDLE and pip.

**Step 3 - Download Metricify**:  
 
Download Metricify by using the GitHub feature that allows you to dowload the repository as a .zip file. Extract the .zip file somewhere you can find it. Now use the file manager to navigate inside the folder named 'metricify'.
 
**Step 4 - Install Python dependencies:**

Open command prompt and navigate inside the `metricify` application folder. Now run `python -m pip install -r requirements.txt`. You might need to add a `--user` flag if you don't have admin premissions.

**Step 5 - Running Metricify:**

Open `metricify.py` in IDLE and press F5 to execute the program. A window will appear prompting you to select a input file (eg. `phb.pdf`), then Metricify will commence converting the units in your pdf to metric ones. This process will take several hours, I suggest that you leave it running overnight.

As Metricify applies edits to you PDF file, it will produce an output file named <page><input>-metric.pdf, where <page> is the number of pages that the software has processed. You can view this file when the at any point during the process to check that everything is working correctly. You may find that you need to go into the code edit the font of font size depending on the resolution and fonts of your input pdf. Note that the font size for edits must be smaller than that of the original pdf, as the word 'metres' is longer than the word 'feet'.
 
Any .ttf font can be used by Metricify. The default font is `BOD_CB.TTF`, size 33. This is easily editable within the `metricify.py` code file.

**Step 5 - Bookmarks, searchable text, and compressing the file**:
 
Apparently you can do all this stuff in Adobe Acrobat? If you're no sure how, Google it. Or install Linux and follow the previous tutorial. That's probably easier ;).
 

Planned Features
----------------

New capabilities to look forward to in future versions of Metricify:

 - Input files specified via the command line.

Features I'm not currently planning to include in Metricify, but that I'll consider adding if enough people are interested:

 - Complete tested Windows support.
 - OCR, bookmark, and compression functions conducted directly by the `metricify.py` script.
 
**Versioning:** Releases will follow a [semantic versioning format](http://semver.org/): `<major>.<minor>.<patch>`


License
-------

    Metricify: A software to convert Imperial units in a PDF file to Metric values.
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
