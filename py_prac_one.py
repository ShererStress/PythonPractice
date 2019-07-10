
print("Hello World!");
haveInput = False;
# while !haveInput
try:
    age = int(input("How old are you? "));
except ValueError:
    print("That's not an integer");
    age = "NOPE"
except:
    print("You broke it somehow")
print(age);
