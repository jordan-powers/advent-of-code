from pathlib import Path

in_p = Path(__file__).parent / 'input.txt'

list1 = []
list2 = []

with in_p.open("r") as inf:
    for line in inf.readlines():
        n1, n2 = line.strip().split()
        n1 = int(n1)
        n2 = int(n2)

        list1.append(n1)
        list2.append(n2)

list1.sort()
list2.sort()

assert len(list1) == len(list2)

solution1 = 0

for i in range(len(list1)):
    solution1 += abs(list1[i] - list2[i])

print(f"Part 1: {solution1}")

list2_count: 'dict[int, int]' = {}

for elem in list2:
    list2_count[elem] = list2_count.get(elem, 0) + 1


solution2 = 0

for elem in list1:
    solution2 += elem * list2_count.get(elem, 0)

print(f"Part 2: {solution2}")
