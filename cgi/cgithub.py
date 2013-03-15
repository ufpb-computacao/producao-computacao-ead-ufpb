#!/usr/bin/python
import subprocess
import os

#acao = "pull-pdf"
acao = "delete"


WWWPATH = "/home/santana/temp/"

repositorio = "https://github.com/edusantana/introducao-a-computacao-livro.git"
usuario="edusantana"
nome_do_projeto="introducao-a-computacao-livro"

diretorio_do_usuario= WWWPATH + usuario + "/"
diretorio_do_projeto = diretorio_do_usuario + nome_do_projeto + "/"


if acao == "pull-pdf" :
  if not os.path.exists(diretorio_do_usuario):
    p = subprocess.Popen(["mkdir", diretorio_do_usuario])
    p.wait()
  if not os.path.exists(diretorio_do_projeto):    
    p = subprocess.Popen(["git", "clone", "https://github.com/edusantana/introducao-a-computacao-livro.git"], cwd=diretorio_do_usuario)
    p.wait()
  p = subprocess.Popen(["git", "pull"], cwd=diretorio_do_projeto)
  p.wait()
  p = subprocess.Popen(["aap", "pdf"], cwd=diretorio_do_projeto + "livro")
  p.wait()
elif acao == "delete" :
  p = subprocess.Popen(["rm", "-v", "-rf", diretorio_do_usuario])
  p.wait()
  


