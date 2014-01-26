#!/usr/bin/env python
# -*- coding utf-8 -*-

# Written by Jacopo Prendin (nidnerpREPLACEWITHANICEATCHARACTERgmail.com)
# This file is part of Aqueduct.
# Aqueduct is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Aqueduct is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Aqueduct.  If not, see <http://www.gnu.org/licenses/>.

import headers

class AqueductDriver(object):
    """
    AqueductDriver how a AqueductFSM writes output. This is a default driver,
    it returns a XML code. Not very usefull, but good for debug
    """

    def __init__(self):
        """
        """
        self.header_text=headers.xml
        self.output=[]
        
    # AddTitlePage
    def AddTitlePage(self,head):
        """
        Adds title page to header, using a format-string for
        header

        @param a format string for current output mode
        """
        self.output.append(self.header_text%\
        (head['Draft date'],head['Title'],
         head['Source'],head['Author'],
            head['Contact']))
        
      # OPEN/CLOSE Methods
    def OpenDescription(self):
        self.output.append("<description>\n")

    def OpenSceneHeader(self,line):
        self.output.append("<scene_header>\n")
        self.output.append(line)

    def OpenDialogueForCharacter(self,character):
        self.output.append(('<say w="%s">\n')%(character,))

    def AddSceneTitle(self,line):
        self.output.append(("<scene>%s</scene>\n")%(line,))

    def CloseDescription(self):
        self.output.append("\n</description>\n")

    def CloseSceneHeader(self):
        self.output.append("</scene_header>\n")

    def CloseDialogue(self):
        self.output.append("\n</say>\n")

    def CloseSceneTitle(self):
        self.output.append("</scene>\n")


    # AddPageBreak
    def AddPageBreak(self):
        """
        Uses breakpage to define a format-specific break page
        """
        self.output.append("<br/>")

    # AddNewLine
    def AddNewLine(self):
        """
        Force a new lines
        """
        self.output.append("<br/>")
        
    # CloseDocument
    def CloseDocument(self):
        """
        Appends closing statements
        """
        self.output.append("</screenplay>")
