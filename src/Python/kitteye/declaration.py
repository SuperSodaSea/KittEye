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

class ImportDeclaration:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        s = 'import ' + '.'.join(self.name)
        return s

class ConstantDeclaration:
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def __str__(self):
        return 'constant ' + self.name + ' -> ' + str(self.type)

class EnumDeclaration:
    def __init__(self, name, type, enumerators):
        self.name = name
        self.type = type
        self.enumerators = enumerators
    def __str__(self):
        s = 'enum ' + self.name + ' : ' + str(self.type) + ' {\n'
        for enumerator in self.enumerators:
            s += '    ' + enumerator + ',\n'
        s += '}'
        return s

class StructDeclaration:
    def __init__(self, name, parent, members):
        self.name = name
        self.parent = parent
        self.members = members
    def __str__(self):
        s = 'struct ' + self.name
        if self.parent is not None:
            s += ' : ' + str(self.parent)
        s += ' {\n'
        for member in self.members:
            s += '    ' + member[0] + ': ' + str(member[1]) + '\n'
        s += '}'
        return s

class InterfaceDeclaration:
    def __init__(self, name, parent, members):
        self.name = name
        self.parent = parent
        self.members = members
    def __str__(self):
        s = 'interface ' + self.name
        if self.parent is not None:
            s += ' : ' + str(self.parent)
        s += ' {\n'
        for member in self.members:
            s += '    ' + member[0] + ': ' + str(member[1]) + '\n'
        s += '}'
        return s
