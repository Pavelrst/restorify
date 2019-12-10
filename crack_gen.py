from PIL import Image
import numpy as np
from random import randint
from random import choice

class Point():
    def __init__(self, updown, leftright):
        self.updown = updown
        self.leftright = leftright

kernels = (
    np.array([[0.5, 0.7, 0.5],
     [0.7, 1  , 0.7],
     [0.7, 0.7, 0.5]]),

    np.array([[0.1, 0.3, 0.7, 0.3, 0.1],
     [0.3, 0.7, 0.8, 0.7, 0.3],
     [0.7, 0.8, 1  , 0.8, 0.7],
     [0.3, 0.7, 0.8, 0.7, 0.3],
     [0.1, 0.3, 0.7, 0.3, 0.1]]),

    np.array([[0  , 0  , 0.1, 0.3, 0.1, 0  , 0  ],
     [0  , 0.1, 0.3, 0.7, 0.3, 0.1, 0  ],
     [0.1, 0.3, 0.7, 0.9, 0.7, 0.3, 0.1],
     [0.3, 0.7, 0.9, 1  , 0.9, 0.7, 0.3],
     [0.1, 0.3, 0.7, 0.9, 0.7, 0.3, 0.1],
     [0  , 0.1, 0.3, 0.7, 0.3, 0.1, 0  ],
     [0  , 0  , 0.1, 0.3, 0.1, 0  , 0  ]])
)

class crackGenerator():
    def __init__(self, target_image=None):
        # TODO change all height to width and vise versa.
        self.width = 1000
        self.heigh = 1500
        self.image = np.zeros((self.heigh, self.width))
        self.max_iter = 10000
        self.crack_path = []


    def show_mask(self):
        image = Image.fromarray(self.image).convert("RGBA")

        for point in self.crack_path:
            if self._legal_point(point):
                # self.mask[point[0]][point[1]] = randint(150, 250)
                kernelarr = kernels[randint(0, len(kernels)-1)] * randint(170, 250)#np.ones((randint(2, 5), randint(2, 5))) * randint(170, 250)
                kernel = Image.fromarray(kernelarr).convert("RGBA")
                # x, y transposed for some reason
                image.paste(kernel, (point.leftright, point.updown), mask=kernel)

        image.show()

    def maybe_init_direction(self):
        rand = randint(0, 500)
        # init crack direction
        if rand == 13:
            self.init_direction()

    def init_direction(self):
        (self.updown_low, self.updown_high) = choice(((-2, -1), (-1, 0), (0, 1), (1, 2), (-1, 1)))
        (self.leftright_low, self.leftright_high) = choice(((-2, -1), (-1, 0), (0, 1), (1, 2), (-1, 1)))


    def generate_crack(self):
        self.init_direction()

        # randomly select starting point
        next_point = Point(updown=randint(0, self.heigh), leftright=randint(0, self.width))
        if len(self.crack_path) != 0:
            next_point2 = self.crack_path[randint(0, len(self.crack_path)-1)]
            next_point = choice((next_point, next_point2))

        self.crack_path.append(next_point)

        iter = 0
        while(self._legal_point(next_point) and iter<self.max_iter):
            next_point = self._next_point(next_point)
            # self.maybe_init_direction()
            if self._legal_point(next_point):
                self.crack_path.append(next_point)
            iter += 1


    def _legal_point(self, point):
        if self._legal_width(point.leftright) and self._legal_height(point.updown):
            return True
        else:
            return False

    def _legal_height(self, val):
        if (val >= 0 and val < self.heigh):
            return True
        else:
            return False

    def _legal_width(self, val):
        if (val >= 0 and val < self.width):
            return True
        else:
            return False

    def _next_point(self, curr_point):
        updown_dir = randint(self.updown_low, self.updown_high)
        leftright_dir = randint(self.leftright_low, self.leftright_high)
        return Point(curr_point.updown + updown_dir, curr_point.leftright + leftright_dir)



def test():
    gen = crackGenerator()
    for i in range(10):
        gen.generate_crack()

    gen.show_mask()



test()
