from ftplib import FTP
import os

def listDir(ftp, dir):
    ftp = FTP(ftp)
    ftp.login()
    ftp.cwd(dir)
    l = ftp.nlst()
    ftp.quit()
    return l

def download(ftp, dir, targetDir, filename):
    ftp = FTP(ftp)
    ftp.login()
    ftp.cwd(dir)
    file = filename
    local_file = os.path.join(targetDir, file)
    try:
        ftp.retrbinary('RETR %s' %file, open(local_file, 'wb').write)
        ftp.quit()
        return filename + ' successfully downloaded'
    except Exception, e:
        return 'Error while downloading layer: ' + filename

def downloadList(ftp, dir, targetDir, files):
    out = []
    ftp = FTP(ftp)
    ftp.login()
    ftp.cwd(dir)
    for filename in files:
        print 'Downloading: ' + filename
        file = filename
        local_file = os.path.join(targetDir, file)
        if not os.path.exists(local_file):
            try:
                ftp.retrbinary('RETR %s' %file, open(local_file, 'wb').write)
                out.append(filename)
            except Exception, e:
                pass
    ftp.quit()
    return out