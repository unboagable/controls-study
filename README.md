# Controls Study

A Python project for studying and practicing control systems theory and applications.

## Project Structure

The project is organized into modules for different control system topics:

### `controls_study/controls/`
Control system implementations and demonstrations. This directory contains:
- PID controller implementations
- Control system visualizations and animations

**Current Examples:**
- `pid_walking.py` - Interactive PID-controlled walking animation with:
  - Real-time animation of a person walking toward a target
  - Position over time plot
  - Velocity over time plot
  - Error (desired - current position) plot
  - Configurable PID gains (Kp, Ki, Kd)

### `controls_study/dynamic_systems/`
Dynamic system simulations and visualizations. This directory contains:
- Educational examples and simulations
- System response analysis

**Current Examples:**
- `mass_spring_damper.py` - Interactive animation of a mass-spring-damper system with:
  - System diagram showing physical components
  - Force equations and differential equations
  - Real-time animation of system response
  - Step response plot

## Installation

This project uses Poetry for dependency management.

```bash
# Install dependencies
poetry install

# Or using pip
pip install -r requirements.txt
```

## Dependencies

- Python 3.11+
- NumPy - Numerical computing
- Matplotlib - Plotting and visualization
- SciPy - Scientific computing and signal processing
- Pandas - Data manipulation

## Usage

### PID Walking Animation

Run the interactive PID-controlled walking animation:

```bash
poetry run python controls_study/controls/pid_walking.py
```

Or as a module:

```bash
poetry run python -m controls_study.controls.pid_walking
```

This will display:
- **Walking Animation**: Real-time visualization of a person walking toward a target location
- **Position Over Time**: Plot showing position vs time with target position indicator
- **Velocity Over Time**: Plot showing velocity vs time
- **Error Plot**: Plot showing position error (desired - current) over time

**PID Parameters:**
- Proportional gain (Kp): 0.1 (default)
- Integral gain (Ki): 0.0 (default)
- Derivative gain (Kd): 0.0 (default)

These can be modified in the script to explore different control behaviors.

### Mass-Spring-Damper System Animation

Run the interactive animation:

```bash
poetry run python controls_study/dynamic_systems/mass_spring_damper.py
```

Or as a module:

```bash
poetry run python -m controls_study.dynamic_systems.mass_spring_damper
```

This will display:
- **System Diagram**: Visual representation of the mass-spring-damper system
- **Force Equations**: Mathematical equations governing the system
  - Spring force: F_spring = -kx
  - Damper force: F_damper = -bẋ
  - Differential equation: mẍ + bẋ + kx = F(t)
- **System Animation**: Real-time visualization of the system's response
- **Step Response**: Plot showing the system's response to a unit step input

**System Parameters:**
- Mass (m): 1.0 kg
- Damping coefficient (b): 5.0 N·s/m
- Spring stiffness (k): 20.0 N/m

These can be modified in the script to explore different system behaviors.

## Development

The project structure supports:
- Control system implementations (`controls/`)
- Dynamic system simulations (`dynamic_systems/`)
- Experimentation with control theory concepts
- Interactive visualizations and animations

## License

[Add your license here]

## Contributing

[Add contribution guidelines if applicable]
