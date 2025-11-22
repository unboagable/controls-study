# Controls Study

A Python project for studying and practicing control systems theory and applications.

## Project Structure

The project is organized into two main modules:

### `src/study/`
Experimentation and learning modules. This directory contains:
- Educational examples and simulations
- Concept exploration and experimentation
- Learning exercises and demonstrations
- Visualizations and animations

**Current Examples:**
- `mass_spring_damper.py` - Interactive animation of a mass-spring-damper system with:
  - System diagram showing physical components
  - Force equations and differential equations
  - Real-time animation of system response
  - Step response plot

### `src/practice/`
Practical industry applications. This directory contains:
- Real-world control system implementations
- Industry-standard practices and patterns
- Production-ready code examples

## Installation

This project uses Poetry for dependency management.

```bash
# Install dependencies
poetry install

# Or using pip
pip install -r requirements.txt
```

## Dependencies

- Python 3.12+
- NumPy - Numerical computing
- Matplotlib - Plotting and visualization
- SciPy - Scientific computing and signal processing

## Usage

### Mass-Spring-Damper System Animation

Run the interactive animation:

```bash
python src/study/mass_spring_damper.py
```

This will display:
- **System Diagram**: Visual representation of the mass-spring-damper system
- **Force Equations**: Mathematical equations governing the system
  - Spring force: F_spring = -kx
  - Damper force: F_damper = -bẋ
  - Differential equation: mẍ + bẋ + kx = F(t)
- **System Animation**: Real-time visualization of the system's response
- **Step Response**: Plot showing the system's response to a unit step input

### System Parameters

The default system parameters are:
- Mass (m): 1.0 kg
- Damping coefficient (b): 4.0 N·s/m
- Spring stiffness (k): 20.0 N/m

These can be modified in the script to explore different system behaviors.

## Development

The project structure supports both experimental work (`study/`) and practical applications (`practice/`), making it easy to:
- Experiment with control theory concepts
- Develop industry-ready implementations
- Maintain clear separation between learning and production code

## License

[Add your license here]

## Contributing

[Add contribution guidelines if applicable]
