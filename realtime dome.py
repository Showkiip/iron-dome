import math
import random
import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MIN_MISSILE_SPEED = 3  # Minimum speed for missiles
MAX_MISSILE_SPEED = 8  # Maximum speed for missiles
INTERCEPTOR_SPEED = 10  # Speed of interceptor missile
RADAR_RADIUS = 150  # Detection range of the radar
RADAR_POSITION = (400, 500)  # Radar position on the screen
RADAR_SWEEP_SPEED = 0.05  # Speed of radar sweep (radians per frame)
FRAME_RATE = 60  # Frame rate for the simulation

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Missile class: represents an incoming threat
class Missile:
    def __init__(self, start_x, start_y, target_x, target_y, speed):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed  # Speed is now dynamic
        self.angle = math.atan2(target_y - start_y, target_x - start_x)

    def update_position(self):
        """Move the missile along its trajectory."""
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def is_at_target(self):
        """Check if missile has reached its target."""
        return math.hypot(self.x - self.target_x, self.y - self.target_y) < 5

    def is_in_radar_range(self, radar_x, radar_y):
        """Check if missile is within the radar's detection range."""
        return math.hypot(self.x - radar_x, self.y - radar_y) <= RADAR_RADIUS

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
        """Calculate interception angle and set missile's current position as target."""
        self.target_x = missile.x
        self.target_y = missile.y
        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

    def update_position(self):
        """Move the interceptor toward the target."""
        if self.target_x and self.target_y:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

    def has_intercepted(self, missile):
        """Check if the interceptor is close enough to destroy the missile."""
        return math.hypot(self.x - missile.x, self.y - missile.y) < 5

# Radar class: detects missiles and launches interceptors
class Radar:
    def __init__(self, radar_x, radar_y):
        self.x = radar_x
        self.y = radar_y
        self.interceptors = []
        self.sweep_angle = 0  # Angle of radar sweep

    def detect_and_launch(self, missiles):
        """Detect missiles in range and launch interceptors."""
        for missile in missiles:
            if missile.is_in_radar_range(self.x, self.y) and not self.is_interceptor_launched_for(missile):
                self.launch_interceptor(missile)

    def is_interceptor_launched_for(self, missile):
        """Check if an interceptor is already targeting the missile."""
        for interceptor in self.interceptors:
            if interceptor.target_x == missile.x and interceptor.target_y == missile.y:
                return True
        return False

    def launch_interceptor(self, missile):
        """Launch an interceptor missile towards the detected missile."""
        interceptor = Interceptor(self.x, self.y)
        interceptor.calculate_interception(missile)
        self.interceptors.append(interceptor)

    def update_interceptors(self, missiles):
        """Update the positions of interceptors and check if any have intercepted a missile."""
        intercepted_missiles = []
        for interceptor in self.interceptors:
            interceptor.update_position()
            for missile in missiles:
                if interceptor.has_intercepted(missile):
                    intercepted_missiles.append(missile)
                    print("Missile intercepted!")
        return intercepted_missiles

    def draw_radar(self):
        """Draw the radar with a rotating sweep line."""
        pygame.draw.circle(screen, (0, 0, 255), RADAR_POSITION, RADAR_RADIUS, 1)  # Radar detection range

        # Radar sweep line
        sweep_x = RADAR_POSITION[0] + RADAR_RADIUS * math.cos(self.sweep_angle)
        sweep_y = RADAR_POSITION[1] + RADAR_RADIUS * math.sin(self.sweep_angle)
        pygame.draw.line(screen, (0, 255, 255), RADAR_POSITION, (sweep_x, sweep_y), 2)

        # Update the radar sweep angle
        self.sweep_angle += RADAR_SWEEP_SPEED
        if self.sweep_angle >= 2 * math.pi:
            self.sweep_angle = 0

# Simulation loop
def main_simulation():
    # Multiple incoming missiles with random speeds between MIN_MISSILE_SPEED and MAX_MISSILE_SPEED
    missiles = [Missile(random.randint(0, SCREEN_WIDTH), 0, *RADAR_POSITION, random.uniform(MIN_MISSILE_SPEED, MAX_MISSILE_SPEED)) for _ in range(5)]
    radar = Radar(*RADAR_POSITION)
    game_speed = 1  # Speed control for the simulation
    running = True
    paused = False  # Pause control

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause/resume simulation
                    paused = not paused
                if event.key == pygame.K_UP:  # Speed up the game
                    game_speed += 1
                if event.key == pygame.K_DOWN:  # Slow down the game
                    game_speed = max(1, game_speed - 1)  # Prevent negative speed

        if not paused:
            screen.fill((0, 0, 0))  # Clear screen

            # Draw the radar
            radar.draw_radar()

            # Update and draw missiles
            for missile in missiles:
                missile.update_position()
                pygame.draw.circle(screen, (255, 0, 0), (int(missile.x), int(missile.y)), 5)

            # Radar detects missiles and launches interceptors
            radar.detect_and_launch(missiles)

            # Update interceptors and check for interceptions
            intercepted_missiles = radar.update_interceptors(missiles)
            for missile in intercepted_missiles:
                missiles.remove(missile)

            # Draw interceptors
            for interceptor in radar.interceptors:
                pygame.draw.circle(screen, (0, 255, 0), (int(interceptor.x), int(interceptor.y)), 5)

            # End simulation if all missiles are intercepted or have reached the target
            missiles = [m for m in missiles if not m.is_at_target()]
            if not missiles:
                print("All missiles intercepted or reached the target. Simulation ended.")
                running = False

            pygame.display.flip()  # Update the display
            clock.tick(FRAME_RATE * game_speed)  # Control frame rate based on game speed

# Run the simulation
main_simulation()
