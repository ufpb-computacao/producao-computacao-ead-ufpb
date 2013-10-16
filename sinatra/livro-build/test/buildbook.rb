require 'open3'
require 'logger'
require 'fileutils'

logger = Logger.new(STDOUT)

ASCIIDOC_BIN = "/home/santana/ambiente/asciidoc-8.6.8/a2x.py"
ASCIIDOC_OPTS = "-v -f pdf --icons -a docinfo1 -a lang=pt-BR -d book --dblatex-opts '-T computacao -P latex.babel.language=brazilian' -a livro-pdf"

def buildBook(releaseDir,subdir,file,logger)
  logger.info '### Gerando o livro ###'

	cmd = "#{ASCIIDOC_BIN} #{ASCIIDOC_OPTS} #{file}"

	stdin, stdout, stderr, wait_thr = 
		Open3.popen3(cmd, :chdir=>"#{releaseDir}/#{subdir}")
	stdin.close
	logger.info stdout.read
	logger.error stderr.read

	logger.info "Status: #{wait_thr.value.success?}"

end

releaseDir='/home/santana/releases/local/santana/playground-asciidoc.git/releases/master'
buildBook releaseDir,'livro','livro.asc',logger

