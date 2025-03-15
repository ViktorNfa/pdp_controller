import pygame
import sys
import os
import time

# Evdev imports for force-feedback
from evdev import InputDevice, ff, ecodes

###################################
# Set your event device here:
###################################
EVENT_DEVICE_PATH = "/dev/input/event7"

def vibrate_strong():
    """
    Example of a 'strong rumble' effect, playing the large motor at full magnitude.
    """
    try:
        dev = InputDevice(EVENT_DEVICE_PATH)
    except OSError as e:
        print(f"Could not open {EVENT_DEVICE_PATH}: {e}")
        return
    
    # Strong rumble = strong_magnitude=0xFFFF, weak_magnitude=0
    effect = ff.Effect(
        ecodes.FF_RUMBLE,
        -1, 
        0,
        ff.Trigger(0, 0),
        ff.Replay(500, 0),  # 0.5 second
        ff.EffectType(
            ff_rumble_effect=ff.Rumble(strong_magnitude=0xFFFF, weak_magnitude=0x0000)
        )
    )

    eid = dev.upload_effect(effect)
    dev.write(ecodes.EV_FF, eid, 1)  # play it once
    time.sleep(0.5)
    dev.erase_effect(eid)


def vibrate_weak():
    """
    Example of a 'weak rumble' effect, playing the smaller motor at full magnitude.
    """
    try:
        dev = InputDevice(EVENT_DEVICE_PATH)
    except OSError as e:
        print(f"Could not open {EVENT_DEVICE_PATH}: {e}")
        return
    
    effect = ff.Effect(
        ecodes.FF_RUMBLE,
        -1, 
        0,
        ff.Trigger(0, 0),
        ff.Replay(500, 0),
        ff.EffectType(
            ff_rumble_effect=ff.Rumble(strong_magnitude=0x0000, weak_magnitude=0xFFFF)
        )
    )

    eid = dev.upload_effect(effect)
    dev.write(ecodes.EV_FF, eid, 1)
    time.sleep(0.5)
    dev.erase_effect(eid)


def vibrate_sine():
    """
    Example of a 'sine wave' periodic effect. This often produces a pulsing or buzzing rumble.
    """
    try:
        dev = InputDevice(EVENT_DEVICE_PATH)
    except OSError as e:
        print(f"Could not open {EVENT_DEVICE_PATH}: {e}")
        return
    
    # A sine wave periodic effect, ~2 seconds
    # Adjust 'magnitude', 'period', etc. as desired.
    effect = ff.Effect(
        ecodes.FF_PERIODIC,
        -1, 
        0,
        ff.Trigger(0, 0),
        ff.Replay(2000, 0),  # 2 seconds
        ff.EffectType(
            ff_periodic_effect=ff.Periodic(
                waveform=ecodes.FF_SINE,
                period=100,      # ms between peaks
                magnitude=0x4000,  # amplitude
                offset=0,
                phase=0,
                envelope=ff.Envelope(
                    attack_length=0, attack_level=0,
                    fade_length=0, fade_level=0
                ),
                custom_len=0,
                custom_data=None
            )
        )
    )

    eid = dev.upload_effect(effect)
    dev.write(ecodes.EV_FF, eid, 1)
    time.sleep(2)
    dev.erase_effect(eid)


