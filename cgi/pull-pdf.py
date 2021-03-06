#!/usr/bin/python

import cgi
import cgitb
import shutil

# The subprocess module is new in 2.4
import os, urllib, subprocess as sub


cgitb.enable()

# Retrieve form fields
form   = cgi.FieldStorage()			# Get POST data
repositorio  = form.getfirst("repositorio").strip()			# Pull fname field data
if repositorio.startswith("git@github.com:"):
  #repositorio = git@github.com:edusantana/producao-computacao-ead-ufpb.git
  repositorio = "https://github.com/" + repositorio[15:-4]

#repositorio = "https://github.com/edusantana/introducao-a-computacao-livro.git"
WWWPATH = "/var/www/books/"
ASCIIDOC_PATH = "/home/santana/ambiente/asciidoc-8.6.8/"
A2X_BIN = ASCIIDOC_PATH+"a2x.py"
ASCIIDOC_BIN=ASCIIDOC_PATH+"asciidoc.py"
#PDFTK_BIN = "/usr/bin/pdftk"
SEJDA_BIN = "/home/santana/ambiente/sejda/bin/sejda-console"


usuario=repositorio.split("/")[3]
if (repositorio.endswith("git")):
  nome_do_projeto=repositorio.split("/")[4][:-4] # remove .git
else:
  nome_do_projeto=repositorio.split("/")[4]

diretorio_do_usuario = WWWPATH + usuario + "/"
diretorio_do_projeto = diretorio_do_usuario + nome_do_projeto + "/"
diretorio_livro = diretorio_do_projeto + 'livro' + "/"
livro_tex = diretorio_do_projeto + 'livro.tex'
livro_asc = diretorio_livro + 'livro.asc'
slides_asc = diretorio_livro + 'slides.asc'
ignore_html_file = diretorio_do_projeto + 'ignore-html'
ignore_slide_file = diretorio_do_projeto + 'ignore-slide'

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


datep = sub.Popen(["date", "+DATE: %m/%d/%y%nTIME: %H:%M:%S"], cwd=diretorio_do_projeto, stdout=sub.PIPE, stderr=sub.STDOUT)
datep.wait()
status = urllib.unquote(datep.stdout.read())


livro_dir =diretorio_do_projeto+"livro/"
if os.path.exists(livro_asc):
  pdf_file = livro_dir+"livro.pdf"
  pdf_temp = livro_dir+"livro.tmp.pdf"
  chunked_dir = livro_dir+"livro.chunked"
  editora_pdf = livro_dir+"editora/editora.pdf"

  output = output + "\nImprimindo TODO, FIXME e XXX...\n"
  asciidocp = sub.Popen(["grep", "-A","3","-B","0","-n","-r","-e","TODO","-e","FIXME","."], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  asciidocp.wait()
  output = output + urllib.unquote(asciidocp.stdout.read())


  output = output + "\nRemovendo versoes anteriores...\n"
  if os.path.exists(chunked_dir):
    shutil.rmtree(chunked_dir)
  if os.path.exists(pdf_file):
    os.remove(pdf_file)

# --xsltproc-opts "--stringparam generate.section.toc.level 1 --stringparam toc.section.depth 3"

  # -v -f pdf --icons -a docinfo1      --dblatex-opts "-T computacao"     livro.asc
  output = output + "\nGerando o livro (asciidoc - pdf)...\n"
  asciidocp = sub.Popen([A2X_BIN, "-v", "-f","pdf", "--icons", "-a", "docinfo1", "-a", "lang=pt-BR", "-d", "book", "--dblatex-opts", "-T computacao -P latex.babel.language=brazilian","-a livro-pdf" ,"livro.asc"], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  asciidocp.wait()
  output = output + urllib.unquote(asciidocp.stdout.read())

  if os.path.exists(pdf_file):
    if os.path.exists(editora_pdf):
      os.rename(pdf_file, pdf_temp)
#      asciidocp = sub.Popen([PDFTK_BIN, editora_pdf, pdf_temp, "cat", "output", pdf_file], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
      asciidocp = sub.Popen([SEJDA_BIN, "merge", "-f", editora_pdf, pdf_temp, "-o", pdf_file], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)

      asciidocp.wait()
      os.remove(pdf_temp)
    status = status + "\n ----- LIVRO GERADO COM SUCESSO! -----\n"

if os.path.exists(livro_asc) and not os.path.exists(ignore_html_file):
  output = output +  "\nGerando o livro (asciidoc - html chunked)...\n"
  chunkedp = sub.Popen([A2X_BIN, "-v", "-f","chunked", "--icons",  "-a livro-html", "livro.asc"], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  chunkedp.wait()
  output = output + urllib.unquote(chunkedp.stdout.read())


if os.path.exists(slides_asc) and not os.path.exists(ignore_slide_file):
  slides_html = livro_dir + "slides.html"
  if os.path.exists(slides_html):
    output = output + "\nRemovendo slides anteriores...\n"
    os.remove(slides_html)


  output = output +   "\nGerando slides do livro (asciidoc - html slides)...\n"
  asciidocp = sub.Popen([ASCIIDOC_BIN, "-v", "-b","slidy", "slides.asc"], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  asciidocp.wait()
  output = output + urllib.unquote(asciidocp.stdout.read())
  # FIXME: incluir os arquivos *.png do diretorio
  # http://stackoverflow.com/questions/9997048/python-subprocess-wildcard-usage
  # zipp = sub.Popen(["zip", "-v","-r", "slides.zip","images", "slides.html"], cwd=diretorio_do_projeto + "livro", stdout=sub.PIPE, stderr=sub.STDOUT)
  # zipp.wait()
  # output = output + urllib.unquote(zipp.stdout.read())


if os.path.exists(livro_tex):
  livro_dir =diretorio_do_projeto
  pdf_file = livro_dir+"livro.pdf"
  if os.path.exists(pdf_file):
    output = output + "\nRemovendo versoes anteriores...\n"
    os.remove(pdf_file)


  output = output +  "\nGerando o livro (latex - pdf)...\n"

  pdflatexp = sub.Popen(["pdflatex", "livro.tex"], cwd=diretorio_do_projeto, stdout=sub.PIPE, stderr=sub.STDOUT)
  pdflatexp.wait()
  output = output + urllib.unquote(pdflatexp.stdout.read())

link_books = "../books/"
link_usuario  = link_books + usuario + "/"
link_projeto = link_usuario+nome_do_projeto+"/"
link_pdf  = link_projeto+"livro/livro.pdf"
link_html = link_projeto+"/livro/livro.chunked/index.html"

print """\
Content-Type: text/html;charset=utf-8\n
<html><body>
<p>Livros serao gerados aqui: <a href="../books">books</a> &gt;&gt; <a href="../books/%s">%s</a> &gt;&gt; <a href="../books/%s/%s">%s</a> </p>
<p><a href="%s" target="_blank">PDF</a> | <a href="%s" target="_blank">HTML</a> | <a href="../books/edusantana/producao-computacao-ead-ufpb/livro/livro.chunked/index.html" target="_blank">Manual</a> | <a href="javascript:history.back()">Voltar</a>
<pre>
%s
%s
%s
</pre>
</body></html>
""" % (usuario, usuario, usuario, nome_do_projeto, nome_do_projeto, link_pdf, link_html, status, output, status)

