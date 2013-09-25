require 'rubygems'
require 'sinatra'
#require 'server.rb'
require File.expand_path '../webhook.rb', __FILE__



run Sinatra::Application
