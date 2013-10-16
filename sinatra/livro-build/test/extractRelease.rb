require 'open3'
require 'logger'
require 'fileutils'

logger = Logger.new(STDOUT)

RELEASES_DIR = '/home/santana/releases/local'
repo_dir='/home/santana/asciibook/playground-asciidoc'
userDir='/home/santana/releases/local/santana'

def extractRelease(repo_dir,branch,logger)

	# delete releaseDir/user/projecy/branch

	cmd = "git archive -v --prefix=#{releases}/#{branch}/ #{branch} | tar -x"

	stdin, stdout, stderr, wait_thr = Open3.popen3(cmd, :chdir => repo_dir)
	stdin.close
	logger.info stdout.read
	logger.error stderr.read

	releaseDir = "#{repo_dir}/releases/#{branch}"
	logger.info "Release dir: #{releaseDir}"
	releaseDir
end

userRepository='/home/santana/releases/local/santana/playground-asciidoc.git'
extractRelease userRepository,'master',logger

