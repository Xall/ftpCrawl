import ftputil
import os
import sys
import re

#Arg test
if len(sys.argv) < 5:
    print 'Error: Invalid arguments'
    print 'Usage: host username password sitename [serverfolder]'
    sys.exit()
else:
    print 'Downloading...'

#Setup
host = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
website = sys.argv[4]
if len(sys.argv) == 6:
    path = sys.argv[5]
else:
    path = '/'

#Create website subfolder
if not os.path.exists('./' + website):
    os.makedirs('./' + website)

#Create HTML output
fobj_out = open(website + '/_out.html', 'w')
fobj_out.write("<html>")
fobj_out.write("<head>")
fobj_out.write("<link rel='stylesheet' type='text/css' href='../styles.css'>")
fobj_out.write("</head>")
fobj_out.write("<body>")

#Connect to FTP
try:
    ftp = ftputil.FTPHost(host, user, password)
except Exception, e:
    print e
    print "Exiting..."
    sys.exit()
print "Authentication Successful"

#Recursively walk through all folders, write result to array
allDirectories = ftp.walk(path, topdown=True, onerror=None)
#Iterate over array and filter all images bigger than 1KB
j = 0
for root, dirs, files in allDirectories:
    i = 0
    for name in files:
        filepath = root + '/' + name
        #Check for images
        if not ".png" in filepath:
            if not ".gif" in filepath:
                if not ".jpg" in filepath:
                    continue
        #Check for resized Wordpress images. Pattern: ###x### (#=number)
        m = re.search("[0-9][0-9][0-9]x[0-9][0-9][0-9]", filepath)
        if m:
            continue
        #Check excluded folder
        if "wp-admin" in filepath:
            continue
        if "plugin" in filepath:
            continue
        #Download
        try:
            ftp.download_if_newer(filepath, './' + website + '/' + name, 'b')
        except Exception, e:
            print e
        #Write to html
        fobj_out.write("<img src='" + name + "'>")
        fobj_out.write("<p>" + filepath + "</p>")
        #Some output (Inc Files)
        i = i + 1
    print "Downloaded " + str(i) + " images from" + root
    j = j + i
print "Downloaded " + str(j) + " images total"
#Close FTP
ftp.close()

#Close HTML
fobj_out.write("</body>")
fobj_out.write("</html>")
