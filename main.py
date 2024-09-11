from Gui import Gui
import clipboard
import config

def show_clipboard_text():
    try:
      text = clipboard.get_from_clipboard()
    except Exception as e:
      print("Could not get data from clipboard. Make sure you have some text-like data there.")
      raise e
    Gui(text, [config["name"] for config in config.PROMPTS])

if __name__ == "__main__":
  # Register the context menu for all windows
  # win32gui.EnumWindows(register_context_menu, None)

  show_clipboard_text()
