from PyQt6.QtWidgets import QDialog, QTextBrowser, QLineEdit, QVBoxLayout, QCheckBox

class ChatDialog(QDialog):
    def __init__(self, parent=None):
        super(ChatDialog, self).__init__()
        self.setWindowTitle('Chat History')
        self.text_browser = QTextBrowser(self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Enter your question here...")
        self.voice_checkbox = QCheckBox("Answer with voice", self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text_browser)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.voice_checkbox)

        self.line_edit.returnPressed.connect(parent.ask_question)

    def update_chat(self, chat_history):
        self.text_browser.clear()
        for message in chat_history:
            self.text_browser.append(message)

    def closeEvent(self, event):
        event.ignore() 
        self.hide()