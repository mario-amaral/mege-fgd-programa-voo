# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 13:49:22 2022

@author: mario
"""

import simplekml
import utm

kml = simplekml.Kml()

P1_utm = (484845.0, 4290518.0)

P1 = utm.to_latlon(P1_utm[0], P1_utm[1], 29, zone_letter="S") #é necessário definir a zona e a letra da projeção UTM

kml.newpoint(name='Point1', coords=[(P1[1], P1[0])])
# kml.newpoint(name='Point3', coords=[(484775., 4287816.)])
# kml.newpoint(name='Point4', coords=[(488722., 4287616.)])
kml.save('points.kml')

