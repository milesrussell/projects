formatter = "{} {} {} {}"

print(formatter.format(1, 2, 3, 4))
print(formatter.format("one", "two", "three", "four"))
print(formatter.format(True, False, False, True))
print(formatter.format(formatter, formatter, formatter, formatter))
print(formatter.format(
    "To be or not to be",
    "That is the question",
    "Whether it is nobler in the mind",
    "To suffer the slings and arrows of outrageous fortune"
))
