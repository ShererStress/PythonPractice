#Lessons 17+
def printNoise(argOne = 0):
    print("AAAAAA");
    print(argOne);

printNoise(3);
printNoise("A string appeared");
printNoise(23+77);

#functionFirstTest();

def functionFirstTest():
    print("FUNCTION DEFS FIRST");
    functionSecondTest();

def functionSecondTest():
    print("Called in function one")

def recursionTest(numLeft):
    print(f"{numLeft} times remain");
    if numLeft > 1:
        return (recursionTest(numLeft-1)+1);
    else:
        return 1;

functionFirstTest();


print(f"{recursionTest(7)} total calls");
