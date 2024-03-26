import pygame
import random
import math

# Variables to track progress and scores
current_level = 1
best_score = 0

# Defining each level and increasing the speed and frequency of enemies(the lower the enemy frenquency the more frequent the enemies become)
LEVELS = [
    {"ENEMY_SPEED": 1, "ENEMY_FREQUENCY": 100},  # Level 1
    {"ENEMY_SPEED": 1.5, "ENEMY_FREQUENCY": 90},  # Level 2
    {"ENEMY_SPEED": 2, "ENEMY_FREQUENCY": 80},  # level 3
    {"ENEMY_SPEED": 2.5, "ENEMY_FREQUENCY": 70},  # level 4
    {"ENEMY_SPEED": 3, "ENEMY_FREQUENCY": 60},  # level 5
    {"ENEMY_SPEED": 3.5, "ENEMY_FREQUENCY": 50},  # level 6
    {"ENEMY_SPEED": 4, "ENEMY_FREQUENCY": 40},  # level 7
    {"ENEMY_SPEED": 4.5, "ENEMY_FREQUENCY": 35},  # level 8
    {"ENEMY_SPEED": 4.5, "ENEMY_FREQUENCY": 30},  # level 9
    {"ENEMY_SPEED": 5, "ENEMY_FREQUENCY": 25},  # level 10
]
pygame.init()


# Functional Variables(Changes these per your needs)
SCREEN_WIDTH, SCREEN_HEIGHT = 1250, 750
ROCKET_SCALE = (100, 100)
ENEMY_SCALE = (81, 110)
MISSILE_SCALE = (50, 50)
STAR_COUNT = 200
STAR_SPEED = 7
ROCKET_SPEED = 5
ENEMY_SPEED = LEVELS[current_level - 1]["ENEMY_SPEED"]
MISSILE_SPEED = 3
ENEMY_FREQUENCY = LEVELS[current_level - 1]["ENEMY_FREQUENCY"]
MAX_LEVELS = 10
SCORE_TO_ADVANCE = 50
score = 0
current_level = 1
player = None
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Ops")


# Uploading game images and characters
rocket_image = pygame.transform.scale(
    pygame.image.load("./images/rocket2.png"), ROCKET_SCALE
)

missile_image = pygame.transform.scale(
    pygame.image.load("./images/missile.png"), MISSILE_SCALE
)

