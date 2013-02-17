import numpy
import pdb
from math import sqrt

# return a 95% confidence interval [a to b]
# given a distribution

# dirty hack to get around no scipy
ppf = {}
ppf[1] =  12.7062047364
ppf[2] =  4.30265272991
ppf[3] =  3.18244630528
ppf[4] =  2.7764451052
ppf[5] =  2.57058183661
ppf[6] =  2.44691184879
ppf[7] =  2.36462425101
ppf[8] =  2.30600413503
ppf[9] =  2.26215716274
ppf[10] =  2.22813885196
ppf[11] =  2.20098516008
ppf[12] =  2.17881282966
ppf[13] =  2.16036865646
ppf[14] =  2.14478668792
ppf[15] =  2.13144954556
ppf[16] =  2.11990529922
ppf[17] =  2.10981557783
ppf[18] =  2.10092204024
ppf[19] =  2.09302405441
ppf[20] =  2.08596344727
ppf[21] =  2.07961384473
ppf[22] =  2.0738730679
ppf[23] =  2.06865761042
ppf[24] =  2.06389856163
ppf[25] =  2.05953855275
ppf[26] =  2.05552943864
ppf[27] =  2.05183051648
ppf[28] =  2.0484071418
ppf[29] =  2.04522964213
ppf[30] =  2.0422724563

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
        z = abs(ppf[df])
        
    else:
        return None # can't say anything with a sample size of 0 or 1

    lb_ci = avg - z * std / (sqrt(n))
    up_ci = avg + z * std / (sqrt(n))        

    return (lb_ci, up_ci)

