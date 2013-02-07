import cPickle as pickle

jar = open('hero_points.pickle', 'rb')
(hero_avg, hero_std) = pickle.load(jar)
jar.close()
