'''
Created on Jan 3, 2020

@author: ballance
'''
from syspy.object import Object

class Port(Object):
    
    def __init__(self, T, max_size=1):
        self._imp = None
        
    def bind(self, imp):
        self._imp = imp
    
    def __call__(self):
        return self._imp

    