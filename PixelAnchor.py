import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import pyperclip

# initialize pygame

pygame.init()
icon = pygame.image.load("Assets/PixelAnchor.ico")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pixel Anchor")
screen = pygame.display.set_mode((1920, 1080))


# variables

clock = pygame.time.Clock()
running = True

text_font = pygame.font.SysFont("Times New Roman", 35)

background = pygame.image.load("Assets/main_menu.png").convert_alpha()
main_menu = True

selected = None

images_list = []

# functions

def pick_image_file():
    root = tk.Tk()
    root.withdraw()
    root.update() 

    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp")
        ]
    )
    return file_path


# main loop

while running:

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            for i in range(len(images_list)-1, -1, -1):
                img, rect, alpha = images_list[i]

                if rect.collidepoint(mouse_x, mouse_y):
                    selected = images_list[i]
                    break
        

        elif event.type == pygame.MOUSEMOTION:
            if selected is not None:
                selected[1].move_ip(event.rel)

        elif event.type == pygame.MOUSEBUTTONUP:
            selected = None

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_l:
                image_path = pick_image_file()
                if image_path:
                    main_menu = False

                    image = pygame.image.load(image_path).convert_alpha()
                    image_rect = image.get_rect()
                    alpha = 255

                    images_list.append([image, image_rect, alpha])
            if event.key == pygame.K_d and selected is not None:
                images_list.remove(selected)
                selected = None

            if event.key == pygame.K_c and selected is not None:
                rect = selected[1]
                coord_text = (rect.x, rect.y)

                pyperclip.copy(coord_text)

            if selected is not None:

                if event.key == pygame.K_UP:
                    selected[2] += 15
                    selected[2] = max(0, min(255, selected[2]))

                elif event.key == pygame.K_DOWN:
                    selected[2] -= 20
                    selected[2] = max(0, min(255, selected[2]))


                if event.key == pygame.K_e:
                    idx = images_list.index(selected)

                    if idx < len(images_list) - 1:
                        images_list[idx], images_list[idx + 1] = images_list[idx + 1], images_list[idx]

                if event.key == pygame.K_q:
                    idx = images_list.index(selected)

                    if idx > 0:
                        images_list[idx], images_list[idx - 1] = images_list[idx - 1], images_list[idx]
            if event.key == pygame.K_x:
                running = False


    screen.fill((0, 0, 0))

    if main_menu:
        screen.blit(background, (0, 0))

    for img, rect, alpha in images_list:
        img.set_alpha(alpha)
        screen.blit(img, rect)

    if selected is not None:
        x, y = selected[1].topleft

        coord_text = f"x: {x}, y: {y}"
        text_surface = text_font.render(coord_text, True, (255, 255, 255))

        screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
