from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PIL import Image
import os
from imageBox import imageBox
from createDialog import createProjectDialog
import skelMainscreen
from previewWind import previewWindow
import sys

qt_app = QApplication(sys.argv)

class eventFilterWindow(QPushButton):

    def __init__(self, name):
        QPushButton.__init__(self)

        self.button = QPushButton(name)
        self.button.installEventFilter(self)

        self.button.setFixedSize(50, 90)


    def eventFilter(self, object, event):

        if event.type() == QEvent.MouseButtonPress:
            print ("You pressed the button")
            return True

        elif event.type() == QEvent.HoverMove:
            self.button.setStyleSheet("""background-color:rgba(0,0,0,1);
                   border: 3px solid rgb(0,0,255);""")

            print ("C'mon! CLick-meeee!!!")
            return True

        return False

class AbsolutePositioningExample(QWidget):
    ''' An example of PySide absolute positioning; the main window
        inherits from QWidget, a convenient widget for an empty window. '''

    def __init__(self):
        # Initialize the object as a QWidget
        QWidget.__init__(self)

        # We have to set the size of the main window
        # ourselves, since we control the entire layout
        self.setMinimumSize(400, 185)
        self.setWindowTitle('Dynamic Greeter')

        # Create the controls with this object as their parent and set
        # their position individually; each row is a label followed by
        # another control

        # Label for the salutation chooser
        self.salutation_lbl = QLabel('Salutation:', self)
        self.salutation_lbl.move(5, 5)  # offset the first control 5px
        # from top and left
        self.salutations = ['Ahoy',
                            'Good day',
                            'Hello',
                            'Heyo',
                            'Hi',
                            'Salutations',
                            'Wassup',
                            'Yo']
        # Create and fill the combo box to choose the salutation
        self.salutation = QComboBox(self)
        self.salutation.addItems(self.salutations)

        # Allow 100px for the label and 5px each for borders at the
        # far left, between the label and the combobox, and at the far
        # right
        self.salutation.setMinimumWidth(285)
        # Place it five pixels to the right of the end of the label
        self.salutation.move(110, 5)

        # The label for the recipient control
        self.recipient_lbl = QLabel('Recipient:', self)
        # 5 pixel indent, 25 pixels lower than last pair of widgets
        self.recipient_lbl.move(5, 30)

        # The recipient control is an entry textbox
        self.recipient = QLineEdit(self)
        # Add some ghost text to indicate what sort of thing to enter
        self.recipient.setPlaceholderText( "jhbjh")
        # Same width as the salutation
        self.recipient.setMinimumWidth(285)
        # Same indent as salutation but 25 pixels lower
        self.recipient.move(110, 30)

        # The label for the greeting widget
        self.greeting_lbl = QLabel('Greeting:', self)
        # Same indent as the others, but 45 pixels lower so it has
        # physical separation, indicating difference of function
        self.greeting_lbl.move(5, 75)

        # The greeting widget is also a label
        self.greeting = QLabel('', self)
        # Same indent as the other controls
        self.greeting.move(110, 75)

        self.changebutton = QPushButton("change")
        # The build button is a push button
        self.build_button = eventFilterWindow("Build Greeting")

        self.build_button.move(110, 30)

        # self.build_button.setStyleSheet("""background-color:rgba(0,0,0,1);
        # border: 3px solid rgb(0,0,255);""")
        #
        # # Place it at the bottom right, narrower than
        # # the other interactive widgets
        # #self.build_button.setMinimumWidth(145)
        # self.build_button.setFixedSize(50, 90)
        # self.build_button.move(110, 30)


    def run(self):
        # Show the form
        self.show()
        # Run the Qt application
        qt_app.exec_()


# Create an instance of the application window and run it
app = AbsolutePositioningExample()
app.run()
