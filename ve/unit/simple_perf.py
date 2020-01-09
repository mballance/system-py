'''
Created on Jan 4, 2020

@author: ballance
'''
from unittest.case import TestCase
import cocotb
from syspy.module import Module
from syspy.port import Port
from syspy.kernel.elaborator import Elaborator
from syspy import sp_run
from cocotb.triggers import Timer

class SimplePerf(TestCase):
    
    def test_simple_perf(self):

        class write_if(): # TODO: Interface
            
            def __init__(self):
                pass
            
            @cocotb.coroutine
            def write(self, ch):
                pass
            
            def reset(self):
                pass
        
        class read_if(): # TODO: Interface
            
            def __init__(self):
                pass

            @cocotb.coroutine            
            def read(self):
                pass
            
            def num_available(self):
                pass
            

        class fifo(Module): # TODO: Channel
            
            def __init__(self, parent, size):
                super().__init__(parent)
                
                self.data = [0] * size
                self.num_elements = 0
                self.first = 0
                self.size = size
                self.num_read = 0
                self.max_used = 0
                self.average = 0
                self.last_time = 0
                self.write_event = cocotb.triggers.Event()
                self.read_event = cocotb.triggers.Event()

            @cocotb.coroutine
            def write(self, ch):
                while self.num_elements == self.size:
                    yield self.read_event.wait()
                    self.read_event.clear()
                    
                self.data[(self.first + self.num_elements) % self.size] = ch
                self.num_elements += 1
                
                self.write_event.set()

            @cocotb.coroutine
            def read(self): 
                self.last_time = 0 # TODO: fetch time
#                print("--> read: num_elems=" + str(self.num_elements))
                while self.num_elements == 0:
                    yield self.write_event.wait()
                    self.write_event.clear()
                    
                # TODO: compute_stats
                
                c = self.data[self.first]
                self.num_elements -= 1
                self.first = (self.first + 1) % self.size
                self.read_event.set()
                
#                print("<-- read: num_elems=" + str(self.num_elements))
                return c
                
            def reset(self):
                self.num_elements = 0
                self.first = 0
                
            def num_available(self):
                return self.num_elements
            
        class producer(Module):
            
            def __init__(self, parent):
                super().__init__(parent)
                self.out_p = Port(write_if)
                self.sp_thread(producer.main)

            @cocotb.coroutine                
            def main(self):
                print("--> producer.main")
#                total = 1000000
                total = 10000
#                total = 1000
                
                while total > 0:
                    
                    # TODO: randomly select i
                    i = 20
                    while i > 0:
#                        print("--> write " + str(total))
                        yield self.out_p().write(0)
#                        print("<-- write")
                        i -= 1
                        total -= 1
                        
                    if total > 0:
                        yield Timer(1000)
                    
#                    total -= 1
                    
                # TODO: yield for time
                print("<-- producer.main")

        class consumer(Module):
            
            def __init__(self, parent):
                super().__init__(parent)
                self.in_p = Port(read_if)
                self.sp_thread(consumer.main)
                
            @cocotb.coroutine
            def main(self):
                print("consumer.main")
                while True:
                    
                    for i in range(100):
                        c = yield self.in_p().read()
                    
                    # TODO: wait 100 NS
                    yield Timer(100)


        class top(Module):
            
            def __init__(self, parent, size):
                super().__init__(parent)
                self.fifo_inst = fifo(self, size)
                self.prod_inst = producer(self)
                self.cons_inst = consumer(self)

                self.prod_inst.out_p.bind(self.fifo_inst)
                self.cons_inst.in_p.bind(self.fifo_inst)
        
#        top_i = Elaborator.elab(lambda:top(None,1000))
        sp_run(lambda:top(None,10), 0)

        
        