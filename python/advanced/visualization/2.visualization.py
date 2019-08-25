#!/usr/bin/python3

import matplotlib.pyplot as plt


fig6 = plt.figure("Scatter")
ax5 = fig6.add_subplot(1,1,1)
ax5.scatter([-1,0,2,3,5],[2,1,3,0.5,4])
plt.show()


fig7 = plt.figure("Scatter")
ax6 = fig7.add_subplot(1,1,1)
ax6.scatter([-1,0,2,3,5],[2,1,3,0.5,4],[120,200,300,150,30],['r','g','#BCDFF0','#BCDF55','#BCDF55'], alpha=0.5)
plt.show()

fig8 = plt.figure("Pie")
sizes = [50,50,44,36]
labels = ['Wade','James','Kobe','Curry']
explode = (0.1,0,0,0)
colors = ['red','purple','yellow','blue']
plt.pie(sizes, explode = explode, labels = labels, colors = colors, autopct = '%1.1f%%', shadow = True, startangle= 140)
plt.axis('equal')
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)


N = 50
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.show()
