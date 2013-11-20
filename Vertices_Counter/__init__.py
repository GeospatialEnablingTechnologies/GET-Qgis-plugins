# -*- coding: utf-8 -*-
"""
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
  from Vertices_Counter import Vertices_Counter
  return Vertices_Counter(iface)
