import sys
import pygame
import requests
import tkinter as tk
from PIL import Image
from io import BytesIO


def spn_find(t):
    return [str(abs(float(t['lowerCorner'].split()[0]) - float(t['upperCorner'].split()[0]))),
            str(abs(float(t['lowerCorner'].split()[1]) - float(t['upperCorner'].split()[1])))]


toponym_to_find = input()

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get("http://geocode-maps.yandex.ru/1.x/", params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

spn = spn_find(toponym['boundedBy']['Envelope'])

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(spn),
    "l": "map"
}

response = requests.get("http://static-maps.yandex.ru/1.x/", params=map_params)

# Image.open(BytesIO(response.content)).show()

pygame.init()
running = True
size = 600, 485
pygame.display.set_caption('Поисковик')
while running:
    pygame.display.set_mode(size).blit(pygame.image.load(BytesIO(response.content)), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                spn = list(map(lambda x: str(float(x) * 2/3), spn))
            else:
                spn = list(map(lambda x: str(float(x) * 1.5), spn))
            map_params = {
                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                "spn": ",".join(spn),
                "l": "map"
            }
            response = requests.get("http://static-maps.yandex.ru/1.x/", params=map_params)
        pygame.display.update()
