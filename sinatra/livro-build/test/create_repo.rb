require 'open3'
require 'logger'
require 'fileutils'

logger = Logger.new(STDOUT)

RELEASES_DIR = '/home/santana/releases/local'
repo_dir='/home/santana/asciibook/playground-asciidoc'
userDir='/home/santana/releases/local/santana'


def getOrCreateUserRepository(repo_dir,project,user,logger)
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

getOrCreateUserRepository repo_dir,'playground-asciidoc','santana',logger

