require 'open3'
require 'logger'
require 'fileutils'

logger = Logger.new(STDOUT)

RELEASES_DIR = '/home/santana/releases/local'
repo_dir='/home/santana/asciibook/playground-asciidoc'
userDir='/home/santana/releases/local/santana'


def updateReleaseRepository(repo_dir,project,user,logger)
	userRepository = "/home/santana/releases/local/santana/playground-asciidoc.git"

	cmd = "git fetch #{repo_dir}"
	stdin, stdout, stderr, wait_thr = Open3.popen3(cmd, :chdir => userRepository)
	stdin.close
	logger.info stdout.read
	logger.error stderr.read

	userRepository
end

updateReleaseRepository repo_dir,'playground-asciidoc','santana',logger

