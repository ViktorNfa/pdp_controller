import pygame
import sys
import os

def main():
    pygame.init()

    # Create a window for displaying the controller image
    screen_width, screen_height = 640, 640
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Xbox One Controller - Button Position Calibration")

    # Load the controller image
    script_dir = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(script_dir, "xbox_controller.png")

    try:
        controller_img = pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f"Could not load image from '{image_path}': {e}")
        pygame.quit()
        sys.exit()

    # If your image is bigger or smaller than the window, you can scale it.
    img_width, img_height = controller_img.get_size()
    if img_width > screen_width or img_height > screen_height:
        # Example: scale down to fit the window
        scale_factor = min(screen_width / img_width, screen_height / img_height)
        new_w = int(img_width * scale_factor)
        new_h = int(img_height * scale_factor)
        controller_img = pygame.transform.scale(controller_img, (new_w, new_h))
        img_width, img_height = new_w, new_h

    # Center the image in the window (optional)
    img_x = (screen_width - img_width) // 2
    img_y = (screen_height - img_height) // 2

    # These are the button names from your xbox_one_mapping:
    # ("A": 0, "B": 1, "X": 2, etc.).
    # We’ll ask you to click each one in sequence.
    button_names = [
        "A",
        "B",
        "X",
        "Y",
        "LB",
        "RB",
        "View(Back)",
        "Menu(Start)",
        "Xbox",
        "LS_Click",
        "RS_Click"
    ]

    # We'll store the clicked positions here
    button_positions = {}

    font = pygame.font.SysFont(None, 32)

    # For each button in sequence, ask user to click on it
    for bname in button_names:
        mapped = False
        while not mapped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Record the click
                    mx, my = pygame.mouse.get_pos()
                    button_positions[bname] = (mx, my)
                    mapped = True

            # Draw background and image
            screen.fill((255, 255, 255))
            screen.blit(controller_img, (img_x, img_y))

            # Render instructions
            text_surf = font.render(
                f"Click on the '{bname}' button location",
                True,
                (0, 0, 0)
            )
            text_x = (screen_width - text_surf.get_width()) // 2
            text_y = 20
            screen.blit(text_surf, (text_x, text_y))

            pygame.display.flip()

    # Once finished, we print out your dictionary in a neat format
    print("\nCalibration complete! Copy/paste the following lines into your script:\n")
    print("button_positions = {")
    for bname, (px, py) in button_positions.items():
        print(f'    "{bname}": ({px}, {py}),')
    print("}")
    print("\n(Use these coordinates in your highlight script.)")

    # Keep the window open so you can see final results (optional)
    print("Close the window to exit.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        screen.blit(controller_img, (img_x, img_y))

        # Show final positions on the screen
        y_off = 20
        for bname, (px, py) in button_positions.items():
            line = font.render(f"{bname}: ({px}, {py})", True, (0, 0, 0))
            screen.blit(line, (20, y_off))
            y_off += 30

            # Optionally, draw a circle where you clicked
            pygame.draw.circle(screen, (255, 0, 0), (px, py), 8)

        pygame.display.flip()

if __name__ == "__main__":
    main()
