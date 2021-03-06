try:
  from PyQt5 import QtWidgets
except ImportError:
  from PySide import QtGui
  QtWidgets = QtGui

import idc

from . import base
from .. import network, netnode


class AddProjectDialog(base.BaseDialog):
  def __init__(self, **kwargs):
    super(AddProjectDialog, self).__init__(title="Add Project", **kwargs)

    gridLyt = QtWidgets.QGridLayout()
    layout = QtWidgets.QVBoxLayout()

    gridLyt.addWidget(QtWidgets.QLabel("Project name:"), 0, 0)
    gridLyt.addWidget(QtWidgets.QLabel("Description:"), 1, 0)

    self.nameTxt = QtWidgets.QLineEdit()
    gridLyt.addWidget(self.nameTxt, 0, 1)

    self.descriptionTxt = QtWidgets.QTextEdit()
    gridLyt.addWidget(self.descriptionTxt, 1, 1)

    layout.addLayout(gridLyt)

    self.privateCkb = QtWidgets.QCheckBox("Make project private")
    layout.addWidget(self.privateCkb)
    self.bindCurrentCkb = QtWidgets.QCheckBox("Bind current file to project")
    layout.addWidget(self.bindCurrentCkb)
    if not netnode.bound_file_id:
      self.bindCurrentCkb.setEnabled(False)

    self.statusLbl = QtWidgets.QLabel()
    layout.addWidget(self.statusLbl)

    addBtn = QtWidgets.QPushButton("&Add")
    addBtn.setDefault(True)
    cancelBtn = QtWidgets.QPushButton("&Cancel")
    SizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                       QtWidgets.QSizePolicy.Fixed)
    addBtn.setSizePolicy(SizePolicy)
    cancelBtn.setSizePolicy(SizePolicy)
    buttonLyt = QtWidgets.QHBoxLayout()
    buttonLyt.addWidget(addBtn)
    buttonLyt.addWidget(cancelBtn)
    layout.addLayout(buttonLyt)

    self.setLayout(layout)

    addBtn.clicked.connect(self.submit)
    cancelBtn.clicked.connect(self.reject)

  def data(self):
    name = self.nameTxt.text()
    description = self.descriptionTxt.toPlainText()
    private = self.privateCkb.isChecked()
    bind_current = self.bindCurrentCkb.isChecked()

    return name, description, private, bind_current

  def submit(self):
    name = self.nameTxt.text()
    description = self.descriptionTxt.toPlainText()
    private = self.privateCkb.isChecked()
    bind_current = self.bindCurrentCkb.isChecked()

    data = {'name': name, 'description': description, 'private': private,
            'files': []}

    if bind_current:
      data['files'].append(netnode.bound_file_id)

    self.response = network.query("POST", "collab/projects/", params=data,
                                  json=True)
    self.accept()


class AddFileDialog(base.BaseDialog):
  def __init__(self, **kwargs):
    super(AddFileDialog, self).__init__(title="Add File", **kwargs)

    name = idc.GetInputFile()
    md5hash = idc.GetInputMD5()

    gridLyt = QtWidgets.QGridLayout()
    layout = QtWidgets.QVBoxLayout()

    gridLyt.addWidget(QtWidgets.QLabel("File name:"), 0, 0)
    gridLyt.addWidget(QtWidgets.QLabel("Description:"), 1, 0)
    gridLyt.addWidget(QtWidgets.QLabel("MD5 hash:"), 2, 0)

    self.nameTxt = QtWidgets.QLineEdit()
    self.nameTxt.setText(name)
    gridLyt.addWidget(self.nameTxt, 0, 1)

    self.descriptionTxt = QtWidgets.QTextEdit()
    gridLyt.addWidget(self.descriptionTxt, 1, 1)

    gridLyt.addWidget(QtWidgets.QLabel(md5hash), 2, 1)

    layout.addLayout(gridLyt)

    self.shareidbCkb = QtWidgets.QCheckBox("Share IDB (let others without "
                                           "the idb to participate)")
    layout.addWidget(self.shareidbCkb)

    self.statusLbl = QtWidgets.QLabel()
    layout.addWidget(self.statusLbl)

    addBtn = QtWidgets.QPushButton("&Add")
    addBtn.setDefault(True)
    cancelBtn = QtWidgets.QPushButton("&Cancel")
    SizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                       QtWidgets.QSizePolicy.Fixed)
    addBtn.setSizePolicy(SizePolicy)
    cancelBtn.setSizePolicy(SizePolicy)
    buttonLyt = QtWidgets.QHBoxLayout()
    buttonLyt.addWidget(addBtn)
    buttonLyt.addWidget(cancelBtn)
    layout.addLayout(buttonLyt)

    self.setLayout(layout)

    addBtn.clicked.connect(self.submit)
    cancelBtn.clicked.connect(self.reject)

  def data(self):
    name = self.nameTxt.text()
    description = self.descriptionTxt.toPlainText()
    shareidb = self.shareidbCkb.isChecked()

    return name, description, shareidb

  def submit(self):
    name = self.nameTxt.text()
    md5hash = idc.GetInputMD5()
    description = self.descriptionTxt.toPlainText()
    shareidb = self.shareidbCkb.isChecked()

    data = {'name': name, 'md5hash': md5hash, 'description': description,
            'instances': []}

    if shareidb:
      # TODO: uploadfile
      pass

    self.response = network.query("POST", "collab/files/", params=data,
                                  json=True)
    self.accept()
