#!/usr/bin/env python
"""
FixedPoint objects support decimal arithmetic with a fixed number of
digits (called the object's precision) after the decimal point.  The
number of digits before the decimal point is variable & unbounded.

The precision is user-settable on a per-object basis when a FixedPoint
is constructed, and may vary across FixedPoint objects.  The precision
may also be changed after construction via FixedPoint.set_precision(p).
Note that if the precision of a FixedPoint is reduced via set_precision,
information may be lost to rounding.

>>> x = FixedPoint("5.55")  # precision defaults to 2
>>> print x
5.55
>>> x.set_precision(1)      # round to one fraction digit
>>> print x
5.6
>>> print FixedPoint("5.55", 1)  # same thing setting to 1 in constructor
5.6
>>> repr(x) #  returns constructor string that reproduces object exactly
"FixedPoint('5.6', 1)"
>>>

When FixedPoint objects of different precision are combined via + - * /,
the result is computed to the larger of the inputs' precisions, which also
becomes the precision of the resulting FixedPoint object.

>>> print FixedPoint("3.42") + FixedPoint("100.005", 3)
103.425
>>>

When a FixedPoint is combined with other numeric types (ints, floats,
strings representing a number) via + - * /, then similarly the computation
is carried out using-- and the result inherits --the FixedPoint's
precision.

>>> print FixedPoint(1) / 7
0.14
>>> print FixedPoint(1, 30) / 7
0.142857142857142857142857142857
>>>

The string produced by str(x) (implictly invoked by "print") always
contains at least one digit before the decimal point, followed by a
decimal point, followed by exactly x.get_precision() digits.  If x is
negative, str(x)[0] == "-".

The FixedPoint constructor can be passed an int, long, string, float,
FixedPoint, or any object convertible to a float via float() or to a
long via long().  Passing a precision is optional; if specified, the
precision must be a non-negative int.  There is no inherent limit on
the size of the precision, but if very very large you'll probably run
out of memory.

Note that conversion of floats to FixedPoint can be surprising, and
should be avoided whenever possible.  Conversion from string is exact
(up to final rounding to the requested precision), so is greatly
preferred.

>>> print FixedPoint(1.1e30)
1099999999999999993725589651456.00
>>> print FixedPoint("1.1e30")
1100000000000000000000000000000.00
>>>

The following Python operators and functions accept FixedPoints in the
expected ways:

    binary + - * / % divmod
        with auto-coercion of other types to FixedPoint.
        + - % divmod  of FixedPoints are always exact.
        * / of FixedPoints may lose information to rounding, in
            which case the result is the infinitely precise answer
            rounded to the result's precision.
        divmod(x, y) returns (q, r) where q is a long equal to
            floor(x/y) as if x/y were computed to infinite precision,
            and r is a FixedPoint equal to x - q * y; no information
            is lost.  Note that q has the sign of y, and abs(r) < abs(y).
    unary -
    == != < > <= >=  cmp
    min  max
    float  int  long    (int and long truncate)
    abs
    str  repr
    hash
    use as dict keys
    use as boolean (e.g. "if some_FixedPoint:" -- true iff not zero)

Methods unique to FixedPoints:
   .copy()              return new FixedPoint with same value
   .frac()              long(x) + x.frac() == x
   .get_precision()     return the precision(p) of this FixedPoint object
   .set_precision(p)    set the precision of this FixedPoint object
   
Provided as-is; use at your own risk; no warranty; no promises; enjoy!
"""

# Released to the public domain 28-Mar-2001,
# by Tim Peters (tim.one@home.com).


