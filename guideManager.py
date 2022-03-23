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
from builders import buildBaseTree

import file_IO
importlib.reload(file_IO)
from file_IO import loadCompanies

# locals
from sharedValues import JSON_PATH


### Variables
isDraft = True

### Instructions
baseCompanies, plusCompanies, sponsorCompanies = loadCompanies(JSON_PATH)

buildBaseTree(4, baseCompanies)
