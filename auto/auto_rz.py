-*- coding: utf-8 -*-


from pywinauto import Application
import SendKeys
import time
from PIL import ImageGrab
from pywinauto import taskbar


app = Application().connect(path=r'C:\Program Files (x86)\TeamViewer\TeamViewer.exe')


taskbar.ClickHiddenSystemTrayIcon("会话管理", exact=True, double=True)


taskbar.SystemTrayIcons.Texts()

app.Maximize()

top_dlg = app.window(title="TeamViewer")
top_dlg.Maximize()
#
top_dlg.Minimize()
top_dlg.Restore()
#
top_dlg.type_keys("123")
#
time.sleep(1)
#
im = ImageGrab.grab()
im.save('F:\\1.jpg', 'jpeg')

top_dlg.type_keys("rz{SPACE}-bye")
top_dlg.type_keys("~")123
describe the window inside Notepad.exe process123
dlg_spec = app.UntitledNotepad
wait till the window is really open
actionable_dlg = dlg_spec.wait('visible')