# 28-Mar-01 ver 0.0,4
#     Use repr() instead of str() inside __str__, because str(long) changed
#     since this was first written (used to produce trailing "L", doesn't
#     now).
#
# 09-May-99 ver 0,0,3
#     Repaired __sub__(FixedPoint, string); was blowing up.
#     Much more careful conversion of float (now best possible).
#     Implemented exact % and divmod.
#
# 14-Oct-98 ver 0,0,2
#     Added int, long, frac.  Beefed up docs.  Removed DECIMAL_POINT
#     and MINUS_SIGN globals to discourage bloating this class instead
#     of writing formatting wrapper classes (or subclasses)
#
# 11-Oct-98 ver 0,0,1
#     posted to c.l.py

__copyright__ = "Copyright (C) Python Software Foundation"
__author__ = "Tim Peters"
__version__ = 0, 1, 0

def bankersRounding(self, dividend, divisor, quotient, remainder):
    """
    rounding via nearest-even
    increment the quotient if
         the remainder is more than half of the divisor
      or the remainder is exactly half the divisor and the quotient is odd
    """
    c = cmp(remainder << 1, divisor)
    # c < 0 <-> remainder < divisor/2, etc
    if c > 0 or (c == 0 and (quotient & 1) == 1):
        quotient += 1
    return quotient

def addHalfAndChop(self, dividend, divisor, quotient, remainder):
    """
    the equivalent of 'add half and chop'
    increment the quotient if
         the remainder is greater than half of the divisor
      or the remainder is exactly half the divisor and the quotient is >= 0
    """
    c = cmp(remainder << 1, divisor)
    # c < 0 <-> remainder < divisor/2, etc
    if c > 0 or (c == 0 and quotient >= 0):
        quotient += 1
    return quotient

# 2002-10-20 dougfort - fake classes for pre 2.2 compatibility
try:
    object
except NameError:
    class object:
        pass
    def property(x, y):
        return None

# The default value for the number of decimal digits carried after the
# decimal point.  This only has effect at compile-time.
DEFAULT_PRECISION = 2

