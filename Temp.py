# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:11:40 2019

@author: Quentin
"""

import os

def alive(host,it):
    if(it==0):
        return False
    else:
        if os.system("ping -c 1 "+host):
            return True
        else:
            return alive(host,it-1)
