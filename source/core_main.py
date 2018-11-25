import sys
import shlex, subprocess
import threading

stdout_result = 1
stderr_result = 1


def stdout_thread(pipe):
    global stdout_result
    while True:
        out = pipe.stdout.read(1)
        stdout_result = pipe.poll()
        if out == '' and stdout_result is not None:
            sys.stdout.write("closing")
            break

        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()


def stderr_thread(pipe):
    global stderr_result
    while True:
        err = pipe.stderr.read(1)
        stderr_result = pipe.poll()
        if err == '' and stderr_result is not None:
            break

        if err != '':
            sys.stdout.write(err)
            sys.stdout.flush()



def exec_command(command, cwd=None):
    if cwd is not None:
        print ('[' + ' '.join(command) + '] in ' + cwd)
    else:
        print ('[' + ' '.join(command) + ']')

    p = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd=cwd
    )

    out_thread = threading.Thread(name='stdout_thread', target=stdout_thread, args=(p,))
    err_thread = threading.Thread(name='stderr_thread', target=stderr_thread, args=(p,))

    err_thread.start()
    out_thread.start()

    out_thread.join()
    err_thread.join()

    #return stdout_result + stderr_result

#if __name__ == '__main__':
#    exec_command("ls -la")

answer_cmd="d:\\cgwin-64\\Sipp_3.2\\sipp.exe -r 1 -rp 1 -sf C:\\sipp\\answer.xml -i [172.17.125.12] -p 5070  -default_behaviors -bye"

exec_command(answer_cmd)