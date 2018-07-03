import os
import re
import sys


class Token:
    def __init__(self, type, data):
        self.type = type
        self.data = data
    def __str__(self):
        return '({}, {})'.format(self.type, self.data)

class Tokenizer:
    def __init__(self):
        self.space = re.compile('[ \t\r\n]+')
        self.tokenTypes = [
            ('Identifier', '[A-Z_a-z][0-9A-Z_a-z]*'),
            ('(', '\('),
            (')', '\)'),
            (',', ','),
            (':', ':'),
            (';', ';'),
            ('{', '{'),
            ('}', '}'),
            ('->', '->'),
        ]
        self.regexs = []
        for tokenType in self.tokenTypes:
            self.regexs.append(re.compile(tokenType[1]))
    def tokenize(self, data):
        tokens = []
        pos = 0
        while pos < len(data):
            m = self.space.match(data, pos)
            if m:
                pos = m.end()
                continue
            match = False
            for i in range(0, len(self.regexs)):
                regex = self.regexs[i]
                result = regex.match(data, pos)
                if result:
                    tokens.append(Token(self.tokenTypes[i][0], data[pos : result.end()]))
                    pos = result.end()
                    match = True
                    break
            if not match:
                raise RuntimeError('Unknown token at ' + str(pos) + ': ' + data[pos])
        tokens.append(Token('End', '<End>'))
        return tokens

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
            print('    type', self.token.data)
            self.nextToken()
            if self.token.type == '(':
                self.nextToken()
                self.parseType()
                self.expectToken(')')
                self.nextToken()
        elif self.token.type == '(':
            self.nextToken()
            first = True
            while self.token.type != ')':
                if not first:
                    self.expectToken(',')
                    self.nextToken()
                else:
                    first = False
                self.expectToken('Identifier')
                print('    argument', self.token.data)
                self.nextToken()
                self.expectToken(':')
                self.nextToken()
                self.parseType()
            self.nextToken()
            if self.token.type == '->':
                self.nextToken()
                self.parseType()
        else:
            self.parseError()
    def parseStruct(self):
        self.nextToken()
        self.expectToken('Identifier')
        print('struct', self.token.data)
        self.nextToken()
        self.expectToken('{')
        self.nextToken()
        while self.token.type != '}':
            self.expectToken('Identifier')
            print('    member', self.token.data)
            self.nextToken()
            self.expectToken(':')
            self.nextToken()
            self.parseType()
            self.expectToken(';')
            self.nextToken()
        self.nextToken()
    def parseInterface(self):
        self.nextToken()
        self.expectToken('Identifier')
        print('interface', self.token.data)
        self.nextToken()
        self.expectToken('{')
        self.nextToken()
        while self.token.type != '}':
            self.expectToken('Identifier')
            print('    member', self.token.data)
            self.nextToken()
            self.expectToken('(')
            self.parseType()
            self.expectToken(';')
            self.nextToken()
        self.nextToken()
    def parse(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token = self.tokens[0]
        while self.token.type != 'End':
            if self.token.type == 'Identifier':
                if self.token.data == 'struct':
                    self.parseStruct()
                    continue
                elif self.token.data == 'interface':
                    self.parseInterface()
                    continue
            self.parseError()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:')
        print('    Parser <file>')
        exit(1)
    with open(sys.argv[1], 'r') as file:
        data = file.read()
    
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(data)
    parser = Parser()
    parser.parse(tokens)
