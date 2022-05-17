import pygame
import math
import random
from typing import Tuple, Optional


def distanceSqr(pointA: Tuple[float, float], pointB: Tuple[float, float]) -> float:
    return (pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2


def normalize(pointA: Tuple[float, float], pointB: Tuple[float, float], steep: float) -> tuple:
    direction = (pointA[0] - pointB[0]), (pointA[1] - pointB[1])
    dis = math.sqrt(distanceSqr(pointA, pointB))
    steep = 1. if dis < steep else steep / dis
    direction = direction[0] * steep, direction[1] * steep
    return (pointA[0] - direction[0]), (pointA[1] - direction[1])


class Node:
    def __init__(self, pos: Tuple[float, float], parent: Optional['Node']):
        self.pos = pos
        self.toTarget = False
        self.parent = parent
        self.children = []

    def getMinDistance(self, world: 'World', pos: Tuple[float, float], steep: float):
        nxt = normalize(self.pos, pos, steep)
        minPoint = None
        minNxt = None
        minDis = float('inf')
        if world.checkEdgeValid((self.pos[0], self.pos[1], pos[0], pos[1])):
            minPoint = self
            minNxt = nxt
            minDis = distanceSqr(pos, self.pos)
        for child in self.children:
            p, n, d = child.getMinDistance(world, pos, steep)
            if d < minDis:
                minPoint = p
                minNxt = n
                minDis = d
        return minPoint, minNxt, minDis

    def expend(self, pos: Tuple[float, float]):
        child = Node(pos, self)
        self.children.append(child)
        return child

    def render(self, screen: pygame.Surface) -> None:
        for child in self.children:
            color = (127, 0, 127) if child.toTarget else (0, 127, 0)
            pygame.draw.line(screen, color, self.pos, child.pos, 3)
            child.render(screen)
        pygame.draw.circle(screen, (0, 63, 63), self.pos, 5, 5)

    def foundTarget(self) -> None:
        self.toTarget = True
        if self.parent is not None:
            self.parent.foundTarget()


class Tree:
    def __init__(self, world: 'World'):
        self._root = Node(world.origin, None)
        self._world = world

    def build(self, steep: float) -> bool:
        nxt = random.randint(0, self._world.size[0] - 1), random.randint(0, self._world.size[1] - 1)
        while not self._world.checkNodeValid(nxt):
            nxt = random.randint(0, self._world.size[0] - 1), random.randint(0, self._world.size[1] - 1)
        parent, nxt, dis = self._root.getMinDistance(self._world, nxt, steep)
        if parent is not None:
            child = parent.expend(nxt)
            if distanceSqr(nxt, self._world.target) < steep ** 2:
                child.expend(self._world.target).foundTarget()
                return True
        return False

    def render(self, screen: pygame.Surface) -> None:
        self._root.render(screen)
