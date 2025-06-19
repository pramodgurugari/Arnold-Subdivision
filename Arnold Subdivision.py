import maya.cmds as cmds
import maya.OpenMayaUI as omui

# Cross-version PySide compatibility
try:
    from PySide2 import QtWidgets, QtCore, QtGui
    from shiboken2 import wrapInstance
except ImportError:
    try:
        from PySide6 import QtWidgets, QtCore, QtGui
        import shiboken6 as shiboken
        def wrapInstance(ptr, base=None):
            if ptr is None:
                return None
            if base is None:
                base = QtWidgets.QWidget
            return shiboken.wrapInstance(int(ptr), base)
    except ImportError:
        from PySide import QtGui, QtCore
        import shiboken
        QtWidgets = QtGui
        def wrapInstance(ptr, base=None):
            if ptr is None:
                return None
            if base is None:
                base = QtGui.QWidget
            return shiboken.wrapInstance(int(ptr), base)

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

class ArnoldSubdivisionUI(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)
        self.setWindowTitle("Arnold Subdivision Tool")
        self.setMinimumWidth(340)
        self.setWindowFlag(QtCore.Qt.Window)
        self.setStyleSheet("""
            QDialog {
                background-color: #2B2B2B;
                color: #DDDDDD;
                font-family: Segoe UI, sans-serif;
                font-size: 11pt;
            }
            QLabel {
                color: #FFFFFF;
            }
            QComboBox, QSpinBox {
                background-color: #3C3F41;
                color: #FFFFFF;
                border: 1px solid #555;
                padding: 2px;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #555;
            }
            QSlider::handle:horizontal {
                background: #00AAFF;
                width: 10px;
                margin: -6px 0;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #00AAFF;
                color: #FFFFFF;
                padding: 6px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #007ACC;
            }
        """)
        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Arnold Subdivision Settings")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #00AAFF;")
        layout.addWidget(title)

        # Subdivision settings
        settings_box = QtWidgets.QGroupBox()
        settings_layout = QtWidgets.QVBoxLayout(settings_box)

        type_layout = QtWidgets.QHBoxLayout()
        type_label = QtWidgets.QLabel("Subdivision Type:")
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["none", "catclark", "linear"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        settings_layout.addLayout(type_layout)

        iter_layout = QtWidgets.QHBoxLayout()
        iter_label = QtWidgets.QLabel("Iterations:")
        self.iter_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.iter_slider.setRange(0, 30)
        self.iter_slider.setValue(1)
        self.iter_spin = QtWidgets.QSpinBox()
        self.iter_spin.setRange(0, 30)
        self.iter_spin.setValue(1)
        iter_layout.addWidget(iter_label)
        iter_layout.addWidget(self.iter_slider)
        iter_layout.addWidget(self.iter_spin)
        settings_layout.addLayout(iter_layout)

        self.iter_slider.valueChanged.connect(self.iter_spin.setValue)
        self.iter_spin.valueChanged.connect(self.iter_slider.setValue)

        layout.addWidget(settings_box)

        self.scope_group = QtWidgets.QGroupBox("Apply To")
        scope_layout = QtWidgets.QHBoxLayout(self.scope_group)
        self.selected_radio = QtWidgets.QRadioButton("Selected Objects")
        self.all_radio = QtWidgets.QRadioButton("All Scene Objects")
        self.auto_radio = QtWidgets.QRadioButton("Auto Assign")
        self.selected_radio.setChecked(True)
        scope_layout.addWidget(self.selected_radio)
        scope_layout.addWidget(self.all_radio)
        scope_layout.addWidget(self.auto_radio)
        layout.addWidget(self.scope_group)

        apply_btn = QtWidgets.QPushButton("Apply Subdivision")
        apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(apply_btn)

        credits_label = QtWidgets.QLabel()
        credits_label.setTextFormat(QtCore.Qt.RichText)
        credits_label.setOpenExternalLinks(True)
        credits_label.setAlignment(QtCore.Qt.AlignCenter)
        credits_label.setStyleSheet("color: #AAAAAA; font-size: 9pt;")
        credits_label.setText(
            'Created by <b>Pramod G</b> | Version: 1.2<br>'
            '<a href="https://www.artstation.com/pramod_pro" style="color:#00aaff;">ArtStation</a> | '
            '<a href="https://www.linkedin.com/in/pramod-g-38064a53/" style="color:#00aaff;">LinkedIn</a>'
        )
        layout.addWidget(credits_label)

    def apply_settings(self):
        subd_type = self.type_combo.currentText()
        iterations = self.iter_spin.value()
        auto_assign = self.auto_radio.isChecked()

        if self.all_radio.isChecked() or auto_assign:
            all_meshes = cmds.ls(type='mesh', long=True) or []
            sel = list(set([
                cmds.listRelatives(m, parent=True, fullPath=True)[0]
                for m in all_meshes if cmds.listRelatives(m, parent=True)
            ]))
        else:
            sel = cmds.ls(selection=True, long=True) or []

        if not sel:
            cmds.warning("No geometry found.")
            return

        for obj in sel:
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
            if not shapes:
                continue
            shape = shapes[0]

            if not cmds.attributeQuery('aiSubdivType', node=shape, exists=True):
                cmds.addAttr(shape, longName='aiSubdivType', attributeType='enum',
                             enumName="none:catclark:linear", keyable=True)
            if not cmds.attributeQuery('aiSubdivIterations', node=shape, exists=True):
                cmds.addAttr(shape, longName='aiSubdivIterations',
                             attributeType='long', keyable=True)

            if auto_assign:
                face_count = cmds.polyEvaluate(obj, face=True)
                if face_count > 100000:
                    level = 1
                elif face_count > 10000:
                    level = 2
                else:
                    level = 3
                cmds.setAttr(shape + '.aiSubdivType', 1)  # catclark
                cmds.setAttr(shape + '.aiSubdivIterations', level)
            else:
                cmds.setAttr(shape + '.aiSubdivType',
                             ["none", "catclark", "linear"].index(subd_type))
                cmds.setAttr(shape + '.aiSubdivIterations', iterations)

        cmds.inViewMessage(amg='Arnold Subdivision <hl>applied</hl> successfully.',
                           pos='topCenter', fade=True)

# Launch Function
def show_arnold_subdivision_ui():
    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        if isinstance(widget, ArnoldSubdivisionUI):
            widget.close()
    win = ArnoldSubdivisionUI()
    win.show()

# Run
show_arnold_subdivision_ui()
