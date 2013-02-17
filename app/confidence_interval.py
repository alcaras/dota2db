import numpy
import pdb
from math import sqrt

# return a 95% confidence interval [a to b]
# given a distribution


def confidence_interval(distribution):
    # dirty hack to get around no scipy
    ppf = {}
    ppf[1] = 12.7062
    ppf[2] = 4.3026
    ppf[3] = 3.1824
    ppf[4] = 2.7764
    ppf[5] = 2.5705
    ppf[6] = 2.4469
    ppf[7] = 2.3646
    ppf[8] = 2.3060
    ppf[9] = 2.2621
    ppf[10] = 2.2281
    ppf[11] = 2.2009
    ppf[12] = 2.1788
    ppf[13] = 2.1603
    ppf[14] = 2.1447
    ppf[15] = 2.1314
    ppf[16] = 2.1199
    ppf[17] = 2.1098
    ppf[18] = 2.1009
    ppf[19] = 2.0930
    ppf[20] = 2.0859
    ppf[21] = 2.0796
    ppf[22] = 2.0738
    ppf[23] = 2.0686
    ppf[24] = 2.0638
    ppf[25] = 2.0595
    ppf[26] = 2.0555
    ppf[27] = 2.0518
    ppf[28] = 2.0484
    ppf[29] = 2.0452
    ppf[30] = 2.0422
    # end of dirty hack

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
        if df not in ppf:
            z = 1.96
        else:
            z = abs(ppf[df])
        
    else:
        return None # can't say anything with a sample size of 0 or 1

    lb_ci = avg - z * std / (sqrt(n))
    up_ci = avg + z * std / (sqrt(n))        

    return (lb_ci, up_ci)

