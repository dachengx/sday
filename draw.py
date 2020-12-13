# -*- coding: utf-8 -*-

import numpy as np
from celluloid import Camera
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

a = 4
np.random.seed(0)
# plt.xkcd()

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
        self.s = (np.ones_like(x) * 16 + np.random.normal(0, 1, len(x)))[vali]
        self.c = c
        self.a = np.ones_like(self.x)
    
    def draw(self, ax):
        rgba_colors = np.zeros((len(self.x), 4))
        if self.c == 'red':
            rgba_colors[:, 0] = 1.0
        elif self.c == 'blue':
            rgba_colors[:, 2] = 1.0
        rgba_colors[:, 3] = self.a
        ax.scatter(self.x, self.y, c=rgba_colors, marker='.', s=np.clip(self.s, 0, np.inf))

    def move(self, dir, withhat=True):
        step = 0.01 * a
        if dir == 'up':
            x = self.x + np.random.uniform(-2 * step, 2 * step, len(self.x))
            y = self.y + np.random.uniform(-step, 3 * step, len(self.y))
        elif dir == 'down':
            x = self.x + np.random.uniform(-2 * step, 2 * step, len(self.x))
            y = self.y + np.random.uniform(-3 * step, step, len(self.y))
        elif dir == 'random':
            x = self.x + np.random.uniform(-2 * step, 2 * step, len(self.x))
            y = self.y + np.random.uniform(-step, step, len(self.y))
        if withhat:
            vali = self.validot(x, y)
            self.x = np.where(vali, x, self.x)
            self.y = np.where(vali, y, self.y)
        else:
            vali = self.validot(x, y, False)
            self.x = np.where(vali, x, self.x)
            self.y = np.where(vali, y, self.y)
            alphavali = vali & np.logical_not(self.validot(x, y)) & np.logical_not(self.a == 0)
            self.a[alphavali] = np.clip(self.a[alphavali] - np.random.uniform(0, 0.05, sum(alphavali)), 0, 1)
        self.s = self.s + np.random.normal(0.1, 1, len(self.s))
    
    def stay(self):
        pass

    def validot(self, x, y, withhat=True):
        if withhat:
            vali = ((a + x) * np.sqrt(3) > y) & ((a - x) * np.sqrt(3) > y) & (y > 0) & (y < 3 / 4 * np.sqrt(3) * a)
        else:
            vali = (x > -1 * a) & (x < a) & (((x > -1 * a) & (x < -1 / 4 * a) & ((a + x) * np.sqrt(3) > y)) | ((x < a) & (x > 1 / 4 * a) & ((a - x) * np.sqrt(3) > y)) | ((x > -1 / 4 * a) & (x < 1 / 4 * a))) & (y > 0)
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
        self.l0 = np.array([[a, a / 4, 0, -1 * a / 4, -1 * a, a], [0, 3 / 4 * np.sqrt(3) * a, np.sqrt(3) * a, 3 / 4 * np.sqrt(3) * a, 0, 0]])
        self.l1 = np.array([[a / 4, -1 * a / 4], [3 / 4 * np.sqrt(3) * a, 3 / 4 * np.sqrt(3) * a]])
        self.l2 = np.array([[a / 4, a, -1 * a, -1 * a / 4], [3 / 4 * np.sqrt(3) * a, 0, 0, 3 / 4 * np.sqrt(3) * a]])

    def draw(self, ax):
        ax.plot(self.l0[0], self.l0[1], color='k', linewidth=4.)
        ax.plot(self.l1[0], self.l1[1], color='k', linewidth=4.)

    def l2draw(self, ax):
        ax.plot(self.l2[0], self.l2[1], color='k', linewidth=4.)

def convert(red, blue):
    vali = np.random.choice(2, len(red.x), p=[0.9, 0.1]).astype(np.bool)
    blue.x = np.append(blue.x, red.x[vali])
    blue.y = np.append(blue.y, red.y[vali])
    blue.s = np.append(blue.s, red.s[vali])
    blue.a = np.append(blue.a, red.a[vali])
    red.x = red.x[np.logical_not(vali)]
    red.y = red.y[np.logical_not(vali)]
    red.s = red.s[np.logical_not(vali)]
    red.a = red.a[np.logical_not(vali)]

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
    frame.draw(ax)
    red.move('random')
    red.draw(ax)
    blue.move('random')
    blue.draw(ax)
    camera.snap()

for _ in range(100):
    hat.draw(ax)
    frame.draw(ax)
    red.move('random')
    red.draw(ax)
    blue.move('random')
    blue.draw(ax)
    camera.snap()

for i in range(50):
    hat.draw(ax)
    frame.draw(ax)
    red.move('random')
    red.draw(ax)
    blue.move('up')
    blue.draw(ax)
    camera.snap()
    hat.draw(ax)
    frame.draw(ax)
    red.move('random')
    red.draw(ax)
    blue.move('random')
    blue.draw(ax)
    camera.snap()
    hat.draw(ax)
    frame.draw(ax)
    red.move('down')
    red.draw(ax)
    blue.move('random')
    blue.draw(ax)
    camera.snap()
    if i // 2 * 2 == i:
        convert(red, blue)

for i in range(200):
    frame.l2draw(ax)
    red.move('random')
    red.draw(ax)
    blue.move('up', withhat=False)
    blue.draw(ax)
    camera.snap()

animation = camera.animate(interval=100)
animation.save('animation.mp4')