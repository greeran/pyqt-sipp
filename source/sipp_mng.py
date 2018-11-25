import multiprocessing
import sipp_user
import time

def run_sipp(cmd):
    sipp_p = sipp_user.sipp_user(cmd)
    sipp_p.run_sipp()

    time.sleep(5)
    
    sipp_p.stop_sipp()

def run_sipps():
    jobs = []
    
    jobs.append(multiprocessing.Process(target=run_sipp, name="sipp_answer",
        args=("d:\\cgwin-64\\Sipp_3.2\\sipp.exe -r 1 -rp 1 -sf C:\\sipp\\answer.xml -i [172.17.125.12] -p 5072  -default_behaviors -bye",)))
    jobs.append(multiprocessing.Process(target=run_sipp, name="sipp_caller",
        args=("d:\\cgwin-64\\Sipp_3.2\\sipp.exe 172.17.125.126 -r 100 -l 892 -sf C:\\sipp\\calling_dSec.xml -i [172.17.125.12] -p 5090  -trace_err  -default_behaviors -bye",)))

    for p in jobs:
        p.start()

    
    for p in jobs:
        p.join()

if __name__ == '__main__':
    run_sipps()
