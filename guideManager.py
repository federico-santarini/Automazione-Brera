#!/usr/bin/env python3
# coding: utf-8

# --------------------- #
# Design Week Catalogue #
# --------------------- #

### Modules
# std library
import sys
import importlib
from os.path import abspath
#sys.path.append(abspath('../IndesignXML'))

# dependencies
import builders
importlib.reload(builders)
from builders import buildFileTree
from builders import buildBaseTree, buildPlusTree

import file_IO
importlib.reload(file_IO)
from file_IO import loadCompanies

# locals
from sharedValues import JSON_PATH


### Variables
isDraft = True

### Instructions
baseCompanies, plusCompanies, sponsorCompanies = loadCompanies(JSON_PATH)

# Starting Indexes
sponsorStartIndex = 1
plusStartIndex = len(sponsorCompanies)+1
baseStartIndex = len(sponsorCompanies) + len(plusCompanies)+1

# Sponsor Companies

# Plus Companies
#buildFileTree('plus', plusCompanies, dwImg=False)
buildPlusTree(3, plusCompanies, plusStartIndex)

buildBaseTree(4, baseCompanies, baseStartIndex)
