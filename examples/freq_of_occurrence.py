#!/usr/bin/python3

import sys
# just needed to find pyLARDA from this location
sys.path.append('../')
sys.path.append('.')

import matplotlib
matplotlib.use('Agg')
import pyLARDA
import datetime
import numpy as np

import logging

log = logging.getLogger('pyLARDA')
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

# Load LARDA
larda = pyLARDA.LARDA().connect('lacros_dacapo')
c_info = [larda.camp.LOCATION, larda.camp.VALID_DATES]

print('available systems:', larda.connectors.keys())
print("available parameters: ", [(k, larda.connectors[k].params_list) for k in larda.connectors.keys()])
print('days with data', larda.days_with_data())


date = '20190206'
begin_dt = datetime.datetime.strptime(date + ' 00:00:00', '%Y%m%d %H:%M:%S')
end_dt = datetime.datetime.strptime(date + ' 23:59:59', '%Y%m%d %H:%M:%S')
plot_range = [0, 12000]

# string for png name
time_height_MDF = '{}_{}_'.format(begin_dt.strftime("%Y%m%d_%H%M%S"), end_dt.strftime("%H%M%S")) \
                  + '{}-{}'.format(str(plot_range[0]), str(plot_range[1]))

"""
    Create frequency of occurrence plot for reflectivity values
"""
# load first LIMRAD dict to gather some more information
LIMRAD94_Ze = larda.read("LIMRAD94", "Ze", [begin_dt, end_dt], plot_range)

# load range_offsets, dashed lines where chirp shifts
range_C1 = larda.read("LIMRAD94", "C1Range", [begin_dt, end_dt], plot_range)['var'].max()
range_C2 = larda.read("LIMRAD94", "C2Range", [begin_dt, end_dt], plot_range)['var'].max()

# load sensitivity limits (time, height) and calculate the mean over time
LIMRAD94_SLv = larda.read("LIMRAD94", "SLv", [begin_dt, end_dt], plot_range)
sens_lim = np.mean(LIMRAD94_SLv['var'], axis=0)

# create frequency of occurrence plot of LIMRAD94 reflectivity and save as png
titlestring = 'LIMRAD94 Ze -- date: {}'.format(begin_dt.strftime("%Y-%m-%d"))
fig, ax = pyLARDA.Transformations.plot_frequency_of_occurrence(LIMRAD94_Ze, x_lim=[-70, 10], y_lim=plot_range,
                                                              sensitivity_limit=sens_lim, z_converter='lin2z',
                                                              range_offset=[range_C1, range_C2], title=titlestring)

fig.savefig('limrad_FOC_' + time_height_MDF + '.png', dpi=250)

