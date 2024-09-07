import tkinter as tk
import config
from OpenAiClient import OpenAiClient
import clipboard

class Gui():
    def __init__(self, text, dropdown_values):
      """
      Creates a new window with a text, a dropdown, and a button using Tkinter.

      Args:
          text (str): The text to display in the window.
          dropdown_values (list): A list of values for the dropdown.
          tooltips (list): A list of tooltips corresponding to the dropdown values.
      """

      self.text = text

      # Create the main window
      root = tk.Tk()
      root.title("My Window")
      root.geometry("500x500")  # Set the window size to 500x500 pixels

      # Create a label to display the text
      label = tk.Label(root, text=text, wraplength=450)
      label.pack(pady=10)

      # Create a dropdown menu
      variable = tk.StringVar()
      variable.set(dropdown_values[0])
      dropdown = tk.OptionMenu(root, variable, *dropdown_values)
      dropdown.pack(pady=5)

      # Create a button to trigger an action
      button = tk.Button(root, text="Run", command=lambda: self.run_action(variable.get()))
      button.pack(pady=5)

      # Start the Tkinter event loop
      self.root = root
      root.mainloop()
      
    # Define a function to handle the button click
    def run_action(self, prompt_name: str):
      selected_prompt = next((prompt_option["prompt"] for prompt_option in config.PROMPTS if prompt_option["name"] == prompt_name), None)
      prompt =  selected_prompt + "\nThe text is:\n" + self.text

      response, tokens_used = OpenAiClient().get_openai_response(prompt)
      if hasattr(self, "response_label"):
         self.response_label.destroy()

      self.response_label = tk.Label(self.root, text=response + " TOKENS USED: " + str(tokens_used), wraplength=450)
      self.response_label.pack(pady=10)

      if hasattr(self, "copy_button"):
         self.copy_button.destroy()

      self.copy_button = tk.Button(
         self.root, 
         text="Copy Text to Clipboard", 
         command=lambda: clipboard.copy_to_clipboard(response)
      )
      self.copy_button.pack(pady=20)


if __name__ == "__main__":
  # Example usage
  text = "This is a sample text."
  window = Gui(text, [config["name"] for config in config.PROMPTS])
