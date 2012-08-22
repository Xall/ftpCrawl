# ftpCrawl
ftpCrawl is a python script, which searches an FTP server for images, downloads and puts them into an HTML file

# Prereq
* Python 2.7 has to be installed
* ftputils have to be installed: (http://ftputil.sschwarzer.net/)

# Usage
`cd "Script Location"`
`python ftpLib host username password website [serverfolder]`
* `host: ` url of ftp server
* `username: ` ftp account username
* `password: ` ftp account password
* `website: ` website name (used only for subfolder creation)
* `serverfolder: ` optional: sets root folder for image search on server