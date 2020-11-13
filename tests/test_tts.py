from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import sys
from pathlib import Path
from gtts import gTTS

'''
https://wikidocs.net/15213
'''
# text = "HI, everybody. Playing with Python is fun!!!"
# tts = gTTS(text=text, lang='en')
# tts.save("helloEN.mp3")

# text = "안녕하세요 여러분, 파이썬을 재밌게 해봐요"
# tts = gTTS(text=text, lang='ko')
# tts.save("./resources/tts/"+text+".mp3")

class TTS():
    def __init__(self):
        self.player = QMediaPlayer()
    
    def makeVoice(self, text): 
        tts = gTTS(text=text, lang='ko')
        tts.save("./resources/tts/"+text+".mp3")
        # tts.save("./resources/tts/test.mp3")

    def play(self, text):
        my_file = Path("./resources/tts/"+text+'.mp3')  
        
        if my_file.is_file():
            print('exist')
        else :
            print('not exist')
            self.makeVoice(text)

        self.filename = text+'.mp3'
        self.fullpath = QDir.current().absoluteFilePath(self.filename) 
        self.media = QUrl.fromLocalFile(self.fullpath)
        self.content = QMediaContent(self.media)
        self.player.setMedia(self.content)
        self.player.play()

if __name__ == "__main__":
    # text = "HI, everybody. Playing with Python is fun!!!"
    # tts = gTTS(text=text, lang='en')
    # tts.save("helloEN.mp3")
    tts = TTS()
    tts.play('티티에스를 테스트합니다')