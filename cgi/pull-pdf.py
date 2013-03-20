#!/usr/bin/python
import cgi
import cgitb


# The subprocess module is new in 2.4
import os, urllib, subprocess as sub


cgitb.enable()

# Retrieve form fields
form   = cgi.FieldStorage()			# Get POST data
repositorio  = form.getfirst("repositorio")			# Pull fname field data


#repositorio = "https://github.com/edusantana/introducao-a-computacao-livro.git"
WWWPATH = "/var/www/books/"
ASCIIDOC_PATH = "/home/santana/ambiente/asciidoc-8.6.8/"
A2X_BIN = ASCIIDOC_PATH+"a2x.py"
ASCIIDOC_BIN=ASCIIDOC_PATH+"asciidoc.py"



usuario=repositorio.split("/")[3]
nome_do_projeto=repositorio.split("/")[4][:-4] # remove .git

diretorio_do_usuario = WWWPATH + usuario + "/"
diretorio_do_projeto = diretorio_do_usuario + nome_do_projeto + "/"
diretorio_livro = diretorio_do_projeto + 'livro' + "/"
livro_tex = diretorio_do_projeto + 'livro.tex'
livro_asc = diretorio_livro + 'livro.asc'
slides_asc = diretorio_livro + 'slides.asc'

# Retrieve the command from the query string
# and unencode the escaped %xx chars
# str_command = urllib.unquote(os.environ['QUERY_STRING'])
output=""

if not os.path.exists(diretorio_do_usuario):
  mkdirp = sub.Popen(["mkdir", diretorio_do_usuario], stdout=sub.PIPE, stderr=sub.STDOUT)
  mkdirp.wait()
  output = output + urllib.unquote(mkdirp.stdout.read())
if not os.path.exists(diretorio_do_projeto):    
  gclonep = sub.Popen(["git", "clone", repositorio], cwd=diretorio_do_usuario, stdout=sub.PIPE, stderr=sub.STDOUT)
  gclonep.wait()
  output = output + urllib.unquote(gclonep.stdout.read())

gpullp = sub.Popen(["git", "pull"], cwd=diretorio_do_projeto, stdout=sub.PIPE, stderr=sub.STDOUT)
gpullp.wait()
output = output + urllib.unquote(gpullp.stdout.read())


if os.path.exists(livro_asc):
  # Gera pdf do asciidoc
  # -v -f pdf --icons -a docinfo1      --dblatex-opts "-T computacao"     livro.asc
  asciidocp = sub.Popen([A2X_BIN, "-v", "-f","pdf", "--icons",  "livro.asc"], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  asciidocp.wait()
  output = output + urllib.unquote(asciidocp.stdout.read())

  chunkedp = sub.Popen([A2X_BIN, "-v", "-f","chunked", "--icons",  "livro.asc"], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  chunkedp.wait()
  output = output + urllib.unquote(chunkedp.stdout.read())


if os.path.exists(slides_asc):
  # Gera slides do livro
  asciidocp = sub.Popen([ASCIIDOC_BIN, "-v", "-b","slidy", "slides.asc"], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  asciidocp.wait()
  output = output + urllib.unquote(asciidocp.stdout.read())
  # FIXME: incluir os arquivos *.png do diretorio
  # http://stackoverflow.com/questions/9997048/python-subprocess-wildcard-usage
  zipp = sub.Popen(["zip", "-v","-r", "slides.zip","images", "slides.html"], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  zipp.wait()
  output = output + urllib.unquote(zipp.stdout.read())


if os.path.exists(livro_tex):
  #gera livro a partir do latex
  pdflatexp = sub.Popen(["pdflatex", "livro.tex"], cwd=diretorio_do_projeto, stdout=sub.PIPE, stderr=sub.STDOUT)
  pdflatexp.wait()
  output = output + urllib.unquote(pdflatexp.stdout.read())


print """\
Content-Type: text/html\n
<html><body>
<p>Livros serao gerados aqui: <a href="../books">books</a> &gt;&gt; <a href="../books/%s">%s</a> &gt;&gt; <a href="../books/%s/%s">%s</a></p>
<pre>
%s
</pre>
</body></html>
""" % (usuario, usuario, usuario, nome_do_projeto, nome_do_projeto, output)

