from math import sqrt

def _confidence(n, wins):
    if n == 0:
        return 0

    z = 1.6 
    phat = float(wins) / n
    return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

def wilson(n, wins):
    if n == 0:
        return 0
    else:
        return _confidence(n, wins)


