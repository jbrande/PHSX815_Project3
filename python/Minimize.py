import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy import optimize

sys.path.append(".")
from python.Random import Random

from scipy.special import comb
import time

# uses scipy.optimize.minimize_scalar to maximize the likelihood function of our coin flips
# uses bounded brent's method since p can only be between 0 and 1

file = None

if "-file" in sys.argv:
	p = sys.argv.index("-file")
	file = sys.argv[p+1]
	if file == None:
		print("You must pass a valid filename.")
		sys.exit(1)
else:
	print("You must pass a valid filename.")
	sys.exit(1)

# read in the data
data = np.loadtxt(file)

# use the data to make some parameters
xi = np.sum(data)
n = np.size(data)

# function to be minimized: -(xi*log(p) + (n-xi)log(1-p)) which will maximimize the likelihood function of our bernoulli coin flips
def minfunc(p):
	return -1.0*(xi*np.log(p) + (n - xi)*np.log(1.0-p))


# minimize the function, in the range 0 to 1
res = optimize.minimize_scalar(minfunc, method="bounded", bounds=[0,1])
pmeas = res["x"]
print("The minimum of minfunc is: {}".format(pmeas))

# use the neyman construction approach to approximate the confidence intervals on the minimized coin probability

random = Random()

histx = []
histy = []

Nmeas = n
Nexp = 1

# time this to see how it changes with data size
start = time.time()
for i in np.linspace(0, 1, Nmeas):
	ptrue = i
	for e in range(Nexp):
		pbest = np.sum(np.random.binomial(Nmeas, ptrue, Nexp))
		pbest = pbest / Nmeas
		histx.append(ptrue)
		histy.append(pbest)

end = time.time()

print("Neyman Construction took: ", end-start, "seconds.")

# make neyman plots
fig, ax = plt.subplots(1, 2, figsize=(20, 8.5))
ax[0].set_aspect("equal")
H = ax[0].hist2d(histx, histy, bins=int(Nmeas/10.0), density=False)
plt.colorbar(H[3], ax=ax[0], fraction=0.046, pad=0.04)
ax[0].set_xlabel(r"$\mu$ true")
ax[0].set_ylabel(r"$\mu$ measured")
ax[0].set_title("Neyman Plot")

# get bin edges from histogram
xedges = H[1]
yedges = H[2]

# "experimental" mu
test_mu = pmeas #np.random.rand()
ax[0].axhline(test_mu, c="white", ls="--", label=r"Test $\mu$: {:.4f}".format(test_mu))
ax[0].legend(loc="upper left")

#get bin index of measurement 
ind = np.digitize(test_mu, yedges) - 1
if (ind == len(H[0])):
	ind = ind-1

# get 2d weights from measurement
exp = H[0][:,ind]

# histogram of measurement
H2 = ax[1].hist(yedges[:-1], yedges, weights=exp, color="darkgray")
n = H2[0]
bins = H2[1]

#print(n, bins)

# get experiment values
mids = 0.5*(bins[1:] + bins[:-1])
mean = np.average(mids, weights=n)
std = np.sqrt(np.average((mids-mean)**2, weights=n))

print("Mean: {}, Std. Dev.: {}, 1-sigma CI: [{}, {}]".format(mean, std, mean-std, mean+std))

ax[1].axvline(mean, c="C0", ls="--", label=r"binned $\mu$")
ax[1].axvline(test_mu, c="k", ls="--", label=r"$p_{meas}$")
ax[1].axvline(mean+std, c="tomato", ls="--", label=r"$+\sigma$")
ax[1].axvline(mean-std, c="tomato", ls="--", label=r"$-\sigma$")

# this is a really thin PMF, so scale it to be +/- 3 sigma, to neatly show our +/- 1 sigma intervals
lim = [0, 1]

if (mean-3*std) < 0:
	lim[0] = 0
else:
	lim[0] = mean-3*std

if (mean+3*std) > 1:
	lim[1] = 1
else:
	lim[1] = mean+3*std


ax[1].set_xlim(lim)
ax[1].set_xlabel(r"$\mu$")
ax[1].set_ylabel("Frequency")
ax[1].legend()
ax[1].set_title(r"PDF for Measurement: $\mu=${:.4f}, $\sigma=${:.4f}".format(mean, std))
#plt.show() # this dies at really high data sizes lmao
fig.savefig("plots{}.jpg".format(np.size(data)), dpi=300)