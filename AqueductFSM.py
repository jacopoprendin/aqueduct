#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Written by Jacopo Prendin (nidnerp@gmail.com)
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

import datetime
import headers

from AqueductDriver import AqueductDriver

def DebugPrint(string):
    print string


class AqueductFSMException(Exception):
    pass

# AqueductFSM
class AqueductFSM(object):
    """
    A finite state machine to manage a Fountain file.
    """
    # States
    TITLE_TITLE=0
    TITLE_CREDIT=1
    TITLE_AUTHOR=2
    TITLE_SOURCE=3
    TITLE_DATE=4
    TITLE_CONTACT=5
    PROBABLE_TITLE_END=6
    SCENE_TITLE=7
    SCENE_HEADER=8
    DESCRIPTION=9
    DIALOGUE=10

    # init
    def __init__(self,driver):
        """
        Creates a new AqueductFSM which uses a AqueductDriver to
        write output
        """
        self.current_state=self.TITLE_TITLE
        self.header_text=headers.xml
        self.head_dictionary={
            'Title':'title',
            'Author':'author name',
            'Source':'source',
            'Draft date':datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
            'Contact':'email, address, ecc.',
            }

        self.driver=driver
        self.scene_number=1

    # __TitleSet
    def __TitleSet(self,key,value,index):
        """
        Sugar method to set title keys
        """
        if (key not in self.head_dictionary.keys()):
            raise AqueductFSMException(("ParseLine:Unknown title key %s at line %d")%(key,index))

        else:
            self.head_dictionary[key]=value
            if (key=='Title'): self.current_state=self.TITLE_TITLE
            elif (key=='Author'): self.current_state=self.TITLE_AUTHOR
            elif (key=='Contact'): self.current_state=self.TITLE_CONTACT
            elif (key=='Source'): self.current_state=self.TITLE_SOURCE
            elif (key=='Draft Date'): self.current_state=self.TITLE_DATE

    # __isSceneHeader
    def __isSceneHeader(self,line):
        """
        is current line a scene header?
        
        @param line line to analize
        """
        if (line=="\n"):
            return False
        
        k=line[0:3]
        s=line[4]
        if ((k=='INT' and (s=='.' or s==' ')) or\
                (k=='EXT' and (s=='.' or s==' ')) or\
                (k=='EST' and (s=='.' or s==' ')) or\
                (k=='INT' and (s=='.' or s==' ')) or\
                (k=='I/E' and (s=='.' or s==' ')) or\
                (line[0:7]=='INT./EXT') or\
                (line[0:6]=='INT./EXT') ):
            return True
        else:
            return False


    # ParseLine
    def ParseLine(self,line,index):
        """
        Write line and/or change Finite State Machine state

        @param line line to parse
        @param index is current line index
        """

        # if line is not just a new-line character, remove
        # the new-line character
        if (line!="\n"):
            line=line[:-1]
            
        # title_* state
        if (self.current_state==self.TITLE_TITLE or\
                self.current_state==self.TITLE_AUTHOR or\
                self.current_state==self.TITLE_DATE or\
                self.current_state==self.TITLE_SOURCE or\
                self.current_state==self.TITLE_CONTACT):
            if (line=='\n'):
                self.current_state=self.PROBABLE_TITLE_END
            # we have text. it MUST be a title key/value
            else:
                kw=line.split(':')
                if (len(kw)<2):
                    raise AqueductFSMException(("""ParseLine. Expected a title
key-value at line %d instead of %s""")%(index,line))

                # line ok: let's parse it
                else:
                    self.__TitleSet(kw[0],kw[1],index)

        # Probable title end
        elif (self.current_state==self.PROBABLE_TITLE_END):
            # if we have another \n, then title page
            # is over. Write title page and close
            if (line=='\n'):
                self.driver.AddTitlePage(self.head_dictionary)
                self.driver.AddPageBreak()

                # have a scene title or a scene description?
                if (line[0:4]=='Scene'):
                    self.current_state=self.SCENE_TITLE
                    self.driver.OpenSceneTitle(line)
                else:
                    self.current_state=self.SCENE_HEADER
                    self.driver.OpenSceneHeader(line)
        
        # scene title: this isn't part of fountain's definition. It's
        # something I use to easily organize my work (JaK)
        elif (self.current_state==self.SCENE_TITLE):
            # empty new line: go to scene header
            if (self.__isSceneHeader(line)):
                self.driver.CloseSceneTitle()
                self.driver.OpenSceneHeader(line)
                self.current_state=self.SCENE_HEADER

        # scene header
        elif (self.current_state==self.SCENE_HEADER):
            self.current_state=self.DESCRIPTION
            self.driver.CloseSceneHeader()
            self.driver.OpenDescription()
            self.driver.output.append(line)

        # Description state
        elif (self.current_state==self.DESCRIPTION):
            if (line=='\n'):
                return
            # pass to description if current line is a 
            # full-uppercase string
            if (line.isupper()):
                self.current_state=self.DIALOGUE
                self.driver.CloseDescription()
                self.driver.OpenDialogueForCharacter(line)

            # new scene title?
            elif (line[0:7]=='SCENE: '):
                self.current_state=self.SCENE_TITLE

            # new scene header?
            elif (self.__isSceneHeader(line)):
                self.driver.OpenSceneHeader(line)
                self.current_state=self.SCENE_HEADER
            else:
                self.driver.output.append(line)

        # dialogue state
        elif (self.current_state==self.DIALOGUE):
            # a empty line means "description!"
            if (line=='\n'):
                self.current_state=self.DESCRIPTION
                self.driver.CloseDialogue()
                self.driver.OpenDescription()
                return
            else:
                self.driver.output.append(line)

        # else... add a line to current state
        else:
            raise AqueductFSMException("Unknown state")

    # CloseDocument
    def CloseDocument(self):
        if (self.current_state==self.DESCRIPTION):
            self.driver.CloseDescription()
        elif (self.current_state==self.DIALOGUE):
            self.driver.CloseDialogue()
        else:
            raise AqueductFSMException("Unknow state on closing")

        self.driver.CloseDocument()
################################# UNIT TEST #################################
if (__name__=='__main__'):
    driver=AqueductDriver()
    afsm=AqueductFSM(driver)
    
    x=file("test_script.funtain")

    lines=x.readlines()
    
    for index in range(0,len(lines)):
        afsm.ParseLine(lines[index],index)

    afsm.CloseDocument()
    
    x.close()
    y=file("Test.xml",'w')
    y.writelines(driver.output)
    y.close()
