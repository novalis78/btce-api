import warnings

class KeyData(object):
    def __init__(self, secret, nonce):
        self.secret = secret
        self.nonce = nonce

class KeyHandler(object):
    '''KeyHandler handles the tedious task of managing nonces associated
    with a BTC-e API key/secret pair.
    The getNextNonce method is threadsafe, all others are not.'''
    def __init__(self, filename = None, resaveOnDeletion = False):
        '''The given file is assumed to be a text file with three lines
        (key, secret, nonce) per entry.'''
        if not resaveOnDeletion:
            warnings.warn("The resavenDeletion argument to KeyHandler will default to True in future versions.")
        self._keys = {}
        self.resaveOnDeletion = False
        self.filename = filename
        if filename is not None:
            self.resaveOnDeletion = resaveOnDeletion
            f = open(filename, "rt")
            while True:
                key = f.readline().strip()
                if not key:
                    break
                secret = f.readline().strip()
                nonce = int(f.readline().strip())
                self.addKey(key, secret, nonce)
                
    def __del__(self):
        if self.resaveOnDeletion:
            self.save(self.filename)
            
    @property
    def keys(self):
        warnings.warn("The keys property will return a list of keys instead of a dict in the future.")
        return dict(((k, (d.secret, d.nonce)) for k, d in self._keys.items()))
        
    def getKeys(self):
        return self._keys.keys()
        
    def save(self, filename):
        f = open(filename, "wt")
        for k, data in self._keys.items():
            f.write("%s\n%s\n%d\n" % (k, data.secret, data.nonce))
        
    def addKey(self, key, secret, next_nonce):
        self._keys[key] = KeyData(secret, next_nonce)

    def getNextNonce(self, key):
        data = self._keys.get(key)
        if data is None:
            raise Exception("Key not found: %r" % key)
        
        nonce = data.nonce
        data.nonce += 1
       
        return nonce

    def getSecret(self, key):
        data = self._keys.get(key)
        if data is None:
            raise Exception("Key not found: %r" % key)
        
        return data.secret
        
    def setNextNonce(self, key, next_nonce):
        warnings.warn("This method may be removed in a future version.")
        data = self._keys.get(key)
        if data is None:
            raise Exception("Key not found: %r" % key)
        data.nonce = next_nonce
