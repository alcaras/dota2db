import numpy
import scipy
import pdb
from math import sqrt
from scipy import stats
from scipy.stats import t

# return a 95% confidence interval [a to b]
# given a distribution
def confidence_interval(distribution):

    avg = numpy.average(distribution)
    std = numpy.std(distribution)
    n = len(distribution)
    



    if n >= 30:
        # if we have 30 or more samples, we assume a normal distribution
        # assuming a normal distribution
        z = 1.96    # 95% confidence interval
    elif n >= 2:
        # here we use a student's t distribution
        x = 0.025 # 95% confidence interval
        df = n-1

        z = abs(t.ppf(x, df))
        
    else:
        return None # can't say anything with a sample size of 0 or 1

    lb_ci = avg - z * std / (sqrt(n))
    up_ci = avg + z * std / (sqrt(n))        

    return (lb_ci, up_ci)

