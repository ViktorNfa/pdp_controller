import pygame
import sys

def main():
    pygame.init()

    # Set up a small display window
    screen_width, screen_height = 640, 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Xbox Controller Inspector")

    # Initialize joystick
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No joystick connected!")
        pygame.quit()
        sys.exit()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Detected joystick: {joystick.get_name()}")

    # Simple font for text
    font = pygame.font.SysFont(None, 24)

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill background
        screen.fill((0, 0, 0))

        # Collect axis values
        axis_count = joystick.get_numaxes()
        axes = [joystick.get_axis(i) for i in range(axis_count)]

        # Collect button values
        button_count = joystick.get_numbuttons()
        buttons = [joystick.get_button(i) for i in range(button_count)]

        # Collect hat values
        hat_count = joystick.get_numhats()
        hats = [joystick.get_hat(i) for i in range(hat_count)]

        # -- Display results --

        y = 20
        # Axes
        text = font.render(f"Axes ({axis_count}):", True, (255,255,255))
        screen.blit(text, (20, y))
        y += 30
        for i, val in enumerate(axes):
            text = font.render(f"Axis {i}: {val:.3f}", True, (255,255,255))
            screen.blit(text, (40, y))
            y += 20

        y += 10
        # Buttons
        text = font.render(f"Buttons ({button_count}):", True, (255,255,255))
        screen.blit(text, (20, y))
        y += 30
        for i, val in enumerate(buttons):
            text = font.render(f"Button {i}: {val}", True, (255,255,255))
            screen.blit(text, (40, y))
            y += 20

        y += 10
        # Hats (D-pad)
        text = font.render(f"Hats ({hat_count}):", True, (255,255,255))
        screen.blit(text, (20, y))
        y += 30
        for i, val in enumerate(hats):
            text = font.render(f"Hat {i}: {val}", True, (255,255,255))
            screen.blit(text, (40, y))
            y += 20

        pygame.display.flip()

if __name__ == "__main__":
    main()