items = [("Books", 4200), ("Travel", 28500), ("Food", 1750)]

print(f"{'Name':<10} {'Amount':>12}")
print("-" * 22)

total = 0

for name, amount in items:
    print(f"{name:<10} ${amount:>11,}")
    total += amount

print("-" * 22)
print(f"{'Total':<10} ${total:>11,}")