import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append(".")
from python.Random import Random

# Creating a bunch of simulated coin flip data
seed = 42069
Nexp = 1000
ptrue = None
outfile = None

# check command line args
if "-seed" in sys.argv:
	p = sys.argv.index("-seed")
	seed = int(sys.argv[p+1])
if "-Nexp" in sys.argv:
	p = sys.argv.index("-Nexp")
	Nexp = int(sys.argv[p+1])
if "-ptrue" in sys.argv:
	p = sys.argv.index("-ptrue")
	ptrue = float(sys.argv[p+1])
if "-outfile" in sys.argv:
	p = sys.argv.index("-outfile")
	outfile = sys.argv[p+1]

# instantiate random number generator
random = Random(seed=seed)

if (ptrue != None) and (ptrue < 0.0 or ptrue > 1.0):
	print("Ptrue must be a float between 0 and 1")
	sys.exit(1)

# if ptrue not given in arguments, make a random probability
if (ptrue == None):
	ptrue = random.rand()
	print(ptrue) # for debugging

# instantiate the random class, make a bunch of random coin flips
rands = [random.Bernoulli(ptrue) for i in range(Nexp)]

# print the data either to a file, or to the console if no file was given.
if outfile:
	with open(outfile, "w+") as f:
		f.write(" ".join(map(str, rands)))
		f.close()
else:
	print(rands)
	plt.hist(rands)
	plt.show()