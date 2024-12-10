import os
import sys
import random
import pygame
from gtts import gTTS
from desktop_pet.chat_dialog import ChatDialog
from desktop_pet.openai_integration import OpenAIIntegration
from pygame import mixer
from PySide6.QtGui import QIcon, QCursor, QAction, QMovie, QFont
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtWidgets import QWidget, QLabel, QMenu, QApplication, QSystemTrayIcon

class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.init()
        self.initTray()
        self.initPetImage()
        self.petNormalAction()

        self.chat_dialog = ChatDialog(self)
        self.chat_history = []
        self.openai_integration = OpenAIIntegration()
           
    def init(self):
        self.is_follow_mouse = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.repaint()

    def initTray(self):
        quit_action = QAction(QIcon("./desktop_pet/assets/icons/exit.png"), 'Exit', self, triggered=self.quit)
        showing = QAction(QIcon("./desktop_pet/assets/icons/display.png"),'Display', self, triggered=self.showwin)

        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(showing)
        self.tray_icon_menu.addAction(quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join('./desktop_pet/assets/icon.ico')))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    def initPetImage(self):
        self.talkLabel = QLabel(self)
        self.talkLabel.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")
        self.image = QLabel(self)
        self.movie = QMovie("./desktop_pet/assets/pet_images/pet1.gif")
        self.movie.setScaledSize(QSize(200, 200))
        self.image.setMovie(self.movie)
        self.movie.start()
        self.resize(1024, 1024)
        self.randomPosition()
        self.show()
        self.pet_list = []
        for i in os.listdir("./desktop_pet/assets/pet_images"):
            self.pet_list.append("./desktop_pet/assets/pet_images/" + i)
        self.dialog = []
        with open("./desktop_pet/assets/dialog.txt", "r", encoding='utf8') as f:
            text = f.read()
            self.dialog = text.split("\n")

    def petNormalAction(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(3000)
        self.condition = 0
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(self.talk)
        self.talkTimer.start(3000)
        self.talk_condition = 0
        self.talk()

    def randomAct(self):
        if not self.condition:
            self.movie = QMovie(random.choice(self.pet_list))
            self.movie.setScaledSize(QSize(200, 200))
            self.image.setMovie(self.movie)
            self.movie.start()
        else:
            self.movie = QMovie("./desktop_pet/assets/pet_images/pet3.gif")
            self.movie.setScaledSize(QSize(200, 200))
            self.image.setMovie(self.movie)
            self.movie.start()
            self.condition = 0
            self.talk_condition = 0

    def talk(self):
        if not self.talk_condition:
            self.talkLabel.setText(random.choice(self.dialog))
            self.talkLabel.setStyleSheet(
                "font: bold 25pt 'Times New Roman';"
                "color:white;"
                "background-color: black"
                "url(:/)"
            )
            self.talkLabel.adjustSize()
        else:
            self.talkLabel.setText("Let's           chat!")
            self.talkLabel.setStyleSheet(
                "font: bold 15pt 'Times New Roman';"  
                "color: red;"
                "background-color: white"
                "url(:/)"
            )
            self.talkLabel.adjustSize()
            self.talk_condition = 0

    def update_chat(self, message):
        self.chat_history.append(message)
        self.chat_dialog.update_chat(self.chat_history)

    def ask_question(self):
        question = self.chat_dialog.line_edit.text()
        self.update_chat("You: " + question)   
        response = self.openai_integration.openai_query(question)
        self.update_chat("Pet: " + response)
        self.chat_dialog.line_edit.clear()

        if self.chat_dialog.voice_checkbox.isChecked():
            pygame.init()
            pygame.mixer.init()
            tts = gTTS(response)
            tts.save('./desktop_pet/assets/gTTS/output.mp3')
            mixer.init()
            mixer.music.load("./desktop_pet/assets/gTTS/output.mp3")
            mixer.music.play()
            mixer.music.get_endevent()
            while mixer.music.get_busy():
                continue
            mixer.music.load("./desktop_pet/assets/gTTS/test.mp3")
            os.remove("./desktop_pet/assets/gTTS/output.mp3")

    def quit(self):
        self.close()
        sys.exit()

    def showwin(self):
        self.setWindowOpacity(1)

    def randomPosition(self):
        screen_geo = self.screen().geometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(width, height)

    def mousePressEvent(self, event):
        self.condition = 1
        self.talk_condition = 1
        self.timer.stop()
        self.talkTimer.stop()
        self.talk()
        self.randomAct()
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_follow_mouse = True
        self.mouse_drag_pos = event.globalPosition().toPoint() - self.pos()
        event.accept()
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPosition().toPoint() - self.mouse_drag_pos)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.timer.start()
        self.talkTimer.start()

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        quitAction = menu.addAction(QIcon("./desktop_pet/assets/icons/exit.png"), "Exit")
        hideAction = menu.addAction(QIcon("./desktop_pet/assets/icons/hide.png"), "Hide")
        chatAction = menu.addAction(QIcon("./desktop_pet/assets/icons/chat.png"), "Chat")
        reminderAction = menu.addAction(QIcon("./desktop_pet/assets/icons/chat.png"), "Reminder")
    

        # Set fonts for the actions
        font = QFont()
        font.setBold(True)
        quitAction.setFont(font)
        hideAction.setFont(font)
        chatAction.setFont(font)
        
        # Add actions to the menu
        menu.addAction(quitAction)
        menu.addAction(hideAction)
        menu.addAction(chatAction)
        menu.addAction(reminderAction)

        menu.setStyleSheet("""
        QMenu {
            background-color: #F7E7CE; /* Light beige background */
            color: #5C3317; /* Brown text */
            border: 2px solid #F7E7CE; /* Light beige border */
            margin: 2px; /* Margin between the border and the content */
        }
        QMenu::item:selected {
            background-color: #EE9A49; /* Orange background when an item is selected */
        }
        QMenu::item:disabled {
            color: #AAAAAA; /* Gray text when an item is disabled */
        }
        """)

        action = menu.exec(self.mapToGlobal(event.pos()))
        
        if action == quitAction:
            QApplication.quit()
        if action == hideAction:
            self.setWindowOpacity(0)
        if action == chatAction:
            self.chat_dialog.show()
        if action == chatAction:
            self.chat_dialog.show()