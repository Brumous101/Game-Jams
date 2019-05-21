import math

class Vector(object):
    """ This class represents a general-purpose vector class.  We'll
        add more to this in later labs.  For now, it represents a
        position and/or offset in n-dimensonal space. """

    def __init__(self, *args):
        """
        The constructor
        :param args: This is a variable-length argument-list.  In reality, you create a Vector like this:
               v = Vector(1, 2, 3)
        :return: N/A for constructors
        """
        self.mData = []
        for value in args:
            self.mData.append(float(value))
        self.mDim = len(args)

        # This is a little bit ugly, but if the user passes us one of the "special" number of elements in args,
        # use the specialized class.  For example, if there are 2 elements in args, make this new instance a Vector2 instead
        # of a generic Vector object.
        if len(args) == 2:
            self.__class__ = Vector2
        elif len(args) == 3:
            self.__class__ = Vector3

    def __str__(self):
        """
        Note: You don't normally call this directly.  It is called indirectly when you do something like:
            v = Vector(1, 2, 3)
            x = str(v)               # Same as x = v.__str__()
            print(v)                 # print calls str internally
        :return: The string-representation of this Vector
        """
        s = "<Vector" + str(len(self)) + ": "
        for i in range(len(self.mData)):
            s += str(self.mData[i])
            if i < len(self) - 1:
                s += ", "
        s += ">"
        return s

    def __len__(self):
        """
        Note: You don't normally call this method directly.  It's called by the built-in len function
            v = Vector(1, 2, 4)
            print(len(v))           # 3
        :return: An integer indicating the dimension of this vector
        """
        return self.mDim

    def __getitem__(self, index):
        """
        Note: You don't normally call this method directly.  It's called by using [] on a Vector
            v = Vector(1, 2, 3)
            print(v[0])                 # 1
            print(v[-1])                # 3
        :param index: An integer.  A python exception will be thrown if it's not a valid position in self.mData
        :return: The float value at position index.
        """
        return self.mData[index]

    def __setitem__(self, index, newval):
        """
        This method is similar to __getitem__, but it is called when we assign something to an index
           v = Vector(1, 2, 3)
           v[0] = 99
           print(v)                 # <Vector3: 1.0, 2.0, 99.0>
        :param index: An integer.  A python exception will be thrown if it's not a valid position in self.mData
        :param newval: A value that can be converted to a float using the float function
        :return: None
        """
        self.mData[index] = float(newval)

    def __eq__(self, other):
        """
        Note: This method isn't normally called directly.  Instead, it is called indirectly when a Vector
              is on the left-hand side of an ==.  It returns True if the values within the other vector
              are the same as those in this vector.
        :param other: any value
        :return: a boolean.  True if the other thing is a Vector *and* has the same values as this Vector.
        """
        if isinstance(other, Vector) and len(self) == len(other):
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
            return True
        else:
            return False
        
        
    def __add__(self, otherV):
        """
        Adds this vector to the other vector (on the right-hand side of the '+' operator), producing a new vector
        :param otherV: A Vector of the same size as this vectorN
        :return: The Vector sum (of the same type as the left-hand side of the '+' operator)
        """
        if not isinstance(otherV, Vector) or len(otherV) != len(self):
            n = str(len(self))
            raise ValueError("You can only add another Vector" + n + " to this Vector" + n + " (you passed '" + str(otherV) + "')")
        r = self.copy()
        for i in range(self.mDim):
            r[i] += otherV[i]
        return r


    def __sub__(self, otherV):
        """
        Subtracts the other vector (on the right-hand side of the '+' operator) from this vector, producing a new vector
        :param otherV: A Vector of the same size as this vectorN
        :return: The Vector sum (of the same type as this object)
        """
        if not isinstance(otherV, Vector) or len(otherV) != len(self):
            n = str(len(self))
            raise ValueError("You can only add another Vector" + n + " to this Vector" + n + " (you passed '" + str(otherV) + "')")
        r = self.copy()
        for i in range(self.mDim):
            r[i] -= otherV[i]
        return r


    def __mul__(self, scalar):
        """
        Multiplies this vector with a scalar.
        :param scalar: the value to multiply this vector by (integer or float)
        :return: a copy of this vector with all values multiplied by the scalar
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.mDim)
            raise TypeError("You can only multiply this " + n + " and a scalar. You attempted to multiply by '" + str(scalar) + "'")
        r = self.copy()
        for i in range(self.mDim):
            r[i] *= scalar
        return r


    def __rmul__(self, scalar):
        """
        This performs vector-scalar multiplication (like __mul__).  This method is necessary, though, in the
        case in which the scalar is on the left hand side of the '*' (rather than the right-hand side in the __mul__
        method.
        :param scalar: the value to multiply this vector by (integer or float)
        :return: a copy of this vector with all values multiplied by the scalar
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.mDim)
            raise TypeError("You can only multiply this " + n + " and a scalar. You attempted to multiply by '" + str(scalar) + "'")
        r = self.copy()
        for i in range(self.mDim):
            r[i] *= scalar
        return r



    def __truediv__(self, scalar):
        """
        Returns a copy of this vector divided by the given scalar
        :param scalar: the value to multiply this vector by (integer or float)
        :return: a copy of this vector with all values multiplied by the scalar
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.mDim)
            raise TypeError("You can only divide this " + n + " by a scalar. You attempted to divide by '" + str(scalar) + "'")
        r = self.copy()
        for i in range(self.mDim):
            r[i] /= scalar
        return r



    def __neg__(self):
        """
        :return: A negated copy of this vector
        """
        r = self.copy()
        for i in range(self.mDim):
            r[i] = -r[i]
        return r



    @property
    def magnitude(self):
        """
        :return: The scalar magnitude of this vector
        """
        m = 0.0
        for val in self.mData:
            m += val ** 2
        return m ** 0.5


    @property
    def magnitudeSquared(self):
        """
        :return: The magnitude of this vector squared.  Wherever possible, use this method rather than
                 magnitude as this method doesn't involve a square root (which is costly to compute)
        """
        m = 0.0
        for val in self.mData:
            m += val ** 2
        return m


    @property
    def normalized(self):
        """
        :return: A normalized copy of this vector.   If this vector is a zero vector, a copy is returned.
        """
        if self.isZero:
            return self.copy()         # We can't actually normalize a zero-vector, but instead of crashing, let's just
                                       # return self (a zero vector)
        r = self.copy()
        mag = self.magnitude
        if mag == 0.0:
            return r
        for i in range(self.mDim):
            r[i] /= mag
        return r


    @property
    def isZero(self):
        """
        :return: True if this vector is a zero-vector.
        """
        for val in self.mData:
            if val != 0.0:
                return False
        return True


    def copy(self):
        """
        Creates a 'deep' copy of this Vector and returns it
        :return: a new Vector copy of this Vector
        """
        v = Vector(*self.mData)
        # This makes sure the copy is of the same type as the original (this is especially important if self
        # is a specialized vector class like Vector2.
        v.__class__ = self.__class__
        return v


    @property
    def i(self):
        """
        :return: A tuple containing all elements of this Vector, converted to integers
        """
        L = []
        for val in self.mData:
            L.append(int(val))
        return tuple(L)





class Vector2(Vector):
    """ This is a specialization of Vector.  This will mainly be used for 2d applications and makes
        accessing the components (by name) a little easier as well as adding some polar conversion properties """
    def __init__(self, x, y):
        # Feed these elements to the base-class constructor
        super().__init__(x, y)

    @property
    def x(self):
        return self.mData[0]

    @x.setter
    def x(self, new_val):
        self.mData[0] = float(new_val)

    @property
    def y(self):
        return self.mData[1]

    @y.setter
    def y(self, new_val):
        self.mData[1] = float(new_val)

    @property
    def degrees(self):
        return math.degrees(math.atan2(self.mData[1], self.mData[0]))

    @property
    def degrees_inv(self):
        return math.degrees(math.atan2(-self.mData[1], self.mData[0]))

    @property
    def radians(self):
        return math.atan2(self.mData[1], self.mData[0])

    @property
    def radians_inv(self):
        return math.atan2(-self.mData[1], self.mData[0])

    @property
    def perpendicular(self):
        return Vector2(-self.y, self.x)





class Vector3(Vector):
    """ This is a specialization of Vector.  This will mainly be used for 3d applications and makes
            accessing the components (by name) a little easier """
    def __init__(self, x, y, z):
        # Feed these elements to the base-class constructor
        super().__init__(x, y, z)

    @property
    def x(self):
        return self.mData[0]

    @x.setter
    def x(self, new_val):
        self.mData[0] = float(new_val)

    @property
    def y(self):
        return self.mData[1]

    @y.setter
    def y(self, new_val):
        self.mData[1] = float(new_val)

    @property
    def z(self):
        return self.mData[2]

    @z.setter
    def z(self, new_val):
        self.mData[2] = float(new_val)



def polar_to_vector2(radians, hypotenuse, invert_y = True):
    if invert_y:
        return Vector2(hypotenuse * math.cos(radians), -hypotenuse * math.sin(radians))
    else:
        return Vector2(hypotenuse * math.cos(radians), hypotenuse * math.sin(radians))


def dot(vector1,vector2):
    dot_product = 0
    if len(vector1) == len(vector2):
        for i in range(len(vector1)):
            dot_product += vector1[i] * vector2[i]
        return dot_product
    else:
        raise TypeError("Error. Vectors do not equal in length!")

def cross(vector1,vector2):
    if isinstance(vector1,Vector3) and isinstance(vector2, Vector3):
        vector3 = Vector3(vector1[1] * vector2[2] - vector1[2] * vector2[1],
                      vector1[2] * vector2[0] - vector1[0] * vector2[2],
                      vector1[0] * vector2[1] - vector1[1] * vector2[0])
    else:
        raise TypeError("Both vectors have to be Vector 3s!")
    return vector3



