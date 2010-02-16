#! /usr/bin/env python
from plasTeX.Renderers.Text import Renderer

class _LatexTagRenderer(Renderer):
    def default(self, node):
        return '(%s)%s(/%s)' % (node.nodeName, node, node.nodeName)

class Renderer(Renderer):
    list_prefix = ''
    def center(self, text):
        return '\n<center>%s</center>\n' % text
    def do_par(self, node):
        return '\n\n%s\n\n' % unicode(node)
    def do_math(self, node):
        return '<math>%s</math>' % unicode(node.source).replace('$','')
    def do_equation(self, node):
        return '\n\n<center><math>%s\,\!</math></center>\n\n' % unicode(node.source).replace('\[','').replace('\]','')
    do_displaymath = do_eqnarray = do_equation
    def do_section(self, node):
        return u'\n\n== %s ==\n\n%s' % (node.fullTitle, node)
    def do_subsection(self, node):
        return u'\n\n=== %s ===\n\n%s' % (node.fullTitle, node)
    def do_subsubsection(self, node):
        return u'\n\n==== %s ====\n\n%s' % (node.fullTitle, node)
    def do_it(self, node):
        return u"''%s''" % (node)
    def do_bf(self, node):
        return "'''%s'''" % unicode(node)
    def do_item(self, node):
        return "\n%s %s" % (self.list_prefix, unicode(node))
    def do_subitem(self, node):
        return "\n%s%s %s" % (self.list_prefix, self.list_prefix, unicode(node))
    def do_subsubitem(self, node):
        return "\n%s%s%s %s" % (self.list_prefix, self.list_prefix, self.list_prefix, unicode(node))
    def do_itemize(self, node):
        self.list_prefix = '*'
        return unicode(node)
    def do_enumerate(self, node):
        self.list_prefix = '#'
        return unicode(node)
    def do_verbatim(self, node):
        return '<source lang="text">%s</source>' % unicode(node)
    def do_table(self, node):
        return '\n<center>\n{|border="1" cellpadding="10" cellspacing="0"\n%s\n|}\n</center>\n' % unicode(node)
    def do_caption(self, node):
        return '''\n|+align="bottom" style="color:#e76700;" |''%s''\n''' % unicode(node)
    def do_ArrayRow(self, node):
        return '\n|-\n%s\n' % unicode(node)
    def do_ArrayCell(self, node):
        return '\n| %s\n' % unicode(node)
    #def do_includegraphics(self, node):
    #    return '[[File:%s|center|%s]]' % (unicode(node),
            
            
if __name__ == '__main__':
    from plasTeX.TeX import TeX
    import sys, os
    tex = TeX()
    filename = '/tmp/latex2wiki.txt'
    tex.ownerDocument.config['files']['filename'] = filename
    tex.input(sys.stdin.read())
    doc = tex.parse()
    renderer = Renderer()
    #renderer = _LatexTagRenderer()
    renderer.render(doc)
    lines = open(filename).readlines()
    
    data = '\n'.join([L.strip() for L in lines])
    data = '__NOEDITSECTION__ __TOC__' + data
    data = data.replace(r'\boxed','')
    data = data.replace(r'{aligned}',r'{align}')
    data = data.replace(r'\square',r' square ')
    sys.stdout.write(data.strip().replace('\n'*3, '\n'*2))
