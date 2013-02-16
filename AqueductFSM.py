#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import headers

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
    def __init__(self):
        self.current_state=self.TITLE_TITLE
        self.header_text=headers.xml
        self.head_dictionary={
            'Title':'title',
            'Author':'author name',
            'Source':'source',
            'Draft date':datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
            'Contact':'email, address, ecc.',
            }

        self.output=[]
        self.scene_number=1

    # AddTitlePage
    def AddTitlePage(self):
        """
        Adds title page to header, using a format-string for
        header

        @param a format string for current output mode
        """
        self.output.append(self.header_text%\
                               (self.head_dictionary['Draft date'],
                                self.head_dictionary['Title'],
                                self.head_dictionary['Source'],
                                self.head_dictionary['Author'],
                                self.head_dictionary['Contact']))

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

        # title_* state
        if (self.current_state==self.TITLE_TITLE or\
                self.current_state==self.TITLE_AUTHOR or\
                self.current_state==self.TITLE_DATE or\
                self.current_state==self.TITLE_SOURCE or\
                self.current_state==self.TITLE_CONTACT):
            if (line=='\n'):
                DebugPrint("Passo a Probable title end")
                self.current_state=self.PROBABLE_TITLE_END
                return
            # we have text. it MUST be a title key/value
            else:
                kw=line.split(':')
                if (len(kw)<2):
                    raise AqueductFSMException(("""ParseLine. Expected a title
key-value at line %d instead of %s""")%(index,line))

                # line ok: let's parse it
                else:
                    self.__TitleSet(kw[0],kw[1],index)
                    return

        # Probable title end
        elif (self.current_state==self.PROBABLE_TITLE_END):
            # if we have another \n, then title page
            # is over. Write title page and close
            if (line=='\n'):
                self.AddTitlePage()
                self.AddPageBreak()
                self.current_state=self.SCENE_TITLE
                self.OpenSceneTitle(line)
                return
        
        # scene title: this isn't part of fountain's definition. It's
        # something I use to easily organize my work (JaK)
        elif (self.current_state==self.SCENE_TITLE):
            # empty new line: go to scene header
            if (self.__isSceneHeader(line)):
                self.CloseSceneTitle()
                self.OpenSceneHeader(line)
                self.current_state=self.SCENE_HEADER
                return

        # scene header
        elif (self.current_state==self.SCENE_HEADER):
            self.current_state=self.DESCRIPTION
            self.CloseSceneHeader()
            self.OpenDescription(line)
            return 

        # Description state
        elif (self.current_state==self.DESCRIPTION):
            if (line=='\n'):
                return
            # pass to description if current line is a 
            # full-uppercase string
            if (line.isupper()):
                self.CloseDescription()
                self.current_state=self.DIALOGUE
                self.OpenDialogueForCharacter(line)
                return

            # new scene title?
            elif (line[0:7]=='SCENE: '):
                self.current_state=self.SCENE_TITLE
                return

            # new scene header?
            elif (self.__isSceneHeader(line)):
                self.OpenSceneHeader(line)
                self.current_state=self.SCENE_HEADER

            else:
                DebugPrint("Aggiungo riga")
                self.output.append(line)

        # dialogue state
        elif (self.current_state==self.DIALOGUE):
            # a empty line means "description!"
            if (line=='\n'):
                self.CloseDialogue()
                self.current_state=self.DESCRIPTION
                self.OpenDescription(line)
                return
            else:
                self.output.append(line)

        # else... add a line to current state
        else:
            raise AqueductFSMException("Unknown state")

    # OPEN/CLOSE Methods
    def OpenDescription(self,line):
        self.output.append("<description>\n")
        self.output.append(line)

    def OpenSceneHeader(self,line):
        self.output.append("<scene_header>\n")
        self.output.append(line)

    def OpenDialogueForCharacter(self,character):
        self.output.append(('<say w="%s">\n')%(character,))

    def OpenSceneTitle(self,line):
        self.output.append("<scene>\n")
        self.output.append(line)

    def CloseDescription(self):
        self.output.append("</description>\n")

    def CloseSceneHeader(self):
        self.output.append("</scene_header>\n")

    def CloseDialogue(self):
        self.output.append("</say>\n")

    def CloseSceneTitle(self):
        self.output.append("</scene>\n")


    # AddPageBreak
    def AddPageBreak(self):
        """
        Uses breakpage to define a format-specific break page
        """
        self.output.append("<br/>")

################################# UNIT TEST #################################
if (__name__=='__main__'):
    afsm=AqueductFSM()
    
    x=file("/home/jprendin/personal/StoriaDiUnaCampana.txt")

    lines=x.readlines()
    
    for index in range(0,len(lines)):
        afsm.ParseLine(lines[index],index)

    x.close()
    y=file("Test.xml",'w')
    y.writelines(afsm.output)
    y.close()
