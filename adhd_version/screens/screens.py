# screens/base_screen.py


class Screens:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.SCREEN = screen_manager.SCREEN
        self.log = screen_manager.log

    def handle_events(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError
