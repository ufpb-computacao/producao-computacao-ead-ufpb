require 'sinatra'
require 'json'

set :public_folder, File.dirname(__FILE__) + '/public'

post '/payload' do
  push = JSON.parse(params[:payload])
  puts "I got some JSON: #{push.inspect}"
end
