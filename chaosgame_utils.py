import math
import random
import itertools
import decimal
from decimal import Decimal

decimal.getcontext().prec = 5

def round_dec(n):
    return float(Decimal(n))

def euc_dist(point1:tuple, point2:tuple) -> tuple:
    return round_dec(math.sqrt((point2[1] - point1[1])**2 + (point2[0] - point1[0])**2))

def get_random_point(min_x, max_x, min_y, max_y):
    return random.randint(math.ceil(min_x), math.floor(max_x)), random.randint(math.ceil(min_y), math.floor(max_y))

def midpoint(point1:tuple, point2:tuple) -> tuple:
    return ((point1[0] + point2[0])/2, (point1[1] + point2[1])/2)

def inter_point(point1:tuple, point2:tuple, jump_factor:float) -> tuple:
    '''
    NOTE: Point returned has integer coordinates. Coordinates are coerced
    to int for rendering as pixel locations.
    '''
    return (int((point1[0] + point2[0]) * jump_factor), int((point1[1] + point2[1]) * jump_factor))

def gamma(a:float, b:float, c:float):
    '''
    Returns angle given three points using law of cosines.
    '''
    return round_dec(math.degrees(math.acos( (a**2 + b**2 - c**2) / (2 * a * b) )))

def is_contained(polygon:tuple, test_point:tuple) -> bool:
    '''
    '''
    dists_to_point = [euc_dist(vertex, test_point) for vertex in polygon]
    # edge_length = euc_dist(polygon[0], polygon[1])
    edge_lengths = [euc_dist(v1, v2) for v1, v2 in itertools.pairwise(polygon)]
    # Include first item at the end for the last combination
    inner_edge_pairs = itertools.pairwise(dists_to_point + [dists_to_point[0]])
    # inner_triangles = [pair + (edge_length,) for pair in inner_edge_pairs]
    inner_triangles = [pair + (edge_length,) for pair in inner_edge_pairs for edge_length in edge_lengths]

    sum_of_angles = sum([gamma(p[0], p[1], p[2]) for p in inner_triangles])

    if sum_of_angles == (len(polygon) - 1) * 360:
        return True
    return False

def polygon_from_center(center:tuple, radius:int, num_vertices:int) -> tuple:
    '''
    Assume polygon is equilateral.

    Given a center and a radius, and assuming the baseline of the polygon is
    parallel to the x-axis, we can easily compute the "top" point of the
    polygon. This is simply (cx, cy+r), where cx and cy are the coordinates
    of the center point. (Effectively we're just drawing a straight line of
    length r up from the center point.)

    To compute the other two points of the polygon, we can use trigonometry
    to compute the center point of the baseline of the polygon, then compute
    the length of the baseline, and finally determine points out to the left
    and right from that center baseline point by respectively adding and
    subtracting half the length of the baseline tothe x-coord of the center
    baseline point.

    Returns polygon coordinates, wherein the first point is 0 degrees relative
    to the center, the second 360/N degrees from center, and so on.
    '''

    # Alias math.radians for using trig functions, which assume values are
    # in radians
    rad = math.radians

    alpha = 360 / num_vertices

    x_part = lambda i: radius * math.cos(rad(i * alpha))
    y_part = lambda i: radius * math.sin(rad(i * alpha))

    return [(round_dec(center[0] + x_part(i)), round_dec(center[1] + y_part(i))) for i in range(num_vertices)]

