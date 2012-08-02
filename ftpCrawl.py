import ftputil
import os

#Setup
host = '88.80.210.101'
user = 'web3'
password = 'blub'
path = '/html/typolight-original/tl_files/projects/lill-conference-2012'
website = 'contao'

#Create website subfolder
if not os.path.exists('./' + website):
    os.makedirs('./' + website)

#Create HTML output
fobj_out = open('out.html', 'w')
fobj_out.write("<html>")
fobj_out.write("<head>")
fobj_out.write("<link rel='stylesheet' type='text/css' href='../styles.css'>")
fobj_out.write("</head>")
fobj_out.write("<body>")

#Connect to FTP
ftp = ftputil.FTPHost(host, user, password)
# Recursively walk through all folders, write result to 3D array
allDirectories = ftp.walk(path, topdown=True, onerror=None)
#Iterate over array and filter all images bigger than 1KB
for root, dirs, files in allDirectories:
    for name in files:
        filepath = root + '/' + name
        if ftp.stat(filepath).st_size < 1000:
            continue
        if not ".png" in filepath:
            if not ".gif" in filepath:
                if not ".jpg" in filepath:
                    continue
        #Download
        ftp.download_if_newer(filepath, './' + website + '/' + name, 'b')
        #Write to html
        fobj_out.write("<img src='" + website + "/" + name + "'>")
        fobj_out.write("<p>" + filepath + "</p>")
        #DEBUG
        #print ftp.stat(filepath).st_size
ftp.close()

#Close HTML
fobj_out.write("</body>")
fobj_out.write("</html>")
