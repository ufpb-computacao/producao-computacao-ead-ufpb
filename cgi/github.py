#!/usr/bin/python
import cgi
import cgitb
import subprocess
import os

cgitb.enable()

# Retrieve form fields
form   = cgi.FieldStorage()			# Get POST data
repositorio  = form.getfirst("repositorio")			# Pull fname field data

p = subprocess.Popen(["git", "clone", "git@github.com:edusantana/edfisica-livro.git"], cwd="/var/www/books")
p.wait()


# Begin HTML generation
print "Content-Type: text/html; charset=UTF-8"	# Print headers
print ""					# Signal end of headers

# HTML is pushed to the page with print
# To save time you can use ''' to open and close a print
# statement for block printing
print '''
<html>
<body>
'''
print "Repositorio:",repositorio
print '''
</body>
</html>
'''
