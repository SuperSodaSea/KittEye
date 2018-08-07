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

class Type:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class TemplateType:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
    def __str__(self):
        s = self.name + '('
        first = True
        for argument in self.arguments:
            if not first:
                s += ', '
            else:
                first = False
            s += str(argument)
        s += ')'
        return s

class FunctionType:
    def __init__(self, arguments, ret):
        self.arguments = arguments
        self.ret = ret
    def __str__(self):
        s = '('
        first = True
        for argument in self.arguments:
            if not first:
                s += ', '
            else:
                first = False
            s += argument[0] + ': ' + str(argument[1])
        s += ')'
        if self.ret is not None:
            s += ' -> ' + str(self.ret)
        return s
