import numpy as np
import struct

def read_binary_file(filename):
  ''' reads a binary file where the first 2x2bytes are num rows and columns
      the remainder of the file are float64 values '''
  f = open(filename, 'rb')
  rows = struct.unpack('i', f.read(4))[0]
  cols = struct.unpack('i', f.read(4))[0]
  return np.fromfile(f, dtype=np.float64).reshape((rows, cols))

prefix = 'dp'

controls     = read_binary_file(prefix + '.controls')
particles    = read_binary_file(prefix + '.particles')
weights      = read_binary_file(prefix + '.weights')
coefficients = read_binary_file(prefix + '.coefficients')
means        = read_binary_file(prefix + '.trainingMeans')
variances    = read_binary_file(prefix + '.trainingVariances')
values       = read_binary_file(prefix + '.trainingValues')

stages       = len(controls) + 1

value_functions = [
  lambda mean, variance : 1,
  lambda mean, variance : mean,
  lambda mean, variance : mean * mean,
  lambda mean, variance : np.log(np.sqrt(variance)),
  lambda mean, variance : variance,
]

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

for k in range(stages - 1):
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  # print means[:,k]
  xmin, xmax = np.min(means[:,k]), np.max(means[:,k])
  ymin, ymax = np.min(variances[:,k]), np.max(variances[:,k])
  if k == 0:
    xmin, xmax = -1, 1
    ymin, ymax = 0.5, 1.5
  nx, ny = 51, 51
  X = np.linspace(xmin, xmax, nx)
  Y = np.logspace(np.log10(ymin), np.log10(ymax), ny, base=10)
  X, Y = np.meshgrid(X, Y)
  Z = np.zeros((nx, ny))
  for index, value_function in enumerate(value_functions):
    for i in range(nx):
      for j in range(ny):
        Z[i, j] += coefficients[index, k] * value_function(X[i, j], Y[i, j])
  surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=1, antialiased=True)
  if k > 0:
    scat = ax.scatter(means[:,k], variances[:,k], values[:,k], c='k', marker='o')
  ax.zaxis.set_major_locator(LinearLocator(10))
  ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
  fig.colorbar(surf, shrink=0.5, aspect=5)
  plt.show()
