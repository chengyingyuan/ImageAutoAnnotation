ImageAutoAnnotation

A tool to detect moving objects and save them for further trainning. 

This tool is derived from kerberos.io, a great project to make deteciton easier. 


opencv for python 3.5
===============================================
https://stackoverflow.com/questions/35466429/opencv-for-python-3-5-1

First you need to install Microsoft Visual C++ 2015 Redistributable, which you 
can download from 
https://www.microsoft.com/en-us/download/details.aspx?id=53587.
Then you can download the wheel file from 
http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv. 
Make sure you download the file which corresponds to your python version. 
For example: my python version is 3.5 so I downloaded 
opencv_python-3.2.0+contrib-cp35-cp35m-win_amd64.whl.
And install it with "pip install filename".

Profile
===============================================
# sort by time
python -m cProfile -s time main.py

# cProfile only works in main thread. 
Instead of running one cProfile, you could run separate cProfile instance in 
each thread, then combine the stats. Stats.add() does this automatically.

