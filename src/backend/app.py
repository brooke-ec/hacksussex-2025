from logging import NullHandler
from api import Api
import webview
#import cryptography # type: ignore
from os import path
from communiko import CommunikoBookworm


def handler():
  print(f'There are {len(webview.windows)} windows')
  print(f'Active window: {webview.active_window()}')

def logic():
   #reading meesages from pico
   def consumer(input):
      output = input.decode()
      results = output.split(":")
      sender = results[0]
      message = results[1]
      window.evaluate_js(f"addNewMessage('{sender}', '{message}')")
    
         
   bookworm.join(bookworm, consumer)
   

   


def on_closing():
    print("Such devastation... this was NOT my intention")


bookworm = CommunikoBookworm()


#print(os.getcwd())
window = webview.create_window('test', '../frontend/index.html')
window.events.closing += on_closing
webview.start(logic)


pass