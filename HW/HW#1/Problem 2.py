def count_lines(path):
    bob = 0
    with open(path, "r", encoding="utf-8") as file:
        #lines = file.readlines()
        for line in file:
            bob+=1
    
    return bob


def total(path):
    with open(path, "r") as file:
        numbers = file.readlines()

    sum = 0
    for number in numbers:
        sum += int(number)

    return sum


print(count_lines("HW/HW#1/colors.txt"))
print(total("HW/HW#1/numbers.txt"))