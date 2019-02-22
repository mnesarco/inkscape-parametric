#! /usr/bin/python
'''
Copyright (C) 2019 Frank Martinez, mnesarco <at> gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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
