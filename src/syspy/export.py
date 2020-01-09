'''
Created on Jan 3, 2020

@author: ballance
'''
from syspy.object import Object

class Export(Object):
    
    def __init__(self, T):
        super().__init__()
        self._t = T
        self._imp = None
        
    def __call__(self):
        if self._imp is None:
            # TODO: report an unbound error
            pass
        
        return self._imp
    
    def bind(self, imp):
        if type(imp) != self._t:
            print("Error: type mismatch")
        self._imp = imp