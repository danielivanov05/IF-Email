import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
g = 9.81 # [m/s^2]
rho = 1.225  # air density [kg/m^3]

def get_flight_time(v0, angle_rad):
    return 2 * v0 * math.sin(angle_rad) / g

def get_analytical_trajectory(v0, angle_rad, T, num_points=100):
    t_values = [i * T / num_points for i in range(num_points + 1)]
    x_values = [v0 * math.cos(angle_rad) * t for t in t_values]
    y_values = [v0 * math.sin(angle_rad) * t - 0.5 * g * t**2 for t in t_values]
    return x_values, y_values

def run_projectile_with_drag(v0, angle_rad, mass=1., Cd=0.47, A=0.1, dt=0.001):
    """
    Simulate movement of a projectile thrown at angle with Vo with air drag
    Parameters:
        v0 - initial velocity (m/s)
        angle_rad - angle of projection (rad)
        mass - mass of the body (kg)
        Cd - friction coefficient (dimensionless)
        A - object face area (m^2)
        dt - time step (s)
    returns:
        list of x, y, T, lists of velocities components (vx, vy) and forces (Fx, Fy)
    """
    vx = v0 * math.cos(angle_rad)
    vy = v0 * math.sin(angle_rad)

    x, y = [0], [0]
    t = 0
    vx_values, vy_values = [vx], [vy]
    Fx_values, Fy_values = [], []

    while y[-1] >= 0:
        v = math.sqrt(vx**2 + vy**2)
        # drag force
        Fd = 0.5 * rho * Cd * A * v**2

        # drag direction
        if v > 1e-6:  # Avoid division by zero if velocity is zero
            Fx = -Fd * (vx / v)
            Fy = -Fd * (vy / v) - mass * g
        else:
            Fx = 0
            Fy = -mass * g

        Fx_values.append(Fx)
        Fy_values.append(Fy)

        # velocity changes
        vx += (Fx / mass) * dt
        vy += (Fy / mass) * dt

        # new position values
        x.append(x[-1] + vx * dt)
        y.append(y[-1] + vy * dt)
        vx_values.append(vx)
        vy_values.append(vy)

        t += dt
    # Ensure the last force values correspond to the last position
    Fx_values.append(Fx_values[-1] if Fx_values else 0)
    Fy_values.append(Fy_values[-1] if Fy_values else 0)

    return x, y, t, vx_values, vy_values, Fx_values, Fy_values

# Input data
v0 = float(input("Въведете начална скорост v0 (m/s): "))
angle_deg = float(input("Въведете ъгъл на хвърляне (градуси): "))

angle_rad = math.radians(angle_deg)

# No drag simulation (no air friction)
T_no_drag = get_flight_time(v0, angle_rad)
x_no_drag, y_no_drag = get_analytical_trajectory(v0, angle_rad, T_no_drag)

# Values with drag
x_drag, y_drag, T_drag, vx_drag, vy_drag, Fx_drag, Fy_drag = run_projectile_with_drag(v0, angle_rad)



# Results
print(f"\nTime of flight (no drag): {T_no_drag:.2f} s")
print(f"Legth (no drag): {x_no_drag[-1]:.2f} m")
print(f"Max height (no drag): {max(y_no_drag):.2f} m")

print(f"\nTime of flight (drag): {T_drag:.2f} s")
print(f"Legth (drag): {x_drag[-1]:.2f} m")
print(f"Max height (drag): {max(y_drag):.2f} m")


# Plots
plt.figure(figsize=(10, 6))
# Get current axes
ax = plt.gca()
ax.plot(x_drag, y_drag, label="drag")
ax.plot(x_no_drag, y_no_drag, '--', label="no drag")
ax.set_aspect('equal', adjustable='box')

plt.title("Projectile Motion")
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.legend()
# Add both major and minor grid lines
ax.grid(True, which='both', linestyle='-', linewidth=0.5)

# Turn on minor ticks
ax.minorticks_on()

# Set the y-axis limits
ax.set_ylim(-1, max(max(y_no_drag), max(y_drag)) * 1.5)

# Adjust layout to prevent labels overlapping
plt.tight_layout()
plt.show()

# --- Create animation ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Projectile Motion Animation with Vectors")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Height (m)")
ax.grid(True)
ax.set_aspect('equal', adjustable='box')

ax.plot(x_no_drag, y_no_drag, '--', color='gray', label='No drag')
line_drag, = ax.plot([], [], 'r-', label='With drag')
point, = ax.plot([], [], 'bo', markersize=8)

# Initialize vector objects
velocity_arrow = ax.arrow(0, 0, 0, 0, head_width=0.1, head_length=0.2, fc='purple', ec='purple', label='Velocity')
force_arrow = ax.arrow(0, 0, 0, 0, head_width=0.1, head_length=0.2, fc='green', ec='green', label='Force')

ax.legend()
# adjust axes limits
ax.set_xlim(0, max(max(x_no_drag), max(x_drag)) * 1.1)
ax.set_ylim(-1, max(max(y_no_drag), max(y_drag)) * 1.5)

# Animation update function
def update(frame):
    if frame < len(x_drag):
        line_drag.set_data(x_drag[:frame], y_drag[:frame])
        point.set_data([x_drag[frame]], [y_drag[frame]]) # Pass as lists

        # Update velocity vector - scale velocity vector for better visualization
        velocity_arrow.set_data(x=x_drag[frame], y=y_drag[frame], dx=vx_drag[frame]*0.2, dy=vy_drag[frame]*0.2) 

        # Update force vector - scale force vector for better visualization
        force_arrow.set_data(x=x_drag[frame], y=y_drag[frame], dx=Fx_drag[frame]*0.02, dy=Fy_drag[frame]*0.02)

    return line_drag, point, velocity_arrow, force_arrow

# Create the animation
ani = FuncAnimation(fig, update, frames=len(x_drag), interval=20, blit=True)
ani.save("projectile_motion_with_vectors.mp4", fps=30)

# from IPython.display import Video
# Video("projectile_motion_with_vectors.mp4")