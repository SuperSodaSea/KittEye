# -*- coding: utf-8 -*-
'''
    Copyright (c) 2016-2018 The Cats Project

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
'''

import os

from kitteye.parser import *
from kitteye.language.c import *


def parse(path):
    modules = {}
    for x in os.listdir(path):
        p = os.path.join(path, x)
        if os.path.isdir(p):
            modules[x] = parse(p)
        elif os.path.isfile(p) and os.path.splitext(x)[1] == '.kei':
            declarations = Parser.parseFile(p)
            modules[os.path.splitext(x)[0]] = declarations
    return modules

def generate(modules, name):
    generator = CGenerator()
    for x in modules:
        if isinstance(modules[x], list):
            generator.generate(modules[x], name)
        else:
            generate(modules[x], name + [x])
            

def isInternalType(type):
    if type == 'Uint8' or type == 'Uint16' or type == 'Uint32' or type == 'Uint64'
        return True
    if type == 'Int8' or type == 'Int16' or type == 'Int32' or type == 'Int64'
        return True
    if type == 'Float32' or type == 'Float64'
        return True
    return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:')
        print('    generator <path>')
        exit(1)
    
    modules = parse(os.path.normpath(sys.argv[1]))
    generate(modules, [])
