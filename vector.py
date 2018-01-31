
class Vector(object):
    """
    """

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.coordinates, other.coordinates)])

    def __iadd__(self, other):
        self.coordinates = [a + b for a, b in zip(self.coordinates, other.coordinates)]
        return self

    def mulScalar(self, n):
        self.coordinates = [n*x for x in self.coordinates]
        return self

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.coordinates, other.coordinates)])

    def __isub__(self, other):
        self.coordinates = [a - b for a, b in zip(self.coordinates, other.coordinates)]
        return self


print(Vector([8.218, -9.341]) + Vector([-1.129, 2.111]))

print(Vector([7.119, 8.215]) - Vector([-8.223, 0.878]))

print(Vector([1.671, -1.012, -0.318]).mulScalar(7.41))
