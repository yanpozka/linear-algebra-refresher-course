from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):
    """
    """

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def _validate_dimension(self, other):
        if self.dimension != other.dimension:
            raise ValueError('Vector dimensions must match')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, other):
        self._validate_dimension(other)
        return Vector([a + b for a, b in zip(self.coordinates, other.coordinates)])

    def __iadd__(self, other):
        self._validate_dimension(other)
        self.coordinates = [a + b for a, b in zip(self.coordinates, other.coordinates)]
        return self

    def __sub__(self, other):
        self._validate_dimension(other)
        return Vector([a - b for a, b in zip(self.coordinates, other.coordinates)])

    def __isub__(self, other):
        self._validate_dimension(other)
        self.coordinates = [a - b for a, b in zip(self.coordinates, other.coordinates)]
        return self

    def mul_scalar(self, n):
        return Vector([Decimal(n)*x for x in self.coordinates])

    def magnitude(self):
        return sqrt(sum([n*n for n in self.coordinates]))

    def normalized(self):
        return self.mul_scalar(Decimal('1.0')/Decimal(self.magnitude()))

    def dot(self, other):
        return sum([a * b for a, b in zip(self.coordinates, other.coordinates)])

    def angle(self, other, in_degrees=False):
        if self.is_zero() or other.is_zero():
            raise Exception('Cannot compute an angle with the zero vector')

        dr = self.normalized().dot(other.normalized())
        angle_rad = acos(min(1.0, max(dr, -1.0)))

        if in_degrees:
            return angle_rad * (180. / pi)
        return angle_rad

    def is_orthogonal_to(self, other, tolerance=1e-10):
        return abs(self.dot(other)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_parallel_to(self, other):
        return self.is_zero() or other.is_zero() or self.angle(other) == 0.0 or self.angle(other) == pi

    def cross(self, other):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = other.coordinates
            new_coordinates = [y_1*z_2 - y_2*z_1,
                               -(x_1*z_2 - x_2*z_1),
                               x_1*y_2 - x_2*y_1]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_emb_in_R3 = Vector(self.coordinates + ('0',))
                other_emb_in_R3 = Vector(other.coordinates + ('0',))
                return self_emb_in_R3.cross(other_emb_in_R3)
            else:
                raise e

    def area_parallelogram_with(self, other):
        cross_product = self.cross(other)
        return cross_product.magnitude()

    def area_triangle_with(self, other):
        return Decimal(self.area_parallelogram_with(other)) / Decimal('2.0')



# add, sub, scalar multiplication
print(Vector([8.218, -9.341]) + Vector([-1.129, 2.111]))
print(Vector([7.119, 8.215]) - Vector([-8.223, 0.878]))
print(Vector([1.671, -1.012, -0.318]).mul_scalar(7.41))

# magnitude & direciton
print("magnitude & direciton")
print("%.3f" % Vector([-0.221, 7.437]).magnitude())
print("%.3f" % Vector([8.813, -1.331, -6.247]).magnitude())
print(Vector([-1, 1, 1]).normalized())
print(Vector([5.581, -2.136]).normalized())
print(Vector([1.996, 3.108, -4.554]).normalized())

# inner product
print("inner(dot) product")
print(Vector([1, 2, -1]).dot(Vector([3, 1, 0])))
print(Vector([1, 2, -1]).angle(Vector([3, 1, 0])))

print("%.3f" % Vector([7.887, 4.138]).dot(Vector([-8.802, 6.776])))
print("%.3f" % Vector([-5.955, -4.904, -1.874]).dot(Vector([-4.496, -8.755, 7.103])))

print("%.3f" % Vector([3.183, -7.627]).angle(Vector([-2.668, 5.319])))
print("%.3f" % Vector([7.35, 0.221, 5.188]).angle(Vector([2.751, 8.259, 3.985]), in_degrees=True))

# parallel & orthogonal:
print("parallel & orthogonal")
print(Vector([-7.579, -7.88]).is_parallel_to(Vector([22.737, 23.64])))
print(Vector([-7.579, -7.88]).is_orthogonal_to(Vector([22.737, 23.64])))
print("")
print(Vector([-2.029, 9.97, 4.172]).is_parallel_to(Vector([-9.231, -6.6639, -7.245])))
print(Vector([-2.029, 9.97, 4.172]).is_orthogonal_to(Vector([-9.231, -6.6639, -7.245])))
print("")
print(Vector([-2.328, -7.284, -1.214]).is_parallel_to(Vector([-1.821, 1.072, -2.94])))
print(Vector([-2.328, -7.284, -1.214]).is_orthogonal_to(Vector([-1.821, 1.072, -2.94])))
print("")
print(Vector([2.118, 4.827]).is_parallel_to(Vector([0, 0])))
print(Vector([2.118, 4.827]).is_orthogonal_to(Vector([0, 0])))

# cross products
print("cross products")
v = Vector([8.462, 7.893, -8.187])
w = Vector([6.984, -5.975, 4.778])
print(v.cross(w))

v = Vector([-8.987, -9.838, 5.031])
w = Vector([-4.268, -1.861, -8.866])
print(v.area_parallelogram_with(w))

v = Vector([1.5, 9.547, 3.691])
w = Vector([-6.007, 0.124, 5.772])
print(v.area_triangle_with(w))
