import sys, time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

'''
    ↓ Menu Widget
'''
class MenuWidget(QGroupBox):
    def __init__(self, menu1, menu2, eventName1, eventName2, eventHandler):
        QGroupBox.__init__(self)

        self.box = QHBoxLayout()
        self.setLayout(self.box)
        self.setTitle("메뉴")
        
        #define button
        btn1 = QPushButton(menu1)
        btn2 = QPushButton(menu2)

        #style
        self.setStyleSheet("background: white;")
        buttonStyle = "height : 300px; \
            border-width:5px; border-color:blue; border-radius: 10px; border-style:solid; \
            background: white; \
            font-size: 30px; font-weight: bold; font-family: 맑은 고딕;"
        btn1.setStyleSheet(buttonStyle)
        btn2.setStyleSheet(buttonStyle)

        # add event handler
        btn1.clicked.connect(lambda : eventHandler(eventName1))
        btn2.clicked.connect(lambda : eventHandler(eventName2))
        
        # add buttons to box
        self.box.addWidget(btn1)
        self.box.addWidget(btn2)

'''
    ↓ TempWidget
'''
class TempWidget(QGroupBox):
    def __init__(self, eventHandler):
        QGroupBox.__init__(self)
        self.box = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.box)
        self.setTitle("체온 확인")

        # define label
        self.name = QLabel('이름과 소속')
        self.temp = QLabel('체온')
        self.status = QLabel('확인중입니다')

        # style
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setStyleSheet(
            "background: white;"
            "font-size: 25px;"
            "font-family: 맑은 고딕;"
            "border-width:3px;"
            "border-style:solid;"
            "border-color:black;"
        )
        self.temp.setAlignment(Qt.AlignCenter)
        self.temp.setStyleSheet(
            "background: white;"
            "font-size: 25px;"
            "font-family: 맑은 고딕;"
            "border-width:3px;"
            "border-style:solid;"
            "border-color:black;"
        )
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet(
            "background: white;"
            "font-size: 25px;"
            "font-family: 맑은 고딕;"
            "border-width:3px;"
            "border-style:solid;"
            "border-color:black;"
        )

        # add labels to box
        self.box.addWidget(self.name)
        self.box.addWidget(self.temp)
        self.box.addWidget(self.status)

    def setName(self, name):
        self.name.setText(name)

    def getName(self):
        return self.name.text()
    
    def setTemp(self, temperature):
        self.temp.setText(temperature)
    
    def getTemp(self):
        return self.temp.text()
    
    def setStatus(self, status):
        self.status.setText(status)
    
    def getStatus(self):
        return self.status.text()

'''
    ↓ AdminAdd Widget
'''
class AdminAddWidget(QGroupBox):
    def __init__(self, eventHandler):
        QGroupBox.__init__(self)
        self.box = QFormLayout()
        self.setLayout(self.box)
        self.setTitle("멤버 추가")

        # define widgets
        self.nfcIdLabel = QLabel('NFC ID : ')
        self.nfcIdEditor = QLineEdit()
        self.nameLabel = QLabel('이름 : ')
        self.nameEditor = QLineEdit()
        self.belongLabel = QLabel('소속 : ')
        self.belongEditor = QLineEdit()

        self.cancelButton = QPushButton('뒤로가기')
        self.addButton = QPushButton('추가하기')
        horizonLayout = QHBoxLayout()
        horizonLayout.addWidget(self.cancelButton)
        horizonLayout.addWidget(self.addButton)

        # event handle
        self.cancelButton.clicked.connect(lambda :eventHandler('adminAdd_cancel'))
        self.addButton.clicked.connect(lambda : eventHandler('adminAdd_add', self.getElements()))

        # define style
        self.box.setContentsMargins(40, 100, 40, 0)
        labelStyle = "font-size:20px;font-family: 맑은 고딕;"
        editorStyle = "font-size:20px;font-family: 맑은 고딕;"
        buttonStyle = "margin-top:90px; height: 50px; font-size:20px; font-family: 맑은 고딕;"

        # label style
        self.nfcIdLabel.setStyleSheet(labelStyle)
        self.nameLabel.setStyleSheet(labelStyle)
        self.belongLabel.setStyleSheet(labelStyle)
        
        # editor style
        self.nfcIdEditor.setStyleSheet(editorStyle)
        self.nameEditor.setStyleSheet(editorStyle)
        self.belongEditor.setStyleSheet(editorStyle)
        
        #button style
        self.cancelButton.setStyleSheet(buttonStyle)
        self.addButton.setStyleSheet(buttonStyle)

        # add widgets to box
        self.box.addRow(self.nfcIdLabel, self.nfcIdEditor)
        self.box.addRow(self.nameLabel, self.nameEditor)
        self.box.addRow(self.belongLabel, self.belongEditor)
        self.box.addRow(horizonLayout)

    def getElements(self):
        target = {}
        target['nfcId'] = self.nfcIdEditor.text()
        target['name'] = self.nameEditor.text()
        target['belong'] = self.belongEditor.text()
        return target

