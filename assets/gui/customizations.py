class Customizations:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager

    def get_background_color(self):
        return self.settings_manager.get_setting('background_color', '#000000')  # Default black

    def get_font_color(self):
        return self.settings_manager.get_setting('font_color', '#00FF00')  # Default green

    def set_background_color(self, color):
        self.settings_manager.update_setting('background_color', color)

    def set_font_color(self, color):
        self.settings_manager.update_setting('font_color', color)
