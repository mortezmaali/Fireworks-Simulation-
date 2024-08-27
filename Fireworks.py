import cv2
import numpy as np
import random
import math
import ctypes

# Get screen resolution using ctypes
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Parameters for fireworks
num_fireworks = 20  # Increase the number of simultaneous fireworks
fireworks = []

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('fireworks_simulation_fullscreen.avi', fourcc, 20.0, (screen_width, screen_height))

# A list of vibrant colors to choose from
color_palette = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (255, 165, 0),   # Orange
    (75, 0, 130),    # Indigo
    (238, 130, 238), # Violet
    (0, 191, 255)    # Deep Sky Blue
]

class Firework:
    def __init__(self):
        self.x = random.randint(100, screen_width - 100)
        self.y = screen_height
        self.explosion_height = random.randint(100, screen_height // 2)
        self.color = random.choice(color_palette)  # Choose a random color from the palette
        self.exploded = False
        self.particles = []
        self.frame_count = 0

    def move_up(self):
        if self.y > self.explosion_height:
            self.y -= 7  # Increase the speed of ascent
        else:
            self.exploded = True
            self.create_particles()

    def create_particles(self):
        if not self.particles:
            num_particles = random.randint(50, 100)  # Increase the number of particles after explosion
            for _ in range(num_particles):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(3, 6)  # Increase the speed of particles
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                self.particles.append([self.x, self.y, vx, vy])

    def update_particles(self):
        for i, particle in enumerate(self.particles):
            particle[0] += particle[2]
            particle[1] += particle[3]
            particle[3] += 0.15  # Increase the gravity effect

            # Draw the particle with a larger radius
            if 0 <= particle[0] < screen_width and 0 <= particle[1] < screen_height:
                cv2.circle(canvas, (int(particle[0]), int(particle[1])), 4, self.color, -1)  # Larger radius for particles

            # Fade out
            if self.frame_count > 40:  # Reduce the lifespan of particles for a faster fade
                self.color = tuple(max(0, c - 7) for c in self.color)
        
        self.frame_count += 1

    def draw(self):
        if not self.exploded:
            cv2.circle(canvas, (self.x, self.y), 8, self.color, -1)  # Larger radius for the firework before explosion
        else:
            self.update_particles()

# Main loop
while True:
    # Clear the canvas
    canvas = np.zeros((screen_height, screen_width, 3), dtype="uint8")

    # Randomly create new fireworks
    if len(fireworks) < num_fireworks and random.random() > 0.90:  # Increase the likelihood of new fireworks
        fireworks.append(Firework())

    # Update and draw each firework
    for firework in fireworks:
        firework.move_up()
        firework.draw()

    # Remove finished fireworks
    fireworks = [fw for fw in fireworks if fw.frame_count <= 80]  # Decrease the total lifespan of fireworks

    # Write the frame to the video file
    out.write(canvas)

    # Display the frame in full screen mode
    cv2.namedWindow("Fireworks Simulation", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Fireworks Simulation", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Fireworks Simulation", canvas)

    # Exit on key press
    if cv2.waitKey(20) & 0xFF == 27:  # ESC key, reduce the delay between frames for faster speed
        break

# Release everything if job is finished
out.release()
cv2.destroyAllWindows()
