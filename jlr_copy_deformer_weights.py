#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import pymel.core as pm
from maya import OpenMayaUI as Omui

mayaMainWindowPtr = Omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QMainWindow)


##############################################
# Menus Items
##############################################

def create_menu_commands():
    """
    Create the menu commands.
    """
    pass


class CopyDeformerWeights(object):

    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog_name = "copy_deformer_weights_dialog"
        if pm.window(self.dialog_name, exists=True):
            pm.deleteUI(self.dialog_name)

        # Parent widget under Maya main window
        self.dialog.setParent(mayaMainWindow)
        self.dialog.setWindowFlags(QtCore.Qt.Window)

        self.setup_ui(self.dialog)

    def setup_ui(self, dialog):
        dialog.setObjectName(self.dialog_name)
        dialog.resize(400, 400)
        dialog.setWindowTitle("Copy Deformer Weights")

        self.dialog_layout = QtWidgets.QGridLayout(dialog)
        self.dialog_layout.setObjectName("dialog_layout")

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setObjectName("main_layout")

        self.source_group_box = QtWidgets.QGroupBox(dialog)
        self.source_group_box.setObjectName("source_group_box")
        self.source_group_box.setTitle("Source")

        self.source_gb_layout = QtWidgets.QGridLayout(self.source_group_box)
        self.source_gb_layout.setObjectName("source_gb_layout")

        self.source_layout = QtWidgets.QVBoxLayout()
        self.source_layout.setContentsMargins(2, 2, 2, 2)
        self.source_layout.setObjectName("source_layout")

        self.btn_source = QtWidgets.QPushButton(self.source_group_box)
        self.btn_source.setObjectName("btn_source")
        self.btn_source.setText("Get Source")
        self.btn_source.clicked.connect(lambda: self.get_source_items())
        self.source_layout.addWidget(self.btn_source)

        self.source_list_layout = QtWidgets.QHBoxLayout()
        self.source_list_layout.setContentsMargins(2, 2, 2, 2)
        self.source_list_layout.setObjectName("source_list_layout")

        self.object_source_list = QtWidgets.QListWidget(self.source_group_box)
        self.object_source_list.setObjectName("object_source_list")
        self.source_list_layout.addWidget(self.object_source_list)

        self.deformer_source_list = QtWidgets.QListWidget(self.source_group_box)
        self.deformer_source_list.setObjectName("deformer_source_list")
        self.source_list_layout.addWidget(self.deformer_source_list)

        self.source_layout.addLayout(self.source_list_layout)
        self.source_gb_layout.addLayout(self.source_layout, 0, 0, 1, 1)

        self.main_layout.addWidget(self.source_group_box)

        self.target_group_box = QtWidgets.QGroupBox(dialog)
        self.target_group_box.setObjectName("target_group_box")
        self.target_group_box.setTitle("Target")

        self.target_gb_layout = QtWidgets.QGridLayout(self.target_group_box)
        self.target_gb_layout.setObjectName("target_gb_layout")

        self.target_layout = QtWidgets.QVBoxLayout()
        self.target_layout.setContentsMargins(2, 2, 2, 2)
        self.target_layout.setObjectName("target_layout")

        self.btn_target = QtWidgets.QPushButton(self.target_group_box)
        self.btn_target.setObjectName("btn_target")
        self.btn_target.setText("Get Target")
        self.btn_target.clicked.connect(lambda: self.get_target_items())
        self.target_layout.addWidget(self.btn_target)

        self.target_list_layout = QtWidgets.QHBoxLayout()
        self.target_list_layout.setContentsMargins(2, 2, 2, 2)
        self.target_list_layout.setObjectName("target_list_layout")

        self.object_target_list = QtWidgets.QListWidget(self.target_group_box)
        self.object_target_list.setObjectName("object_target_list")
        self.target_list_layout.addWidget(self.object_target_list)

        self.deformer_target_list = QtWidgets.QListWidget(self.target_group_box)
        self.deformer_target_list.setObjectName("deformer_target_list")
        self.target_list_layout.addWidget(self.deformer_target_list)

        self.target_layout.addLayout(self.target_list_layout)
        self.target_gb_layout.addLayout(self.target_layout, 0, 0, 1, 1)
        self.main_layout.addWidget(self.target_group_box)

        self.buttons_group_box = QtWidgets.QGroupBox(dialog)
        self.buttons_group_box.setTitle("")
        self.buttons_group_box.setObjectName("buttons_group_box")

        self.buttons_gb_layout = QtWidgets.QHBoxLayout(self.buttons_group_box)
        self.buttons_gb_layout.setObjectName("buttons_gb_layout")

        self.copy_button = QtWidgets.QPushButton(self.buttons_group_box)
        self.copy_button.setObjectName("copy_button")
        self.copy_button.setText("Copy")
        self.copy_button.clicked.connect(lambda: self.copy_deformer_weigths())
        self.buttons_gb_layout.addWidget(self.copy_button)

        self.cancel_button = QtWidgets.QPushButton(self.buttons_group_box)
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setText("Cancel")
        self.buttons_gb_layout.addWidget(self.cancel_button)

        self.main_layout.addWidget(self.buttons_group_box)
        self.dialog_layout.addLayout(self.main_layout, 0, 0, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(dialog)

    def get_source_items(self):
        if pm.selected():
            self.update_source_list(pm.selected())
            self.update_source_deformer_list()

    def update_source_list(self, l_items):
        if l_items:
            self.populate_list_widget(self.object_source_list, l_items)

    def update_source_deformer_list(self):
        item = pm.PyNode(self.object_source_list.currentItem().text())
        self.populate_list_widget(self.deformer_source_list, self.get_deformer_list(item))

    def get_target_items(self):
        if pm.selected():
            self.update_target_list(pm.selected())
            self.update_target_deformer_list()

    def update_target_list(self, l_items):
        if l_items:
            self.populate_list_widget(self.object_target_list, l_items)

    def update_target_deformer_list(self):
        item = pm.PyNode(self.object_target_list.currentItem().text())
        self.populate_list_widget(self.deformer_target_list, self.get_deformer_list(item))

    @staticmethod
    def get_deformer_list(item):
        if pm.objExists(item):
            shape = item.getShapes()[0]
            deformer_list = shape.listConnections(type=("ffd", "skinCluster", "wire", "cluster"))
            return deformer_list
        else:
            return list()

    @staticmethod
    def populate_list_widget(list_widget, l_items):
        list_widget.clear()
        for item in l_items:
            list_widget_item = QtWidgets.QListWidgetItem()
            list_widget_item.setText(item.nodeName())
            list_widget.addItem(list_widget_item)

        list_widget.setCurrentRow(0)

    def copy_deformer_weigths(self):
        data = {"geo_source": pm.PyNode(self.object_source_list.currentItem().text()),
                "geo_target": pm.PyNode(self.object_target_list.currentItem().text()),
                "def_source": pm.PyNode(self.deformer_source_list.currentItem().text()),
                "def_target": pm.PyNode(self.deformer_target_list.currentItem().text()),
                }
        self.transfer_deformer_weights(**data)

    def show(self):
        self.dialog.show()

    @staticmethod
    def transfer_deformer_weights(geo_source, geo_target=None, def_source=None, def_target=None):

        assert geo_source and def_source and def_target, \
            "select a source and target geometry and then the source and target deformers"

        if not geo_target:
            geo_target = geo_source

        # wire_a_weights = None
        deformer_weights = def_source.weightList[0].weights.get()

        tmp_source = pm.duplicate(geo_source)[0]
        tmp_target = pm.duplicate(geo_target)[0]
        tmp_source.v.set(True)
        tmp_target.v.set(True)

        pm.select(clear=True)
        l_jnt = list()
        l_jnt.append(pm.joint(n="jnt_tmpA_01", p=[0, 0, 0]))
        l_jnt.append(pm.joint(n="jnt_tmpA_02", p=[0, 1, 0]))
        skin_source = pm.skinCluster(l_jnt, tmp_source, nw=1)
        skin_target = pm.skinCluster(l_jnt, tmp_target, nw=1)

        skin_source.setNormalizeWeights(0)
        pm.skinPercent(skin_source, tmp_source, nrm=False, prw=100)
        skin_source.setNormalizeWeights(True)
        [pm.setAttr('{}.wl[{}].w[{}]'.format(skin_source, i, 0), value) for i, value in enumerate(deformer_weights)]
        [pm.setAttr('{}.wl[{}].w[{}]'.format(skin_source, i, 1), 1.0 - value) for i, value in
         enumerate(deformer_weights)]

        pm.copySkinWeights(ss=skin_source, ds=skin_target, nm=True, sa="closestPoint")

        wire_b_weights = [v for v in skin_target.getWeights(tmp_target, 0)]
        [def_target.weightList[0].weights[i].set(val) for i, val in enumerate(wire_b_weights)]

        pm.delete([tmp_source, tmp_target, l_jnt])


ui = CopyDeformerWeights()
ui.show()
