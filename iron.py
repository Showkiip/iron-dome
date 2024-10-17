import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Class to represent an incoming threat (rocket/missile)
class Threat:
    def __init__(self, x, y, speed):
        self.x = x  # X-coordinate of the threat
        self.y = y  # Y-coordinate of the threat
        self.speed = speed  # Speed of the threat

    def move(self):
        """Simulate the movement of the threat."""
        self.x += self.speed
        self.y += self.speed

    def distance_from_target(self, target_x, target_y):
        """Calculate the distance from the target area (e.g., populated area)."""
        return math.sqrt((self.x - target_x)**2 + (self.y - target_y)**2)

# Class to simulate the Iron Dome air defense system
class IronDome:
    def __init__(self, target_x, target_y, interception_range):
        self.target_x = target_x  # The target (populated area) coordinates
        self.target_y = target_y
        self.interception_range = interception_range  # How close a threat needs to get to be intercepted

    def detect_threat(self, threat):
        """Detect if a threat is within interception range."""
        distance = threat.distance_from_target(self.target_x, self.target_y)
        return distance < self.interception_range

    def intercept_threat(self, threat):
        """Simulate intercepting a threat."""
        print(f"Threat intercepted at position ({threat.x:.2f}, {threat.y:.2f})!")
        return True

# Initialize target area
target_x = 50
target_y = 50
interception_range = 15

# Initialize the Iron Dome system
dome = IronDome(target_x, target_y, interception_range)

# Initialize the threat
threat = Threat(x=random.randint(0, 20), y=random.randint(0, 20), speed=random.uniform(0.1, 0.5))

# Set up real-time plotting
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Plot the target area
target_marker = plt.scatter(target_x, target_y, color='red', label='Target Area')

# Plot the threat
threat_marker = plt.scatter(threat.x, threat.y, color='blue', label='Incoming Threat')

# Plot the interception range
circle = plt.Circle((target_x, target_y), interception_range, color='green', fill=False, linestyle='--')
ax.add_artist(circle)

def update(frame):
    """Update the plot every frame."""
    threat.move()
    
    # Update threat position on the plot
    threat_marker.set_offsets([threat.x, threat.y])

    if dome.detect_threat(threat):
        dome.intercept_threat(threat)
        threat_marker.set_offsets([target_x, target_y])  # Move the threat to target if intercepted
        plt.title("Threat Intercepted!")
        return threat_marker,
    
    return threat_marker,

# Set up animation
ani = FuncAnimation(fig, update, frames=range(100), interval=500, repeat=False)

plt.legend(loc="upper right")
plt.title("Iron Dome Simulation")
plt.show()
