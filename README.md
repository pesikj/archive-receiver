# Deployment to production environment

Resources:
* https://www.codementor.io/@aswinmurugesh/deploying-a-django-application-in-windows-with-apache-and-mod_wsgi-uhl2xq09e
* https://shellcreeper.com/how-to-create-valid-ssl-in-localhost-for-xampp/

## Git installation

1. Download and install [Git](https://git-scm.com/).
2. Clone the repository with the source code.
3. Create the `.env` file.


## Python installation
1. Download and install [Python](https://www.python.org/downloads/).
2. Create virtual environment in the directory with the cloned project.
3. Activate virtual environment: `PS C:\web\asvv> .\env\Scripts\activate`
4. Go to the `asvv` subfolder `(env) PS C:\web\asvv> cd .\asvv\` and install requirements by `pip install -r requirements.txt`.
5. Run database migration: `(env) PS C:\web\asvv\asvv> python .\manage.py migrate`
6. Create admin user: `(env) PS C:\web\asvv\asvv> python .\manage.py createsuperuser`
7. Start `celery` worker: `celery --app "asvv" worker --loglevel=info --pool=solo`
8. Load data dump into the database: `python manage.py loaddata templates.json`

## Web Server

1. Download and install [XAMPP](https://www.apachefriends.org/index.html).
1. Create a new environment variable `MOD_WSGI_APACHE_ROOTDIR`: `$env:MOD_WSGI_APACHE_ROOTDIR="C:\xampp\apache"` (the command for PowerShell) and `set MOD_WSGI_APACHE_ROOTDIR=C:/xampp/apache` (the command for the command line)
1. Install `mod_wsgi` module: `pip install mod_wsgi`
1. Run the following command: `mod_wsgi-express module-config`

After running the command, a simillar output should be generated:

```
LoadFile "C:/Users/jirip/AppData/Local/Programs/Python/Python38/python38.dll"
LoadModule wsgi_module "c:/web/asvv/env/lib/site-packages/mod_wsgi/server/mod_wsgi.cp38-win_amd64.pyd"
WSGIPythonHome "c:/web/asvv/env"
```

Copy the output to the `httpd.conf` file and add following two lines (the first line leads to the project root).
Replace the path with the actual path to the application.

```
WSGIPythonPath "C:/web/asvv/asvv"
WSGIApplicationGroup %{GLOBAL}
```

Add a following lines to the `C:\xampp\apache\conf\extra\httpd-vhosts.conf` file and create empty log files at the specified locations.


## Generate certificate

1. Create directory `C:\xampp\apache\crt`.
2. Copy files `certificate/cert.conf` and `certificate/make-cert.bat` into the directory.
3. Replace `localhost` by actual domain name in the `cert.conf` and run the file.
4. Install generated certificate to Windows. A detailed guide for the installation is provided in HTML file in the `certificate` directory.
5. Add the following code to the `httpd-vhosts.conf`. Update `ServerName` and `ServerAlias`

```
<VirtualHost *:443>
	ServerName localhost
	ServerAlias *.localhost
	SSLEngine on
	SSLCertificateFile "ssl/localhost/server.crt"
	SSLCertificateKeyFile "ssl/localhost/server.key"
    WSGIPassAuthorization On
    ErrorLog "logs/asvv.error.log"
    CustomLog "logs/asvv.access.log" combined
    WSGIScriptAlias /  "C:/web/huld_archive_receiver/huld_archive_receiver/huld_archive_receiver/wsgi.py"
    <Directory "C:/web/huld_archive_receiver/huld_archive_receiver/huld_archive_receiver/">
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    Alias /static "C:/web/huld_archive_receiver/huld_archive_receiver/huld_archive_receiver/static"
    <Directory "C:/web/huld_archive_receiver/huld_archive_receiver/huld_archive_receiver/static">
        Require all granted
    </Directory>  
</VirtualHost>
 ```