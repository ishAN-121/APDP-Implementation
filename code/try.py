import numpy as np
import matplotlib.pyplot as plt

# Define the range of x values
x = np.linspace(0, 1, 10)  # Range from 0 to 5 with 100 points

# Calculate the corresponding y values
y = np.exp(-x)

# Plot the graph
plt.plot(x, y, label=r'$e^{-x}$')
plt.xlabel('Comprehensive Attribute Value')
plt.ylabel('Privacy Budget $\epsilon$')
plt.xticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
plt.show()
