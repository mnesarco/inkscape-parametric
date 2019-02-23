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
import inkex, simplestyle, simplepath, math, copy, sys
from StringIO import StringIO

class SvgObject(object):
    """
    This class is a wrapper of the svg node, attributes are mapped
    to lxml node attributes
    """
    def __init__(self, lxml):
        object.__setattr__(self, 'e', lxml)

    def getE(self):
        return object.__getattribute__(self, 'e')

    def __getattr__(self, name):
        return self.e.attrib[name]

    def __setattr__(self, name, value):
        self.e.attrib[name] = str(value)

    def isgroup(self):
        return self.getE().tag == 'g'

    def gettag(self):
        return inkex.etree.QName(self.getE())

class SvgDoc(object):
    """
    This class is a wrapper of the svg document.
    """
    def __init__(self, lxml):
        self.lxml = lxml

    def findById(self, id):
        """
        Returns a wrapped svg object by its id
        """
        node = self.lxml.find('//*[@id="%s"]' % str(id), namespaces=inkex.NSS)
        if node == None:
            return None
        else:
            return SvgObject(node)

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

    def evalScript(self, ctx):
        root = self.getroot()
        script = root.find('.//{%s}script' % self.namespace)
        if script != None:
            try:
                exec(script.text, ctx, ctx)
            except Exception as e:
                inkex.errormsg(str(e))

    def evalAttributes(self, ctx):
        root = self.getroot()
        px = "{%s}" % self.namespace
        pxn = len(px)
        errors = ""
        for node in self.document.xpath("//*[@*[namespace-uri()='%s']]" % self.namespace):
            if node != root:
                for att in node.items():
                    if att[0].startswith(px):
                        name  = att[0][pxn:]
                        try:
                            value = str(eval(att[1], ctx, ctx))
                            node.attrib[name] = value
                        except Exception as e:
                            errors = errors + str(e) + "\n" 
        if errors != "":
            inkex.errormsg(errors)

    def effect(self):
        ctx = {'_svg' : SvgDoc(self.document)}
        self.evalScript(ctx)
        self.evalAttributes(ctx)

if __name__ == '__main__':
    e = Parametric()
    e.affect()


# vim: expandtab shiftwidth=4 tabstop=4 softtabstop=4 fileencoding=utf-8 textwidth=99
