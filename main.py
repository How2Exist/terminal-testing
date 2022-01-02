from types import TracebackType
import pygame
from vector2 import *
import random
import enum
from lblang import *

pygame.init()

class GameObject:
    def __init__(self, pos, color):
        self.pos = pos
        self.prevPos = Vector2(pos.x, pos.y)
        self.color = color
        self.initialPos = Vector2(self.pos.x, self.pos.y)

    def prevPosUpdate(self):
        self.prevPos = Vector2(self.pos.x, self.pos.y)

class Image:
    def __init__(self, image):
        self.image = pygame.image.load(image)

class Rect(GameObject):
    def __init__(self, pos, size, color, texture = None):
        super().__init__(pos, color)
        self.size = size
        self.texture = texture
        self.topLeft = Vector2(self.pos.x, self.pos.y)
        self.bottomRight = self.pos + self.size

    # =====================================
    def isCollidingWith(self, otherRect):
        if self.topLeft.x < otherRect.bottomRight.x and self.bottomRight.x > otherRect.topLeft.x:
            if self.topLeft.y < otherRect.bottomRight.y and self.bottomRight.y > otherRect.topLeft.y:
                return True

        return False
        
    # =====================================
    def isPointInside(self, point):
        if self.topLeft.x < point.x and self.bottomRight.x > point.x:
            if self.topLeft.y < point.y and self.bottomRight.y > point.y:
                return True

        return False

    # =====================================
    def update(self):
        if self.texture != None:
            screen.blit(self.texture.image, (self.pos.x, self.pos.y))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))

        self.topLeft = Vector2(self.pos.x, self.pos.y)
        self.bottomRight = self.pos + self.size


# ================= circle class =================
class Circle(GameObject):
    def __init__(self, pos, radius, color):
        super().__init__(pos, color)
        self.radius = radius

    def update(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)


# ================= button class =================
class Button:
    def __init__(self, rect):
        self.rect = rect
        self.canPress = True

    def isPressed(self):
        mousePos = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        if not pygame.mouse.get_pressed()[0] and not self.canPress:
            self.canPress = True

        if pygame.mouse.get_pressed()[0]:
            if self.rect.isPointInside(mousePos):
                if self.canPress:
                    self.canPress = False
                    return True

        return False


# ================= font class =================
class Font:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.font = pygame.font.Font(name, size)
 
        
# ================= text class =================
class Text:
    def __init__(self, string, pos, color, font, lineSpacing = 10):
        self.string = str(string).split("\n")
        self.lines = len(self.string)
        self.pos = pos
        self.color = color
        self.font = font
        self.lineSpacing = lineSpacing

    def update(self):
        self.lines = len(self.string)

        yPosOffset = 0

        for line in self.string:
            line = self.font.font.render(line, True, self.color)
            screen.blit(line, (self.pos.x, self.pos.y + yPosOffset))

            yPosOffset += self.font.size + self.lineSpacing
        

# ================= text input class =================
class TextInput:
    def __init__(self, text, rect):
        self.text = text
        self.curLine = 0
        self.rect = rect
        self.button = Button(self.rect)
        self.typing = False

    def textUpdate(self, char, key):
        # simple checks
        if self.typing == False:
            return
        if char == None:
            return

        # enter key
        if key == 13:
            self.curLine += 1
            self.text.string += "\n"
            self.text.string[self.curLine] = self.text.string[self.curLine][:-1]
            return

        # backspace key
        if key == pygame.K_BACKSPACE:
            if len(self.text.string[self.curLine]) <= 0:
                if self.curLine > 0:
                    self.text.string.remove(self.text.string[self.curLine])
                    self.curLine -= 1

            self.text.string[self.curLine] = self.text.string[self.curLine][:-1]
            return
            
        # keys to go up and down in text
        if key == pygame.K_UP:
            if self.curLine > 0:
                self.curLine -= 1
        elif key == pygame.K_DOWN:
            if self.curLine < len(self.text.string) - 1:
                self.curLine += 1

        self.text.string[self.curLine].strip("\n")
        self.text.string[self.curLine] += char

    def update(self):
        if self.button.isPressed():

            # when it gets clicked
            if self.typing:
                self.typing = False
            else:
                self.typing = True

        self.rect.update()
        self.text.update()


