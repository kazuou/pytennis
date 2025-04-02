
class Object3D:
    def __init__(self, pod):
        self._pos = pos


    def move(self, dx, dy, dz):
        self.x += dx
        self.y += dy
        self.z += dz

    def get_position(self):
        return self.x, self.y, self.z

    def draw(self, screen):
        # サブクラスでオーバーライドする
        pass
