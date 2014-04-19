require 'open3'
require 'logger'
require 'fileutils'
require 'stringio'

logger = Logger.new(STDOUT)
RELEASES_DIR = '/home/santana/releases/local'

def extractProjectRelease(parametros)

	deletePreviousReleseDir(parametros)
	extractRelease(parametros)

end

def extractRelease(parametros)
	tag = tag(parametros)

	logger = Logger.new(STDOUT)
	logger.info "Updating extracting release (#{tag})... "

	chdir = repo_dir(parametros)
	cmd = "git archive -v --prefix=releases/#{tag}/ #{tag} | tar -x"

	o, e, s = Open3.capture3(cmd, :chdir => chdir)
	log(o, e, parametros)
end

def repo_dir(parametros)
	File.join(RELEASES_DIR, parametros[:user_name], parametros[:repo_name])
end

def tag(parametros)
	parametros[:tag] or 'HEAD'
end

def release_dir(parametros)
	File.join(repo_dir(parametros),'releases',tag(parametros))
end

def releaseDirExists?(parametros)
	File.directory? release_dir(parametros)
end

def deletePreviousReleseDir(parametros)
	if releaseDirExists?(parametros) then
		logger = Logger.new(STDOUT)
		logger.info "Deleting previous release: #{release_dir(parametros)}... "

		FileUtils.rm_rf(release_dir(parametros))
	end
end


def log(o, e, parametros)
	parametros[:o].write o
	parametros[:e].write e
end


parametros = {
	:o => StringIO.new,
	:e => StringIO.new,
	:repo_name => 'playground-asciidoc',
	:user_name => 'edusantana',
	:repo_url_html => 'http://github.com/edusantana/playground-asciidoc',
	:tag => 'v0.1.0',
}

extractProjectRelease(parametros)

print parametros[:e].string
print parametros[:o].string

