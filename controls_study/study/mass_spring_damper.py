import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import scipy.signal as signal

# System parameters
m = 1.0   # mass (kg)
b = 5.0   # damping coefficient
k = 20.0  # spring stiffness

# System characteristics
omega_n = np.sqrt(k / m)  # natural frequency: ωn = √(k/m)
zeta = b / (2 * np.sqrt(m * k))  # damping ratio: ζ = c / (2√(mk))
omega_d = omega_n * np.sqrt(1 - zeta**2) if zeta < 1 else 0  # damped natural frequency: ωd = ωn√(1 − ζ²)

# Transfer function numerator and denominator
num = [1]
den = [m, b, k]

system = signal.TransferFunction(num, den)

# Time vector
t = np.linspace(0, 5, 500)

# Step response (input is a unit step force)
t, x = signal.step(system, T=t)

# Create figure with four subplots: diagram, equations, animation, response
fig = plt.figure(figsize=(16, 11))
gs = fig.add_gridspec(4, 2, height_ratios=[1, 0.8, 1.5, 1], width_ratios=[1, 1], 
                       left=0.08, right=0.95, top=0.93, bottom=0.08, 
                       hspace=0.3, wspace=0.3)
fig.suptitle('Mass-Spring-Damper System', fontsize=16, fontweight='bold')

# System diagram (top left)
ax_diagram = fig.add_subplot(gs[0, 0])
ax_diagram.set_xlim(-0.5, 3.5)
ax_diagram.set_ylim(-0.5, 1.5)
ax_diagram.set_aspect('equal')
ax_diagram.axis('off')
ax_diagram.set_title('System Diagram', fontsize=12, fontweight='bold')

# Draw wall in diagram
wall_diagram = patches.Rectangle((-0.2, 0.2), 0.2, 1.0, 
                                  facecolor='#8B7355', edgecolor='black', linewidth=2)
ax_diagram.add_patch(wall_diagram)

# Draw spring in diagram (coil representation)
spring_length = 1.5
spring_coils = 8
spring_x_diagram = np.linspace(0, spring_length, 100)
spring_y_diagram = 0.7 + 0.15 * np.sin(spring_x_diagram * spring_coils * 2 * np.pi / spring_length)
ax_diagram.plot(spring_x_diagram, spring_y_diagram, 'b-', linewidth=3, label='Spring (k)')

# Draw damper in diagram (piston-cylinder)
damper_y_diagram = 0.3
# Cylinder
damper_cylinder = patches.Rectangle((0.1, damper_y_diagram - 0.1), 1.3, 0.2,
                                    facecolor='#CCCCCC', edgecolor='black', linewidth=2)
ax_diagram.add_patch(damper_cylinder)
# Piston rod
ax_diagram.plot([0.1, 1.4], [damper_y_diagram, damper_y_diagram], 'r-', linewidth=3)
# Piston head
piston = patches.Circle((1.4, damper_y_diagram), 0.08, facecolor='red', edgecolor='black', linewidth=2)
ax_diagram.add_patch(piston)
ax_diagram.plot([0, 0.1], [damper_y_diagram, damper_y_diagram], 'r-', linewidth=3, label='Damper (b)')

# Draw mass in diagram
mass_x_diagram = 1.5
mass_width = 0.4
mass_height = 0.3
mass_diagram = FancyBboxPatch((mass_x_diagram, 0.5), mass_width, mass_height,
                              boxstyle="round,pad=0.02", facecolor='#4A90E2', 
                              edgecolor='black', linewidth=2)
ax_diagram.add_patch(mass_diagram)
ax_diagram.text(mass_x_diagram + mass_width/2, 0.65, 'm', ha='center', va='center', 
                fontsize=14, fontweight='bold', color='white')

# Add labels
ax_diagram.text(0.75, 0.95, 'k', ha='center', fontsize=12, fontweight='bold', color='blue')
ax_diagram.text(0.75, 0.15, 'b', ha='center', fontsize=12, fontweight='bold', color='red')
ax_diagram.text(1.7, 0.35, 'x(t)', ha='center', fontsize=11, style='italic')
ax_diagram.arrow(1.7, 0.35, 0.3, 0, head_width=0.05, head_length=0.05, fc='black', ec='black')

# Add force arrow
force_arrow = FancyArrowPatch((2.0, 0.65), (2.3, 0.65),
                              arrowstyle='->', mutation_scale=20, 
                              color='green', linewidth=2)
ax_diagram.add_patch(force_arrow)
ax_diagram.text(2.15, 0.8, 'F(t)', ha='center', fontsize=11, fontweight='bold', color='green')

# Equations panel (below diagram)
ax_eq = fig.add_subplot(gs[1, 0])
ax_eq.axis('off')
ax_eq.set_title('Force Equations', fontsize=12, fontweight='bold')

