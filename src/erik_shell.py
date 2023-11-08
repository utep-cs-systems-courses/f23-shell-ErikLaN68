#! /usr/bin/env python3

import os, sys, re

while True:
    userCommand = input('erikShell$ ')
    if userCommand.lower() == 'exit':
        exit()
    print(" Echo given command " + userCommand)