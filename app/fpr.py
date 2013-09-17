import cPickle as pickle

jar = open('app/fpr_minmax.pickle', 'rb')
(fantasy_min, fantasy_max) = pickle.load(jar)
jar.close()