'''
    ↓ AdminDeleteWidget
'''
class AdminDeleteWidget(QGroupBox):
    def __init__(self, eventHandler):
        QGroupBox.__init__(self)
        #props 
        self.eventHandler = eventHandler

        self.data = [
            {"name":"홍길동1", "belong":"숭실대학교 소프트웨어학부", "nfcid":'1234556'},
            {"name":"홍길동1", "belong":"숭실대학교 소프트웨어학부", "nfcid":'1234556'},
        ]
        self.checkBoxs = []
        self.init_widget()
    
    def init_widget(self):
        self.box = QFormLayout()
        hbox = QHBoxLayout()
        self.setLayout(self.box)
        self.setTitle("멤버 삭제")

        # define widgets
        self.table = QTableWidget(len(self.data),4)
        self.table.setHorizontalHeaderLabels(["이름", "소속", "NFC ID", "삭제"])
        self.cancelButton = QPushButton('뒤로가기')
        self.deleteButton = QPushButton('삭제하기')

        # button event handler
        self.cancelButton.clicked.connect(lambda : self.eventHandler('adminDelete_cancel'))
        self.deleteButton.clicked.connect(lambda : self.eventHandler('adminDelete_delete',  self.getSelected()))

        # style
        buttonStyle = "height:40px; font-size: 20px; font-family: 맑은 고딕;"
        self.cancelButton.setStyleSheet(buttonStyle)
        self.deleteButton.setStyleSheet(buttonStyle)

        # set header width
        self.resizeHeaderWidth()

        # add widgets to box
        self.box.addWidget(self.table)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.deleteButton)
        self.box.addRow(hbox)
    
        self.drawTable()

    # data setter
    def setData(self, data):
        self.data = data
        self.table.setRowCount(len(self.data))
        self.drawTable()
        self.resizeHeaderWidth()
    
    # resize header with content
    def resizeHeaderWidth(self):
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    # draw table
    def drawTable(self):
        i = 0
        for current in self.data:
            nameLabel = QLabel(current['name'])
            belongLabel = QLabel(current['belong'])
            nfcLabel = QLabel(current['nfcid'])
            checkbox = MyCheckBox(current['nfcid'])
            
            self.checkBoxs.append(checkbox)

            self.table.setCellWidget(i,0,nameLabel)
            self.table.setCellWidget(i,1, belongLabel)
            self.table.setCellWidget(i,2, nfcLabel)

            checkBoxCellWidget = QWidget()
            lay_out = QHBoxLayout(checkBoxCellWidget)
            lay_out.addWidget(checkbox)
            lay_out.setAlignment(Qt.AlignCenter)
            lay_out.setContentsMargins(0,0,0,0)
            checkBoxCellWidget.setLayout(lay_out)
            self.table.setCellWidget(i,3, checkBoxCellWidget)

            i+=1
    
    def getSelected(self): 
        targets = []
        for box in self.checkBoxs:
            if(box.getUID() != False):
                targets.append(box.getUID())
        print(targets)
        return targets
        
'''
    ↓ My Checkbox for Admin Delete Widget
'''
class MyCheckBox(QCheckBox):
    def __init__(self, nfcId):
        super().__init__()
        self.nfcId = nfcId
        self.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")

    def getUID(self):
        if(self.isChecked()):
            return self.nfcId
        else :
            return False        
'''
    ↓ Widgets Controller
'''
class WidgetsController(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.resize(700,450)
        self.widgetStack = QStackedWidget(self)
        self.init_widget()
        self.toCenter()
        self.show()

    def init_widget(self):
        self.setWindowTitle("Body Temperature Scanner")
        widget_laytout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(widget_laytout)

        self.menuWidget = MenuWidget('사용자 메뉴', '관리자 메뉴', 'userMenu','adminMenu', self.eventHandler)
        self.tempWidget = TempWidget(self.eventHandler)
        self.adminMenuWidget = MenuWidget('멤버 추가', '멤버 삭제','addMember','deleteMember', self.eventHandler)
        self.adminAddWidget = AdminAddWidget(self.eventHandler)
        self.adminDeleteWidget = AdminDeleteWidget(self.eventHandler)

        self.widgetStack.addWidget(self.menuWidget)
        self.widgetStack.addWidget(self.tempWidget)
        self.widgetStack.addWidget(self.adminMenuWidget)
        self.widgetStack.addWidget(self.adminAddWidget)
        self.widgetStack.addWidget(self.adminDeleteWidget)
        self.widgetStack.setCurrentIndex(3)

        widget_laytout.addWidget(self.widgetStack)
    
    def toCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def eventHandler(self, kind, params=None):
        print(kind)
        if(params!=None):
            print(params)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = WidgetsController()
    form.show()
    exit(app.exec_())