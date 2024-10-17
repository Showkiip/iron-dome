import math
import random
import pygame  # For simulation/visualization

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MISSILE_SPEED = 5  # Speed of incoming missile
INTERCEPTOR_SPEED = 10  # Speed of interceptor missile

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Missile class: represents an incoming threat
class Missile:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = MISSILE_SPEED
        self.angle = math.atan2(target_y - start_y, target_x - start_x)

    def update_position(self):
        # Move the missile along its trajectory
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def is_at_target(self):
        # Check if missile has reached its target
        return math.hypot(self.x - self.target_x, self.y - self.target_y) < 5

# Interceptor class: represents the defensive missile
class Interceptor:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.speed = INTERCEPTOR_SPEED
        self.target_x = None
        self.target_y = None
        self.angle = None

    def calculate_interception(self, missile):
        # Calculate interception point using basic geometry
        self.target_x = missile.x
        self.target_y = missile.y
        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

    def update_position(self):
        # Move the interceptor toward the target (missile's current position)
        if self.target_x and self.target_y:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

    def has_intercepted(self, missile):
        # Check if the interceptor is close enough to destroy the missile
        return math.hypot(self.x - missile.x, self.y - missile.y) < 5

# Radar class: detects missiles and launches interceptors
class Radar:
    def __init__(self):
        self.interceptors = []

    def detect_and_launch(self, missile):
        # Launch an interceptor for an incoming missile
        interceptor = Interceptor(400, 500)  # Interceptor starts at fixed location
        interceptor.calculate_interception(missile)
        self.interceptors.append(interceptor)

    def update_interceptors(self, missile):
        for interceptor in self.interceptors:
            interceptor.update_position()
            if interceptor.has_intercepted(missile):
                print("Missile intercepted!")
                return True
        return False

# Simulation loop
def main_simulation():
    missile = Missile(random.randint(0, SCREEN_WIDTH), 0, 400, 500)  # Random incoming missile
    radar = Radar()

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen

        # Draw the missile
        missile.update_position()
        pygame.draw.circle(screen, (255, 0, 0), (int(missile.x), int(missile.y)), 5)

        # Detect missile and launch interceptor
        radar.detect_and_launch(missile)

        # Update interceptors and check for interception
        intercepted = radar.update_interceptors(missile)
        if intercepted or missile.is_at_target():
            print("Simulation ended.")
            running = False

        # Draw the interceptor(s)
        for interceptor in radar.interceptors:
            pygame.draw.circle(screen, (0, 255, 0), (int(interceptor.x), int(interceptor.y)), 5)

        pygame.display.flip()  # Update the display
        pygame.time.delay(50)

# Run the simulation
main_simulation()
