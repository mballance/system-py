'''
Created on Jan 3, 2020

@author: ballance
'''
from syspy.object import Object
import cocotb

class Module(Object):
    
    def __init__(self, parent=None):
        super().__init__()

        self.name = "<unknown>"        
        self.children = []
        self.thread_proc_l = []
        
        if parent is not None:
            parent.add_child(self)
        else:
            # This is a top-level module
            self.elab(str(type(self)))
            
    def add_child(self, c):
        self.children.append(c)
        
    def sp_thread(self, f):
        self.thread_proc_l.append(f)
        
    def elab(self, parent_path):
        for f in dir(self):
            fo = getattr(self, f)
            
            if isinstance(fo, Module):
                fo.name = f
                fo.elab(parent_path + "." + f)
                
    def start(self):
        if len(self.children) > 0:
            for c in self.children:
                c.start()
                
        for p in self.thread_proc_l:
            cocotb.get_context().scheduler.add(p(self))
            