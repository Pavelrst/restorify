from PIL import Image
import numpy as np
from random import randint
from random import choice

class Point():
    def __init__(self, updown, leftright):
        self.updown = updown
        self.leftright = leftright

class Kernels():
    def __init__(self, min_size=1, max_size=5, oreol=1):
        self.min_size = min_size
        self.max_size = max_size
        self.oreol = oreol
        self.last_size = min_size
        self.getting_bigger = True
        self.chance_to_grow = 3 # bigger val -> smaller chance

    def get_kernel(self):
        if self.getting_bigger == True:
            # maybe get bigger:
            if randint(0, self.chance_to_grow) == 1:
                self.last_size += 1
                if self.last_size == self.max_size:
                    # No more getting bigger
                    self.getting_bigger = False
        else:
            # maybe get smaller:
            if randint(0, self.chance_to_grow) == 1:
                self.last_size -= 1
                if self.last_size == self.min_size:
                    # No more getting smaller
                    self.getting_bigger = True

        kernel = np.ones((self.last_size, self.last_size))

        def pad_with(vector, pad_width, iaxis, kwargs):
            pad_value = kwargs.get('padder', 0)
            vector[:pad_width[0]] = pad_value
            vector[-pad_width[1]:] = pad_value

        kernel = np.pad(kernel, self.oreol, pad_with)
        oreol = np.random.randint(2, size=kernel.shape)
        kernel = np.logical_or(kernel, oreol).astype(int)
        return kernel


class crackGenerator():
    def __init__(self, target_image=None):
        # TODO change all height to width and vise versa.
        self.width = target_image.width
        self.heigh = target_image.height
        self.image = target_image #np.zeros((self.heigh, self.width))
        self.max_iter = 10000
        self.crack_path = []
        self.kernel_getter = Kernels()


    def get_cracked_image(self):
        assert len(self.crack_path) != 0

        for point in self.crack_path:
            if self._legal_point(point):

                kernelarr = self.kernel_getter.get_kernel()*randint(240, 255)#np.ones((randint(1, 3), randint(1, 3))) * randint(240, 250) #kernels[randint(0, len(kernels)-1)] * randint(170, 250)#
                kernel = Image.fromarray(kernelarr).convert("L")
                # x, y transposed for some reason
                self.image.paste(kernel, (point.leftright, point.updown), mask=kernel)

        return self.image

    def maybe_init_direction(self):
        rand = randint(0, 500)
        # init crack direction
        if rand == 13:
            self.init_direction()

    def init_direction(self):
        (self.updown_low, self.updown_high) = choice(((-2, -1), (-1, 0), (0, 1), (1, 2), (-1, 1)))
        (self.leftright_low, self.leftright_high) = choice(((-2, -1), (-1, 0), (0, 1), (1, 2), (-1, 1)))

        if (self.updown_low, self.updown_high) == (-1,1) and (self.leftright_low, self.leftright_high) == (-1, 1):
            # To avoid big white spots
            self.max_iter = 1000
        else:
            self.max_iter = 10000


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


