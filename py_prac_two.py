from sys import argv

print(argv)

script = argv[0];
first = argv[1];
second = argv[2];
third = argv[3];

print(first)
print(second)
print(third)

testInput = input(" > ")

print( f"""
{first}
{second}
test input: {testInput}
""")

num = 0;
while (num < 10):
    print("AAA")
    num += 1
