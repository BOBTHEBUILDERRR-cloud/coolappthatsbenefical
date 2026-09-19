def celsius_to_fahrenheit(c):
	return c * 9 / 5 + 32


assert celsius_to_fahrenheit(0) == 32
assert celsius_to_fahrenheit(100) == 212
assert celsius_to_fahrenheit(-40) == -40

x = input("Please input a Celsius")
print(celsius_to_fahrenheit(int(x)))