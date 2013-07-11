#!/usr/bin/python

import cgi
import cgitb
import shutil

# The subprocess module is new in 2.4
import os, urllib, subprocess as sub


cgitb.enable()

# Retrieve form fields
form   = cgi.FieldStorage()			# Get POST data
capituloLink = form.getfirst("capituloLink").strip()
temp = capituloLink.split('/')
repositorio=''

#Example curl http://localhost/cgi-bin/abnt.py?capituloLink=https://github.com/edusantana/introducao-a-computacao-livro/blob/master/livro/capitulos/historia-do-computador.asc
# https://github.com/edusantana/dissertacao-eduardo/blob/master/dissertacao/proposta.asc
# http://localhost/cgi-bin/abnt.py?capituloLink=https://github.com/edusantana/dissertacao-eduardo/blob/master/dissertacao/proposta.asc

if capituloLink.startswith("https://github.com/"):
#repositorio = https://github.com/edusantana/introducao-a-computacao-livro/blob/master/livro/capitulos/historia-do-computador.asc 
# ['https:', '', 'github.com', 'edusantana', 'introducao-a-computacao-livro', 'blob', 'master', 'livro', 'capitulos', 'historia-do-computador.asc']
  usuario = temp[3]
  nome_do_projeto = temp[4]
  nome_do_capitulo = temp[-1]
  filedir_in_project = '/'.join(temp[7:-1])
  filepath_in_project = '/'.join(temp[7:])
if capituloLink.startswith("https://raw.github.com/"):
# https://raw.github.com/edusantana/introducao-a-computacao-livro/master/livro/capitulos/historia-do-computador.asc
# ['https:', '', 'raw.github.com', 'edusantana', 'introducao-a-computacao-livro', 'master', 'livro', 'capitulos', 'historia-do-computador.asc']
  temp = capituloLink.split('/')
  usuario = temp[3]
  nome_do_projeto = temp[4]
  nome_do_capitulo = temp[-1]
  filedir_in_project = '/'.join(temp[6:-1])
  filepath_in_project = '/'.join(temp[6:])

#repositorio = "https://github.com/edusantana/introducao-a-computacao-livro"
repositorio = "https://github.com/" + usuario + "/"+ nome_do_projeto
WWWPATH = "/var/www/abnt/"
ASCIIDOC_PATH = "/home/santana/ambiente/abnt-asciidoc-8.6.8/"
A2X_BIN = ASCIIDOC_PATH+"a2x.py"
ASCIIDOC_BIN=ASCIIDOC_PATH+"asciidoc.py"
PDFTK_BIN = "/usr/bin/pdftk"

diretorio_do_usuario = WWWPATH + usuario + "/"
diretorio_do_projeto = diretorio_do_usuario + nome_do_projeto + "/"
capitulos_dir = diretorio_do_projeto + filedir_in_project + "/"
arquivo_capitulo_asc = diretorio_do_projeto + filepath_in_project


# Retrieve the command from the query string
# and unencode the escaped %xx chars
# str_command = urllib.unquote(os.environ['QUERY_STRING'])
output=""

if not os.path.exists(diretorio_do_usuario):
  mkdirp = sub.Popen(["mkdir", diretorio_do_usuario], cwd=WWWPATH, stdout=sub.PIPE, stderr=sub.STDOUT)
  mkdirp.wait()
  output = output + urllib.unquote(mkdirp.stdout.read())

if not os.path.exists(diretorio_do_projeto):
  gclonep = sub.Popen(["git", "clone", '-v', repositorio], cwd=diretorio_do_usuario, stdout=sub.PIPE, stderr=sub.STDOUT)
  gclonep.wait()
  output = output + urllib.unquote(gclonep.stdout.read())

gpullp = sub.Popen(["git", "pull"], cwd=diretorio_do_projeto, stdout=sub.PIPE, stderr=sub.STDOUT)
gpullp.wait()
output = output + urllib.unquote(gpullp.stdout.read())


datep = sub.Popen(["date", "+DATE: %m/%d/%y%nTIME: %H:%M:%S"], cwd=diretorio_do_projeto, stdout=sub.PIPE, stderr=sub.STDOUT)
datep.wait()
status = urllib.unquote(datep.stdout.read())

if os.path.exists(arquivo_capitulo_asc):
  pdf_file = arquivo_capitulo_asc[:-4] + '.pdf'

  output = output + "\nImprimindo TODO, FIXME e XXX...\n"
  asciidocp = sub.Popen(["grep", "-A","3","-B","0","-n","-r","-e","TODO","-e","FIXME",capitulos_dir], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  asciidocp.wait()
  output = output + urllib.unquote(asciidocp.stdout.read())


  output = output + "\nRemovendo versoes anteriores...\n"
  if os.path.exists(pdf_file):
    os.remove(pdf_file)

# --xsltproc-opts "--stringparam generate.section.toc.level 1 --stringparam toc.section.depth 3"

if os.path.exists(arquivo_capitulo_asc):
  # -v -f pdf --icons -a docinfo1      --dblatex-opts "-T computacao"     livro.asc
  output = output + "\nGerando o livro (asciidoc - pdf)...\n"
  asciidocp = sub.Popen([A2X_BIN, "-v", "-f","pdf", "-k", "--icons", "-a", "docinfo1", "-a", "ascii-ids", "-a", "lang=pt-BR", "-d", "book", "--dblatex-opts", "-P latex.babel.language=brazilian","-a livro-pdf",nome_do_capitulo], cwd=capitulos_dir, stdout=sub.PIPE, stderr=sub.STDOUT)
  asciidocp.wait()
  output = output + urllib.unquote(asciidocp.stdout.read())

  if os.path.exists(pdf_file):
    status = status + "\n ----- CAPITULO GERADO COM SUCESSO! -----\n"


link_abnt = "../abnt/"
link_usuario  = link_abnt + usuario + "/"
link_projeto = link_usuario+nome_do_projeto+"/"
link_pdf  = link_projeto+"livro/capitulos/" + nome_do_capitulo[:-4] + ".pdf"

print """\
Content-Type: text/html;charset=utf-8\n
<html><body>
<p>Livros serao gerados aqui: <a href="../abnt">abnt</a> &gt;&gt; <a href="../abnt/%s">%s</a> &gt;&gt; <a href="../abnt/%s/%s">%s</a> </p>
<p><a href="%s" target="_blank">PDF</a> | <a href="../abnt/edusantana/producao-computacao-ead-ufpb/livro/livro.chunked/index.html" target="_blank">Manual</a> | <a href="javascript:history.back()">Voltar</a>
<pre>
%s
%s
%s
</pre>
</body></html>
""" % (usuario, usuario, usuario, nome_do_projeto, nome_do_projeto, link_pdf, status, output, status)

