import dearpygui.dearpygui as dpg

dpg.create_context()

class MyApp:

    def __init__(self):
        dpg.create_viewport(title="SomeTitle", width=600, height=400)
        self.setup()

    def setup(self):
        with dpg.window(label="Primary Window", tag="primary_window"):
            dpg.add_text("Hello, world!")
            dpg.add_button(label="Click me")

            # Создание второго окна
        with dpg.window(label="Secondary Window", tag="secondary_window", pos=(350, 100)):
            dpg.add_text("This is the second window")
            dpg.add_button(label="Press me")

        # Установите primary_window в качестве основного окна
        dpg.set_primary_window("primary_window", True)

    def run(self):
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

if __name__ == '__main__':
    app = MyApp()
    app.run()