class FixedPoint(object):
    """Basic FixedPoint object class,
        The exact value is self.n / 10**self.p;
        self.n is a long; self.p is an int
    """
    __slots__ = ['n', 'p']
    def __init__(self, value=0, precision=DEFAULT_PRECISION):
        self.n = self.p = 0
        self.set_precision(precision)
        p = self.p

        if isinstance(value, type("42.3e5")):
            n, exp = _string2exact(value)
            # exact value is n*10**exp = n*10**(exp+p)/10**p
            effective_exp = exp + p
            if effective_exp > 0:
                n = n * _tento(effective_exp)
            elif effective_exp < 0:
                n = self._roundquotient(n, _tento(-effective_exp))
            self.n = n
            return

        if isinstance(value, type(42)) or isinstance(value, type(42L)):
            self.n = long(value) * _tento(p)
            return

        if isinstance(value, type(self)):
            temp = value.copy()
            temp.set_precision(p)
            self.n, self.p = temp.n, temp.p
            return

        if isinstance(value, type(42.0)):
            # XXX ignoring infinities and NaNs and overflows for now
            import math
            f, e = math.frexp(abs(value))
            assert f == 0 or 0.5 <= f < 1.0
            # |value| = f * 2**e exactly

            # Suck up CHUNK bits at a time; 28 is enough so that we suck
            # up all bits in 2 iterations for all known binary double-
            # precision formats, and small enough to fit in an int.
            CHUNK = 28
            top = 0L
            # invariant: |value| = (top + f) * 2**e exactly
            while f:
                f = math.ldexp(f, CHUNK)
                digit = int(f)
                assert digit >> CHUNK == 0
                top = (top << CHUNK) | digit
                f = f - digit
                assert 0.0 <= f < 1.0
                e = e - CHUNK

            # now |value| = top * 2**e exactly
            # want n such that n / 10**p = top * 2**e, or
            # n = top * 10**p * 2**e
            top = top * _tento(p)
            if e >= 0:
                n = top << e
            else:
                n = self._roundquotient(top, 1L << -e)
            if value < 0:
                n = -n
            self.n = n
            return

        if isinstance(value, type(42-42j)):
            raise TypeError("can't convert complex to FixedPoint: " +
                            `value`)

        # can we coerce to a float?
        yes = 1
        try:
            asfloat = float(value)
        except:
            yes = 0
        if yes:
            self.__init__(asfloat, p)
            return

        # similarly for long
        yes = 1
        try:
            aslong = long(value)
        except:
            yes = 0
        if yes:
            self.__init__(aslong, p)
            return

        raise TypeError("can't convert to FixedPoint: " + `value`)

    def get_precision(self):
        """Return the precision of this FixedPoint.

           The precision is the number of decimal digits carried after
           the decimal point, and is an int >= 0.
        """

        return self.p

    def set_precision(self, precision=DEFAULT_PRECISION):
        """Change the precision carried by this FixedPoint to p.

           precision must be an int >= 0, and defaults to
           DEFAULT_PRECISION.

           If precision is less than this FixedPoint's current precision,
           information may be lost to rounding.
        """

        try:
            p = int(precision)
        except:
            raise TypeError("precision not convertable to int: " +
                            `precision`)
        if p < 0:
            raise ValueError("precision must be >= 0: " + `precision`)

        if p > self.p:
            self.n = self.n * _tento(p - self.p)
        elif p < self.p:
            self.n = self._roundquotient(self.n, _tento(self.p - p))
        self.p = p

    precision = property(get_precision, set_precision)

    def __str__(self):
        n, p = self.n, self.p
        i, f = divmod(abs(n), _tento(p))
        if p:
            frac = repr(f)[:-1]
            frac = "0" * (p - len(frac)) + frac
        else:
            frac = ""
        return "-"[:n<0] + \
               repr(i)[:-1] + \
               "." + frac

    def __repr__(self):
        return "FixedPoint" + `(str(self), self.p)`

    def copy(self):
        return _mkFP(self.n, self.p, type(self))

    __copy__ = copy

    def __deepcopy__(self, memo):
        return self.copy()

    def __cmp__(self, other):
        xn, yn, p = _norm(self, other, FixedPoint=type(self))
        return cmp(xn, yn)

    def __hash__(self):
        """ Caution!  == values must have equal hashes, and a FixedPoint
            is essentially a rational in unnormalized form.  There's
            really no choice here but to normalize it, so hash is
            potentially expensive.
            n, p = self.__reduce()

            Obscurity: if the value is an exact integer, p will be 0 now,
            so the hash expression reduces to hash(n).  So FixedPoints
            that happen to be exact integers hash to the same things as
            their int or long equivalents.  This is Good.  But if a
            FixedPoint happens to have a value exactly representable as
            a float, their hashes may differ.  This is a teensy bit Bad.
        """
        n, p = self.__reduce()
        return hash(n) ^ hash(p)

    def __nonzero__(self):
        """ Returns true if this FixedPoint is not equal to zero"""
        return self.n != 0

    def __neg__(self):
        return _mkFP(-self.n, self.p, type(self))

    def __abs__(self):
        """ Returns new FixedPoint containing the absolute value of this FixedPoint"""
        if self.n >= 0:
            return self.copy()
        else:
            return -self

    def __add__(self, other):
        n1, n2, p = _norm(self, other, FixedPoint=type(self))
        # n1/10**p + n2/10**p = (n1+n2)/10**p
        return _mkFP(n1 + n2, p, type(self))

    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            other = type(self)(other, self.p)
        return self.__add__(-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        n1, n2, p = _norm(self, other, FixedPoint=type(self))
        # n1/10**p * n2/10**p = (n1*n2/10**p)/10**p
        return _mkFP(self._roundquotient(n1 * n2, _tento(p)), p, type(self))

    __rmul__ = __mul__

    def __div__(self, other):
        n1, n2, p = _norm(self, other, FixedPoint=type(self))
        if n2 == 0:
            raise ZeroDivisionError("FixedPoint division")
        if n2 < 0:
            n1, n2 = -n1, -n2
        # n1/10**p / (n2/10**p) = n1/n2 = (n1*10**p/n2)/10**p
        return _mkFP(self._roundquotient(n1 * _tento(p), n2), p, type(self))

    def __rdiv__(self, other):
        n1, n2, p = _norm(self, other, FixedPoint=type(self))
        return _mkFP(n2, p, FixedPoint=type(self)) / self

    def __divmod__(self, other):
        n1, n2, p = _norm(self, other, FixedPoint=type(self))
        if n2 == 0:
            raise ZeroDivisionError("FixedPoint modulo")
        # floor((n1/10**p)/(n2*10**p)) = floor(n1/n2)
        q = n1 / n2
        # n1/10**p - q * n2/10**p = (n1 - q * n2)/10**p
        return q, _mkFP(n1 - q * n2, p, type(self))

    def __rdivmod__(self, other):
        n1, n2, p = _norm(self, other, FixedPoint=type(self))
        return divmod(_mkFP(n2, p), self)

    def __mod__(self, other):
        return self.__divmod__(other)[1]

    def __rmod__(self, other):
        n1, n2, p = _norm(self, other, FixedPoint=type(self))
        return _mkFP(n2, p, type(self)).__mod__(self)

    def __float__(self):
        """Return the floating point representation of this FixedPoint. 
            Caution! float can lose precision.
        """
        n, p = self.__reduce()
        return float(n) / float(_tento(p))

    def __long__(self):
        """EJG/DF - Should this round instead?
            Note e.g. long(-1.9) == -1L and long(1.9) == 1L in Python
            Note that __int__ inherits whatever __long__ does,
                 and .frac() is affected too
        """
        answer = abs(self.n) / _tento(self.p)
        if self.n < 0:
            answer = -answer
        return answer

    def __int__(self):
        """Return integer value of FixedPoint object."""
        return int(self.__long__())
    
    def frac(self):
        """Return fractional portion as a FixedPoint.

           x.frac() + long(x) == x
        """
        return self - long(self)

    def _roundquotient(self, x, y):
        """
        Divide x by y,
        return the result of rounding
        Developers may substitute their own 'round' for custom rounding
        y must be > 0
        """
        assert y > 0
        n, leftover = divmod(x, y)
        return self.round(x, y, n, leftover)

    def __reduce(self):
        """ Return n, p s.t. self == n/10**p and n % 10 != 0"""
        n, p = self.n, self.p
        if n == 0:
            p = 0
        while p and n % 10 == 0:
            p = p - 1
            n = n / 10
        return n, p

# 2002-10-04 dougfort - Default to Banker's Rounding for backward compatibility
FixedPoint.round = bankersRounding

# return 10L**n

def _tento(n, cache={}):
    """Cached computation of 10**n"""
    try:
        return cache[n]
    except KeyError:
        answer = cache[n] = 10L ** n
        return answer

def _norm(x, y, isinstance=isinstance, FixedPoint=FixedPoint,
                _tento=_tento):
    """Return xn, yn, p s.t.
           p = max(x.p, y.p)
           x = xn / 10**p
           y = yn / 10**p

        x must be FixedPoint to begin with; if y is not FixedPoint,
        it inherits its precision from x.

        Note that this method is called a lot, so default-arg tricks are helpful.
    """
    assert isinstance(x, FixedPoint)
    if not isinstance(y, FixedPoint):
        y = FixedPoint(y, x.p)
    xn, yn = x.n, y.n
    xp, yp = x.p, y.p
    if xp > yp:
        yn = yn * _tento(xp - yp)
        p = xp
    elif xp < yp:
        xn = xn * _tento(yp - xp)
        p = yp
    else:
        p = xp  # same as yp
    return xn, yn, p

def _mkFP(n, p, FixedPoint=FixedPoint):
    """Make FixedPoint objext - Return a new FixedPoint object with the selected precision."""
    f = FixedPoint()
    #print '_mkFP Debug: %s, value=%s' % (type(f),n)
    f.n = n
    f.p = p
    return f

# crud for parsing strings
import re

# There's an optional sign at the start, and an optional exponent
# at the end.  The exponent has an optional sign and at least one
# digit.  In between, must have either at least one digit followed
# by an optional fraction, or a decimal point followed by at least
# one digit.  Yuck.

_parser = re.compile(r"""
    \s*
    (?P<sign>[-+])?
    (
        (?P<int>\d+) (\. (?P<frac>\d*))?
    |
        \. (?P<onlyfrac>\d+)
    )
    ([eE](?P<exp>[-+]? \d+))?
    \s* $
""", re.VERBOSE).match

del re


def _string2exact(s):
    """Return n, p s.t. float string value == n * 10**p exactly."""
    m = _parser(s)
    if m is None:
        raise ValueError("can't parse as number: " + `s`)

    exp = m.group('exp')
    if exp is None:
        exp = 0
    else:
        exp = int(exp)

    intpart = m.group('int')
    if intpart is None:
        intpart = "0"
        fracpart = m.group('onlyfrac')
    else:
        fracpart = m.group('frac')
        if fracpart is None or fracpart == "":
            fracpart = "0"
    assert intpart
    assert fracpart

    i, f = long(intpart), long(fracpart)
    nfrac = len(fracpart)
    i = i * _tento(nfrac) + f
    exp = exp - nfrac

    if m.group('sign') == "-":
        i = -i

    return i, exp

def _test():
    """Unit testing framework"""
    fp = FixedPoint
    o = fp("0.1")
    assert str(o) == "0.10"
    t = fp("-20e-2", 5)
    assert str(t) == "-0.20000"
    assert t < o
    assert o > t
    assert min(o, t) == min(t, o) == t
    assert max(o, t) == max(t, o) == o
    assert o != t
    assert --t == t
    assert abs(t) > abs(o)
    assert abs(o) < abs(t)
    assert o == o and t == t
    assert t.copy() == t
    assert o == -t/2 == -.5 * t
    assert abs(t) == o + o
    assert abs(o) == o
    assert o/t == -0.5
    assert -(t/o) == (-t)/o == t/-o == 2
    assert 1 + o == o + 1 == fp(" +00.000011e+5  ")
    assert 1/o == 10
    assert o + t == t + o == -o
    assert 2.0 * t == t * 2 == "2" * t == o/o * 2L * t
    assert 1 - t == -(t - 1) == fp(6L)/5
    assert t*t == 4*o*o == o*4*o == o*o*4
    assert fp(2) - "1" == 1
    assert float(-1/t) == 5.0
    for p in range(20):
        assert 42 + fp("1e-20", p) - 42 == 0
    assert 1/(42 + fp("1e-20", 20) - 42) == fp("100.0E18")
    o = fp(".9995", 4)
    assert 1 - o == fp("5e-4", 10)
    o.set_precision(3)
    assert o == 1
    o = fp(".9985", 4)
    o.set_precision(3)
    assert o == fp(".998", 10)
    assert o == o.frac()
    o.set_precision(100)
    assert o == fp(".998", 10)
    o.set_precision(2)
    assert o == 1
    x = fp(1.99)
    assert long(x) == -long(-x) == 1L
    assert int(x) == -int(-x) == 1
    assert x == long(x) + x.frac()
    assert -x == long(-x) + (-x).frac()
    assert fp(7) % 4 == 7 % fp(4) == 3
    assert fp(-7) % 4 == -7 % fp(4) == 1
    assert fp(-7) % -4 == -7 % fp(-4) == -3
    assert fp(7.0) % "-4.0" == 7 % fp(-4) == -1
    assert fp("5.5") % fp("1.1") == fp("5.5e100") % fp("1.1e100") == 0
    assert divmod(fp("1e100"), 3) == (long(fp("1e100")/3), 1)

if __name__ == '__main__':
    _test()

