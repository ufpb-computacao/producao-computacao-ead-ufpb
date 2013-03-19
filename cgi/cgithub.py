#!/usr/bin/python
import subprocess
import os

print "Content-type: text/html\r\n\r\n"


# Begin HTML generation
print '''
<html>
<body>
<a href="books/lisieux/matematica-elementar-livro-tex/livro.pdf'>PDF Gerado</a>
</body>
</html>
'''

acao = "pull-pdf"
#acao = "delete"
repositorio = "https://github.com/edusantana/introducao-a-computacao-livro.git"


REPO_PERMITIDOS = ["introducao-a-computacao-livro.git"]
WWWPATH = "/var/www/books/"

usuario=repositorio.split("/")[3]
nome_do_projeto=repositorio.split("/")[4][:-4] # remove .git

diretorio_do_usuario = WWWPATH + usuario + "/"
diretorio_do_projeto = diretorio_do_usuario + nome_do_projeto + "/"

if acao == "pull-pdf" :
  if not os.path.exists(diretorio_do_usuario):
    p = subprocess.Popen(["mkdir", diretorio_do_usuario])
    p.wait()
  if not os.path.exists(diretorio_do_projeto):    
    p = subprocess.Popen(["git", "clone", repositorio], cwd=diretorio_do_usuario, stderr=None, stdout=None)
    p.wait()
  p = subprocess.Popen(["git", "pull"], cwd=diretorio_do_projeto)
  p.wait()
  if os.path.exists(diretorio_do_projeto+"livro"):
    # Gera pdf do asciidoc
    p = subprocess.Popen(["aap", "pdf"], cwd=diretorio_do_projeto + "livro")
    p.wait()
  else:
    p = subprocess.Popen(["pdflatex", "livro.tex"], cwd=diretorio_do_projeto)
    p.wait()
elif acao == "delete" :
  p = subprocess.Popen(["rm", "-v", "-rf", diretorio_do_usuario])
  p.wait()

