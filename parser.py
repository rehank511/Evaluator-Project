# Rehan Kedia
# Phase 2
import scanner
import sys

i = 0


class Tree:
    def __init__(self, data, left=None, right=None, mid=None):
        self.key = data
        self.leftchild = left
        self.rightchild = right
        self.midchild = mid

    def insertleft(self, newnode):
        if self.leftchild is None:
            self.leftchild = Tree(newnode)
        else:
            t = Tree(newnode)
            t.leftchild = self.leftchild
            self.leftchild = t

    def insertright(self, newnode):
        if self.rightchild is None:
            self.rightchild = Tree(newnode)
        else:
            t = Tree(newnode)
            t.rightchild = self.rightchild
            self.rightchild = t

    def insertmid(self, newnode):
        if self.midchild is None:
            self.midchild = Tree(newnode)
        else:
            t = Tree(newnode)
            t.midchild = self.midchild
            self.midchild = t

    def printt(self, outfile, level=0):
        if self.key != "WHILE-LOOP" and self.key != "IF-STATEMENT" and self.key != "SKIP":
            temp = " ".join(self.key)
        else:
            temp = "".join(self.key)
        # print("      " * level + temp + "\n")

        outfile.write("      " * level + temp)
        outfile.write("\n")
        if self.leftchild:
            self.leftchild.printt(outfile, level + 1)

        if self.midchild:
            self.midchild.printt(outfile, level + 1)

        if self.rightchild:
            self.rightchild.printt(outfile, level + 1)

    def clonetree(self):
        if self is None:
            return None
        temp = self
        temp.key = self.key
        if self.leftchild:
            temp.leftchild = self.leftchild.clonetree()

        if self.midchild:
            temp.midchild = self.midchild.clonetree()

        if self.rightchild:
            temp.rightchild = self.rightchild.clonetree()

        return temp


def checkindex(a, outfile, length):
    if a >= length:
        outfile.write("Error !!")
        sys.exit(-1)


def parsestatement(token, outfile, tree):
    global i
    tree = parsebasestatement(token, outfile, tree)
    if i < len(token):
        while token[i][0] == ";":
            i += 1
            checkindex(i,  outfile, len(token))
            tree = Tree(token[i - 1], tree, parsebasestatement(token, outfile, None))
            if i >= len(token):
                break
    return tree


def parsebasestatement(token, outfile, tree):
    global i
    if token[i][1] == "IDENTIFIER":
        if token[i + 1][0] != ":=":
            outfile.write("Error in Assignment, No Assignment Found")
            sys.exit(-1)
        if i == 0:
            tree = Tree(token[i], None, None)
        else:
            tree = Tree(token[i], tree, None)
        i += 1
        tree = parseassignment(token, outfile, tree)
        return tree
    if token[i][0] == "while":
        i += 1
        checkindex(i, outfile, len(token))
        temp1 = parseexpression(token, outfile, None)
        if token[i][0] != "do":
            outfile.write("Error in while loop, no do statement!!")
            sys.exit(-1)
        i += 1
        checkindex(i, outfile, len(token))
        temp2 = parsestatement(token, outfile, None)
        if token[i][0] != "endwhile":
            outfile.write("Error in while loop, no end while!!")
            sys.exit(-1)
        tree = Tree("WHILE-LOOP", temp1, temp2)
        i += 1
        return tree
    if token[i][0] == "if":
        i += 1
        checkindex(i, outfile, len(token))
        temp1 = parseexpression(token, outfile, None)
        if token[i][0] != "then":
            outfile.write("Error in if statement, no then keyword!!")
            sys.exit(-1)
        i += 1
        checkindex(i, outfile, len(token))
        temp2 = parsestatement(token, outfile, None)
        if token[i][0] != "else":
            outfile.write("Error in if statement, no else keyword!!")
            sys.exit(-1)
        i += 1
        checkindex(i, outfile, len(token))
        temp3 = parsestatement(token, outfile, None)
        if token[i][0] != "endif":
            outfile.write("Error in if statement, no endif keyword!!")
            sys.exit(-1)
        tree = Tree("IF-STATEMENT", temp1, temp3, temp2)
        i += 1
        return tree
    if token[i][0] == "skip":
        i += 1
        checkindex(i, outfile, len(token))
        tree = Tree("SKIP")
        return tree


def parseassignment(token, outfile, tree):
    global i
    if token[i][0] == ":=":
        i += 1
        checkindex(i,  outfile, len(token))
        tree = Tree(token[i - 1], tree, parseexpression(token, outfile, None))
        return tree


def parseexpression(token, outfile, tree):
    global i
    tree = parseterm(token, outfile, tree)
    if i < len(token):
        while token[i][0] == "+":
            i += 1
            checkindex(i, outfile, len(token))
            tree = Tree(token[i - 1], tree, parseterm(token, outfile, None))
            if i >= len(token):
                break
    return tree


def parseterm(token, outfile, tree):
    global i
    tree = parsefactor(token, outfile, tree)
    if i < len(token):
        while token[i][0] == "-":
            i += 1
            checkindex(i, outfile, len(token))
            tree = Tree(token[i - 1], tree, parsefactor(token, outfile, None))
            if i >= len(token):
                break
    return tree


def parsefactor(token, outfile, tree):
    global i
    tree = parsepiece(token, outfile, tree)
    if i < len(token):
        if token[i][0] == "/":
            i += 1
            checkindex(i,  outfile, len(token))
            tree = Tree(token[i - 1], tree, parsepiece(token, outfile, None))
    return tree


def parsepiece(token, outfile, tree):
    global i
    tree = parseelement(token, outfile)
    if i < len(token):
        while token[i][0] == "*":
            i += 1
            checkindex(i,  outfile, len(token))
            tree = Tree(token[i - 1], tree, parseelement(token, outfile))
            if i >= len(token):
                break
    return tree


def parseelement(token, outfile):
    global i
    if token[i][1] == "NUMBER":
        tree = Tree(token[i], None, None)
        i += 1
        checkindex(i,  outfile, len(token))
        return tree
    if token[i][1] == "IDENTIFIER":
        tree = Tree(token[i], None, None)
        i += 1
        checkindex(i,  outfile, len(token))
        return tree
    if token[i][0] == "(":
        i += 1
        checkindex(i,  outfile, len(token))
        tree = parseexpression(token, outfile, None)
        if token[i][0] != ")":
            outfile.write("Error No Closing Brackets")
        i += 1
        return tree


def main():
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    infile = open(inputfile, "r")
    outfile = open(outputfile, "w+")
    # infile = open("input.txt", "r")
    # outfile = open("output.txt", "w+")
    data = infile.read()
    tokens = scanner.imp_lexer(data)
    outfile.write("Tokens:\n")
    for j in range(len(tokens)):
        outfile.write(tokens[j][1] + " " + tokens[j][0] + "\n")
    tree = parser(outfile, tokens)
    outfile.write("\n\nAST:\n")
    tree.printt(outfile)
    infile.close()
    outfile.close()


def parser(outfile, tokens):
    tree = Tree('', None, None)
    global i
    length = len(tokens)
    i = 0
    while i < length:
        tree = parsestatement(tokens, outfile, tree)
        i += 1
    return tree


if __name__ == '__main__':
    main()