background_image = pygame.transform.scale(
    pygame.image.load("./images/background1.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)


# Sprite groups for different enemies and functionalities
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group()
bullets = pygame.sprite.Group()
homing_enemies = pygame.sprite.Group()


# Using a list comprehension to create a list of stars where each star is represented as a dictionary and it's the key(pos) is given a random height and width
stars = [
    {"pos": [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]}
    for _ in range(STAR_COUNT)
]


# Rocket class with movement and animations
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.transform.scale(
                pygame.image.load("./images/rocket1.png"), ROCKET_SCALE
            ),
            pygame.transform.scale(
                pygame.image.load("./images/rocket2.png"), ROCKET_SCALE
            ),
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - ROCKET_SCALE[1])
        )

        # Rocket movement functionalities
        self.speed = ROCKET_SPEED
        self.animation_time = pygame.time.get_ticks()
        self.animation_speed = 50
        self.last_fired = 0
        self.vx = 0
        self.vy = 0
        self.acceleration = 1.2

    # Creating animation
    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.animation_time > self.animation_speed:
            self.animation_time = now
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

    def update(self):
        self.animate()
        keys = pygame.key.get_pressed()

        # Adjusting the velocity based on the keys presses
        if keys[pygame.K_LEFT]:
            self.vx -= self.acceleration
        if keys[pygame.K_RIGHT]:
            self.vx += self.acceleration
        if keys[pygame.K_UP]:
            self.vy -= self.acceleration
        if keys[pygame.K_DOWN]:
            self.vy += self.acceleration

        # Adjustments to make the rocket more or less slippery
        self.vx *= 0.90
        self.vy *= 0.90

        # Updating the position with velocity
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Keeping the rocket from moving off screen
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vx = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.vy = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vy = 0

        self.last_fired += clock.get_time()

    def add_score(self, points):
        global score
        score += points


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Randomly determine the scale for this enemy instance
        scale_width = random.randint(60, 120)
        SCale_height = random.randint(80, 180)
        self.color = "blue"
        # Uploading images for animation
        self.images = [
            pygame.transform.scale(pygame.image.load("./images/1.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/2.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/3.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/4.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/5.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/6.png"), ENEMY_SCALE),
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(
            x=random.randint(0, SCREEN_WIDTH - ENEMY_SCALE[0]), y=-ENEMY_SCALE[1]
        )

        # Assign a random speed to each enemy within a range, for example 1 to 5
        self.speed = random.randint(1, 10)

        self.animation_time = pygame.time.get_ticks()
        self.animation_interval = 50

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.animation_time > self.animation_interval:
            self.animation_time = now
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

    def update(self):
        self.animate()
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()
        self.color = "pink"
        self.target = target  # The target (Rocket) that the enemy will follow
        self.images = [
            pygame.transform.scale(pygame.image.load("./images/e1.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/e2.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/e3.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/e4.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/e5.png"), ENEMY_SCALE),
            pygame.transform.scale(pygame.image.load("./images/e6.png"), ENEMY_SCALE),
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(
            x=random.randint(0, SCREEN_WIDTH - ENEMY_SCALE[0]), y=-ENEMY_SCALE[1]
        )
        self.speed = random.randint(1, 3)  # Slower speed for homing behavior
        self.animation_time = pygame.time.get_ticks()
        self.animation_interval = 100  # Adjust as needed

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.animation_time > self.animation_interval:
            self.animation_time = now
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

    def update(self):
        self.animate()
        # Calculating the direction towards the target
        dx, dy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
        dist = math.sqrt(dx**2 + dy**2)

        chase_distance = (
            200  # The distance within which the enemy will start chasing the player
        )

        # Check if the player is within the chase distance
        if (
            dist < chase_distance and dist > 0
        ):  # Ensure that the distance is not zero to avoid division by zero
            # Normalize the direction vector and move towards the target
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        else:
            # If the player is not within the chase distance, move down the screen
            self.rect.y += self.speed

        # Kill the sprite if it goes off-screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Point(pygame.sprite.Sprite):
    def __init__(self, pos, value, color, target):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.text = f"+{value}"  # Keep the string representation for rendering
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect(center=pos)
        self.value = value  # Keep the actual value as an integer for scoring
        self.target = target
        self.speed = 10

    def update(self):
        # Calculate the direction vector (dx, dy) towards the target
        dx, dy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        if dist > 0:  # Ensure that the distance is not zero to avoid division by zero
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # Check for collision with the player (rocket)
        if pygame.sprite.collide_rect(self, self.target):
            self.kill()  # Remove the point if it collides with the playe
            self.target.add_score(self.value)  # Add the value to the player's score


# Define the PinkPoint class similar to Point but for pink enemies
class PinkPoint(pygame.sprite.Sprite):
    def __init__(self, pos, value, color, target):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.text = f"+{value}"
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect(center=pos)
        self.value = value
        self.target = target
        self.speed = 10

    def update(self):
        dx, dy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        if dist > 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        if pygame.sprite.collide_rect(self, self.target):
            self.kill()
            self.target.add_score(self.value)


# Define the Missile class
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = missile_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = MISSILE_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# Define the ExplosionParticle class for enemy explosions
class ExplosionParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.size = random.randint(3, 7)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * random.uniform(1, 2)
        self.vy = math.sin(angle) * random.uniform(1, 2)
        self.lifetime = random.randint(30, 60)  # Frames before it disappears

    def update(self):
        self.lifetime -= 1
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.lifetime <= 0:  # Remove the particle when it's "dead"
            self.kill()


class MissileParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255, 255, 255)):  # Default color is white
        super().__init__()
        self.size = random.randint(1, 3)  # Smaller size for missile particles
        self.image = pygame.Surface(
            (self.size, self.size), pygame.SRCALPHA
        )  # Ensure the surface supports alpha
        self.image.fill(color)  # Fill with the specified color
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = random.uniform(-0.5, 0.5)  # Slower velocity for smaller particles
        self.vy = random.uniform(
            -1, -3
        )  # Particles should generally move up to emulate the fuel trail
        self.lifetime = random.randint(10, 30)  # Shorter lifetime for smaller particles

    def update(self):
        self.lifetime -= 1
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.lifetime <= 0:  # Remove the particle when it's "dead"
            self.kill()


