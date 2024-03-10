from pygame import Vector2

from entities.entity import Entity


def isOnLineSegment(pt1: Vector2, pt2: Vector2, pt3: Vector2):
    if pt3.x <= max(pt1.x, pt2.x) and pt3.x >= min(pt1.x, pt2.x) and pt3.y <= max(pt1.y, pt2.y) and pt3.y >= min(pt1.y, pt2.y):
        return True
    return False


def orientation(pt1: Vector2, pt2: Vector2, pt3: Vector2):
    val = (pt2.x - pt1.x) * (pt3.y - pt1.y) - \
        (pt3.x - pt1.x) * (pt2.y - pt1.y)
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0


def findClosestPointOnLine(pt1: Vector2, pt2: Vector2, pos: Vector2):
    v = pt2 - pt1

    a = pos - pt1

    t = a.dot(v)

    t = t / v.length_squared()

    if t < 0:
        return pt1
    elif t > 1:
        return pt2

    return pt1 + v*t


def findClosestPointOnPolygon(points: list[Vector2], pos: Vector2):
    nearest_pt = Vector2(0, 0)
    line_idx: list[int, int] = (-1, -1)

    mi_dst = 1000000000000

    for i in range(0, len(points)):
        pt = findClosestPointOnLine(
            points[i], points[(i+1) % len(points)], pos)

        dst = (pt - pos).length_squared()

        if dst < mi_dst:
            mi_dst = dst
            nearest_pt = pt
            line_idx = (i, (i+1) % len(points))

    return nearest_pt, line_idx


def isPointInsidePolygon(points: list[Vector2], pos: Vector2):
    cnt = len(points)
    p1 = pos
    p2 = Vector2(1000000000, 1000000000)

    intersectCnt = 0
    for i in range(cnt):
        p3 = points[i]
        p4 = points[(i+1) % cnt]

        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        if o1 != o2 and o3 != o4:
            intersectCnt += 1
            continue

        if o1 == 0 and isOnLineSegment(p1, p2, p3):
            intersectCnt += 1
            continue

        if o2 == 0 and isOnLineSegment(p1, p2, p4):
            intersectCnt += 1
            continue

        if o3 == 0 and isOnLineSegment(p3, p4, p1):
            intersectCnt += 1
            continue

        if o4 == 0 and isOnLineSegment(p3, p4, p2):
            intersectCnt += 1
            continue

    return intersectCnt % 2 == 1
