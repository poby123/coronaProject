from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from pathlib import Path
import sys

# if __name__ == "__main__":

#     app = QApplication(sys.argv)

#     playlist = QMediaPlaylist()
#     url = QUrl.fromLocalFile("./helloKO.mp3")
#     playlist.addMedia(QMediaContent(url))
#     # playlist.setPlaybackMode(QMediaPlaylist.Loop)

#     player = QMediaPlayer()
#     player.setPlaylist(playlist)
#     player.play()

#     app.lastWindowClosed.connect(player.stop)
#     sys.exit(app.exec_())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_file = Path("./resources/tts/helloKO.mp3")

    # fullpath = QUrl.fromLocalFile("../helloKO.mp3")  
    if my_file.is_file():
        print('exist')
    else :
        print('not exist')
    # if()
    #     media = QUrl.fromLocalFile(fullpath)
    #     content = QMediaContent(media)
    #     player = QMediaPlayer()
    #     player.setMedia(content)
    #     # player.play()
    #     # sys.exit(app.exec_())
