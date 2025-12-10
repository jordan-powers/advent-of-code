from pathlib import Path

USE_SAMPLE_INPUT = True
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip()

else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return isinstance(other, Vec2) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return "Vec2" + str(self)

    def cross(self, other):
        assert isinstance(other, Vec2)
        return self.x*other.y - self.y*other.x

points = []
for line in input.split():
    x, y = line.split(',')
    points.append(Vec2(int(x), int(y)))


largest_rect = None
for i in range(len(points)):
    for j in range(i+1, len(points)):
        diff = points[j] - points[i]
        area = (abs(diff.x)+1) * (abs(diff.y)+1)
        #print(points[i], points[j], area)
        if largest_rect is None or area > largest_rect[0]:
            largest_rect = (area, (points[i], points[j]))

print("Part 1:", largest_rect[0])

lines = [(points[(i+1) % len(points)], points[i]) for i in range(len(points))]

def test_rec(i, j):
    p1 = points[i]
    p3 = points[j]

    diff = p3 - p1
    if diff.x > 0 == diff.y > 0:
        p2 = Vec2(p3.x, p1.y)
        p4 = Vec2(p1.x, p3.y)
    else:
        p2 = Vec2(p1.x, p3.y)
        p4 = Vec2(p3.x, p1.y)

    rect = [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]
    for l1, l2 in lines:






largest_rect = None
for i in range(len(points)):
    for j in range(i+1, len(points)):
        if not test_rect(i, j):
            continue
        diff = points[j] - points[i]
        area = (abs(diff.x)+1) * (abs(diff.y)+1)
        if largest_rect is None or area >= largest_rect[0]:
            largest_rect = (area, (points[i], points[j]))

print(largest_rect)
print("Part 2:", largest_rect[0])
