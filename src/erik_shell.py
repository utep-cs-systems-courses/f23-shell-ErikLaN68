#! /usr/bin/env python3

import os, sys, re

pidRunning = []

def runProcess(args):
    pid = os.getpid()
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    # child
    elif rc == 0:
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error
    # parent (forked ok)
    else:
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                    (pid, rc)).encode())
        # waits for child to exit out
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                    childPidCode).encode())

def runProcessBackGround(args):
    pid = os.getpid()
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    # child
    elif rc == 0:
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                # pidRunning[rc] = pid
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error
    # parent (forked ok)
    else:
        pidRunning.append(rc)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                    (pid, rc)).encode())

def parseCommand():
    parsedCommand = userCommand.split()
    if len(parsedCommand) == 0:
        return
    if parsedCommand[-1] == '&':
        parsedCommand.remove('&')
        runProcessBackGround(parsedCommand)
    else:
        runProcess(parsedCommand)

def checkZombie():
    print('checking zombie')
    if len(pidRunning) <= 0:
        return
    if (waitResult := os.waitid(os.P_ALL, 0, os.WEXITED | os.WNOHANG)):
        print(waitResult)
        zPid, zStatus = waitResult.si_pid, waitResult.si_status
        print(f"""zombie reaped:\tpid={zPid}, status={zStatus}""")
        pidRunning.remove(zPid)
        print('reaped')
    else:
        print('nothing to reap')
        return               # no zombies; break from loop

while True:
    userCommand = input('erikShell$ ')
    if userCommand.lower() == 'exit':
        exit()
    checkZombie()
    parseCommand()
    print(pidRunning)