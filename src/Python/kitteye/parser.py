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
import sys

from kitteye.tokenizer import *
from kitteye.type import *


class Parser:
    def nextToken(self):
        self.pos += 1
        self.token = self.tokens[self.pos]
    def parseError(self):
        raise RuntimeError('Unexpected token ' + str(self.token.data))
    def expectToken(self, type):
        if self.token.type != type: self.parseError()
    def parseType(self):
        if self.token.type == 'Identifier':
            name = self.token.data
            self.nextToken()
            if self.token.type == '(':
                self.nextToken()
                arguments = []
                first = True
                while self.token.type != ')':
                    if not first:
                        self.expectToken(',')
                        self.nextToken()
                    else:
                        first = False
                    arguments.append(self.parseType())
                self.nextToken()
                return TemplateType(name, arguments)
            else:
                return Type(name)
        elif self.token.type == '(':
            self.nextToken()
            arguments = []
            first = True
            while self.token.type != ')':
                if not first:
                    self.expectToken(',')
                    self.nextToken()
                else:
                    first = False
                self.expectToken('Identifier')
                name = self.token.data
                self.nextToken()
                self.expectToken(':')
                self.nextToken()
                arg = self.parseType()
                arguments.append((name, arg))
            self.nextToken()
            ret = None
            if self.token.type == '->':
                self.nextToken()
                ret = self.parseType()
            return FunctionType(arguments, ret)
        else:
            self.parseError()
    def parseConstant(self):
        self.nextToken()
        self.expectToken('Identifier')
        name = self.token.data
        self.nextToken()
        self.expectToken('->')
        self.nextToken()
        type = self.parseType()
        return ConstantType(name, type)
    def parseEnum(self):
        self.nextToken()
        self.expectToken('Identifier')
        name = self.token.data
        self.nextToken()
        self.expectToken(':')
        self.nextToken()
        self.expectToken('Identifier')
        type = Type(self.token.data)
        self.nextToken()
        self.expectToken('{')
        self.nextToken()
        enumerators = []
        while self.token.type != '}':
            self.expectToken('Identifier')
            enumerators.append(self.token.data)
            self.nextToken()
            if self.token.type == '}':
                break
            elif self.token.type == ',':
                self.nextToken()
            else:
                self.parseError()
        self.nextToken()
        return EnumType(name, type, enumerators)
    def parseStruct(self):
        type = self.token.data
        self.nextToken()
        self.expectToken('Identifier')
        name = self.token.data
        self.nextToken()
        parent = None
        if self.token.type == ':':
            self.nextToken()
            parent = self.parseType()
        self.expectToken('{')
        self.nextToken()
        members = []
        while self.token.type != '}':
            self.expectToken('Identifier')
            memberName = self.token.data
            self.nextToken()
            self.expectToken(':')
            self.nextToken()
            memberType = self.parseType()
            self.expectToken(';')
            self.nextToken()
            members.append((memberName, memberType))
        self.nextToken()
        if type == 'struct':
            return StructType(name, parent, members)
        else:
            return InterfaceType(name, parent, members)
    def parse(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token = self.tokens[0]
        types = []
        while self.token.type != 'End':
            if self.token.type == 'Identifier':
                if self.token.data == 'constant':
                    types.append(self.parseConstant())
                    continue
                if self.token.data == 'enum':
                    types.append(self.parseEnum())
                    continue
                if self.token.data == 'struct' or self.token.data == 'interface':
                    types.append(self.parseStruct())
                    continue
            self.parseError()
        return types

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:')
        print('    Parser.py <file>')
        exit(1)
    with open(sys.argv[1], 'r') as file:
        data = file.read()
    
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(data)
    
    parser = Parser()
    types = parser.parse(tokens)
    
    for type in types:
        print(type)