# Display equations
equations_text = [
    r'$F_{spring} = -kx$',
    r'$F_{damper} = -b\dot{x} = -bv$',
    r'$F_{net} = ma = m\ddot{x}$',
    '',
    r'$m\ddot{x} + b\dot{x} + kx = F(t)$',
    '',
    f'Parameters: $m={m}$ kg, $b={b}$ N·s/m, $k={k}$ N/m',
    '',
    f'Natural frequency: $\\omega_n = \\sqrt{{k/m}} = {omega_n:.3f}$ rad/s',
    f'Damping ratio: $\\zeta = b/(2\\sqrt{{mk}}) = {zeta:.3f}$',
]
if zeta < 1:
    equations_text.append(f'Damped natural frequency: $\\omega_d = \\omega_n\\sqrt{{1-\\zeta^2}} = {omega_d:.3f}$ rad/s')
else:
    equations_text.append(f'System is {"critically damped" if abs(zeta - 1) < 1e-6 else "overdamped"} ($\\zeta \\geq 1$)')

y_pos = 0.9
for eq in equations_text:
    if eq:
        ax_eq.text(0.05, y_pos, eq, fontsize=14,
                  verticalalignment='top', transform=ax_eq.transAxes)
    y_pos -= 0.15

# Animation subplot (top right and middle)
ax_anim = fig.add_subplot(gs[0:2, 1])
ax_anim.set_xlim(-0.5, 2.5)
ax_anim.set_ylim(-0.3, 1.2)
ax_anim.set_aspect('equal')
ax_anim.set_xlabel('Position (m)', fontsize=11)
ax_anim.set_ylabel('Height (m)', fontsize=11)
ax_anim.grid(True, alpha=0.3, linestyle='--')
ax_anim.set_title('System Animation', fontsize=12, fontweight='bold')

# Initial positions for animation
wall_x = 0.0
x0 = 0.0  # equilibrium position
mass_width = 0.3
mass_height = 0.25
spring_rest_length = 0.8
spring_coils_anim = 6

# Draw wall
wall = patches.Rectangle((wall_x - 0.15, 0.1), 0.15, 0.9, 
                         facecolor='#8B7355', edgecolor='black', linewidth=2)
ax_anim.add_patch(wall)

# Draw ground line
ax_anim.plot([-0.5, 2.5], [0, 0], 'k-', linewidth=1, alpha=0.5)

# Spring and damper lines (will be updated)
spring_line, = ax_anim.plot([], [], 'b-', linewidth=3, label='Spring (k)')
damper_line, = ax_anim.plot([], [], 'r-', linewidth=3, label='Damper (b)')

# Mass rectangle (will be updated)
mass_rect = FancyBboxPatch((x0, 0.4), mass_width, mass_height,
                          boxstyle="round,pad=0.02", facecolor='#4A90E2', 
                          edgecolor='black', linewidth=2)
ax_anim.add_patch(mass_rect)

# Mass label
mass_text = ax_anim.text(0, 0, 'm', ha='center', va='center', 
                        fontsize=12, fontweight='bold', color='white')

# Response plot (bottom)
ax_response = fig.add_subplot(gs[3, :])
ax_response.set_xlim(0, 5)
ax_response.set_ylim(0, max(x) * 1.1)
ax_response.set_xlabel('Time (s)', fontsize=11)
ax_response.set_ylabel('Displacement x(t) (m)', fontsize=11)
ax_response.grid(True, alpha=0.3, linestyle='--')
ax_response.set_title('Step Response', fontsize=12, fontweight='bold')

# Plot full response curve (static background)
ax_response.plot(t, x, 'b-', linewidth=1.5, alpha=0.3, label='Full Response')

# Response curve (animated)
response_line, = ax_response.plot([], [], 'b-', linewidth=2.5, label='Animated Response')
time_marker, = ax_response.plot([], [], 'ro', markersize=8, label='Current Time')
ax_response.legend(loc='upper right')

# Animation function
def animate(frame):
    # Current time and displacement
    current_t = t[frame]
    current_x = x[frame]
    mass_x = x0 + current_x
    
    # Update mass position
    mass_rect.set_x(mass_x)
    mass_text.set_position((mass_x + mass_width/2, 0.525))
    
    # Draw spring (coil representation that compresses/extends)
    spring_length_anim = spring_rest_length + current_x
    if spring_length_anim > 0.1:  # Only draw if spring has positive length
        spring_x_anim = np.linspace(wall_x, mass_x, 80)
        spring_y_anim = 0.6 + 0.12 * np.sin(spring_x_anim * spring_coils_anim * 2 * np.pi / max(spring_length_anim, 0.1))
        spring_line.set_data(spring_x_anim, spring_y_anim)
    else:
        spring_line.set_data([], [])
    
    # Draw damper (horizontal line that extends/contracts)
    damper_y_anim = 0.25
    damper_x_anim = [wall_x, mass_x]
    damper_y_data = [damper_y_anim, damper_y_anim]
    damper_line.set_data(damper_x_anim, damper_y_data)
    
    # Update response plot
    response_line.set_data(t[:frame+1], x[:frame+1])
    time_marker.set_data([current_t], [current_x])
    
    return mass_rect, mass_text, spring_line, damper_line, response_line, time_marker

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=len(t), 
                                interval=10, blit=False, repeat=True)

plt.show()
