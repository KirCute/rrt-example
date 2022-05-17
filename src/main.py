from frame import World

if __name__ == '__main__':
    world = World()
    world.delay = .02
    world.addPolygon([
        (200, 0),
        (300, 0),
        (300, 400),
        (200, 400)
    ])
    world.addPolygon([
        (500, 200),
        (600, 200),
        (600, 600),
        (500, 600)
    ])
    world.start()