def show_home_screen():
    home_running = True
    title_font = pygame.font.SysFont("Arial", 120)
    instruction_font = pygame.font.SysFont("Arial", 50)
    quit_game_font = pygame.font.SysFont("Arial", 50)
    while home_running:
        SCREEN.blit(background_image, (0, 0))
        title_text = title_font.render("S P A C E   O P S", True, (255, 255, 255))
        instruction_text = instruction_font.render("START", True, (255, 255, 255))
        quit_game_text = quit_game_font.render("QUIT", True, (255, 255, 255))

        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5)
        )
        instruction_rect = instruction_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        )
        quit_game_rect = quit_game_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.3)
        )

        SCREEN.blit(title_text, title_rect)
        SCREEN.blit(instruction_text, instruction_rect)
        SCREEN.blit(quit_game_text, quit_game_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Exits the game entirely
            if event.type == pygame.MOUSEBUTTONDOWN:
                home_running = False  # Exits the home screen and starts the game
    return True  # Continues to the game


def create_enemy():
    enemy = Enemy()
    # Increase enemy speed based on level
    enemy.speed += current_level - 1
    all_sprites.add(enemy)
    enemies.add(enemy)


def create_homing_enemy(target):
    homing_enemy = Enemy2(target)
    all_sprites.add(homing_enemy)
    homing_enemies.add(homing_enemy)


# Function to fire a missile with a timer
def fire_missile(x, y, last_fired):
    current_time = pygame.time.get_ticks()
    if current_time - last_fired >= 200:  # missile timer
        missile = Missile(x, y)
        all_sprites.add(missile)
        missiles.add(missile)
        return current_time
    return last_fired


def missile_update_with_particles(missile, particles_group):
    # This function will be called for each missile to update its position and create a trailing particle effect
    missile.update()  # Update the missile's position
    for _ in range(1):
        particle = MissileParticle(
            missile.rect.centerx, missile.rect.bottom, color=(204, 38, 8)
        )  # White color for trail
        particles_group.add(particle)


def update_and_draw_stars(screen):
    for star in stars:
        star["pos"][1] += STAR_SPEED
        if star["pos"][1] > SCREEN_HEIGHT:
            star["pos"][1] = 0
            star["pos"][0] = random.randint(0, SCREEN_WIDTH)
        pygame.draw.circle(screen, (255, 255, 255), star["pos"], 2)


def check_level_advance(player):
    global score, current_level, best_score
    if score >= SCORE_TO_ADVANCE * current_level and current_level < MAX_LEVELS:
        # Before advancing the level, compare and update best_score if necessary
        if score > best_score:
            best_score = score

        current_level += 1

        # Reset score to match best_score
        score = best_score

        # Display Level Advancement Notification
        notification_text = f"Next Level: {current_level}"
        notification_display = notification_text.render(
            notification_text, True, (255, 255, 255)
        )
        notification_rect = notification_display.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        SCREEN.blit(notification_display, notification_rect)
        pygame.display.update()
        pygame.time.wait(2000)  # Pause to display notification

        # Update level settings such as enemy speed and frequency
        ENEMY_SPEED = LEVELS[current_level - 1]["ENEMY_SPEED"]
        ENEMY_FREQUENCY = LEVELS[current_level - 1]["ENEMY_FREQUENCY"]

        reset_game(player)


def reset_game(player):
    global score, best_score
    # Reset the player position and clear enemies and missiles
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - ROCKET_SCALE[1] // 2)

    for enemy in enemies:
        enemy.kill()

    for missile in missiles:
        missile.kill()

    for homing_enemy in homing_enemies:
        homing_enemy.kill()

    # Reset the score to 0 but keep the best score intact
    score = 0


PARTICLES_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLES_EVENT, 40)