# ================= gameobject group class =================
# this may be a little hard to understand, but it's literally just a group of game objects
class GameObjectGroup:
    def __init__(self, pos, gameObjects):
        self.pos = pos
        self.gameObjects = gameObjects

        for gameObject in self.gameObjects:
            gameObject.pos = self.pos + gameObject.initialPos

    def update(self):
        for gameObject in self.gameObjects:
            gameObject.pos = self.pos + gameObject.initialPos
            gameObject.update()

    def prevPosUpdate(self):
        for gameObject in self.gameObjects:
            gameObject.prevPosUpdate()


# ================= trigger class =================
class Trigger:
    def __init__(self, pos1, pos2, listeningGameObjects = []):
        self.pos1 = pos1
        self.pos2 = pos2
        self.rect = Rect(Vector2(self.pos1.x, self.pos1.y), abs(self.pos1 - self.pos2), (0, 255, 0))
        self.activated = False
        self.listeningGameObjects = listeningGameObjects

    def update(self):
        # loop all objects, then if its in the trigger, do smn with it
        for gameObject in self.listeningGameObjects:
            if gameObject.isCollidingWith(self.rect):
                self.activated = True
            else:
                self.activated = False


# ================= scene class =================
class Scene:
    def __init__(self):
        self.gameObjects = []
        self.buttons = []
        self.texts = []
        self.inputTexts = []
        self.triggers = []

    def addObject(self, list, object):
        list.append(object)

    def addObjects(self, list, objects):
        for object in objects:
            list.append(object)

    def removeObject(self, list, object):
        list.remove(object)

    def removeObjects(self, list, objects):
        for object in objects:
            list.remove(object)

    def update(self):
        for gameObject in self.gameObjects:
            gameObject.update()

        for button in self.buttons:
            button.rect.update()

        for text in self.texts:
            text.update()

        for inputText in self.inputTexts:
            inputText.update()

        for trigger in self.triggers:
            trigger.update()

    def textUpdate(self, char, key):
        for inputText in self.inputTexts:
            inputText.textUpdate(char, key)

    def prevPosUpdate(self):
        for gameObject in self.gameObjects:
            gameObject.prevPosUpdate()


# ================= game manager class =================
class GameManager:
    def __init__(self):
        self.scene = None

    def setScene(self, scene):
        self.scene = scene

    def removeScene(self):
        self.scene = Scene()

    def getActiveScene(self):
        return self.scene

    def update(self):
        screen.fill((0, 0, 0))

        self.scene.update()
    
    def prevPosUpdate(self):
        self.scene.prevPosUpdate()

# ======== add custom functions and classes below ========


# ======== pygame variables ========
running = True
framerate = 60
clock = pygame.time.Clock()
screenSize = Vector2(500, 500)
screen = pygame.display.set_mode((screenSize.x, screenSize.y))


# ======== defining regular variables and required variables ========
mainScene = Scene()
gm = GameManager()
gm.setScene(mainScene)


# ======== game objects ========
player = Rect(Vector2(300, 300), Vector2(40, 40), (255, 0, 0))
trigger = Trigger(Vector2(0, 0), Vector2(100, 100), [player])
button = Button(Rect(Vector2(400, 400), Vector2(100, 100), (255, 255, 0)))

mainScene.addObject(mainScene.gameObjects, player)
mainScene.addObject(mainScene.triggers, trigger)
mainScene.addObject(mainScene.buttons, button)

# ======== main loop ========
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            gm.getActiveScene().textUpdate(event.unicode, event.key)

    pressed = pygame.key.get_pressed()
    mousePos = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    gm.prevPosUpdate()
    if pressed[pygame.K_w]: player.pos.y -= 3
    if pressed[pygame.K_a]: player.pos.x -= 3
    if pressed[pygame.K_s]: player.pos.y += 3
    if pressed[pygame.K_d]: player.pos.x += 3

    # debug purposes
    if trigger.activated:
        print("in trigger")

    gm.update()

    pygame.display.update()
    clock.tick(framerate)
