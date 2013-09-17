from fpr import fantasy_min, fantasy_max

def get_scale_factors():
    vectors = ["solo", "carry", "support"]

    offset =  {"solo" : 0.0,
             "carry" : 0.0,
             "support" : 0.0}

    scale = {"solo" : 1.0,
             "carry" : 1.0,
             "support" : 1.0}

    for v in vectors:
        vmin = fantasy_min[v]
        vmax = fantasy_max[v]
        
        offset[v] = 0.0-vmin # set to 100
        scale[v] = 100.0/(vmax-vmin)
        
    return (offset, scale)

# returns scaled scores as a dict with support, carry, solo
# when passed a player dictionary
def calculate_fantasy_scores(p, scaled=False):
    # dota2.com/international/fantasy/rules
    mods = {}
    mods["solo"] = {"kills" : 0.4,
                    "deaths" : -0.35,
                    "assists" : 0, # nothing for assists
                    "last_hits" : 0.002,
                    "gold_per_min" : 0.002,
                    "xp_per_min" : 0.003}
    mods["carry"] = {"kills" : 0.3,
                     "deaths" : -0.2,
                     "assists" : 0, # nothing for assists
                     "last_hits" : 0.004,
                     "gold_per_min" : 0.003,
                     "xp_per_min" : 0,
                     }
    mods["support"] = {"kills" : 0.2,
                       "deaths" : -0.05,
                       "assists" : 0.2,
                       "last_hits" : 0.001,
                       "gold_per_min" : 0.001,
                       "xp_per_min" : 0.004}

    (offset, scale) = get_scale_factors()


    scores = {}
    for k, v in mods.iteritems():
        scores[k] = 0.0
        for l, w in mods[k].iteritems():
            scores[k] += p[l] * w

        if scaled == True:
            scores[k] += offset[k]
            scores[k] *= scale[k]
            scores[k] = int(round(scores[k], 0))

    return scores

              
