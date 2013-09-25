require 'rubygems'
require 'sinatra'
require 'logger'

post '/' do
  push = JSON.parse(params[:payload])
	# Save a string to a file.
	myStr = "This is a test"
	aFile = File.new("myString.txt", "w")
	aFile.write("I got some JSON: #{push.inspect}")
	aFile.close
  logger.info "I got some JSON: #{push.inspect}"
  "I got some JSON: #{push.inspect}"
end
