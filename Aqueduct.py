#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Written by Jacopo Prendin (nidnerp@gmail.com)

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

# ************************************************************
#                           MAIN()
# ************************************************************
if (__name__=='__main__'):
    screenplay_file=file(sys.argv[1])
    screenplay_type=sys.argv[2]
    
    lines=screenplay_file.readlines()

    driver=AqueductLatexDriver()
    afsm=AqueductFSM(driver)
    
    for index in range(0,len(lines)):
        afsm.ParseLine(lines[index],index)

    afsm.CloseDocument()
    
    screenplay_file.close()

    output_filename=sys.argv[1].replace('fountain','tex')
    y=file(output_filename,'w')
    y.writelines(driver.output)
    y.close()
