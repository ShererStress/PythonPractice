#Up to lesson 16
filename =  "./datafiles/sample15.txt";

textFile = open(filename, "w+");

# print(textFile.read());

textFile.truncate();

textFile.write("LINE ONE \nLINE TWO \nLINE THREE");

print(f"here is the file {filename}:");
textFile.seek(0);
print(textFile.read());

textFile.close();
