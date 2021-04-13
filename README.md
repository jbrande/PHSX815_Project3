# PHSX815_P3

This program runs code for the PHSX815 Project 3. We simulate a certain number of coin flips with either a given probability, or a random probability of landing on heads. We then read this data and minimize a function which gives us the maximum likelihood value for the probability, and determine a +/- 1 sigma confidence interval on that value according to the Neyman construction. The programs can be run as follows:

python python/Simulate.py [-seed number] [-Nexp number] [-ptrue float] [-outfile filename]

-seed			The seed for the random number generator. 

-Nexp 			The number of flips to make: default 1000

-ptrue 			The true probability of landing on heads. Default: a random number between 0 and 1. If given a value not in [0, 1], the program quits.

-outfile 		The file to which the output is printed. If not given, the results are printed to the console.


Simulate.py will then create a file with the given filename and print the coin flip data to it. If no filename is given, the data will be printed to the console.


python python/Minimize.py [-file filename]

-file 			The name of the data file to read and use for minimization. If not given, the program will quit.

Minimize.py will then perform the minimization and Neyman construction analysis, and print some relevant information (the minimized p, the time taken to make the 2-dimensional histogram, and the measured mu, std. dev., and confidence interval bounds). The program will also save the plots as plotsXXXX.jpg, where the Xs indicate the size of the data. 

Of non-standard Python libraries, this project requires numpy, scipy, and matplotlib.