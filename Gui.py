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

      self.text_from_selection = text

      # Create the main window
      root = tk.Tk()
      root.title("My Window")
      root.geometry("500x500")  # Set the window size to 500x500 pixels
      self.root = root

      # Create a label to display the text
      label = tk.Label(root, text=text, wraplength=450)
      label.pack(pady=10)
      self.input_label = label

      # Label to display the response
      self.response_label_text = tk.StringVar()
      self.response_label = tk.Label(self.root, textvariable=self.response_label_text, wraplength=450)
      self.response_label.pack(pady=10)

      # Create a dropdown menu
      dropdown_selection = tk.StringVar()
      dropdown_selection.set(dropdown_values[0])
      dropdown = tk.OptionMenu(root, dropdown_selection, *dropdown_values)
      dropdown.pack(pady=5)

      # Create a button to trigger an action
      button = tk.Button(root, text="Run", command=lambda: self.run_action(dropdown_selection.get()))
      button.pack(pady=5)

      # Button to copy the text
      self.copy_button = tk.Button(
         self.root, 
         text="Copy Text to Clipboard", 
         command=lambda: clipboard.copy_to_clipboard(self.response_label_text.get())
      )
      self.copy_button.pack(pady=20)

      # Start the Tkinter event loop
      root.mainloop()

   def update_response_section(self, text: str, mode: str):
      if mode == "append":
         current_content = self.response_label_text.get()
         self.response_label_text.set(current_content + text)
      else:
         self.response_label_text.set(text)
      a = 10

    # Define a function to handle the button click
   def run_action(self, prompt_name: str):
      selected_prompt = next((prompt_option["prompt"] for prompt_option in config.PROMPTS if prompt_option["name"] == prompt_name), None)
      prompt =  selected_prompt + "\nThe text is:\n" + self.text_from_selection

      response_generator = OpenAiClient().get_openai_response(prompt)
      self.root.after(0, lambda: self.update_response_section("", "replace"))
      self.process_response(response_generator)

   def process_response(self, response_generator):
        try:
            # Get the next chunk from the generator
            chunk = next(response_generator)

            if len(chunk.choices) and chunk.choices[0].delta.content is not None:
                content_delta = chunk.choices[0].delta.content

                # Schedule the update to the label using after
                self.root.after(0, self.update_response_section, content_delta, "append")

            # Schedule the next call to process the following chunk
            self.root.after(100, self.process_response, response_generator)

        except StopIteration:
            # Generator is exhausted, stop processing
            pass

if __name__ == "__main__":
  # Example usage
  text = "This is some longer sample text"

  """, want to make sure that my model also has something to do here, right?"""
  window = Gui(text, [config["name"] for config in config.PROMPTS])
