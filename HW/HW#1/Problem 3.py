def pick_color(name):
    if name == "red" or name == "green" or name == "blue":
        return name
    else:
        raise ValueError(f"Invalid color: {name}. Valid colors are red, green, and blue.")

print(pick_color("red"))
print(pick_color("GEEEEEEEEEEN"))