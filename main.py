from Gui import Gui
import clipboard
import config

def show_clipboard_text():
    text = clipboard.get_from_clipboard()
    Gui(text, config.DROPDOWN_VALUES, config.TOOLTIPS)

if __name__ == "__main__":
  # Register the context menu for all windows
  # win32gui.EnumWindows(register_context_menu, None)

  show_clipboard_text()
