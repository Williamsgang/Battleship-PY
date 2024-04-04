""" Add more options (marked below)
1024 x 768
1280 x 720 (720p)
1920 x 1080 (1080p)
1366 x 768
800 x 600 """


class Window:
    HEIGHT = 1024
    WIDTH = 728


    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height

    def main_menu(self):
        print("not implemented")

