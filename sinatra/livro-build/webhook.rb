require 'rubygems'
require 'sinatra'
require 'logger'
require 'open3'
require 'git'
require 'fileutils'


RELEASES_DIR = `git config --get producao.releasesDir`.strip
ASCIIDOC_BIN = "/home/santana/ambiente/asciidoc-8.6.8/a2x.py"
ASCIIDOC_OPTS = "-v -f pdf --icons -a docinfo1 -a lang=pt-BR -d book --dblatex-opts '-T computacao -P latex.babel.language=brazilian' -a livro-pdf livro.asc"

post '/' do
  push = JSON.parse(params[:payload])
  repo_url = push['repository']['url']
	File.open('url.txt', 'w') {|f| f.write(push['repository']['url']) }

	Open3.popen3("/usr/bin/curl http://localhost/cgi-bin/pull-pdf.py?repositorio=#{repo_url}") {|stdin, stdout, stderr, wait_thr|
		pid = wait_thr.pid # pid of the started process.
		
		exit_status = wait_thr.value # Process::Status object returned.
		
		File.open('log.txt', 'w') {|f| f.write(stdout.read) }
	}
end

# git config --global producao.releasesDir ~/releases/local
# curl  "localhost:4567/localbuild?repo_dir=`git rev-parse --show-toplevel`&project=playground"
# curl -d repo_dir=`git rev-parse --show-toplevel` -d branch=master -d user=$USER -d treeish="HEAD" localhost:4567/localbuild
post '/localbuild' do
  logger.info "Parametros recebidos: #{params.to_s}"
  repo_dir = params[:repo_dir]
  branch = params[:branch] or "master"
  project = repo_dir.split('/')[-1]
  user = params[:user] or 'user'

	logger.info "Project: #{project}"

	userRepository = updateReleaseRepository repo_dir,project,user
	releaseDir = extractRelease userRepository,branch

	buildBook releaseDir,'livro','livro.asc'


  #archiveBranch repo_dir,branch,project,user
  #geraReleaseLocal branch
	"Recebido com sucesso.\n"
end

def extractRelease(userRepository,branch)
	cmd = "git archive -v --prefix=releases/#{branch}/ #{branch} | tar -x"

	stdin, stdout, stderr, wait_thr = Open3.popen3(cmd, :chdir => userRepository)
	stdin.close
	logger.info stdout.read
	logger.error stderr.read

	releaseDir = "#{userRepository}/releases/#{branch}"
	logger.info "Release dir: #{releaseDir}"
	releaseDir
end


def updateReleaseRepository(repo_dir,project,user)
	userRepository = getOrCreateUserRepository repo_dir,project,user

	cmd = "git fetch #{repo_dir}"
	stdin, stdout, stderr, wait_thr = Open3.popen3(cmd, :chdir => userRepository)
	stdin.close
	logger.info stdout.read
	logger.error stderr.read

	userRepository
end

def getOrCreateUserRepository(repo_dir,project,user)
	userDir = "#{RELEASES_DIR}/#{user}"
	userRepository = "#{userDir}/#{project}.git"

	if !File.directory?(userRepository)
		logger.info "Creating a new repository: #{userRepository}"
		FileUtils.mkdir_p userDir
		cmd = "git clone --bare #{repo_dir}"
		logger.info "#{userDir}$> #{cmd}"
		stdin, stdout, stderr, wait_thr = Open3.popen3(cmd, :chdir => userDir)
		stdin.close
		logger.info stdout.read
		logger.error stderr.read
	else
		logger.info "Não houve necessidade de criar um novo repositório"
	end

	userRepository
end

def archiveBranch (repo_dir,branch,project)
	targetDir = "#{RELEASES_DIR}/#{project}/#{branch}"
  cmd = "git archive --format=tar --prefix=$BRANCH/ $BRANCH | (cd #{targetDir} && tar xf -)"
	stdin, stdout, stderr, wait_thr = Open3.popen3(cmd, :chdir => repo_dir)
	stdin.close
end

get '/' do
  logger.info 'recebido algo'
  repo_dir = '/var/www/books/edusantana/introducao-a-programacao-livro'
  repo_link = 'https://github.com/edusantana/introducao-a-programacao-livro'
	atualizaRepositorio repo_dir, repo_link
	relatorioDeRevisao
	geraLivro repo_dir
end

def atualizaRepositorio(repo_dir, repo_link)
  logger.info 'Repositório sendo atualizado'
	stdout_str, stderr_str, status = 
		Open3.capture3("/usr/bin/git pull #{repo_link}", :chdir=>repo_dir)
	logger.info stdout_str
	logger.error stderr_str
end


def relatorioDeRevisao
  logger.info '### Relatório de Revisão ###'
end


def buildBook (releaseDir,subdir,file)
  logger.info '### Gerando o livro.pdf ###'
end



def geraLivro(repo_dir)
  logger.info '### Gerando o livro.pdf ###'
  stdout_str, stderr_str, status = 
		Open3.capture3("#{ASCIIDOC_BIN} #{ASCIIDOC_OPTS}", :chdir=>"#{repo_dir}/livro")

  File.open("#{repo_dir}/log.txt", "w") { |file| 
    if status.success?
			file.write "Livro gerado com sucesso\n" 
		else
			file.write "ERRO na geração do Livro\n" 
		end
		file.write stdout_str
		file.write stderr_str
	}

	logger.info stdout_str
	logger.error stderr_str
end



