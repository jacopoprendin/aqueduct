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

class AqueductHTMLDriver(object):
    """
    AqueductDriver how a AqueductFSM writes output. This is a default driver,
    it returns a XML code. Not very usefull, but good for debug
    """

    def __init__(self):
        """
        """
        self.header_text=headers.html
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
        self.output.append('<div class="description">\n')

    def OpenSceneHeader(self,line):
        self.output.append('<div class="description">\n')
        self.output.append(line)

    def OpenDialogueForCharacter(self,character):
        self.output.append(('<div class="dialogue"><div class="character">%s</div>\n')%(character,))

    def AddSceneTitle(self,line):
        print "HTMLDriver: Apro la scena titolata "+line
        self.output.append(("<h3>%s</h3>\n")%(line,))

    def CloseDescription(self):
        self.output.append("\n</div>\n")

    def CloseSceneHeader(self):
        self.output.append("</div>\n")

    def CloseDialogue(self):
        self.output.append("\n</div>\n")

    def CloseSceneTitle(self):
        self.output.append("</h3>\n")


    # AddPageBreak
    def AddPageBreak(self):
        """
        Uses breakpage to define a format-specific break page
        """
        self.output.append("")

    # CloseDocument
    def CloseDocument(self):
        """
        Appends closing statements
        """
        self.output.append("</body>\n</html>\n")
