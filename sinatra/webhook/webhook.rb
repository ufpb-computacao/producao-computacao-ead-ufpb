require 'rubygems'
require 'sinatra'
require 'logger'
require 'open3'
require 'json'

# /usr/bin/curl http://producao.virtual.ufpb.br/cgi-bin/pull-pdf.py?repositorio=https://github.com/edusantana/playground-asciidoc

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

get '/hi' do

Open3.popen3('/usr/bin/curl http://producao.virtual.ufpb.br/cgi-bin/pull-pdf.py?repositorio=https://github.com/edusantana/playground-asciidoc') {|stdin, stdout, stderr, wait_thr|
  pid = wait_thr.pid # pid of the started process.
  
  exit_status = wait_thr.value # Process::Status object returned.
  
  File.open('log.txt', 'w') {|f| f.write(stdout.read) }
}

  logger.info 'Processamento finalizado.'
end

