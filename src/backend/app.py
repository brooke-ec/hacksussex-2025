from api import Api
import webview
#import cryptography # type: ignore
from os import path


def handler():
  print(f'There are {len(webview.windows)} windows')
  print(f'Active window: {webview.active_window()}')

def logic():
   #window.evaluate_js('C:/Users/jh2046/Documents/GitHub/hacksussex-2025/src/frontend/main.js')
   print("aaa")

def on_closing():
    print("Such devastation... this was NOT my intention")


#print(os.getcwd())
window = webview.create_window('test', '../frontend/index.html')
window.events.closing += on_closing
webview.start(logic)


pass