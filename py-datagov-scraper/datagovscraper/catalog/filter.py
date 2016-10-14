import yaml

class LocalFilter(object):
    '''load a yaml file containing query endpoints'''
    def __init__(self, path='filters.yaml'):
        self.path = path
        self._cached = {}

    def load(self):
        stream = file(self.path, 'r')
        self._cached = yaml.load(stream)

    def _lsIO(self):
        # why the fuck does this throw an exception
        # for filtername in self._cached.iterkeys():
        return self._cached
