import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# System parameters
m = 1.0   # mass (kg)
b = 4.0   # damping coefficient
k = 20.0  # spring stiffness

# Transfer function numerator and denominator
num = [1]
den = [m, b, k]

system = signal.TransferFunction(num, den)

# Time vector
t = np.linspace(0, 5, 500)

# Step response (input is a unit step force)
t, x = signal.step(system, T=t)

# Plot the result
plt.plot(t, x)
plt.title("Step Response of Mass-Spring-Damper System")
plt.xlabel("Time (s)")
plt.ylabel("Displacement x(t)")
plt.grid(True)
plt.show()
