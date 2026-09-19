names = ["red", "purple", "blue"]
def pick_color(name):
    if name == "red" or name == "green" or name == "blue":
        return name
    else:
        raise ValueError(f"Invalid color: {name}. Valid colors are red, green, and blue.")

for name in names:
    try:
        pick_color(name)
        print(name + " is a valid color!")
    except ValueError:
        print(name + " is not a valid color.")