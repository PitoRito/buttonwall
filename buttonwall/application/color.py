''' Reuse Color classes from main project '''

class Color(object):
    '''
    Basic color object
    '''
    def __init__(self, r=0, g=0, b=0, i=1):
        '''
        :param float r: Red part
        :param float g: Green part
        :param float b: Blue part
        :param float i: Intensity
        '''
        self.red = r
        self.green = g
        self.blue = b
        self.i = i

    @property
    def r(self):
        '''
        '''
        return max(min(self.red * self.i, 1), 0)

    @property
    def g(self):
        '''
        '''
        return max(min(self.green * self.i, 1), 0)

    @property
    def b(self):
        '''

        '''
        return max(min(self.blue * self.i, 1), 0)

    @property
    def intensity(self):
        return 0.2126 * self.r + 0.7152 * self.g + 0.0722 * self.b

    def normalize(self, intensity):
        if self.intensity == 0:
            return ColorNone()

        k = min(intensity / self.intensity, 1)
        return Color(
            r=self.r,
            g=self.g,
            b=self.b,
            i=k
        )

    def get_i(self, i):
        '''
        '''
        return Color(
            r=self.r,
            g=self.g,
            b=self.b,
            i=i
        )

    def pwm(self, duration):
        '''
        '''
        return [
            int(255 * self.r), int(255 * self.g),
            int(255 * self.b), int(duration)
        ]

    @property
    def sdl(self):
        '''
        '''
        return (
            int(255 * self.r),
            int(255 * self.g),
            int(255 * self.b),
        )

    def invert(self):
        '''
        '''
        red = 1 - self.r
        green = 1 - self.g
        blue = 1 - self.b

        if red > 0.4 and red < 0.6:
            red = 0

        if green > 0.4 and green < 0.6:
            green = 0

        if blue > 0.4 and blue < 0.6:
            blue = 0

        return Color(red, green, blue, i=1)

    def html(self):
        return '#%02x%02x%02x' % (
            int(self.r * 255),
            int(self.g * 255),
            int(self.b * 255),
        )

    def list(self):
        '''
        '''
        return [self.r, self.g, self.b]

    def __str__(self):
        '''
        '''
        return "<color (%d, %d, %d)>" % (self.r, self.g, self.b)


class ColorNone(Color):
    def __init__(self):
        super(ColorNone, self).__init__(0, 0, 0, 0)


class ColorWhite(Color):
    def __init__(self, i=1):
        super(ColorWhite, self).__init__(1, 1, 1, i=i)


class ColorRed(Color):
    def __init__(self, i=1):
        super(ColorRed, self).__init__(1, 0, 0, i=i)


class ColorGreen(Color):
    def __init__(self, i=1):
        super(ColorGreen, self).__init__(0, 1, 0, i=i)


class ColorBlue(Color):
    def __init__(self, i=1):
        super(ColorBlue, self).__init__(0, 0, 1, i=i)


class ColorPurple(Color):
    def __init__(self, i=1):
        super(ColorPurple, self).__init__(1, 0, 1, i=i)
