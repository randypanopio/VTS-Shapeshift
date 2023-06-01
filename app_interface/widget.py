# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_windowv2.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(781, 375)
        font = QFont()
        font.setFamilies([u"Open Sans"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        Form.setFont(font)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet(u"QWidget {\n"
"background-color:#363062; \n"
"color: white;\n"
"font: 10pt \"Open Sans\";\n"
"border-radius: 3px; \n"
"}\n"
"\n"
"QFrame[frameShape=\"4\"],\n"
"QFrame[frameShape=\"5\"]\n"
"{\n"
"    border: none;\n"
"    border-bottom: 1px solid #FFBD69;\n"
"}\n"
"\n"
"QLineEdit {\n"
"background-color:white;\n"
"color:rgb(21, 21, 21);\n"
"    border: 1px solid #363636;\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"background-color:rgb(157, 166, 182);\n"
"\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: 2px solid #827397;\n"
"    border-radius: 4px;\n"
"    background-color: #4D4C7D;\n"
"    min-width: 100px;\n"
"	min-height: 26px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #302b52;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: none; /* no border for a flat push button */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #5d576b;\n"
"	color: #979699;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_20 = QLabel(Form)
        self.label_20.setObjectName(u"label_20")
        font1 = QFont()
        font1.setFamilies([u"Open Sans"])
        font1.setBold(False)
        font1.setItalic(False)
        font1.setUnderline(False)
        self.label_20.setFont(font1)
        self.label_20.setStyleSheet(u"font-size: 17px")

        self.horizontalLayout_17.addWidget(self.label_20)

        self.label_21 = QLabel(Form)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_17.addWidget(self.label_21)

        self.plugin_status_label = QLabel(Form)
        self.plugin_status_label.setObjectName(u"plugin_status_label")
        self.plugin_status_label.setMinimumSize(QSize(80, 0))
        font2 = QFont()
        font2.setFamilies([u"Open Sans"])
        font2.setBold(False)
        font2.setItalic(False)
        self.plugin_status_label.setFont(font2)
        self.plugin_status_label.setStyleSheet(u"font-size: 22px;")

        self.horizontalLayout_17.addWidget(self.plugin_status_label)


        self.horizontalLayout_14.addLayout(self.horizontalLayout_17)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_4)

        self.connection_button = QPushButton(Form)
        self.connection_button.setObjectName(u"connection_button")
        self.connection_button.setMinimumSize(QSize(224, 46))
        self.connection_button.setStyleSheet(u"width: 220px;\n"
"height: 42px;")

        self.horizontalLayout_14.addWidget(self.connection_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_18 = QLabel(Form)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)
        self.label_18.setLayoutDirection(Qt.LeftToRight)
        self.label_18.setStyleSheet(u"")

        self.verticalLayout_7.addWidget(self.label_18)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setSpacing(12)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_19 = QLabel(Form)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_16.addWidget(self.label_19)

        self.url_input = QLineEdit(Form)
        self.url_input.setObjectName(u"url_input")

        self.horizontalLayout_16.addWidget(self.url_input)

        self.label_24 = QLabel(Form)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_16.addWidget(self.label_24)

        self.port_input = QLineEdit(Form)
        self.port_input.setObjectName(u"port_input")

        self.horizontalLayout_16.addWidget(self.port_input)

        self.horizontalLayout_16.setStretch(0, 1)
        self.horizontalLayout_16.setStretch(1, 5)
        self.horizontalLayout_16.setStretch(2, 1)
        self.horizontalLayout_16.setStretch(3, 5)

        self.verticalLayout_7.addLayout(self.horizontalLayout_16)


        self.verticalLayout_2.addLayout(self.verticalLayout_7)

        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 2)

        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_13 = QLabel(Form)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font2)
        self.label_13.setStyleSheet(u"font-size: 17px")

        self.horizontalLayout_9.addWidget(self.label_13)

        self.label_14 = QLabel(Form)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_9.addWidget(self.label_14)

        self.watcher_status_label = QLabel(Form)
        self.watcher_status_label.setObjectName(u"watcher_status_label")
        self.watcher_status_label.setMinimumSize(QSize(80, 0))
        self.watcher_status_label.setStyleSheet(u"font-size: 22px;")

        self.horizontalLayout_9.addWidget(self.watcher_status_label)


        self.horizontalLayout_13.addLayout(self.horizontalLayout_9)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_2)

        self.watcher_button = QPushButton(Form)
        self.watcher_button.setObjectName(u"watcher_button")
        self.watcher_button.setEnabled(True)
        self.watcher_button.setMinimumSize(QSize(224, 46))
        self.watcher_button.setStyleSheet(u"width: 220px;\n"
"height: 42px;")

        self.horizontalLayout_13.addWidget(self.watcher_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_16 = QLabel(Form)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)
        self.label_16.setLayoutDirection(Qt.LeftToRight)
        self.label_16.setStyleSheet(u"")

        self.verticalLayout_6.addWidget(self.label_16)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setSpacing(12)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_17 = QLabel(Form)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_15.addWidget(self.label_17)

        self.directory_input = QLineEdit(Form)
        self.directory_input.setObjectName(u"directory_input")
        self.directory_input.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.directory_input.sizePolicy().hasHeightForWidth())
        self.directory_input.setSizePolicy(sizePolicy)

        self.horizontalLayout_15.addWidget(self.directory_input)

        self.browse_button = QPushButton(Form)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.setEnabled(True)

        self.horizontalLayout_15.addWidget(self.browse_button)

        self.horizontalLayout_15.setStretch(0, 2)
        self.horizontalLayout_15.setStretch(1, 8)
        self.horizontalLayout_15.setStretch(2, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_15)


        self.verticalLayout_3.addLayout(self.verticalLayout_6)

        self.verticalLayout_3.setStretch(0, 2)
        self.verticalLayout_3.setStretch(1, 2)

        self.gridLayout.addLayout(self.verticalLayout_3, 2, 0, 1, 1)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_23 = QLabel(Form)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font)
        self.label_23.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_3.addWidget(self.label_23)

        self.save_pref_button = QPushButton(Form)
        self.save_pref_button.setObjectName(u"save_pref_button")
        self.save_pref_button.setMinimumSize(QSize(104, 30))

        self.horizontalLayout_3.addWidget(self.save_pref_button)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.model_reload_checkbox = QCheckBox(Form)
        self.model_reload_checkbox.setObjectName(u"model_reload_checkbox")
        self.model_reload_checkbox.setChecked(True)

        self.horizontalLayout_12.addWidget(self.model_reload_checkbox)

        self.update_data_checkbox = QCheckBox(Form)
        self.update_data_checkbox.setObjectName(u"update_data_checkbox")
        self.update_data_checkbox.setChecked(True)

        self.horizontalLayout_12.addWidget(self.update_data_checkbox)

        self.backup_checkbox = QCheckBox(Form)
        self.backup_checkbox.setObjectName(u"backup_checkbox")
        self.backup_checkbox.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.backup_checkbox.sizePolicy().hasHeightForWidth())
        self.backup_checkbox.setSizePolicy(sizePolicy1)
        self.backup_checkbox.setChecked(True)
        self.backup_checkbox.setTristate(False)

        self.horizontalLayout_12.addWidget(self.backup_checkbox)

        self.run_watcher_checkbox = QCheckBox(Form)
        self.run_watcher_checkbox.setObjectName(u"run_watcher_checkbox")

        self.horizontalLayout_12.addWidget(self.run_watcher_checkbox)

        self.horizontalLayout_12.setStretch(0, 2)
        self.horizontalLayout_12.setStretch(1, 2)
        self.horizontalLayout_12.setStretch(2, 1)
        self.horizontalLayout_12.setStretch(3, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_12)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setSizeConstraint(QLayout.SetFixedSize)
        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.github_button = QPushButton(Form)
        self.github_button.setObjectName(u"github_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.github_button.sizePolicy().hasHeightForWidth())
        self.github_button.setSizePolicy(sizePolicy2)
        font3 = QFont()
        font3.setFamilies([u"Open Sans"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setUnderline(True)
        self.github_button.setFont(font3)
        self.github_button.setStyleSheet(u"QPushButton {\n"
"	background-color:none; border:none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: #FFBD69; /* no border for a flat push button */\n"
"}")

        self.horizontalLayout.addWidget(self.github_button)

        self.twitter_button = QPushButton(Form)
        self.twitter_button.setObjectName(u"twitter_button")
        sizePolicy2.setHeightForWidth(self.twitter_button.sizePolicy().hasHeightForWidth())
        self.twitter_button.setSizePolicy(sizePolicy2)
        self.twitter_button.setFont(font3)
        self.twitter_button.setStyleSheet(u"QPushButton {\n"
"	background-color:none; border:none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: #FFBD69; /* no border for a flat push button */\n"
"}")

        self.horizontalLayout.addWidget(self.twitter_button)


        self.verticalLayout_9.addLayout(self.horizontalLayout)


        self.verticalLayout_5.addLayout(self.verticalLayout_9)

        self.verticalLayout_5.setStretch(0, 2)
        self.verticalLayout_5.setStretch(1, 1)

        self.gridLayout.addLayout(self.verticalLayout_5, 4, 0, 1, 1)


        self.retranslateUi(Form)

        self.watcher_button.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"Plugin Status", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"  |  ", None))
        self.plugin_status_label.setText(QCoreApplication.translate("Form", u"Offline", None))
        self.connection_button.setText(QCoreApplication.translate("Form", u"Connect", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"Plugin Connection Settings - Likely leave default settings unless specifically modified in VTube Studio", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"URL:", None))
        self.url_input.setText(QCoreApplication.translate("Form", u"ws://localhost:", None))
        self.label_24.setText(QCoreApplication.translate("Form", u"Port:", None))
        self.port_input.setText(QCoreApplication.translate("Form", u"8001", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Watcher Status", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"  |  ", None))
        self.watcher_status_label.setText(QCoreApplication.translate("Form", u"Disabled", None))
        self.watcher_button.setText(QCoreApplication.translate("Form", u"Enable", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"Set the folder directory that VTube Studio is using, and where live changes are saved.", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"Model Directory: ", None))
        self.directory_input.setText(QCoreApplication.translate("Form", u"Set your VTube Studio Model Directory!", None))
        self.browse_button.setText(QCoreApplication.translate("Form", u"Browse", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"Shapeshift Plugin Preferences", None))
        self.save_pref_button.setText(QCoreApplication.translate("Form", u"Save Preferences (Requires Restart)", None))
        self.model_reload_checkbox.setText(QCoreApplication.translate("Form", u"Auto Attempt Model Reloads", None))
        self.update_data_checkbox.setText(QCoreApplication.translate("Form", u"Update Data on new Model", None))
        self.backup_checkbox.setText(QCoreApplication.translate("Form", u"Create Backup Folder", None))
        self.run_watcher_checkbox.setText(QCoreApplication.translate("Form", u"Enable Watcher on Startup", None))
        self.github_button.setText(QCoreApplication.translate("Form", u"Support @ GitHub", None))
        self.twitter_button.setText(QCoreApplication.translate("Form", u"Contact @ Twitter", None))
    # retranslateUi

