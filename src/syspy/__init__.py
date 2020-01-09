from syspy.kernel.elaborator import Elaborator
from syspy.kernel.runtime import Runtime
from cocotb.info import Info
import cocotb
from cocotb.triggers import Timer

@cocotb.coroutine
def _run_coro(rt, top):
    
#    while True:
    print("--> start")    
    top.start()
    print("<-- start")

#        ret = rt.run()
        
#        if not ret:
#            print("nothing scheduled")
#            break
        
    yield Timer(0)
    
def sp_run(T, max_time):
    
    info = Info()
    rt = Runtime()    
    
    ctxt = cocotb.initialize_context(info, rt)
    top = Elaborator.elab(T)

    print("--> add_test")
#    ctxt.run(_run_coro(rt, top))
    ctxt.scheduler.add_test(_run_coro(rt, top))
    print("<-- add_test")
    
    while rt.run():
        pass
    
#    rt.run()
    
    Runtime.m_inst = None
    
