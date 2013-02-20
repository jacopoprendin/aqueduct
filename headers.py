#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
