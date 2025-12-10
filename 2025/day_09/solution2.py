from pathlib import Path
import tqdm

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


lines = [(points[i], points[(i+1)%len(points)]) for i in range(len(points))]


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


def point_on_line(point, line):
    a = line[0]
    b = line[1]
    c = point
    cross = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
    if cross != 0:
        return False

    dot = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)
    if dot < 0:
        return False

    lenba = (b.x - a.x)**2 + (b.y - a.y)**2
    if dot > lenba:
        return False
    return True

def test_point(p):
    intersect_count = 0
    ray = (Vec2(0, 0), p)

    for line in lines:
        if point_on_line(p, line):
            return True
        if line_crosses(ray, line):
            intersect_count += 1

    if intersect_count % 2 == 1:
        return True

    return False

largest_rect = None
for i in tqdm.trange(len(points)):
    for j in range(i+1, len(points)):
        p1 = points[i]
        p2 = points[j]

        p3 = Vec2(p1.x, p2.y)
        p4 = Vec2(p2.x, p1.y)

        if test_point(p3) == False or test_point(p4) == False:
            continue

        t1 = Vec2(min(p1.x, p2.x), min(p1.y, p2.y))
        t2 = Vec2(max(p1.x, p2.x), max(p1.y, p2.y))

        bad_square = False
        for p3 in points:
            if p3.x > t1.x and p3.x < t2.x and p3.y > t1.y and p3.y < t2.y:
                bad_square = True
                break

        if bad_square:
            continue

        diff = p2 - p1
        diff = points[j] - points[i]
        area = (abs(diff.x)+1) * (abs(diff.y)+1)
        #print(points[i], points[j], area)
        if largest_rect is None or area > largest_rect[0]:
            largest_rect = (area, (points[i], points[j]))

print(largest_rect)
