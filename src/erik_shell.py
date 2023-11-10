#! /usr/bin/env python3

import os, sys, re

def childMake(args):
    
    pid = os.getpid()
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
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

def parseCommand():
    return userCommand.split()
    
while True:
    userCommand = input('erikShell$ ')
    if userCommand.lower() == 'exit':
        exit()
    parsedCommand = parseCommand()
    childMake(parsedCommand)