def main():
    global score, best_score, current_level, ENEMY_SPEED, ENEMY_FREQUENCY
    if not show_home_screen():
        return
    player = Rocket()
    all_sprites.add(player)
    font = pygame.font.SysFont(None, 40)
    particles = pygame.sprite.Group()  # Group to hold particles
    clock = pygame.time.Clock()
    running = True
    enemy_spawn_timer = 0
    homing_enemy_spawn_timer = 0  # Separate timer for homing enemies
    last_missile_fired = 0  # Time when the last missile was fired

    while running:
        clock.tick(60)
        enemy_spawn_timer += 4
        homing_enemy_spawn_timer += 2
        for point in pygame.sprite.spritecollide(player, all_sprites, False):
            if isinstance(point, Point):
                score += point.value
                point.kill()

        for missile in missiles:
            missile_update_with_particles(missile, particles)

        # Level advancement and notification
        while score >= SCORE_TO_ADVANCE * current_level and current_level < MAX_LEVELS:
            current_level += 1
            ENEMY_SPEED = LEVELS[current_level - 1]["ENEMY_SPEED"]
            ENEMY_FREQUENCY = LEVELS[current_level - 1]["ENEMY_FREQUENCY"]

            # Display Level Advancement Notification
            notification_text = f"Next Level: {current_level}"
            notification_display = font.render(notification_text, True, (255, 255, 255))
            notification_rect = notification_display.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            SCREEN.blit(notification_display, notification_rect)
            pygame.display.update()
            pygame.time.wait(2000)  # Pause to display notification

            reset_game(player)

        particles.update()

        if score >= SCORE_TO_ADVANCE * current_level and current_level < MAX_LEVELS:
            current_level += 1
        ENEMY_SPEED = LEVELS[current_level - 1]["ENEMY_SPEED"]
        ENEMY_FREQUENCY = LEVELS[current_level - 1]["ENEMY_FREQUENCY"]

        # Inputs and quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                last_missile_fired = fire_missile(
                    player.rect.centerx, player.rect.top, last_missile_fired
                )

        if enemy_spawn_timer >= ENEMY_FREQUENCY:
            create_enemy()
            enemy_spawn_timer = 0

        if homing_enemy_spawn_timer >= ENEMY_FREQUENCY * 2:
            create_homing_enemy(player)
            homing_enemy_spawn_timer = 0

        all_sprites.update()
        # Define color and value maps
        color_map = {
            "blue": (52, 235, 229),
            "pink": (255, 192, 203),
        }  # RGB colors for blue and pink
        value_map = {"blue": 0.5, "pink": 1}  # Points for blue and pink

        # Check for missile collisions with normal enemies and create blue explosion particles
        missile_hits = pygame.sprite.groupcollide(missiles, enemies, True, True)
        for missile, hit_enemies in missile_hits.items():
            for enemy in hit_enemies:
                hit_pos_x, hit_pos_y = (
                    enemy.rect.centerx,
                    enemy.rect.centery,
                )  # Assign the center coordinates of the enemy
                color = color_map.get(
                    enemy.color, (255, 255, 255)
                )  # Default to white if color not found

                # Create a point at the enemy's position with the determined color and value
                dropped_point = Point(
                    enemy.rect.center, value_map[enemy.color], color, player
                )  # Blue color for blue enemies
                all_sprites.add(dropped_point)

            # Create explosion particles (adjust color as needed)
            for _ in range(20):
                explosion_particle = ExplosionParticle(hit_pos_x, hit_pos_y, color)
                particles.add(explosion_particle)
                all_sprites.add(explosion_particle)

            # Update the score for each normal enemy hit
            score += value_map[enemy.color]
            if score > best_score:
                best_score = score

        # Check for missile collisions with homing enemies and create pink explosion particles
        homing_missile_hits = pygame.sprite.groupcollide(
            missiles, homing_enemies, True, True
        )
        for missile, hit_homing_enemies in homing_missile_hits.items():
            for homing_enemy in hit_homing_enemies:
                hit_pos_x, hit_pos_y = (
                    homing_enemy.rect.centerx,
                    homing_enemy.rect.centery,
                )  # Assign the center coordinates of the enemy
                color = color_map.get(
                    homing_enemy.color, (255, 255, 255)
                )  # Use pink color for homing enemies

                # Create a pink point at the homing enemy's position with the determined value
                dropped_point = PinkPoint(
                    homing_enemy.rect.center,
                    value_map[homing_enemy.color],
                    color,
                    player,
                )  # Pink color for pink enemies
                all_sprites.add(dropped_point)

            # Create pink explosion particles
            for _ in range(20):
                explosion_particle = ExplosionParticle(hit_pos_x, hit_pos_y, color)
                particles.add(explosion_particle)
                all_sprites.add(explosion_particle)

            # Update the score for each homing enemy hit
            score += value_map[homing_enemy.color]  # This adds the value to score
            if score > best_score:  # Update best_score if current score is higher
                best_score = score

        # Check for collisions with the player and create white explosion particles
        if pygame.sprite.spritecollide(
            player, enemies, True
        ) or pygame.sprite.spritecollide(player, homing_enemies, True):
            reset_game(player)

        # Drawing section
        SCREEN.fill((0, 0, 0))
        update_and_draw_stars(SCREEN)
        all_sprites.draw(SCREEN)
        particles.draw(SCREEN)  # Draw particles
        particles.update()  # Update particles each frame
        bullets.update()
        bullets.draw(SCREEN)

        score_text = pygame.font.SysFont("Bungee Spice", 60).render(
            f"Score: {score}", True, (255, 255, 255)
        )
        best_score_text = pygame.font.SysFont(None, 60).render(
            f"Best Score: {best_score}", True, (255, 255, 255)
        )
        current1 = pygame.font.SysFont(None, 60).render(
            f"Level: {current_level}", True, (255, 255, 255)
        )
        lvl1 = pygame.font.SysFont(None, 15).render(
            f"lvl 1 - (48 - 52)", True, (255, 255, 255)
        )
        lvl2 = pygame.font.SysFont(None, 15).render(
            f"lvl 2 - (98 - 102)", True, (255, 255, 255)
        )
        lvl3 = pygame.font.SysFont(None, 15).render(
            f"lvl 3 - (148 - 152)", True, (255, 255, 255)
        )
        lvl4 = pygame.font.SysFont(None, 15).render(
            f"lvl 4 - (198 - 202)", True, (255, 255, 255)
        )
        lvl5 = pygame.font.SysFont(None, 15).render(
            f"lvl 5 - (248 - 252)", True, (255, 255, 255)
        )
        lvl6 = pygame.font.SysFont(None, 15).render(
            f"lvl 6 - (298 - 302)", True, (255, 255, 255)
        )
        lvl7 = pygame.font.SysFont(None, 15).render(
            f"lvl 7 - (348 - 352)", True, (255, 255, 255)
        )
        lvl8 = pygame.font.SysFont(None, 15).render(
            f"lvl 8 - (398 - 402)", True, (255, 255, 255)
        )
        lvl9 = pygame.font.SysFont(None, 15).render(
            f"lvl 9 - (448 - 452)", True, (255, 255, 255)
        )
        lvl10 = pygame.font.SysFont(None, 15).render(
            f"lvl 10 - (498 - 502)", True, (255, 255, 255)
        )

        SCREEN.blit(score_text, (10, 10))  # Adjust position as needed
        SCREEN.blit(best_score_text, (10, 50))  # Displaying it below current score
        SCREEN.blit(current1, (10, 100))
        SCREEN.blit(lvl1, (10, 200))
        SCREEN.blit(lvl2, (10, 220))
        SCREEN.blit(lvl3, (10, 240))
        SCREEN.blit(lvl4, (10, 260))
        SCREEN.blit(lvl5, (10, 280))
        SCREEN.blit(lvl6, (10, 300))
        SCREEN.blit(lvl7, (10, 320))
        SCREEN.blit(lvl8, (10, 340))
        SCREEN.blit(lvl9, (10, 360))
        SCREEN.blit(lvl10, (10, 380))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
