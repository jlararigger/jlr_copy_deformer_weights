#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################################################################
# jlr_copy_deformer_weights_UI.py - Python Script
##################################################################################
# Description:
# This tool was created to copy the weight map of a deformer of an object to the deformer of another object.
#
# The deformers do not have to be of the same type between them. It is possible to copy the weight map of
# a wire deformer into a weight map of a cluster deformer or other deformer.
#
# Author: Juan Lara.
##################################################################################

from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI

import pymel.core as pm


class CopyDeformerWeightsUI(object):
    """
    CopyDeformerWeights Class
    """

    def __init__(self):
        self.transfer_function = None

        """
        Create the CopyDeformerWeights UI
        """
        self.dialog = QtWidgets.QDialog()
        self.dialog_name = "copy_deformer_weights_dialog"
        self.delete_instances()

        self.maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        self.maya_main_window = wrapInstance(long(self.maya_main_window_ptr), QtWidgets.QMainWindow)
        self.dialog.setParent(self.maya_main_window)
        self.dialog.setWindowFlags(QtCore.Qt.Window)

        self.dialog.setObjectName(self.dialog_name)
        self.dialog.setFixedSize(400, 500)
        self.dialog.setWindowTitle("Copy Deformer Weights")

        self.dialog_layout = QtWidgets.QGridLayout(self.dialog)
        self.dialog_layout.setObjectName("dialog_layout")

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setObjectName("main_layout")

        self.source_group_box = QtWidgets.QGroupBox(self.dialog)
        self.source_group_box.setObjectName("source_group_box")
        self.source_group_box.setTitle("Source")

        self.source_gb_layout = QtWidgets.QGridLayout(self.source_group_box)
        self.source_gb_layout.setObjectName("source_gb_layout")

        self.source_layout = QtWidgets.QVBoxLayout()
        self.source_layout.setObjectName("source_layout")

        self.btn_source = QtWidgets.QPushButton(self.source_group_box)
        self.btn_source.setObjectName("btn_source")
        self.btn_source.setText("Get Source")
        self.btn_source.clicked.connect(lambda: self.get_source_items())
        self.source_layout.addWidget(self.btn_source)

        self.source_list_layout = QtWidgets.QHBoxLayout()
        self.source_list_layout.setObjectName("source_list_layout")

        self.object_source_list = QtWidgets.QListWidget(self.source_group_box)
        self.object_source_list.setObjectName("object_source_list")
        self.object_source_list.currentItemChanged.connect(lambda: self.update_source_deformer_list())
        self.source_list_layout.addWidget(self.object_source_list)

        self.deformer_source_list = QtWidgets.QListWidget(self.source_group_box)
        self.deformer_source_list.setObjectName("deformer_source_list")
        self.source_list_layout.addWidget(self.deformer_source_list)

        self.source_layout.addLayout(self.source_list_layout)
        self.source_gb_layout.addLayout(self.source_layout, 0, 0, 1, 1)

        self.main_layout.addWidget(self.source_group_box)

        self.target_group_box = QtWidgets.QGroupBox(self.dialog)
        self.target_group_box.setObjectName("target_group_box")
        self.target_group_box.setTitle("Target")

        self.target_gb_layout = QtWidgets.QGridLayout(self.target_group_box)
        self.target_gb_layout.setObjectName("target_gb_layout")

        self.target_layout = QtWidgets.QVBoxLayout()
        self.target_layout.setObjectName("target_layout")

        self.btn_target = QtWidgets.QPushButton(self.target_group_box)
        self.btn_target.setObjectName("btn_target")
        self.btn_target.setText("Get Target")
        self.btn_target.clicked.connect(lambda: self.get_target_items())
        self.target_layout.addWidget(self.btn_target)

        self.target_list_layout = QtWidgets.QHBoxLayout()
        self.target_list_layout.setObjectName("target_list_layout")

        self.object_target_list = QtWidgets.QListWidget(self.target_group_box)
        self.object_target_list.setObjectName("object_target_list")
        self.object_target_list.currentItemChanged.connect(lambda: self.update_target_deformer_list())
        self.target_list_layout.addWidget(self.object_target_list)

        self.deformer_target_list = QtWidgets.QListWidget(self.target_group_box)
        self.deformer_target_list.setObjectName("deformer_target_list")
        self.target_list_layout.addWidget(self.deformer_target_list)

        self.target_layout.addLayout(self.target_list_layout)
        self.target_gb_layout.addLayout(self.target_layout, 0, 0, 1, 1)
        self.main_layout.addWidget(self.target_group_box)

        self.progress_bar_layout = QtWidgets.QVBoxLayout()
        self.progress_bar_layout.setObjectName("progress_bar_layout")
        self.progress_bar = QtWidgets.QProgressBar(self.dialog)

        self.progress_bar.setProperty("value", -1)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar_layout.addWidget(self.progress_bar)

        self.progress_label = QtWidgets.QLabel(self.dialog)
        self.progress_label.setObjectName("progress_label")
        self.progress_label.setMinimumSize(QtCore.QSize(0, 21))
        self.progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_bar_layout.addWidget(self.progress_label)
        self.main_layout.addLayout(self.progress_bar_layout)
        self._progress_bar_steps = 8
        self._progress_bar_value = -1

        self.buttons_group_box = QtWidgets.QGroupBox(self.dialog)
        self.buttons_group_box.setTitle("")
        self.buttons_group_box.setObjectName("buttons_group_box")

        self.buttons_gb_layout = QtWidgets.QHBoxLayout(self.buttons_group_box)
        self.buttons_gb_layout.setObjectName("buttons_gb_layout")

        self.copy_button = QtWidgets.QPushButton(self.buttons_group_box)
        self.copy_button.setObjectName("copy_button")
        self.copy_button.setText("Copy")
        self.copy_button.clicked.connect(lambda: self.copy_deformer_weights())
        self.buttons_gb_layout.addWidget(self.copy_button)

        self.cancel_button = QtWidgets.QPushButton(self.buttons_group_box)
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(lambda: self.delete_instances())
        self.buttons_gb_layout.addWidget(self.cancel_button)

        self.main_layout.addWidget(self.buttons_group_box)
        self.dialog_layout.addLayout(self.main_layout, 0, 0, 1, 1)

    @property
    def progress_bar_steps(self):
        return self._progress_bar_steps

    @progress_bar_steps.setter
    def progress_bar_steps(self, value):
        assert isinstance(value, int), "Progress Bar Steps must be a integer"
        self._progress_bar_steps = value

    @property
    def progress_bar_value(self):
        return self._progress_bar_value

    @progress_bar_value.setter
    def progress_bar_value(self, value):
        assert isinstance(value, (int, float)), "Progress Bar Value must be a integer or float"
        self._progress_bar_value = value

    def progress_bar_init(self):
        """
        Hide the label and initialize the progress bar.
        """
        self.progress_label.hide()
        self.progress_bar_value = 0
        self.progress_bar.show()
        self.progress_bar_layout.update()

    def progress_bar_next(self):
        """
        Update the progress bar value.
        """
        self.progress_bar_value += 1
        self.progress_bar.setValue((100.0 / self.progress_bar_steps) * self.progress_bar_value)

    def progress_bar_ends(self, message):
        """
        Closes the progress bar and show label with a message.
        """
        self.progress_bar.hide()
        self.progress_label.show()
        self.progress_label.setText(message)

    def get_source_items(self):
        """
        Gets the selected objects in the scene and fills the source lists.
        """
        if pm.selected():
            self.update_source_list(pm.selected())
            self.update_source_deformer_list()

    def update_source_list(self, l_items):
        """
        Fills the source list widget.
        :param l_items: list with the name of source objects.
        """
        if l_items:
            self.populate_list_widget(self.object_source_list, l_items)

    def update_source_deformer_list(self):
        """
        Fills the list of deformers according to the selected object in the source object list.
        """
        item = pm.PyNode(self.object_source_list.currentItem().text())
        self.populate_list_widget(self.deformer_source_list, self.get_deformer_list(item))

    def get_target_items(self):
        """
        Gets the selected objects in the scene and fills the target lists.
        """
        if pm.selected():
            self.update_target_list(pm.selected())
            self.update_target_deformer_list()

    def update_target_list(self, l_items):
        """
        Updates the target list widget.
        :param l_items: list with the name of target objects.
        """
        if l_items:
            self.populate_list_widget(self.object_target_list, l_items)

    def update_target_deformer_list(self):
        """
        Fills the list of deformers according to the selected object in the target object list.
        """
        item = pm.PyNode(self.object_target_list.currentItem().text())
        self.populate_list_widget(self.deformer_target_list, self.get_deformer_list(item))

    @staticmethod
    def get_deformer_list(item):
        """
        Returns a list with the deformers connected to a object.
        :param item: PyNode with shapes
        :return: list
        """
        if pm.objExists(item):
            shape = item.getShapes()[0]
            deformer_list = pm.listHistory(shape, ha=1, il=1, pdo=1)
            deformer_types = ["ffd", "wire", "cluster", "softMod", "deltaMush", "textureDeformer"]
            deformer_list = list(filter(lambda x: x.type() in deformer_types, deformer_list))
            return deformer_list
        else:
            return list()

    @staticmethod
    def populate_list_widget(list_widget, l_items):
        """
        Fills a QListWidget with the passed list.
        :param list_widget: QListWidget
        :param l_items: list of PyNodes.
        """
        list_widget.clear()
        for item in l_items:
            list_widget_item = QtWidgets.QListWidgetItem()
            list_widget_item.setText(item.nodeName())
            list_widget.addItem(list_widget_item)

        list_widget.setCurrentRow(0)

    def copy_deformer_weights(self):
        """
        Checks if the selected items are a valid selection and call the copy function.
        """
        assert self.transfer_function is not None, "The transfer_function variable must be contain a transfer_function function."

        geo_source = self.object_source_list.currentItem()
        geo_target = self.object_target_list.currentItem()
        deformer_source = self.deformer_source_list.currentItem()
        deformer_target = self.deformer_target_list.currentItem()

        if geo_source and geo_target and deformer_source and deformer_target:
            data = {"geo_source": pm.PyNode(geo_source.text()),
                    "geo_target": pm.PyNode(geo_target.text()),
                    "deformer_source": pm.PyNode(deformer_source.text()),
                    "deformer_target": pm.PyNode(deformer_target.text()),
                    "surface_association": "closestPoint",
                    "interface": self,
                    }

            self.transfer_function(**data)

    def show(self):
        """
        Shows the CopyDeformerWeights UI.
        If there are selected items previously in the scene, the first selected item will be loaded as source object
        and the rest of objects will be loaded as target objects.
        """
        self.dialog.show()
        self.progress_bar.hide()
        self.progress_label.setText("Select the objects and its deformers")
        self.progress_bar_layout.update()

        if pm.selected():
            self.update_source_list(pm.selected()[0:1])
            self.update_source_deformer_list()
            if len(pm.selected()) > 1:
                self.update_target_list(pm.selected()[1:])
                self.update_target_deformer_list()

    def delete_instances(self):
        """
        Deletes the UI
        """
        if pm.window(self.dialog_name, exists=True):
            pm.deleteUI(self.dialog_name)


