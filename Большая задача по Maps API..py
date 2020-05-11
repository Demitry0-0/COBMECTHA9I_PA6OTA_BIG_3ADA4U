import pygame
import pygame_gui
import requests
import copy
from io import BytesIO
from PIL import Image

insearch = False


def x(tecx):
    try:
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + tecx + "&format=json"
        response = requests.get(geocoder_request)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return list(map(float, toponym['Point']['pos'].split()))
    except Exception as ex:
        return [1000000000.00000, 100000000.000]


def metka(name, ll, spn, typ, pt=None):
    map_params = {
        "ll": ','.join(list(map(str, ll))),
        "spn": '0,' + str(spn),
        "l": typ
    }
    if pt:
        map_params["pt"] = ','.join(list(map(str, pt))) + ',flag'
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).save(name)


xj = [133.795384, -25.694768]
cur = 0
typ = "sat"
mashtag = 1.0
pygame.init()
pygame.display.set_caption('Привет от Андрея Михайлова')
window_surface = pygame.display.set_mode((1000, 600))
screen = pygame.display.set_mode((1000, 450))
background = pygame.Surface((1000, 600))
pikcha = pygame.Surface((1000, 600))
background.fill(pygame.Color('#000000'))
manager = pygame_gui.UIManager((1000, 600))
ultralist = ['sat', 'map', 'sat,skl']
pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((600, 80), (400, 100)), manager=manager,
                              html_text='')
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 0), (100, 30)),
                                            text='Слой',
                                            manager=manager)
hai_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 0), (100, 30)),
                                          text='Искать',
                                          manager=manager)
ha1i_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 0), (100, 30)),
                                           text='Сброс',
                                           manager=manager)
hai_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, 30), (400, 30)),
                                                  manager=manager)
clock = pygame.time.Clock()
is_running = True

ll = [133.795384, -25.694768]
check = ''
while is_running:
    response = None
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={ll[0]},{ll[1]}&spn=0," + str(
        mashtag) + "&l=" + typ
    time_delta = clock.tick(60) / 1000.0
    if map_request != check:
        response = requests.get(map_request)
        map_file = "map.png"
        if not insearch:
            metka(map_file, ll, mashtag, typ)
        else:
            metka(map_file, ll, mashtag, typ, xj)
        screen.blit(pygame.image.load(map_file), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.__dict__['key'] == 280:
                if mashtag > 0.010:
                    mashtag += 0.09
                elif mashtag > 0.000007:
                    mashtag += 0.0009
            if event.__dict__['key'] == 281:
                if mashtag > 0.011:
                    mashtag -= 0.09
                elif mashtag > 0.00083:
                    mashtag -= 0.0009

            if event.__dict__['key'] == 276:  # left
                ll[0] -= mashtag / 10
            if event.__dict__['key'] == 273:  # up
                ll[1] += mashtag / 10
            if event.__dict__['key'] == 275:  # right
                ll[0] += mashtag / 10
            if event.__dict__['key'] == 274:  # down
                ll[1] -= mashtag / 10
        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == hello_button:
                    cur = (cur + 1) % len(ultralist)
                    typ = ultralist[cur]
                    hello_button.text = typ
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == hello_button:
                    cur = (cur + 1) % len(ultralist)
                    typ = ultralist[cur]
                    hello_button.text = typ
            if event.type == pygame.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    if event.ui_element == hai_button:
                        if x(hai_textbox.text) != [1000000000.00000, 100000000.000]:
                            ll = x(hai_textbox.text)
                            geocoder_request = f'''https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={hai_textbox.text}&format=json'''
                            json_response = requests.get(geocoder_request).json()
                            try:
                                toponym = \
                                    json_response["response"]["GeoObjectCollection"][
                                        "featureMember"][0]["GeoObject"]
                                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"][
                                    "text"]
                                pygame_gui.elements.UITextBox(
                                    relative_rect=pygame.Rect((600, 80), (400, 100)),
                                    manager=manager, html_text=toponym_address)
                            except:
                                pygame_gui.elements.UITextBox(
                                    relative_rect=pygame.Rect((600, 80), (400, 100)),
                                    manager=manager, html_text='Адрес не найден')
                            insearch = True
                            xj = copy.copy(ll)
                        else:
                            hai_textbox.text = 'Такого посёлка нет на етой планете'
                            pygame_gui.elements.UITextBox(
                                relative_rect=pygame.Rect((600, 80), (400, 100)),
                                manager=manager, html_text='')
                            insearch = False
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == ha1i_button:
                    insearch = False
                    outbox = pygame_gui.elements.UITextBox(
                        relative_rect=pygame.Rect((600, 80), (400, 100)),
                        manager=manager, html_text='')
                    response = requests.get(map_request)
                    map_file = "map.png"
                    if not insearch:
                        metka(map_file, ll, mashtag, typ)
                    else:
                        metka(map_file, ll, mashtag, typ, xj)
                    screen.blit(pygame.image.load(map_file), (0, 0))
        manager.process_events(event)
    check = map_request
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    pygame.display.update()
pygame.quit()
