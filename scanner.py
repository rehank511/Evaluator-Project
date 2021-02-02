# Rehan Kedia
# Phase 1
import re
import sys

KEY = 'KEYWORD'
PUNC = 'PUNCTUATION'
NUMBER = 'NUMBER'
IDENTIFIER = 'IDENTIFIER'

token_exprs = [
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\:=',                   PUNC),
    (r'\(',                    PUNC),
    (r'\)',                    PUNC),
    (r';',                     PUNC),
    (r'\+',                    PUNC),
    (r'-',                     PUNC),
    (r'\*',                    PUNC),
    (r'/',                     PUNC),
    (r'if',                    KEY),
    (r'then',                  KEY),
    (r'endwhile',              KEY),
    (r'endif',                 KEY),
    (r'else',                  KEY),
    (r'while',                 KEY),
    (r'do',                    KEY),
    (r'end',                   KEY),
    (r'[0-9]+',                NUMBER),
    (r'[A-Za-z][A-Za-z0-9_]*', IDENTIFIER),
]


def imp_lexer(characters):
    return lexer(characters, token_exprs)


def lexer(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens


if __name__ == '__main__':
    filename = "test_input.txt"
    file = open(filename, "r")
    characters = file.read()
    file.close()
    tokens = imp_lexer(characters)
    print(tokens)

