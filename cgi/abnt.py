#!/usr/bin/python

import cgi
import cgitb
import shutil

# The subprocess module is new in 2.4
import os, urllib, subprocess as sub


cgitb.enable()

# Retrieve form fields
form   = cgi.FieldStorage()			# Get POST data
capituloLink = form.getfirst("github_file_link").strip()
temp = capituloLink.split('/')
repositorio=''
usario=''
nome_do_projeto=''
filedir=''
filename=''
usuario=''

if capituloLink.startswith("https://github.com/"):
#repositorio = https://github.com/edusantana/introducao-a-computacao-livro/blob/master/livro/capitulos/historia-do-computador.asc 
# ['https:', '', 'github.com', 'edusantana', 'introducao-a-computacao-livro', 'blob', 'master', 'livro', 'capitulos', 'historia-do-computador.asc']
  repositorio = "https://github.com/" + temp[3] + "/"+ temp[4]
  usuario = temp[3]
  nome_do_projeto = temp[4]
  nome_do_capitulo = temp[9]
  filename=temp[-1]
  filedir='/'.join(temp[7:-1])

#repositorio = "https://github.com/edusantana/introducao-a-computacao-livro.git"
WWWPATH = "/var/www/abnt/"
ASCIIDOC_PATH = "/home/santana/ambiente/abnt-asciidoc-8.6.8/"
A2X_BIN = ASCIIDOC_PATH+"a2x.py"
ASCIIDOC_BIN=ASCIIDOC_PATH+"asciidoc.py"
PDFTK_BIN = "/usr/bin/pdftk"

diretorio_do_usuario = WWWPATH + usuario + "/"
diretorio_do_projeto = diretorio_do_usuario + nome_do_projeto + "/"
livro_dir = diretorio_do_projeto + filedir
server_file_dir = diretorio_do_projeto + "/" + filedir
server_file = diretorio_do_projeto + "/" + filedir + "/" + filename
server_file_pdf = diretorio_do_projeto + "/" + filedir + "/" + ('.'.join(filename.split('.')[0:-1])+'.pdf')




# Retrieve the command from the query string
# and unencode the escaped %xx chars
# str_command = urllib.unquote(os.environ['QUERY_STRING'])
output=""

if not os.path.exists(diretorio_do_usuario):
  mkdirp = sub.Popen(["mkdir", diretorio_do_usuario], stdout=sub.PIPE, stderr=sub.STDOUT)
  mkdirp.wait()
  output = output + urllib.unquote(mkdirp.stdout.read())
if not os.path.exists(diretorio_do_projeto):    
  gclonep = sub.Popen(["git", "clone", '-v', repositorio], cwd=diretorio_do_usuario, stdout=sub.PIPE, stderr=sub.STDOUT)
  gclonep.wait()
  output = output + urllib.unquote(gclonep.stdout.read())

gpullp = sub.Popen(["git", "pull",'-v'], cwd=diretorio_do_projeto, stdout=sub.PIPE, stderr=sub.STDOUT)
gpullp.wait()
output = output + urllib.unquote(gpullp.stdout.read())


datep = sub.Popen(["date", "+DATE: %m/%d/%y%nTIME: %H:%M:%S"], cwd=diretorio_do_projeto, stdout=sub.PIPE, stderr=sub.STDOUT)
datep.wait()
status = urllib.unquote(datep.stdout.read())

if os.path.exists(server_file):
  pdf_file = server_file[:-4] + '.pdf'

  output = output + "\nImprimindo TODO, FIXME e XXX...\n"
  grepp = sub.Popen(["grep", "-A","3","-B","0","-n","-r","-e","TODO","-e","FIXME","."], cwd=server_file_dir, stdout=sub.PIPE, stderr=sub.STDOUT)
  grepp.wait()
  output = output + urllib.unquote(grepp.stdout.read())


  output = output + "\nRemovendo versoes anteriores...\n"
  if os.path.exists(pdf_file):
    os.remove(pdf_file)

# --xsltproc-opts "--stringparam generate.section.toc.level 1 --stringparam toc.section.depth 3"

  # -v -f pdf --icons -a docinfo1      --dblatex-opts "-T computacao"     livro.asc
  output = output + "\nGerando o livro (asciidoc - pdf)...\n"
  asciidocp = sub.Popen([A2X_BIN, "-v", "-f","pdf", "-k", "--icons", "-a", "docinfo1", "-a", "ascii-ids", "-a", "lang=pt-BR", "-d", "book", "--dblatex-opts", "-P latex.babel.language=brazilian",filename], cwd=server_file_dir, stdout=sub.PIPE, stderr=sub.STDOUT)
  asciidocp.wait()
  output = output + urllib.unquote(asciidocp.stdout.read())

  if os.path.exists(pdf_file):
    status = status + "\n ----- CAPITULO GERADO COM SUCESSO! -----\n"


link_books = "../abnt/"
link_usuario  = link_books + usuario + "/"
link_projeto = link_usuario+nome_do_projeto+"/"
link_pdf  = server_file_pdf

print """\
Content-Type: text/html;charset=utf-8\n
<html><body>
<p>Livros serao gerados aqui: <a href="../books">books</a> &gt;&gt; <a href="../books/%s">%s</a> &gt;&gt; <a href="../books/%s/%s">%s</a> </p>
<p><a href="%s" target="_blank">PDF</a> | <a href="../books/edusantana/producao-computacao-ead-ufpb/livro/livro.chunked/index.html" target="_blank">Manual</a> | <a href="javascript:history.back()">Voltar</a>
<pre>
%s
%s
%s
</pre>
</body></html>
""" % (usuario, usuario, usuario, nome_do_projeto, nome_do_projeto, link_pdf, status, output, status)

