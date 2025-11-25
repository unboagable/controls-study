import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.patches import Circle

# PID Walking Parameters
DESIRED_LOCATION = 50
STARTING_POINT = 0
K_P = 0.1  # proportional gain
K_I = 0.0  # integral gain
K_D = 0.0  # derivative gain

# Simulation parameters
DT = 0.05  # time step (s)
T_MAX = 40  # maximum simulation time (s)


def pid_controller(error, integral, prev_error, dt):
    """Calculate PID control output.
    
    Args:
        error: Current error (desired - current)
        integral: Accumulated integral term
        prev_error: Previous error for derivative calculation
        dt: Time step
        
    Returns:
        tuple: (control_output, new_integral)
    """
    proportional = K_P * error
    integral += error * dt
    derivative = K_D * (error - prev_error) / dt
    output = proportional + K_I * integral + derivative
    return output, integral


def simulate_pid_control():
    """Run PID control simulation and return time series data."""
    t = np.arange(0, T_MAX, DT)
    num_frames = len(t)
    
    # Initialize simulation arrays
    position = np.zeros(num_frames)
    velocity = np.zeros(num_frames)
    error = np.zeros(num_frames)
    integral = 0.0
    prev_error = DESIRED_LOCATION - STARTING_POINT
    
    # Simulate PID control
    for i in range(num_frames):
        # Calculate error
        error[i] = DESIRED_LOCATION - position[i]
        
        # PID control
        control_output, integral = pid_controller(error[i], integral, prev_error, DT)
        
        # Simple dynamics: velocity is proportional to control output
        velocity[i] = control_output
        
        # Update position
        if i < num_frames - 1:
            position[i + 1] = position[i] + velocity[i] * DT
        
        prev_error = error[i]
    
    return t, position, velocity, error


def create_animation_plot(t, position, velocity, error):
    """Create and configure the animation figure with all subplots."""
    fig = plt.figure(figsize=(14, 12))
    gs = fig.add_gridspec(4, 1, height_ratios=[1.5, 1, 1, 1],
                          left=0.1, right=0.95, top=0.95, bottom=0.08,
                          hspace=0.3)
    fig.suptitle('PID Controlled Walking Animation', fontsize=16, fontweight='bold')
    
    # Animation subplot (top)
    ax_anim = fig.add_subplot(gs[0])
    ax_anim.set_xlim(-5, DESIRED_LOCATION + 10)
    ax_anim.set_ylim(-1, 3)
    ax_anim.set_aspect('equal')
    ax_anim.set_xlabel('Position (m)', fontsize=11)
    ax_anim.set_ylabel('Height (m)', fontsize=11)
    ax_anim.grid(True, alpha=0.3, linestyle='--')
    ax_anim.set_title('Person Walking Animation', fontsize=12, fontweight='bold')
    
    # Draw ground
    ax_anim.plot([-5, DESIRED_LOCATION + 10], [0, 0], 'k-', linewidth=2)
    
    # Draw target location marker
    target_marker = patches.Rectangle((DESIRED_LOCATION - 0.5, 0), 1, 0.2,
                                      facecolor='green', edgecolor='darkgreen',
                                      linewidth=2, alpha=0.7)
    ax_anim.add_patch(target_marker)
    ax_anim.text(DESIRED_LOCATION, -0.5, 'Target', ha='center', va='top',
                fontsize=11, fontweight='bold', color='green')
    
    # Draw starting point marker
    start_marker = patches.Rectangle((STARTING_POINT - 0.5, 0), 1, 0.2,
                                    facecolor='red', edgecolor='darkred',
                                    linewidth=2, alpha=0.7)
    ax_anim.add_patch(start_marker)
    ax_anim.text(STARTING_POINT, -0.5, 'Start', ha='center', va='top',
                fontsize=11, fontweight='bold', color='red')
    
    # Person representation (simple stick figure)
    person_height = 1.5
    head_radius = 0.15
    
    # Person components (will be updated)
    head = Circle((STARTING_POINT, person_height + 0.3), head_radius,
                 facecolor='#FFDBAC', edgecolor='black', linewidth=2)
    ax_anim.add_patch(head)
    
    body_line, = ax_anim.plot([], [], 'k-', linewidth=3)
    left_leg, = ax_anim.plot([], [], 'k-', linewidth=3)
    right_leg, = ax_anim.plot([], [], 'k-', linewidth=3)
    left_arm, = ax_anim.plot([], [], 'k-', linewidth=3)
    right_arm, = ax_anim.plot([], [], 'k-', linewidth=3)
    
    # Position plot (second)
    ax_position = fig.add_subplot(gs[1])
    ax_position.set_xlim(0, T_MAX)
    ax_position.set_ylim(-2, DESIRED_LOCATION + 5)
    ax_position.set_xlabel('Time (s)', fontsize=11)
    ax_position.set_ylabel('Position (m)', fontsize=11)
    ax_position.grid(True, alpha=0.3, linestyle='--')
    ax_position.set_title('Position Over Time', fontsize=12, fontweight='bold')
    
    # Plot full position curve (static background)
    ax_position.plot(t, position, 'b-', linewidth=1.5, alpha=0.3, label='Full Response')
    ax_position.axhline(y=DESIRED_LOCATION, color='g', linestyle='--', linewidth=2,
                        label='Target Position', alpha=0.7)
    
    # Animated position line
    position_line, = ax_position.plot([], [], 'b-', linewidth=2.5, label='Current Position')
    time_marker, = ax_position.plot([], [], 'ro', markersize=8, label='Current Time')
    ax_position.legend(loc='upper right')
    
    # Velocity plot (third)
    ax_velocity = fig.add_subplot(gs[2])
    ax_velocity.set_xlim(0, T_MAX)
    ax_velocity.set_ylim(-1, max(abs(velocity)) * 1.2 if max(abs(velocity)) > 0 else 5)
    ax_velocity.set_xlabel('Time (s)', fontsize=11)
    ax_velocity.set_ylabel('Velocity (m/s)', fontsize=11)
    ax_velocity.grid(True, alpha=0.3, linestyle='--')
    ax_velocity.set_title('Velocity Over Time', fontsize=12, fontweight='bold')
    ax_velocity.axhline(y=0, color='k', linestyle='-', linewidth=1, alpha=0.5)
    
    # Plot full velocity curve (static background)
    ax_velocity.plot(t, velocity, 'm-', linewidth=1.5, alpha=0.3, label='Full Velocity')
    
    # Animated velocity line
    velocity_line, = ax_velocity.plot([], [], 'm-', linewidth=2.5, label='Current Velocity')
    velocity_marker, = ax_velocity.plot([], [], 'mo', markersize=8)
    ax_velocity.legend(loc='upper right')
    
    # Error plot (bottom)
    ax_error = fig.add_subplot(gs[3])
    ax_error.set_xlim(0, T_MAX)
    ax_error.set_ylim(-5, max(abs(error)) * 1.2 if max(abs(error)) > 0 else 5)
    ax_error.set_xlabel('Time (s)', fontsize=11)
    ax_error.set_ylabel('Error (m)', fontsize=11)
    ax_error.grid(True, alpha=0.3, linestyle='--')
    ax_error.set_title('Position Error (Desired - Current)', fontsize=12, fontweight='bold')
    ax_error.axhline(y=0, color='k', linestyle='-', linewidth=1, alpha=0.5)
    
    # Plot full error curve (static background)
    ax_error.plot(t, error, 'r-', linewidth=1.5, alpha=0.3, label='Full Error')
    
    # Animated error line
    error_line, = ax_error.plot([], [], 'r-', linewidth=2.5, label='Current Error')
    error_marker, = ax_error.plot([], [], 'ro', markersize=8)
    ax_error.legend(loc='upper right')
    
    return (fig, head, body_line, left_leg, right_leg, left_arm, right_arm,
            position_line, time_marker, velocity_line, velocity_marker,
            error_line, error_marker, person_height)


