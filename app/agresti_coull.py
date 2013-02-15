import math

def agresti_coull(n, k, upper_bound=False):
    conf = 0.05
    kappa = 2.24140273 # In general, kappa = ierfc(conf/2)*sqrt(2)
    kest=k+kappa**2/2
    nest=n+kappa**2
    pest=kest/nest
    radius=kappa*math.sqrt(pest*(1-pest)/nest)
    if upper_bound == True:
        return min(1, pest+radius)
    # Upper bound is min(1,pest+radius)
    return max(0,pest-radius) # Lower bound


