import pygame
import time
from graphics import Tree


def mult(x1, y1, x2, y2, x3, y3) -> float:
    return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)


def checkCross(lineA: tuple, lineB: tuple) -> bool:
    if max(lineA[0], lineB[2]) < min(lineB[0], lineB[2]):
        return False
    if max(lineA[1], lineA[3]) < min(lineB[1], lineB[3]):
        return False
    if max(lineB[0], lineB[2]) < min(lineA[0], lineA[2]):
        return False
    if max(lineB[1], lineB[3]) < min(lineA[1], lineA[3]):
        return False
    if (mult(lineB[0], lineB[1], lineA[2], lineA[3], lineA[0], lineA[1])
            * mult(lineA[2], lineA[3], lineB[2], lineB[3], lineA[0], lineA[1]) < 0):
        return False
    if (mult(lineA[0], lineA[1], lineB[2], lineB[3], lineB[0], lineB[1])
            * mult(lineB[2], lineB[3], lineA[2], lineA[3], lineB[0], lineB[1]) < 0):
        return False
    return True


class World:
    def __init__(self):
        self.size = (800, 600)
        pygame.init()
        pygame.display.set_caption('RRT sample')
        self._screen = pygame.display.set_mode(self.size)
        self.origin = (50, 50)
        self.target = (750, 550)
        self.polygon = []
        self.delay = 0.
        self.steep = 60.
        self._tree = Tree(self)

    def addPolygon(self, polygon: tuple) -> None:
        edge = []
        for i in range(-1, len(polygon) - 1):
            edge.append((polygon[i][0], polygon[i][1], polygon[i + 1][0], polygon[i + 1][1]))
        self.polygon.append(edge)

    def start(self):
        process = True
        running = True
        while running:
            self._screen.fill((255, 255, 255))
            if process:
                process = not self._tree.build(self.steep)
            self._render()
            pygame.display.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            time.sleep(self.delay)

    def checkEdgeValid(self, line: tuple) -> bool:
        if line[0] < 0 or line[0] > self.size[0]:
            return False
        if line[1] < 0 or line[1] > self.size[1]:
            return False
        if line[2] < 0 or line[2] > self.size[0]:
            return False
        if line[3] < 0 or line[3] > self.size[1]:
            return False
        for polygon in self.polygon:
            for edge in polygon:
                if checkCross(line, edge):
                    return False
        return True

    def checkNodeValid(self, point: tuple) -> bool:
        if point[0] < 0 or point[0] > self.size[0]:
            return False
        if point[1] < 0 or point[1] > self.size[1]:
            return False
        for polygon in self.polygon:
            count = 0
            for edge in polygon:
                if checkCross(edge, (0, 0, point[0], point[1])):
                    count += 1
            if count % 2 == 1:
                return False
        return True

    def _render(self):
        for polygon in self.polygon:
            for edge in polygon:
                pygame.draw.line(self._screen, (0, 0, 0), (edge[0], edge[1]), (edge[2], edge[3]), 3)
        self._tree.render(self._screen)
        pygame.draw.circle(self._screen, (127, 0, 0), self.origin, 5, 5)
        pygame.draw.circle(self._screen, (127, 0, 0), self.target, 5, 5)
