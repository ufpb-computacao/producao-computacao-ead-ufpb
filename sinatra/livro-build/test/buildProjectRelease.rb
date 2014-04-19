require 'open3'
require 'logger'
require 'fileutils'
require 'stringio'
require 'time'

ASCIIDOC_BIN = "/home/santana/ambiente/asciidoc-8.6.8/a2x.py"
ASCIIDOC_OPTS = "-v -f pdf --icons -a docinfo1 -a lang=pt-BR -d book --dblatex-opts '-T computacao -P latex.babel.language=brazilian' -a livro-pdf"

RELEASES_DIR = '/home/santana/releases/local'

def buildProjectRelease(parametros)
	logger = Logger.new(STDOUT)

	file = asciidoc_file(parametros)
	chdir = release_dir(parametros)
  logger.info "### Gerando o livro: #{chdir} - #{file} ###"
	cmd = "#{ASCIIDOC_BIN} #{ASCIIDOC_OPTS} #{file}"

	o, e, s = Open3.capture3(cmd, :chdir => chdir)
	log(o, e, parametros)
end


def asciidoc_file(parametros)
	parametros[:asciidoc_file] || 'livro/livro.asc'
end

def tag(parametros)
	parametros[:tag] || 'HEAD'
end

def repo_dir(parametros)
	File.join(RELEASES_DIR, parametros[:user_name], parametros[:repo_name])
end

def release_dir(parametros)
	File.join(repo_dir(parametros),'releases',tag(parametros))
end


def log(o, e, parametros)
	parametros[:o].write o
	parametros[:e].write e
end

def saveLogFile(parametros)
	logName = asciidoc_file(parametros).sub('.asc','.log')
	file = File.new File.join(release_dir(parametros), logName), 'w'
	file.write logText(parametros)
	file.close
end

def logText(parametros)
	text = statusMessage(parametros) + "\n"
	text += "\n#{Time.now}"
	text += "\nxxxxxxxxx stdout xxxxxxxxx\n\n#{parametros[:o].string}"
	text += "\nxxxxxxxxx stderr xxxxxxxxx\n\n#{parametros[:e].string} \n"
end

def statusMessage(parametros)
	if sucess?(parametros) then
		return "SUCESSO: livro gerado com sucesso."
	else
		return "ERRO!"
	end
end

def sucess?(parametros)
	File.join(release_dir(parametros), asciidoc_file(parametros).sub('.asc','.pdf'))
end

parametros = {
	:o => StringIO.new,
	:e => StringIO.new,
	:repo_name => 'playground-asciidoc',
	:user_name => 'edusantana',
	:repo_url_html => 'http://github.com/edusantana/playground-asciidoc',
	:tag => 'v0.1.0',
}


buildProjectRelease(parametros)
saveLogFile(parametros)



print parametros[:e].string
print parametros[:o].string

