#!/usr/bin/env python3

"""
Geoscience Australia - Python Geodesy Package
Survey Data Converter - DynAdjust DNA v3 Output Tools
"""

from math import atan, degrees, sqrt
from geodepy.convert import dd2sec


def dnaout_dirset(obslist, same_stdev=True, stdev=1, pointing_err=0.001):
    # Test for Single Observation
    if len(obslist) < 2:
        return []
    fromlist = []
    for ob in obslist:
        fromlist.append(ob.from_id)
    fromlist = list(set(fromlist))
    if len(fromlist) != 1:
        raise ValueError('Direction Set requires obs with same from_id')
    else:
        pass
    dnaobs = []
    if same_stdev:
        # create first line using obslist[0]
        line1 = ('D '
                 + obslist[0].from_id.ljust(20)
                 + obslist[0].to_id.ljust(20)
                 + str(len(obslist)-1).ljust(20)
                 + str(obslist[0].hz_obs.degree).rjust(17)
                 + ' '
                 + str('%02d' % obslist[0].hz_obs.minute)
                 + ' '
                 + str('{:.3f}'.format(obslist[0].hz_obs.second).rjust(6, '0').ljust(8))
                 + ('{:.4f}'.format(stdev)))  # add standard deviation
        dnaobs.append(line1)
        # create other lines using range(1:)
        for num in range(1, len(obslist)):
            line = ('D '
                    + ''.ljust(40)
                    + obslist[num].to_id.ljust(20)
                    + str(obslist[num].hz_obs.degree).rjust(17)
                    + ' '
                    + str('%02d' % obslist[num].hz_obs.minute)
                    + ' '
                    + str('{:.3f}'.format(obslist[num].hz_obs.second).rjust(6, '0').ljust(8))
                    + ('{:.4f}'.format(stdev)))  # add standard deviation
            dnaobs.append(line)
    else:
        # calc stdev for first ob
        if obslist[0].sd_obs == 0:
            stdev_pt = stdev
        else:
            pointing_err_pt = dd2sec(degrees(atan(pointing_err / obslist[0].sd_obs)))
            stdev_pt = str(sqrt((pointing_err_pt ** 2) + (stdev ** 2)))
        # create first line using obslist[0]
        line1 = ('D '
                 + obslist[0].from_id.ljust(20)
                 + obslist[0].to_id.ljust(20)
                 + str(len(obslist)-1).ljust(20)
                 + str(obslist[0].hz_obs.degree).rjust(17)
                 + ' '
                 + str('%02d' % obslist[0].hz_obs.minute)
                 + ' '
                 + str('{:.3f}'.format(obslist[0].hz_obs.second).rjust(6, '0').ljust(8))
                 + stdev_pt[0:5])  # add standard deviation
        dnaobs.append(line1)
        # create other lines using range(1:)
        for num in range(1, len(obslist)):
            if obslist[num].sd_obs == 0:  # keep
                stdev_pt = stdev
            else:
                pointing_err_pt = dd2sec(degrees(atan(pointing_err / obslist[num].sd_obs)))
                stdev_pt = str(sqrt((pointing_err_pt ** 2) + (stdev ** 2)))
            line = ('D '
                    + ''.ljust(40)
                    + obslist[num].to_id.ljust(20)
                    + str(obslist[num].hz_obs.degree).rjust(17)
                    + ' '
                    + str('%02d' % obslist[num].hz_obs.minute)
                    + ' '
                    + str('{:.3f}'.format(obslist[num].hz_obs.second).rjust(6, '0').ljust(8))
                    + stdev_pt[0:5])  # add standard deviation
            dnaobs.append(line)
    return dnaobs


def dnaout_sd(obslist, stdev=0.001):
    dnaobs = []
    for observation in obslist:
        # Exclude slope distances of 0m
        if observation.sd_obs == 0:
            pass
        else:
            line = ('S '
                    + observation.from_id.ljust(20)
                    + observation.to_id.ljust(20)
                    + ''.ljust(19)
                    + ('{:.4f}'.format(observation.sd_obs)).rjust(9)
                    + ''.ljust(21)
                    + ('{:.4f}'.format(stdev)).ljust(8)         # add standard deviation
                    + str(observation.inst_height).ljust(7)      # add intrument height
                    + ('{:.3f}'.format(observation.target_height)))
            dnaobs.append(line)
    return dnaobs


def dnaout_va(obslist, same_stdev=True, stdev=1, pointing_err=0.001):
    dnaobs = []
    if same_stdev:
        for observation in obslist:
            # Format Line
            line = ('V '
                    + observation.from_id.ljust(20)
                    + observation.to_id.ljust(20)
                    + ''.ljust(34)
                    + str(observation.va_obs.degree).rjust(3)
                    + ' '
                    + str(observation.va_obs.minute).rjust(2, '0')
                    + ' '
                    + ('{:.3f}'.format(observation.va_obs.second).rjust(6, '0')).ljust(8)
                    + ('{:.4f}'.format(stdev)).ljust(8)         # add standard deviation
                    + ('{:.3f}'.format(observation.inst_height)).ljust(7)      # add intrument height
                    + ('{:.3f}'.format(observation.target_height)))
            dnaobs.append(line)
    else:
        for observation in obslist:
            # Calc Standard Deviation (in seconds) based on pointing error (in metres)
            # and angular standard deviation (in seconds)
            if observation.sd_obs == 0:
                stdev_pt = stdev
            else:
                pointing_err_pt = dd2sec(degrees(atan(pointing_err / observation.sd_obs)))
                stdev_pt = str(sqrt((pointing_err_pt ** 2) + (stdev ** 2)))
            # Format Line
            line = ('V '
                    + observation.from_id.ljust(20)
                    + observation.to_id.ljust(20)
                    + ''.ljust(34)
                    + str(observation.va_obs.degree).rjust(3)
                    + ' '
                    + str(observation.va_obs.minute).rjust(2, '0')
                    + ' '
                    + str(('{:.3f}'.format(observation.va_obs.second).rjust(6, '0')).ljust(8))
                    + stdev_pt[0:5].ljust(8)  # add standard deviation
                    + ('{:.3f}'.format(observation.inst_height)).ljust(7)  # add intrument height
                    + ('{:.3f}'.format(observation.target_height)))
            dnaobs.append(line)
    return dnaobs
