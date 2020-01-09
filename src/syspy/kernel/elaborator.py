'''
Created on Jan 4, 2020

@author: ballance
'''

class Elaborator():
    
    m_inst = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_elaborator():
        return Elaborator.m_inst
    
    @staticmethod
    def elab(T):
        m_inst = Elaborator()
        top = T()
        m_inst = None
        
        top.elab(str(type(T)))
        
        return top
        
        