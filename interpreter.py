# Rehan Kedia
# Phase 3
import parser
import scanner
import math
import sys

memory = {}


def deletesubtree(tree):
    if tree:
        deletesubtree(tree.leftchild)
        deletesubtree(tree.midchild)
        deletesubtree(tree.rightchild)
        tree.key = None


count = 0


def interpreter(tree):
    global count
    # if tree.key != "WHILE-LOOP" and tree.key != "IF-STATEMENT" and tree.key != "SKIP":
    #     temp = " ".join(tree.key)
    # else:
    #     temp = "".join(tree.key)
    # outfile.write("      " * level + temp)
    # print(temp)
    # outfile.write("\n")
    # print(tree.key)
    if tree.key is None:
        return
    if tree.key == "WHILE-LOOP" or tree.key == "IF-STATEMENT" or tree.key == "SKIP":
        temp = "".join(tree.key)
    else:
        temp = "".join(tree.key[0])
    if temp == ":=":
        value = evaluateassignment(tree.rightchild)
        # print(value)
        # print("".join(tree.leftchild.key[0]))
        dict1 = {"".join(tree.leftchild.key[0]): value}
        memory.update(dict1)
        if count == 0:
            deletesubtree(tree)
    if temp == "IF-STATEMENT":
        evaluateif(tree)
        if count == 0:
            deletesubtree(tree)
        return
    if temp == "WHILE-LOOP":
        evaluatewhile(tree)
        if count == 0:
            deletesubtree(tree)
        return
    if temp == "SKIP":  # remove subtree
        deletesubtree(tree)
        return
    if tree.leftchild:
        interpreter(tree.leftchild)

    if tree.midchild:
        interpreter(tree.midchild)

    if tree.rightchild:
        interpreter(tree.rightchild)


def evaluateassignment(tree):
    if tree.key is None:
        return
    value = 0
    temp = "".join(tree.key[0])
    if scanner.imp_lexer(temp)[0][1] == "NUMBER":
        return temp

    lefttemp = "".join(tree.leftchild.key[0])
    lefttemp = scanner.imp_lexer(lefttemp)[0][0]
    righttemp = "".join(tree.rightchild.key[0])
    righttemp = scanner.imp_lexer(righttemp)[0][0]

    if lefttemp == "+":
        num = evaluateassignment(tree.leftchild)
        if scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = num + int(memory.get(righttemp))
        if scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = num + int(righttemp)
    if lefttemp == "-":
        num = evaluateassignment(tree.leftchild)
        if scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = num - int(memory.get(righttemp))
        if scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = num - int(righttemp)
    if lefttemp == "*":
        num = evaluateassignment(tree.leftchild)
        if scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = num * int(memory.get(righttemp))
        if scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = num * int(righttemp)

    if temp == "+":
        if scanner.imp_lexer(lefttemp)[0][1] == "NUMBER" and scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = int(lefttemp) + int(righttemp)
        elif scanner.imp_lexer(lefttemp)[0][1] == "IDENTIFIER" and scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = int(memory.get(lefttemp)) + int(righttemp)
        elif scanner.imp_lexer(lefttemp)[0][1] == "NUMBER" and scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = int(lefttemp) + int(memory.get(righttemp))
        elif scanner.imp_lexer(lefttemp)[0][1] == "IDENTIFIER" and scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = int(memory.get(lefttemp)) + int(memory.get(righttemp))
    if temp == "-":
        if scanner.imp_lexer(lefttemp)[0][1] == "NUMBER" and scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = int(lefttemp) - int(righttemp)
        elif scanner.imp_lexer(lefttemp)[0][1] == "IDENTIFIER" and scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = int(memory.get(lefttemp)) - int(righttemp)
        elif scanner.imp_lexer(lefttemp)[0][1] == "NUMBER" and scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = int(lefttemp) - int(memory.get(righttemp))
        elif scanner.imp_lexer(lefttemp)[0][1] == "IDENTIFIER" and scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = int(memory.get(lefttemp)) - int(memory.get(righttemp))
    if temp == "*":
        if scanner.imp_lexer(lefttemp)[0][1] == "NUMBER" and scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = int(lefttemp) * int(righttemp)
        elif scanner.imp_lexer(lefttemp)[0][1] == "IDENTIFIER" and scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = int(memory.get(lefttemp)) * int(righttemp)
        elif scanner.imp_lexer(lefttemp)[0][1] == "NUMBER" and scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = int(lefttemp) * int(memory.get(righttemp))
        elif scanner.imp_lexer(lefttemp)[0][1] == "IDENTIFIER" and scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = int(memory.get(lefttemp)) * int(memory.get(righttemp))
    if temp == "/":
        if scanner.imp_lexer(lefttemp)[0][1] == "NUMBER" and scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = math.floor(int(lefttemp) / int(righttemp))
        elif scanner.imp_lexer(lefttemp)[0][1] == "IDENTIFIER" and scanner.imp_lexer(righttemp)[0][1] == "NUMBER":
            value = math.floor(int(memory.get(lefttemp)) / int(righttemp))
        elif scanner.imp_lexer(lefttemp)[0][1] == "NUMBER" and scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = math.floor(int(lefttemp) / int(memory.get(righttemp)))
        elif scanner.imp_lexer(lefttemp)[0][1] == "IDENTIFIER" and scanner.imp_lexer(righttemp)[0][1] == "IDENTIFIER":
            value = math.floor(int(memory.get(lefttemp)) / int(memory.get(righttemp)))
    if value < 0:
        value = 0
    return value


def evaluateif(tree):
    temp1 = tree.leftchild
    num = int(evaluateassignment(temp1))
    if num > 0:
        interpreter(tree.midchild)
    if num == 0:
        interpreter(tree.rightchild)


def evaluatewhile(tree):  # while as root Make tree1 and copy the while in right and in left is the body of while
    global count
    count = 0
    num = 1
    tree1 = tree
    # print(tree.leftchild.leftchild.key)
    # print(tree.rightchild.key)
    if tree.leftchild:
        tree1.midchild = tree.leftchild.clonetree()
    if tree.rightchild:
        tree1.rightchild = tree.rightchild.clonetree()
        tree1.leftchild = tree.rightchild.clonetree()
    # print(tree1.midchild.key)
    while num > 0:
        num = evaluateassignment(tree1.midchild)
        # print(num)
        if num > 0:
            # print(num)
            # print(memory)
            count = 1
            interpreter(tree1.rightchild)
            count = 0
        if num == 0:
            return


def main():
    inputfile = "input.txt" #sys.argv[1]
    outputfile = "output.txt" #sys.argv[2]
    infile = open(inputfile, "r")
    outfile = open(outputfile, "w+")
    data = infile.read()
    tokens = scanner.imp_lexer(data)
    outfile.write("Tokens:\n")
    for j in range(len(tokens)):
        outfile.write(tokens[j][1] + " " + tokens[j][0] + "\n")
    outfile.write("\n\n\n")
    tree = parser.parser(outfile, tokens)
    outfile.write("\n\nAST:\n")
    tree.printt(outfile)
    interpreter(tree)
    # outfile.write(memory.keys())
    outfile.write("\n\nOutput: \n")
    for key, value in memory.items():
        print(key, "=", value)
        outfile.write(str(key) + " = " + str(value) + "\n")
    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
