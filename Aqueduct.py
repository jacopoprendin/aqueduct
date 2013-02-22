#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Written by Jacopo Prendin (nidnerpREPLACEWITHANICEATCHARACTERgmail.com)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

from AqueductFSM import AqueductFSM
from AqueductLatexDriver import AqueductLatexDriver
from AqueductHTMLDriver import AqueductHTMLDriver
# ************************************************************
#                           MAIN()
# ************************************************************
if (__name__=='__main__'):
    if (len(sys.argv)<3):
        print "Usage: Aqueduct.py <filename> <format>"
        sys.exit(1)

    driver=None
    screenplay_file=file(sys.argv[1])
    screenplay_type=sys.argv[2]

    # set choosed driver
    if (screenplay_type=='html'):
        driver=AqueductHTMLDriver()
    elif (screenplay_type=='latex'):
        driver=AqueductLatexDriver()
    else:
        driver=AqueductDriver()

    afsm=AqueductFSM(driver)

    lines=screenplay_file.readlines()

    # for each line, FiniteStateMachine analize it
    for index in range(0,len(lines)):
        afsm.ParseLine(lines[index],index)

    afsm.CloseDocument()
    
    screenplay_file.close()

    # create output file
    if (sys.argv[1].find('fountain')>=0):
        output_filename=sys.argv[1].replace('fountain',screenplay_type)
    else:
        output_filename=sys.argv[1]+"."+screenplay_type
        
    y=file(output_filename,'w')
    y.writelines(driver.output)
    y.close()
