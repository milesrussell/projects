name = "Miles D. Russell"
age = 25
height = 72 # inches
weight = 190 # pounds
eyes = 'Green'
teeth = 'White' # hopefully not yellow
hair = 'Brown'

print(f"Let's talk about {name}.")
print(f"He's {height} inches tall.")
print(f"He's {weight} pounds heavy.")
print(f"Actually that's not too heavy.")
print(f"He's got {eyes} eyes and {hair} hair.")
print(f"His teeth are usually {teeth} depending on the coffee.")

total = age + height + weight
print(f"If I add {age}, {age}, and {weight} I get {total}.")

weight_kg = 0.45 * weight
height_cm = 2.54 * height

print(f"That converts to {weight_kg} kilograms and {height_cm} centimeters")
