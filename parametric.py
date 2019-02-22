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
import inkex, simplestyle, simplepath, math, copy, sys
from StringIO import StringIO

class Parametric(inkex.Effect):
    """
    This extension adds parametric functionality to the svg document.
     1 - Any python code inside <parametric:script></parametric:script> will be
         executed.
     2 - All attributes in the parametric namespace will be evaluated (python expression) and
         the result will be set to the equivalent attribute without namespace.
    """

    namespace = "//fdmtech.com/inkscape/parametric"
    prefix = "parametric"

    def __init__(self):
        inkex.Effect.__init__(self)

    def getroot(self):
        return self.document.getroot()

    def isparametric(self):
        return self.getroot().nsmap.has_key(self.prefix)

    def parse(self, filename=None):
        """Parse document in specified file or on stdin"""

        # First try to open the file from the function argument
        if filename is not None:
            try:
                stream = open(filename, 'r')
            except IOError:
                errormsg(_("Unable to open specified file: %s") % filename)
                sys.exit()

        # If it wasn't specified, try to open the file specified as
        # an object member
        elif self.svg_file is not None:
            try:
                stream = open(self.svg_file, 'r')
            except IOError:
                errormsg(_("Unable to open object member file: %s") % self.svg_file)
                sys.exit()

        # Finally, if the filename was not specified anywhere, use
        # standard input stream
        else:
            stream = sys.stdin

        data = stream.read()
        stream.close()
        p = inkex.etree.XMLParser(huge_tree=True)
        reparsed = False
        try:
            # Parse already parametric svg document
            self.document = inkex.etree.parse(StringIO(data), parser=p)
        except:
            # Parse not parametric svg document with 'invalid' parametric attributes
            reparsed = True
            data = self.add_parametric(data)
            self.document = inkex.etree.parse(StringIO(data), parser=p)

        # Parse non parametric svg document
        if not self.isparametric() and not reparsed:
            data = self.add_parametric(data)
            self.document = inkex.etree.parse(StringIO(data), parser=p)

        # Add parametric script if not exists
        root = self.getroot()
        script = root.find('.//{%s}script' % self.namespace)
        if script == None:
            node = inkex.etree.SubElement(root, '{%s}script' % self.namespace, nsmap={self.prefix : self.namespace})
            node.text = '""" You can write python code here """'        

        self.original_document = copy.deepcopy(self.document)

    def add_parametric(self, data):
        """
        Adds parametric namespace and script to the document
        """
        r = data.replace('<svg', "<svg\n  xmlns:{0}=\"{1}\" {0}:enabled=\"true\" ".format(self.prefix, self.namespace))
        r = r.replace('</svg>', (
            '<parametric:script>'
            '""" You can write python code here """'
            '</parametric:script>'
            '</svg>'))
        return r

    def output(self):
        self.document.write(sys.stdout)

    def effect(self):

        # Execute script if any
        root = self.getroot()
        script = root.find('.//{%s}script' % self.namespace)
        if script != None:
            exec(script.text)

        # Eval parametric attributes
        px = "{%s}" % self.namespace
        pxn = len(px)
        for node in self.document.xpath("//*[@*[namespace-uri()='%s']]" % self.namespace):
            if node != root:
                for att in node.items():
                    if att[0].startswith(px):
                        name  = att[0][pxn:]
                        value = str(eval(att[1]))
                        node.attrib[name] = value

if __name__ == '__main__':
    e = Parametric()
    e.affect()


# vim: expandtab shiftwidth=4 tabstop=4 softtabstop=4 fileencoding=utf-8 textwidth=99
