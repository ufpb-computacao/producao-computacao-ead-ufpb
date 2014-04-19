require 'open3'
require 'logger'
require 'fileutils'
require 'stringio'

logger = Logger.new(STDOUT)

RELEASES_DIR = `git config --get producao.releasesDir`.strip

def updateProjectRepository(parametros)

	if repositoryExists? (parametros) then
		updateRepository(parametros)
	else
		createRepository(parametros)
	end

end

def repo_dir(parametros)
	File.join(RELEASES_DIR, parametros[:user_name], parametros[:repo_name])
end

def repositoryExists?(parametros)
	File.directory? repo_dir(parametros)
end

def log(o, e, parametros)
	parametros[:o].write o
	parametros[:e].write e
end


def createRepository(parametros)
	logger = Logger.new(STDOUT)
	logger.info "Creating repository... "

	FileUtils.mkdir_p repo_dir(parametros)

	cmd = "git clone --bare #{parametros[:repo_url_html]} #{repo_dir(parametros)}"
	o, e, s = Open3.capture3(cmd)
	log(o, e, parametros)

end

def updateRepository (parametros)
	logger = Logger.new(STDOUT)
	logger.info "Updating repository... "

	chdir = repo_dir(parametros)
	cmd = "git fetch -p -t"

	o, e, s = Open3.capture3(cmd, :chdir => chdir)
	log(o, e, parametros)
end

parametros = {
	:o => StringIO.new,
	:e => StringIO.new,
	:repo_name => 'playground-asciidoc',
	:user_name => 'edusantana',
	:repo_url_html => 'http://github.com/edusantana/playground-asciidoc',
}

updateProjectRepository(parametros)

print parametros[:e].string
print parametros[:o].string

