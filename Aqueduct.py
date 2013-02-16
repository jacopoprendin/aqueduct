#!/usr/bin/env python
import sys

import headers


output_type='html'
output=[]



current_state=TITLE_TITLE

## OpenDialogue
def OpenDialogue(character_name):
    """
    Opens a dialogue block for specified character

    @param character_name character whom have something to say
    """
    if (output_type=='latex'):
        output.append("\\begin{dialogue}{%s}\n"%(character_name,))

    elif (output_type=='xml'):
        output.append("<say w=\"%s\" "%(character_name,))

    elif (output_type=='html'):
        output.append("<div class=\"dialogue\"><div class=\"character\">%s</div>\n"%\
                          (character_name,)
                      )

    else:
        print "Unknown output:"
        print output_type

## OpenDescription
def OpenDescription(desc_line):
    """
    Opens a description
    """
    if (output_type=='latex'):
        output.append(desc_line)

    elif (output_type=='xml'):
        output.append("<desc>%s"%(desc_line,))

    elif (output_type=='html'):
        output.append("<div class=\"description\">%s\n"%\
                          (desc_line,)
                      )

    else:
        print "Unknown output:"
        print output_type

## CloseDescription
def CloseDescription():
    if (output_type=='latex'):
        output.append("\\\\ \\\\ \n")

    elif (output_type=='xml'):
        output.append("</desc>\n\n")

    elif (output_type=='html'):
        output.append("</div>\n\n")

    else:
        print "Unknown output:"
        print output_type

## AddLine
def AddLine(line):
    if (output_type=='latex'):
        output.append(line)

    elif (output_type=='xml'):
        output.append(line)

    elif (output_type=='html'):
        output.append(line)

    else:
        print "Unknown output:"
        print output_type

## CloseDialogue
def CloseDialogue():
    if (output_type=='latex'):
        output.append("\\end{dialogue}\n\n")

    elif (output_type=='xml'):
        output.append(" />\n\n")

    elif (output_type=='html'):
        output.append("</div>\n\n")

    else:
        print "Unknown output:"
        print output_type
# ************************************************************
#                           MAIN()
# ************************************************************
if (__name__=='__main__'):
    screenplay_file=file(sys.argv[1])

    lines=screenplay_file.readlines()

    dialogue=False
    description=False

    # informations for title page
    current_state=TITLE_TITLE

    

    
    else:
        output.append(date+" "+title+" "+author+" "+address)
    # parse each line
    for line in lines:
        line=line[:-1]
        # get informations about title page
        # WARNING! It's required at top!
        

        if (line.isupper()):
            dialogue=True
            OpenDialogue(line)
            continue
        
        # are we closing a statement?
        elif (line==""):
            # close dialogue
            if (dialogue==True):
                dialogue=False
                CloseDialogue()

            elif (description==True):
                description=False
                CloseDescription()

            else:
                print "BOH"

        # description
        else:
            if (description==False and dialogue==False):
                description=True
                OpenDescription(line)
                continue

        if (dialogue==True or description==True):
            # put line in current state
            AddLine(line)
            continue

     
    #end for

    for i in output:
        print i
