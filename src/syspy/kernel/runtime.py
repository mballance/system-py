'''
Created on Jan 4, 2020

@author: ballance
'''
from cocotb import simulator_base
from cocotb.simulator_base import SimulatorBase
import traceback

class Runtime(SimulatorBase):
    """SystemPy runtime implementation for cocotb"""
    
    m_inst = None
    
    def __init__(self):
        self.timewheel = [] # list of time,callback tuples
        self.time_ps = 0
        pass

    @staticmethod    
    def get():
        if Runtime.m_inst is None:
            Runtime.m_inst = Runtime()
        return Runtime.m_inst

    def run(self):
        base_time = -1
        ret = len(self.timewheel) > 0
        
        if ret:
            base_time = self.timewheel[0][0]
            
        while len(self.timewheel) > 0:
            if self.timewheel[0][0] > base_time:
                # Reached the end of the current timestep
                break
            
            top = self.timewheel.pop()
            
            try:
                top[1](*top[2])
            except Exception as e:
                print("Exception: " + str(e))
                traceback.print_exc()

        return ret

    def register_timed_callback(self, sim_steps, callback, *args):
        
        if len(self.timewheel) == 0:
            self.timewheel.append([sim_steps, callback, args])
        else:
            for i in range(len(self.timewheel)):
                if (sim_steps > self.timewheel[i][0]):
                    sim_steps -= self.timewheel[i][0]
                    
                    if (i+1) >= len(self.timewheel):
                        self.timewheel.append([sim_steps, callback, args])
                else:
                    offset = self.timewheel[i][0]
                    offset -= sim_steps
                    self.timewheel[i][0] = offset
                    self.timewheel.insert(i, [sim_steps, callback, args])
