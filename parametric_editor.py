#! /usr/bin/python
'''
   Copyright (C) 2019 Frank Martinez, mnesarco <at> gmail.com
   
    This file is part of inkscape-parametric.

    inkscape-parametric is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    inkscape-parametric is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with inkscape-parametric.  If not, see <https://www.gnu.org/licenses/>.    
'''
import inkex, simplestyle, simplepath, math, copy, sys, subprocess, tempfile, os
from StringIO import StringIO
import parametric

class ParametricEditor(parametric.Parametric):
    """
    This extension Opens a Scintilla Editor and load parametric script content.
    """

    def __init__(self):
        parametric.Parametric.__init__(self)

    def effect(self):
        root = self.getroot()
        script = root.find('.//{%s}script' % self.namespace)
        if script != None:
            if script.text == None:
                code = '""" Write Python code Here """'
            else:
                code = script.text
            codeFile = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
            codeFile.write(code)
            codeFileName = codeFile.name
            codeFile.close()
            subprocess.call(['SciTE', codeFileName])
            codeStream = open(codeFileName, 'r')
            code = codeStream.read()
            codeStream.close()
            os.unlink(codeFileName)
            script.text = code
            try:
                parametric.Parametric.effect(self)
            except Exception as e:
                inkex.errormsg(str(e))

if __name__ == '__main__':
    e = ParametricEditor()
    e.affect()


# vim: expandtab shiftwidth=4 tabstop=4 softtabstop=4 fileencoding=utf-8 textwidth=99
