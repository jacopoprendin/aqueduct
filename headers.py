#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

#
# Always require date, title, author, author's address
#

xml="""
<?xml version="1.0" encoding="UTF-8"?>
<screenplay>
<head>
    <date>%s<date>
    <title>%s<title>
    <author>%s<author>
    <source>%s<source>
    <contact>%s<contact>
    </head>

"""

html="""<html>
<head>
  <style>
    body
    {
    width:210mm;
    font-size:12px;
    font-family:Courier New, Monospace;
    }
    
    div.description
    {
    font-style:italic;
    margin-bottom:5mm;
    }

    div.dialogue
    {
    padding-left:20mm;
    padding-right:20mm;
    padding-bottom:5mm;
    }

    div.character
    {
    text-align:center;
    }
  </style>

</head>
<body>

<div class="date">%s</date>
<h1>%s</h1>
<p>by %s<br>
%s
</p>
"""

# ****************************** LATEX
latex="""
\\documentclass{screenplay}[%s]
\\title{%s}
\\credit{%s}
\\author{%s}
\\address{%s}

%% ... preamble finished, let's go ...
\\begin{document}
\\newcommand{\\chapter}[1]{\\large{#1}
%% Make a title page ...
\\coverpage

"""
