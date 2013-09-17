import cPickle as pickle
import os

basedir = os.path.abspath(os.path.dirname(__file__))
jar = open(os.path.join(basedir, 'fpr_minmax.pickle'), 'rb')
(fantasy_min, fantasy_max) = pickle.load(jar)
jar.close()
