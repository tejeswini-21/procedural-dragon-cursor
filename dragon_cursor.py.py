import pygame
import sys
import math

# Initialize Pygame canvas
pygame.init()
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Skeleton Dragon Chase")
clock = pygame.time.Clock()

# KEEP THE STANDARD CURSOR VISIBLE
pygame.mouse.set_visible(True)

# Spine configuration
SEGMENT_COUNT = 32
target_dist = 11

# Initialize coordinates at screen center
mx, my = WIDTH // 2, HEIGHT // 2
segments = [[mx, my] for _ in range(SEGMENT_COUNT)]


def update_dragon_spine(target_x, target_y):
    """Calculates dragging chain physics down the central spine."""
    segments[0] = [target_x, target_y]
    for i in range(1, SEGMENT_COUNT):
        leader = segments[i - 1]
        follower = segments[i]

        dx = leader[0] - follower[0]
        dy = leader[1] - follower[1]
        distance = math.hypot(dx, dy)

        if distance > target_dist and distance > 0:
            ratio = target_dist / distance
            follower[0] = leader[0] - dx * ratio
            follower[1] = leader[1] - dy * ratio


def draw_skeleton_leg(screen, shoulder_pos, hip_angle, side_sign, size_scale):
    """Draws a multi-jointed leg and claw branching from the spine."""
    # Joint lengths
    upper_leg = 45 * size_scale
    lower_leg = 40 * size_scale

    # Calculate knee position using perpendicular angles
    knee_angle = hip_angle + (math.pi / 2.5) * side_sign
    knee_x = shoulder_pos[0] + math.cos(knee_angle) * upper_leg
    knee_y = shoulder_pos[1] + math.sin(knee_angle) * upper_leg

    # Calculate ankle position bending back down
    ankle_angle = knee_angle - (math.pi / 1.8) * side_sign
    ankle_x = knee_x + math.cos(ankle_angle) * lower_leg
    ankle_y = knee_y + math.sin(ankle_angle) * lower_leg

    # Draw leg structural limbs
    pygame.draw.line(screen, (255, 255, 255), (int(shoulder_pos[0]), int(shoulder_pos[1])), (int(knee_x), int(knee_y)),
                     2)
    pygame.draw.line(screen, (255, 255, 255), (int(knee_x), int(knee_y)), (int(ankle_x), int(ankle_y)), 2)

    # Draw 3 structural sharp claw tips (fingers) spreading out from the ankle
    claw_angles = [-0.3, 0, 0.3]
    claw_length = 15 * size_scale
    for c_ang in claw_angles:
        f_angle = ankle_angle + c_ang + (0.2 * side_sign)
        fx = ankle_x + math.cos(f_angle) * claw_length
        fy = ankle_y + math.sin(f_angle) * claw_length
        pygame.draw.line(screen, (255, 255, 255), (int(ankle_x), int(ankle_y)), (int(fx), int(fy)), 1)


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gather Real-Time Input Details
    mx, my = pygame.mouse.get_pos()

    # Process Dragging Math Logic
    update_dragon_spine(mx, my)

    # Render Screen Layer (Pure Black Canvas)
    screen.fill((0, 0, 0))

    # Loop over the spine to draw ribs, legs, and tail anchors
    for i in range(SEGMENT_COUNT - 1, -1, -1):
        pos = segments[i]

        # Calculate angle of this segment relative to the next one
        if i < SEGMENT_COUNT - 1:
            next_pos = segments[i + 1]
            dx = next_pos[0] - pos[0]
            dy = next_pos[1] - pos[1]
            angle = math.atan2(dy, dx)

            # Connect the backbone string line
            pygame.draw.line(screen, (255, 255, 255), (int(pos[0]), int(pos[1])), (int(next_pos[0]), int(next_pos[1])),
                             2)
        else:
            if i > 0:
                prev_pos = segments[i - 1]
                angle = math.atan2(pos[1] - prev_pos[1], pos[0] - prev_pos[0])
            else:
                angle = 0

        # Draw Multi-Segment Arrow Ribs (Tapering smaller towards the tail tip)
        if 2 < i < SEGMENT_COUNT - 4:
            # Curve factor makes ribs sweep backward slightly like your picture
            rib_scale = (SEGMENT_COUNT - i) / SEGMENT_COUNT
            rib_span = max(6, int(35 * rib_scale))

            # Perpendicular angle vector for left and right rib spans
            perp_angle = angle + math.pi / 2

            # Render left sweeping skeleton rib wire
            rx1 = pos[0] + math.cos(perp_angle) * rib_span + math.cos(angle + math.pi) * (rib_span * 0.4)
            ry1 = pos[1] + math.sin(perp_angle) * rib_span + math.sin(angle + math.pi) * (rib_span * 0.4)
            pygame.draw.line(screen, (255, 255, 255), (int(pos[0]), int(pos[1])), (int(rx1), int(ry1)), 1)

            # Render right sweeping skeleton rib wire
            rx2 = pos[0] - math.cos(perp_angle) * rib_span + math.cos(angle + math.pi) * (rib_span * 0.4)
            ry2 = pos[1] - math.sin(perp_angle) * rib_span + math.sin(angle + math.pi) * (rib_span * 0.4)
            pygame.draw.line(screen, (255, 255, 255), (int(pos[0]), int(pos[1])), (int(rx2), int(ry2)), 1)

        # Anchor Front Legs near segment index 6
        if i == 6:
            draw_skeleton_leg(screen, pos, angle, 1, 1.0)  # Left front leg
            draw_skeleton_leg(screen, pos, angle, -1, 1.0)  # Right front leg

        # Anchor Back Legs near segment index 18
        if i == 18:
            draw_skeleton_leg(screen, pos, angle, 1, 0.9)  # Left rear leg
            draw_skeleton_leg(screen, pos, angle, -1, 0.9)  # Right rear leg

        # Render the Tail Tip terminal point pointer
        if i == SEGMENT_COUNT - 1:
            pygame.draw.circle(screen, (255, 255, 255), (int(pos[0]), int(pos[1])), 4, 1)

    pygame.display.flip()
    clock.tick(60)