def animate(frame, t, position, velocity, error, head, body_line, left_leg,
           right_leg, left_arm, right_arm, position_line, time_marker,
           velocity_line, velocity_marker, error_line, error_marker, person_height):
    """Animation function to update all plot elements for each frame."""
    # Current time and state
    current_t = t[frame]
    current_pos = position[frame]
    current_velocity = velocity[frame]
    current_error = error[frame]
    
    # Update person position
    person_x = STARTING_POINT + current_pos
    
    # Update head position
    head.center = (person_x, person_height + 0.3)
    
    # Update body (torso)
    body_x = [person_x, person_x]
    body_y = [person_height, person_height + 0.3]
    body_line.set_data(body_x, body_y)
    
    # Update legs (walking animation - alternating)
    leg_angle = np.sin(current_t * 4) * 0.3  # walking motion
    left_leg_x = [person_x, person_x - 0.2 * np.cos(leg_angle)]
    left_leg_y = [person_height, person_height - 0.4 - 0.1 * np.sin(leg_angle)]
    left_leg.set_data(left_leg_x, left_leg_y)
    
    right_leg_x = [person_x, person_x + 0.2 * np.cos(leg_angle)]
    right_leg_y = [person_height, person_height - 0.4 - 0.1 * np.sin(-leg_angle)]
    right_leg.set_data(right_leg_x, right_leg_y)
    
    # Update arms (swinging motion)
    arm_angle = np.sin(current_t * 4 + np.pi) * 0.4
    left_arm_x = [person_x, person_x - 0.25 * np.cos(arm_angle)]
    left_arm_y = [person_height + 0.15, person_height + 0.15 + 0.2 * np.sin(arm_angle)]
    left_arm.set_data(left_arm_x, left_arm_y)
    
    right_arm_x = [person_x, person_x + 0.25 * np.cos(arm_angle)]
    right_arm_y = [person_height + 0.15, person_height + 0.15 + 0.2 * np.sin(-arm_angle)]
    right_arm.set_data(right_arm_x, right_arm_y)
    
    # Update position plot
    position_line.set_data(t[:frame+1], position[:frame+1])
    time_marker.set_data([current_t], [current_pos])
    
    # Update velocity plot
    velocity_line.set_data(t[:frame+1], velocity[:frame+1])
    velocity_marker.set_data([current_t], [current_velocity])
    
    # Update error plot
    error_line.set_data(t[:frame+1], error[:frame+1])
    error_marker.set_data([current_t], [current_error])
    
    return (head, body_line, left_leg, right_leg, left_arm, right_arm,
            position_line, time_marker, velocity_line, velocity_marker,
            error_line, error_marker)


def main():
    """Main function to run the PID walking animation."""
    # Run simulation
    t, position, velocity, error = simulate_pid_control()
    
    # Create animation plot
    (fig, head, body_line, left_leg, right_leg, left_arm, right_arm,
     position_line, time_marker, velocity_line, velocity_marker,
     error_line, error_marker, person_height) = create_animation_plot(
         t, position, velocity, error)
    
    # Create animation
    num_frames = len(t)
    anim = animation.FuncAnimation(
        fig,
        lambda frame: animate(frame, t, position, velocity, error, head, body_line,
                             left_leg, right_leg, left_arm, right_arm,
                             position_line, time_marker, velocity_line, velocity_marker,
                             error_line, error_marker, person_height),
        frames=num_frames,
        interval=50,
        blit=False,
        repeat=True)
    
    plt.show()


if __name__ == '__main__':
    main()
