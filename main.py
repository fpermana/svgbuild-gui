# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4.QtGui import QApplication
from ui.MainWindow import MainWindow

from SVGBuild import Settings

def main():
    import sys
    app = QApplication(sys.argv)
    
    settings = Settings.Settings()
    settings.restoreSettings()
    
    wnd = MainWindow()
    wnd.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
