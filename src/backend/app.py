import webview
#import cryptography # type: ignore


def handler():
  print(f'There are {len(webview.windows)} windows')
  print(f'Active window: {webview.active_window()}')  

   


def on_closing():
    print("Such devastation... this was NOT my intention")



#print(os.getcwd())
window = webview.create_window('Communiko', '../frontend/index.html')
window.events.closing += on_closing
webview.start()


pass