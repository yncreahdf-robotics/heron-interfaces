# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:11:40 2019

@author: Quentin
"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()
print(type(args.name))
