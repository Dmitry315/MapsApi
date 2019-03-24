import requests
import sys
import os
import pygame
try:
    cords = input('Координаты(долгота,широта):')
    zoom = int(input('Масштаб(0-17):'))
except Exception as err:
    print('Ошибка ввода')
    sys.exit(1)
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
counter = 0

api_server = "http://static-maps.yandex.ru/1.x/"
map_file = 'map.png'
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(1)
    params = {
        "ll": cords,
        "z": zoom,
        "l": "map"
    }
    response = requests.get(api_server, params=params)
    with open(map_file, mode='wb') as f:
        f.write(response.content)
    # if keys[pygame.K_PAGEUP]:
    # if keys[pygame.K_PAGEDOWN]:

    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()


pygame.quit()
