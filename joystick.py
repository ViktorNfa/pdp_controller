import pygame
import sys
import os

def main():
    pygame.init()

    # 1) CREATE A DISPLAY
    screen_width, screen_height = 640, 640
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Xbox One Controller Visualizer")

    # 2) LOAD YOUR CONTROLLER IMAGE
    #    Adjust path if needed. Right now, assumes the PNG is in the same folder.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(script_dir, "xbox_controller.png")

    try:
        controller_image = pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f"Could not load image from '{image_path}'. Error: {e}")
        pygame.quit()
        sys.exit()

    # Scale or move your image if needed.
    img_width, img_height = controller_image.get_size()
    if img_width > screen_width or img_height > screen_height:
        # Example: scale it down to fit
        scale_factor = min(screen_width / img_width, screen_height / img_height)
        new_w = int(img_width * scale_factor)
        new_h = int(img_height * scale_factor)
        controller_image = pygame.transform.scale(controller_image, (new_w, new_h))
        img_width, img_height = new_w, new_h

    # Let's center the image in the window
    img_x = (screen_width - img_width) // 2
    img_y = (screen_height - img_height) // 2

    # 3) INITIALIZE JOYSTICK
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No joystick connected!")
        pygame.quit()
        sys.exit()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Using joystick: {joystick.get_name()}")

    # 4) DEFINE YOUR BUTTON / AXIS / HAT MAPPINGS
    xbox_one_mapping = {
        "A": 0,
        "B": 1,
        "X": 2,
        "Y": 3,
        "LB": 4,
        "RB": 5,
        "View(Back)": 6,
        "Menu(Start)": 7,
        "Xbox": 8,
        "LS_Click": 9,
        "RS_Click": 10
    }

    xbox_one_axes = {
        "LX": 0,
        "LY": 1,
        "LT": 2,
        "RX": 3,
        "RY": 4,
        "RT": 5
    }

    # If you want to observe D-pad hats:
    xbox_one_hats = {
        "right": (1, 0),
        "left": (-1, 0),
        "up": (0, 1),
        "down": (0, -1)
    }

    # 5) USE YOUR CALIBRATED BUTTON POSITIONS (from calibrate_joy.py output)
    button_positions = {
        "A": (458, 333),
        "B": (496, 297),
        "X": (424, 296),
        "Y": (458, 261),
        "LB": (182, 205),
        "RB": (456, 206),
        "View(Back)": (282, 297),
        "Menu(Start)": (360, 297),
        "Xbox": (322, 240),
        "LS_Click": (184, 294),
        "RS_Click": (392, 373),
    }

    # 6) DEFINE STICK CENTERS & RADIUS FOR YOUR IMAGE
    #    Adjust these so the green dot lines up with the actual stick in the PNG.
    left_stick_center = button_positions["LS_Click"]  # an easy way is to start from LS_Click
    right_stick_center = button_positions["RS_Click"]  # same for RS_Click
    # But these "click" positions might not be exactly center. If that doesn't look right,
    # give them custom coordinates:
    # left_stick_center = (200, 300)
    # right_stick_center = (400, 300)

    stick_radius = 30  # how far from center the green dot can move visually

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 7) DRAW THE BACKGROUND AND YOUR CONTROLLER IMAGE
        screen.fill((255, 255, 255))
        screen.blit(controller_image, (img_x, img_y))

        # 8) CHECK EACH BUTTON AND HIGHLIGHT IF PRESSED
        for bname, bindex in xbox_one_mapping.items():
            if joystick.get_button(bindex):
                if bname in button_positions:
                    (bx, by) = button_positions[bname]
                    pygame.draw.circle(screen, (255, 0, 0), (bx, by), 15)

        # 9) READ THE AXES FOR STICKS & TRIGGERS
        lx = joystick.get_axis(xbox_one_axes["LX"])
        ly = joystick.get_axis(xbox_one_axes["LY"])
        rx = joystick.get_axis(xbox_one_axes["RX"])
        ry = joystick.get_axis(xbox_one_axes["RY"])
        lt = joystick.get_axis(xbox_one_axes["LT"])  # might be 0..1 or -1..1
        rt = joystick.get_axis(xbox_one_axes["RT"])  # might be 0..1 or -1..1

        # Position of left stick's green dot
        left_stick_pos = (
            left_stick_center[0] + int(lx * stick_radius),
            left_stick_center[1] + int(ly * stick_radius)
        )
        pygame.draw.circle(screen, (0, 255, 0), left_stick_pos, 8)

        # Position of right stick's green dot
        right_stick_pos = (
            right_stick_center[0] + int(rx * stick_radius),
            right_stick_center[1] + int(ry * stick_radius)
        )
        pygame.draw.circle(screen, (0, 255, 0), right_stick_pos, 8)

        # 10) READ AND SHOW HAT (D-PAD) STATE
        # Many Xbox One controllers have 1 hat with values like (0,0), (1,0), (-1,0), (0,1), (0,-1).
        # Just to display them as text:
        hat_count = joystick.get_numhats()
        hat_text_lines = []
        for i in range(hat_count):
            hat_val = joystick.get_hat(i)
            hat_text_lines.append(f"Hat {i} = {hat_val}")

        # 11) (OPTIONAL) DRAW SOME DEBUG TEXT
        trigger_text = f"LT={lt:.2f}, RT={rt:.2f}"
        stick_text = f"L=({lx:.2f},{ly:.2f}), R=({rx:.2f},{ry:.2f})"
        debug_surf1 = font.render(trigger_text, True, (0, 0, 0))
        debug_surf2 = font.render(stick_text, True, (0, 0, 0))

        screen.blit(debug_surf1, (10, 10))
        screen.blit(debug_surf2, (10, 35))

        # Show any hat messages
        y_offset = 60
        for line in hat_text_lines:
            surf = font.render(line, True, (0,0,0))
            screen.blit(surf, (10, y_offset))
            y_offset += 25

        # 12) UPDATE THE DISPLAY
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
