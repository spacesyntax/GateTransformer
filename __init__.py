# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NetworkTransformer
                                 A QGIS plugin
 This plugin performs basic transformation on a network class in qgis.
                             -------------------
        begin                : 2016-02-29
        copyright            : (C) 2016 by Stephen Law
        email                : s.law@spacesyntax.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load NetworkTransformer class from file NetworkTransformer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .network_transformer import NetworkTransformer
    return NetworkTransformer(iface)