def main():
    pygame.init()

    screen_width, screen_height = 640, 640
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Xbox Controller Visualizer + 3 Rumble Buttons")

    # Load controller image
    script_dir = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(script_dir, "xbox_controller.png")
    try:
        controller_image = pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f"Could not load image from '{image_path}': {e}")
        pygame.quit()
        sys.exit()

    img_width, img_height = controller_image.get_size()
    if img_width > screen_width or img_height > screen_height:
        scale_factor = min(screen_width / img_width, screen_height / img_height)
        new_w = int(img_width * scale_factor)
        new_h = int(img_height * scale_factor)
        controller_image = pygame.transform.scale(controller_image, (new_w, new_h))
        img_width, img_height = new_w, new_h

    # Center the image
    img_x = (screen_width - img_width) // 2
    img_y = (screen_height - img_height) // 2

    # Initialize joystick
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No joystick connected!")
        pygame.quit()
        sys.exit()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Using joystick: {joystick.get_name()}")

    # Mappings (same as your code)
    xbox_one_mapping = {
        "A": 0, "B": 1, "X": 2, "Y": 3,
        "LB": 4, "RB": 5, "View(Back)": 6, "Menu(Start)": 7,
        "Xbox": 8, "LS_Click": 9, "RS_Click": 10
    }
    xbox_one_axes = {"LX": 0, "LY": 1, "LT": 2, "RX": 3, "RY": 4, "RT": 5}
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
    left_stick_center = button_positions["LS_Click"]
    right_stick_center = button_positions["RS_Click"]
    stick_radius = 30

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    # 3 rumble buttons
    #  let's arrange them in a row near bottom:
    rumble_buttons = [
        {
            "label": "Strong",
            "pos": (180, 580),
            "radius": 30,
            "callback": vibrate_strong,
        },
        {
            "label": "Weak",
            "pos": (320, 580),
            "radius": 30,
            "callback": vibrate_weak,
        },
        {
            "label": "Sine",
            "pos": (460, 580),
            "radius": 30,
            "callback": vibrate_sine,
        },
    ]

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Check if we clicked inside any of the 3 rumble buttons
                for btn in rumble_buttons:
                    dx = mx - btn["pos"][0]
                    dy = my - btn["pos"][1]
                    if dx*dx + dy*dy <= btn["radius"]**2:
                        print(f"Clicked {btn['label']} Rumble!")
                        btn["callback"]()

        # Draw background + controller
        screen.fill((255, 255, 255))
        screen.blit(controller_image, (img_x, img_y))

        # Draw rumble buttons
        for btn in rumble_buttons:
            pygame.draw.circle(screen, (200, 200, 200), btn["pos"], btn["radius"])
            label_surf = font.render(btn["label"], True, (0, 0, 0))
            label_rect = label_surf.get_rect(center=btn["pos"])
            screen.blit(label_surf, label_rect)

        # Check joystick buttons
        for bname, bindex in xbox_one_mapping.items():
            if joystick.get_button(bindex):
                if bname in button_positions:
                    (bx, by) = button_positions[bname]
                    pygame.draw.circle(screen, (255, 0, 0), (bx, by), 15)

        # Sticks + triggers
        lx = joystick.get_axis(xbox_one_axes["LX"])
        ly = joystick.get_axis(xbox_one_axes["LY"])
        rx = joystick.get_axis(xbox_one_axes["RX"])
        ry = joystick.get_axis(xbox_one_axes["RY"])
        lt = joystick.get_axis(xbox_one_axes["LT"])
        rt = joystick.get_axis(xbox_one_axes["RT"])

        left_stick_pos = (
            left_stick_center[0] + int(lx * stick_radius),
            left_stick_center[1] + int(ly * stick_radius)
        )
        pygame.draw.circle(screen, (0, 255, 0), left_stick_pos, 8)

        right_stick_pos = (
            right_stick_center[0] + int(rx * stick_radius),
            right_stick_center[1] + int(ry * stick_radius)
        )
        pygame.draw.circle(screen, (0, 255, 0), right_stick_pos, 8)

        # Hats
        hat_count = joystick.get_numhats()
        hat_text_lines = []
        for i in range(hat_count):
            hat_val = joystick.get_hat(i)
            hat_text_lines.append(f"Hat {i} = {hat_val}")

        # Debug text
        trigger_text = f"LT={lt:.2f}, RT={rt:.2f}"
        stick_text = f"L=({lx:.2f},{ly:.2f}), R=({rx:.2f},{ry:.2f})"
        debug_surf1 = font.render(trigger_text, True, (0, 0, 0))
        debug_surf2 = font.render(stick_text, True, (0, 0, 0))

        screen.blit(debug_surf1, (10, 10))
        screen.blit(debug_surf2, (10, 35))

        y_offset = 60
        for line in hat_text_lines:
            surf = font.render(line, True, (0, 0, 0))
            screen.blit(surf, (10, y_offset))
            y_offset += 25

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
