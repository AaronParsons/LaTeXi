#! /usr/bin/env python3
import re
from plasTeX.Renderers.Text import Renderer

LABEL_REGX = re.compile(r'\\label{[^}]+}')

class _LatexTagRenderer(Renderer):
    def default(self, node):
        return '(%s)%s(/%s)' % (node.nodeName, node, node.nodeName)

class Renderer(Renderer):
    caption_type = 'figure'
    list_prefix = ''
    def default(self, node):
        if node.nodeName == '\\': return "<br>"
        elif node.nodeName == '_': return "_"
        elif node.nodeName == '#': return "<nowiki>#</nowiki>"
        else: return str(node)
    def do_center(self, node):
        return '\n<center>%s</center>\n' % node
    def do_title(self, node):
        return '\n<h1>%s</h1>\n' % node
    do_centering = do_center
    def do_par(self, node):
        return '\n\n%s\n\n' % str(node)
    def do_math(self, node):
        return '<math>%s</math>' % str(node.source).replace('$','')
    def do_equation(self, node):
        txt = str(node.source).strip()
        txt = txt.replace(r'\begin{equation}','')
        txt = txt.replace(r'\end{equation}','')
        txt = txt.replace('\[','').replace('\]','')
        txt = LABEL_REGX.sub('', txt)
        #from IPython.Shell import IPShellEmbed; IPShellEmbed()()
        return '\n\n<center><math>%s\,\!</math></center>\n\n' % txt
    do_displaymath = do_equation
    def do_eqnarray(self, node):
        txt = str(node.source).strip()
        txt = txt.replace(r'\begin{eqnarray}',r'\begin{align}')
        txt = txt.replace(r'\end{eqnarray}',r'\end{align}')
        txt = txt.replace('\[','').replace('\]','')
        txt = LABEL_REGX.sub('', txt)
        return '\n\n<center><math>%s\,\!</math></center>\n\n' % txt
    def do_align(self, node):
        txt = str(node.source).strip()
        txt = LABEL_REGX.sub('', txt)
        #from IPython.Shell import IPShellEmbed; IPShellEmbed()()
        return '\n\n<center><math>%s\,\!</math></center>\n\n' % txt
    def do_section(self, node):
        return '\n\n== %s ==\n\n%s' % (node.fullTitle, node)
    def do_subsection(self, node):
        return '\n\n=== %s ===\n\n%s' % (node.fullTitle, node)
    def do_subsubsection(self, node):
        return '\n\n==== %s ====\n\n%s' % (node.fullTitle, node)
    def do_it(self, node):
        return "''%s''" % (node)
    do_emph = do_it
    def do_bf(self, node):
        return "'''%s'''" % str(node)
    def do_item(self, node):
        if len(node.argSource) > 0: return "\n%s '''%s'''%s" % (self.list_prefix, node.argSource[1:-1], str(node).strip())
        else: return "\n%s %s" % (self.list_prefix, str(node).strip())
    def do_subitem(self, node):
        if len(node.argSource) > 0: return "\n%s%s '''%s'''%s" % (self.list_prefix, self.list_prefix, node.argSource[1:-1], str(node).strip())
        else: return "\n%s%s %s" % (self.list_prefix, self.list_prefix, str(node).strip())
    def do_subsubitem(self, node):
        if len(node.argSource) > 0: return "\n%s%s%s '''%s'''%s" % (self.list_prefix, self.list_prefix, self.list_prefix, node.argSource[1:-1], str(node).strip())
        else: return "\n%s%s%s %s" % (self.list_prefix, self.list_prefix, self.list_prefix, str(node).strip())
    def do_description(self, node):
        self.list_prefix = ':'
        return str(node)
    def do_itemize(self, node):
        self.list_prefix = '*'
        return str(node)
    def do_enumerate(self, node):
        self.list_prefix = '#'
        return str(node)
    def do_verbatim(self, node):
        return '<source lang="text">%s</source>' % str(node)
    def do_table(self, node):
        self.caption_type = 'table'
        rv = '\n{|border="1" cellpadding="10" cellspacing="0"\n%s\n|}\n' % str(node)
        self.caption_type = ''
        return rv
    def do_tabular(self, node):
        #return '\n<center>\n{|border="1" cellpadding="10" cellspacing="0"\n%s\n|}\n</center>\n' % unicode(node)
        if self.caption_type == 'table': return str(node)
        else: return '\n{|border="1" cellpadding="10" cellspacing="0"\n%s\n|}\n' % str(node)
    def do_caption(self, node):
        cap = "''%s''" % str(node)
        if self.caption_type == 'table':
            return '''\n|+align="bottom" style="color:#e76700;" |%s\n''' % cap
        elif self.caption_type == 'figure':
            return '<br>%s' % cap
        else:
            return cap
    def do_ArrayRow(self, node):
        return '\n|-\n%s\n' % str(node)
    def do_ArrayCell(self, node):
        return '\n| %s\n' % str(node)
    def do_figure(self, node):
        self.caption_type = 'figure'
        return str(node)
    def do_includegraphics(self, node):
        return '[[File:%s|250px]]' % (node.attributes['file'])
            
            
if __name__ == '__main__':
    from plasTeX.TeX import TeX
    import sys, os
    tex = TeX()
    filename = '/tmp/latex2wiki.txt'
    tex.ownerDocument.config['files']['filename'] = filename
    if True: tex.input(sys.stdin.read())
    else: tex.input(open(sys.argv[-1]).read())
    doc = tex.parse()
    if True: renderer = Renderer()
    else: renderer = _LatexTagRenderer()
    renderer.render(doc)
    lines = open(filename).readlines()
    
    data = '\n'.join([L.strip() for L in lines])
    data = '__NOEDITSECTION__ __TOC__' + data
    data = data.replace(r'\boxed','')
    data = data.replace(r'{aligned}',r'{align}')
    data = data.replace(r'\square',r' square ')
    sys.stdout.write(data.strip().replace('\n'*3, '\n'*2))
