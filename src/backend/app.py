from api import Api
import webview

window = webview.create_window('Woah dude!', 'https://pywebview.flowrl.com', js_api=Api())
webview.start(debug=True)