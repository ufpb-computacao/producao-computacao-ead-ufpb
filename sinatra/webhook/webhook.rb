require 'sinatra'

set :port, 3238

post '/' do
  push = JSON.parse(params[:payload])
  "I got some JSON: #{push.inspect}"
end
