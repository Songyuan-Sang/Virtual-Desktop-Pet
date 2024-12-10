from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateTimeEdit
from PySide6.QtCore import Qt, Signal

class ReminderDialog(QDialog):
    reminder_set = Signal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Set Reminder")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)


        layout = QVBoxLayout()

        self.datetime_edit = QDateTimeEdit()
        layout.addWidget(QLabel("Select Date and Time:"))
        layout.addWidget(self.datetime_edit)

        self.message_edit = QLineEdit()
        layout.addWidget(QLabel("Reminder Message:"))
        layout.addWidget(self.message_edit)

        self.set_button = QPushButton("Set Reminder")
        self.set_button.clicked.connect(self.set_reminder)
        layout.addWidget(self.set_button)

        self.setLayout(layout)

    def set_reminder(self):
        reminder_datetime = self.datetime_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        reminder_message = self.message_edit.text()

        # You can implement the logic to set the reminder here, for example, emit a signal
        # with the reminder datetime and message to be handled by the main application.
        # In this example, we'll just print the reminder datetime and message.
        print("Reminder set for:", reminder_datetime)
        print("Reminder message:", reminder_message)
        self.reminder_set.emit(reminder_datetime, reminder_message)
        self.close()
