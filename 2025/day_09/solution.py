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

def orient(a, b, c):
    return (b-a).cross(c-a)

def line_crosses(l1, l2):
    a = l1[0]
    b = l1[1]
    c = l2[0]
    d = l2[1]

    oa = orient(c,d,a)
    ob = orient(c,d,b)
    oc = orient(a,b,c)
    od = orient(a,b,d)

    return oa*ob < 0 and oc*od < 0


lines = [(points[i], points[(i+1)%len(points)]) for i in range(len(points))]

incoming_vecs = [(points[(i-1+len(points)) % len(points)] - points[i]) for i in range(len(points))]
outgoing_vecs = [(points[(i+1)%len(points)] - points[i]) for i in range(len(points))]

def vec_contained(test, a, b):
    return a.cross(b) * a.cross(test) >= 0 and test.cross(b) * test.cross(a) >= 0

def test_rect(i, j):
    #      v1
    #   p1 -- p2
    # v2 |    | v3
    #   p4 -- p3
    #      v4
    p1 = points[i]
    p3 = points[j]
    p2 = Vec2(p3.x, p1.y)
    p4 = Vec2(p1.x, p3.y)

    v1 = p2 - p1
    v2 = p4 - p1
    v3 = p2 - p3
    v4 = p4 - p3



    if not vec_contained(v1, incoming_vecs[i], outgoing_vecs[i]):
        return False
    if not vec_contained(v2, incoming_vecs[i], outgoing_vecs[i]):
        return False
    if not vec_contained(v3, incoming_vecs[j], outgoing_vecs[j]):
        return False
    if not vec_contained(v4, incoming_vecs[j], outgoing_vecs[j]):
        return False

    for line in lines:
        if line_crosses((p1, p2), line):
            return False
        if line_crosses((p2, p3), line):
            return False
        if line_crosses((p3, p4), line):
            return False
        if line_crosses((p4, p1), line):
            return False
    return True

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
