import math
import random
import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
INTERCEPTOR_SPEED = 10  # Speed of interceptor missile
RADAR_RADIUS = 150  # Detection range of the radar
RADAR_POSITION = (400, 500)  # Radar position on the screen
RADAR_SWEEP_SPEED = 0.05  # Speed of radar sweep (radians per frame)
FRAME_RATE = 60  # Frame rate for the simulation

# Missile types
MISSILE_TYPES = {
    "fast": {"color": (255, 0, 0), "speed": random.uniform(6, 10), "size": 5},
    "slow": {"color": (0, 255, 0), "speed": random.uniform(2, 5), "size": 7},
    "explosive": {"color": (0, 0, 255), "speed": random.uniform(3, 7), "size": 6},
}

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound effects
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load sound effects
missile_sound = pygame.mixer.Sound("./missile_launch.wav")
explosion_sound = pygame.mixer.Sound("./explosion.mp3")

# Font for score display
font = pygame.font.Font(None, 36)

# Missile class: represents an incoming threat
class Missile:
    def __init__(self, start_x, start_y, target_x, target_y, missile_type):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.color = missile_type["color"]
        self.speed = missile_type["speed"]
        self.size = missile_type["size"]
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
        if self.target_x is not None and self.target_y is not None:
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
        missile_sound.play()  # Play missile launch sound

    def update_interceptors(self, missiles):
        """Update the positions of interceptors and check if any have intercepted a missile."""
        intercepted_missiles = []
        for interceptor in self.interceptors:
            interceptor.update_position()
            for missile in missiles:
                if interceptor.has_intercepted(missile):
                    intercepted_missiles.append(missile)
                    explosion_sound.play()  # Play explosion sound
                    print("Missile intercepted!")
        return intercepted_missiles

    def draw_radar(self):
        """Draw the radar with a rotating sweep line."""
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), RADAR_RADIUS, 1)  # Radar detection range

        # Radar sweep line
        sweep_x = self.x + RADAR_RADIUS * math.cos(self.sweep_angle)
        sweep_y = self.y + RADAR_RADIUS * math.sin(self.sweep_angle)
        pygame.draw.line(screen, (0, 255, 255), (self.x, self.y), (sweep_x, sweep_y), 2)

        # Arc indicating the radar sweep
        start_angle = self.sweep_angle - 0.1
        end_angle = self.sweep_angle + 0.1
        pygame.draw.arc(screen, (0, 255, 255), (self.x - RADAR_RADIUS, self.y - RADAR_RADIUS, RADAR_RADIUS * 2, RADAR_RADIUS * 2), start_angle, end_angle, 2)

        # Update the radar sweep angle
        self.sweep_angle += RADAR_SWEEP_SPEED
        if self.sweep_angle >= 2 * math.pi:
            self.sweep_angle = 0

# Function to draw explosions
def draw_explosion(position):
    pygame.draw.circle(screen, (255, 255, 0), (int(position[0]), int(position[1])), 15)
    pygame.draw.circle(screen, (255, 0, 0), (int(position[0]), int(position[1])), 10)

# Draw buttons
# Draw additional buttons for missile types
def draw_buttons():
    # Launch Missile Type Buttons
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, 100, 40))  # Fast missile button
    pygame.draw.rect(screen, (0, 255, 0), (200, 50, 100, 40))  # Slow missile button
    pygame.draw.rect(screen, (0, 0, 255), (350, 50, 100, 40))  # Explosive missile button

    # Draw button text
    fast_text = font.render("Fast", True, (0, 0, 0))
    slow_text = font.render("Slow", True, (0, 0, 0))
    explosive_text = font.render("Explosive", True, (0, 0, 0))

    screen.blit(fast_text, (70, 55))
    screen.blit(slow_text, (220, 55))
    screen.blit(explosive_text, (370, 55))

# Check if missile launch button is clicked
def check_button_click(pos):
    x, y = pos
    if 50 <= x <= 150 and 50 <= y <= 90:  # Fast missile button
        return 'fast'
    elif 200 <= x <= 300 and 50 <= y <= 90:  # Slow missile button
        return 'slow'
    elif 350 <= x <= 450 and 50 <= y <= 90:  # Explosive missile button
        return 'explosive'
    return None

# Launch new missile of specified type
def launch_missile(missile_type, missiles):
    start_x = random.randint(0, SCREEN_WIDTH)
    start_y = 0
    target_x, target_y = RADAR_POSITION
    missile = Missile(start_x, start_y, target_x, target_y, missile_type)
    missiles.append(missile)
    missile_sound.play()  # Play missile launch sound
    print(f"{missile_type} missile launched!")

# Simulation loop
def main_simulation():
    missiles = []  # List of missiles in flight
    radar = Radar(*RADAR_POSITION)
    game_speed = 1
    score = 0
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_action = check_button_click(event.pos)
                if button_action == 'fast':
                    launch_missile(MISSILE_TYPES["fast"], missiles)
                elif button_action == 'slow':
                    launch_missile(MISSILE_TYPES["slow"], missiles)
                elif button_action == 'explosive':
                    launch_missile(MISSILE_TYPES["explosive"], missiles)

        if not paused:
            screen.fill((0, 0, 0))  # Clear the screen

            radar.draw_radar()
            radar.detect_and_launch(missiles)

            for missile in missiles.copy():
                missile.update_position()
                if missile.is_at_target():
                    missiles.remove(missile)  # Remove missile if it hits the target
                radar.detect_and_launch(missiles)

            intercepted_missiles = radar.update_interceptors(missiles)
            for missile in intercepted_missiles:
                missiles.remove(missile)  # Remove intercepted missiles
                score += 1  # Increase score

            # Draw missiles
            for missile in missiles:
                pygame.draw.circle(screen, missile.color, (int(missile.x), int(missile.y)), missile.size)

            # Draw interceptors
            for interceptor in radar.interceptors:
                pygame.draw.circle(screen, (0, 255, 0), (int(interceptor.x), int(interceptor.y)), 5)

            # Draw explosions for intercepted missiles
            for missile in intercepted_missiles:
                draw_explosion((missile.x, missile.y))

            # Draw buttons and score
            draw_buttons()
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (650, 20))

        pygame.display.flip()
        clock.tick(FRAME_RATE)

    pygame.quit()

# Run the simulation
main_simulation()

