# -*- coding: utf-8 -*-

from collections import namedtuple

import numpy as np
from celluloid import Camera
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

a = 4
np.random.seed(42)
plt.xkcd()

def valihat(x, y):
    vali = ((a + x) * np.sqrt(3) > y) & ((a - x) * np.sqrt(3) > y) & (y > 3 / 4  * np.sqrt(3) * a)
    return x[vali], y[vali]

class dot:
    def __init__(self, c):
        x = np.random.uniform(-1 * a, a, 300)
        y = np.random.uniform(0, a * np.sqrt(3), 300)
        vali = self.validot(x, y)
        self.x = x[vali]
        self.y = y[vali]
        self.color = c
    
    def draw(self, ax):
        ax.scatter(self.x, self.y, color=self.color, marker='.', s=2.)

    def move(self, dir):
        step = 0.005 * a
        if dir == 'up':
            x = self.x + np.random.uniform(-step, step, len(self.x))
            y = self.y + np.random.uniform(-step, 3 * step, len(self.y))
            vali = self.validot(x, y)
            self.x = np.where(vali, x, self.x)
            self.y = np.where(vali, y, self.y)
        elif dir == 'down':
            x = self.x + np.random.uniform(-step, step, len(self.x))
            y = self.y + np.random.uniform(-3 * step, step, len(self.y))
            vali = self.validot(x, y)
            self.x = np.where(vali, x, self.x)
            self.y = np.where(vali, y, self.y)
        elif dir == 'random':
            x = self.x + np.random.uniform(-step, step, len(self.x))
            y = self.y + np.random.uniform(-step, step, len(self.y))
            vali = self.validot(x, y)
            self.x = np.where(vali, x, self.x)
            self.y = np.where(vali, y, self.y)
    
    def stay(self):
        pass

    def validot(self, x, y):
        vali = ((a + x) * np.sqrt(3) > y) & ((a - x) * np.sqrt(3) > y) & (y < 3 / 4  * np.sqrt(3) * a)
        return vali

class hat:
    def __init__(self):
        pass

    def draw(self, ax):
        x = np.random.uniform(-1 * a, a, 3000)
        y = np.random.uniform(0, a * np.sqrt(3), 3000)
        vali = self.validot(x, y)
        ax.plot(x[vali], y[vali], color='k', linewidth=1.)
    
    def validot(self, x, y):
        vali = ((a + x) * np.sqrt(3) > y) & ((a - x) * np.sqrt(3) > y) & (y > 3 / 4  * np.sqrt(3) * a)
        return vali

class frame:
    def __init__(self):
        eta = 0.05
        b = (1 + eta) * a
        self.l0 = np.array([[b, 0, -1 * b, b], [0, np.sqrt(3) * b, 0, 0]])
        self.l0[1] = self.l0[1] - eta * a / 2
        self.l1 = np.array([[b / 4, -1 * b / 4], [3 / 4 * np.sqrt(3) * b, 3 / 4 * np.sqrt(3) * b]])
        self.l1[1] = self.l1[1] - eta * a
        pass

    def draw(self, ax):
        ax.plot(self.l0[0], self.l0[1], color='k', linewidth=4.)
        ax.plot(self.l1[0], self.l1[1], color='k', linewidth=4.)

fig = plt.figure()
camera = Camera(fig)
ax = fig.add_subplot(111)
ax.axis('equal')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xlim(-1.5 * a, 1.5 * a)
ax.set_ylim(-1. * a, (1 + np.sqrt(3)) * a)
ax.set_xticks([])
ax.set_yticks([])

red = dot('red')
blue = dot('blue')
hat = hat()
frame = frame()

for _ in range(100):
    hat.draw(ax)
    frame.draw(ax)
    red.move('random')
    red.draw(ax)
    blue.move('random')
    blue.draw(ax)
    camera.snap()

animation = camera.animate(interval=100)
animation.save('animation.mp4')

from IPython.display import HTML
HTML(animation.to_html5_video())