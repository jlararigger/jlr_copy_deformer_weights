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

import pymel.core as pm


def transfer_deformer_weights(geo_source, geo_target=None, deformer_source=None, deformer_target=None,
                              surface_association="closestPoint", interface=None):
    """
    Copies the weight map of a deformer of an object to the deformer of another object.
    :param geo_source: Source Shape
    :param geo_target: Target Shape
    :param deformer_source: Source Deformer
    :param deformer_target: Target Deformer
    :param surface_association: Surface Association. Valid values: closestPoint, rayCast, or closestComponent.
    :param interface: Copy of class CopyDeformerWeightsUI
    """
    assert geo_source and deformer_source and deformer_target, \
        "select a source and target geometry and then the source and target deformers"

    previous_selection = pm.selected()

    if not geo_target:
        geo_target = geo_source

    if interface:
        interface.progress_bar_init()
        interface.progress_bar_next()

    source_weight_list = get_weight_list(deformer_source, geo_source)
    if not source_weight_list:
        pm.warning("The deformer {} does not have the weight list for {}".format(deformer_source, geo_source))
        if interface: interface.progress_bar_ends(message="Finished with errors!")
        return

    target_weight_list = get_weight_list(deformer_target, geo_target)
    if not target_weight_list:
        pm.warning("The deformer {} does not have the weight list for {}".format(deformer_target, geo_target))
        if interface: interface.progress_bar_ends(message="Finished with errors!")
        return

    initialize_weight_list(target_weight_list, geo_target)

    if interface: interface.progress_bar_next()
    tmp_source = pm.duplicate(geo_source)[0]
    tmp_target = pm.duplicate(geo_target)[0]
    pm.rename(tmp_source, tmp_source.nodeName() + "_cdw_DUP")
    pm.rename(tmp_target, tmp_target.nodeName() + "_cdw_DUP")
    tmp_source.v.set(True)
    tmp_target.v.set(True)

    if interface: interface.progress_bar_next()
    pm.select(clear=True)
    l_jnt = list()
    l_jnt.append(pm.joint(n="jnt_tmpA_01", p=[0, 0, 0]))
    l_jnt.append(pm.joint(n="jnt_tmpA_02", p=[0, 1, 0]))
    skin_source = pm.skinCluster(l_jnt, tmp_source, nw=1)
    skin_target = pm.skinCluster(l_jnt, tmp_target, nw=1)

    if interface: interface.progress_bar_next()
    skin_source.setNormalizeWeights(0)
    pm.skinPercent(skin_source, tmp_source, nrm=False, prw=100)
    skin_source.setNormalizeWeights(True)
    n_points = len(geo_source.getShape().getPoints())
    [skin_source.wl[i].w[0].set(source_weight_list.weights[i].get()) for i in range(n_points)]
    [skin_source.wl[i].w[1].set(1.0 - source_weight_list.weights[i].get()) for i in range(n_points)]

    if interface: interface.progress_bar_next()
    pm.copySkinWeights(ss=skin_source, ds=skin_target, nm=True, sa=surface_association)

    if interface: interface.progress_bar_next()
    deformer_target_weights = [v for v in skin_target.getWeights(tmp_target, 0)]
    [target_weight_list.weights[i].set(val) for i, val in enumerate(deformer_target_weights)]

    if interface: interface.progress_bar_next()
    pm.delete([tmp_source, tmp_target, l_jnt])
    pm.select(previous_selection)

    if interface:
        interface.progress_bar_next()
        interface.progress_bar_ends(message="Finished successfully!")


def get_weight_list(in_deformer, in_mesh):
    for index, each_input in enumerate(in_deformer.input):
        shape = in_mesh.getShape()
        l_connections = each_input.inputGeometry.listConnections(s=1, d=0)
        if l_connections:
            l_history = l_connections[0].listHistory(f=1)
            l_mesh = list(filter(lambda x: type(x) == type(shape), l_history))
            l_mesh = [str(mesh.nodeName()) for mesh in l_mesh]
            if str(shape.nodeName()) in l_mesh:
                weight_list = in_deformer.weightList[index]
                if not weight_list:
                    initialize_weight_list(in_deformer.weightList[index], in_mesh)

                return in_deformer.weightList[index]


def initialize_weight_list(weight_list, in_mesh):
    n_points = len(in_mesh.getShape().getPoints())
    [weight_list.weights[i_point].set(1) for i_point in range(n_points)]
