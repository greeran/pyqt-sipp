import time
import sys
import shlex, subprocess
from multiprocessing import Process, Queue, Value
from sipp_log import Sipp_Element
import threading
import signal


class sipp_user:

    def __init__(self, cmd):
        self._execProc = None
        self._SessionCall = 0
        self._SessionSuccess = 0
        self._SessionFails = 0
        self._isStop = 0
        self._out_thread = None
        self._command = cmd

    def setValue(self, isStopValue):
        self._isStop = isStopValue

    def stop_sipp(self):
        self._isStop.value=1
        if self._out_thread is not None:
            self._out_thread.join()
        else:
            print("thread is none id(%d)\n" % id(self))
        
        print("Sipp is closed ")
        
    def __del__(self):
       if self._isStop is False:
           self.stop_sipp





#---------------------------- sipp process running -----------------#


def stdout_thread(q, execProc, isStopValue):
    out_buffer = []
    while isStopValue.value == 0:
        out = execProc.stdout.readline()
        stdout_result = execProc.poll()
        if (out == '' or out is None) and stdout_result is not None:
            print("in break .. result %d: \n" % stdout_result)
            q.put_nowait(Sipp_Element("Error !!"))
            break

        if out != '' and out is not None:
            out_buffer.append(out)
            if str(out).find("Sipp Server Mode") != -1:                    
                q.put_nowait(Sipp_Element(out_buffer))
                out_buffer.clear()
            if str(out).find("Scenario Screen") != -1:                    
                q.put_nowait(Sipp_Element(out_buffer))
                out_buffer.clear()

    execProc.kill()
    print("killed process and thread stop run\n")         

def run_sipp_proc( cmd, q, isStopValue):
    print("start thread")
    execProc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE,universal_newlines=True, shell=True)
    out_thread = threading.Thread(name='stdout_thread', 
        target=stdout_thread, args=(q, execProc, isStopValue))
    out_thread.start()
    out_thread.join()

#--------------------------- create sipp objects---------------------#
def createSippAnswer(cmd):
    q=Queue()
    sipp_Clnt = sipp_user(cmd)
    isStopValue=Value('i', 0)
    sipp_Clnt.setValue(isStopValue)
    sipp_proc = Process(target=run_sipp_proc, name="sipp_answer",
        args=(cmd, q, isStopValue))
    sipp_proc.start()
    return sipp_Clnt, q

if __name__ == '__main__':
    sipp_Clnt=sipp_user(answer_command)
    sipp_Clnt.run_sipp()
    time.sleep(4)
    sipp_Clnt.stop_sipp()

