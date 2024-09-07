import win32clipboard

def get_from_clipboard():
  # set clipboard data
  # win32clipboard.OpenClipboard()
  # win32clipboard.EmptyClipboard()
  # win32clipboard.SetClipboardText('testing 123')
  # win32clipboard.CloseClipboard()

  # get clipboard data
  win32clipboard.OpenClipboard()
  try:
    data = win32clipboard.GetClipboardData()
  except TypeError:
    raise Exception("Could not read data from clipboard. Make sure you have some text there.")
  win32clipboard.CloseClipboard()

  return data

if __name__ == "__main__":
  get_from_clipboard()

  # https://stackoverflow.com/a/101167