from sys import argv;

# ./datafiles/sample15.txt

txt = open(argv[1]);

print(f"here is the file {argv[1]}:");

print(txt.read());
