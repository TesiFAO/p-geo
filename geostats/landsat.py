#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os,sys,math,urllib2,urllib
import optparse
###########################################################################
class OptionParser (optparse.OptionParser):

    def check_required (self, opt):
        option = self.get_option(opt)

        # Assumes the option's 'default' is set to None!
        if getattr(self.values, option.dest) is None:
            self.error("%s option not supplied" % option)

#############################"Connection � Earth explorer sans proxy

def connect_earthexplorer_proxy():
    # user='murzilli\login'
    # passwd='vlasta83'
    # proxy_info = {
    #     'user' : 'murzilli',
    #     'pass' : 'vlasta83',
    #     'host' : 'proxy.esa.int',
    #     'port' : 8050
    # }
    # # contruction d'un "opener" qui utilise une connexion proxy avec autorisation
    # proxy_support = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info,
    #                                       "https" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info})
    #
    # print proxy_support
    #
    # opener = urllib2.build_opener(proxy_support, urllib2.HTTPCookieProcessor)
    #
    # print opener
    # # installation
    # urllib2.install_opener(opener)

    # parametres de connection
    params = urllib.urlencode(dict(username='murzilli', password='vlasta83'))


    # utilisation
    f = urllib2.urlopen('https://earthexplorer.usgs.gov/login', params)
    data = f.read()
    f.close()

    return

#############################"Connection � Earth explorer sans proxy

def connect_earthexplorer_noproxy():
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)
    params = urllib.urlencode(dict(username='Myself', password='secret'))
    f = opener.open("https://earthexplorer.usgs.gov/login/", params)
    data = f.read()
    f.close()
    if data.find('You must sign in as a registered user to download data or place orders for USGS EROS products')>0 :
        print "Authentification failed"
        sys.exit(-1)
    return

#############################"pour des gros fichiers

def downloadChunks(url,rep,nom_fic):
    """Telecharge de gros fichiers par morceaux
       inspire de http://josh.gourneau.com
    """

    try:
        req = urllib2.urlopen(url)
        #taille du fichier
        if (req.info().gettype()=='text/html'):
            print "erreur : le fichier est au format html"
            lignes=req.read()
            if lignes.find('Download Not Found')>0 :
                raise TypeError
            else:
                print lignes
                print sys.exit(-1)
        total_size = int(req.info().getheader('Content-Length').strip())
        if (total_size<50000):
            print "erreur : le fichier est trop petit pour etre une image landsat"
            print url
            sys.exit(-1)
        print nom_fic,total_size
        downloaded = 0
        CHUNK = 1024 * 1024 *8
        with open(rep+'/'+nom_fic, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                sys.stdout.write(str(math.floor((float(downloaded) / total_size) * 100 )) +'%')
                sys.stdout.flush()
                if not chunk: break
                fp.write(chunk)
            print 'fini'
    except urllib2.HTTPError, e:
        print "HTTP Error:",e.code , url
        return False
    except urllib2.URLError, e:
        print "URL Error:",e.reason , url
        return False

    return rep,nom_fic

######################################################################################
###############""main
#################################################################################

################Lecture des arguments
if len(sys.argv) == 1:
    prog = os.path.basename(sys.argv[0])
    print '      '+sys.argv[0]+' [options]'
    print "     Aide : ", prog, " --help"
    print "        ou : ", prog, " -h"
    print "exemple (scene): python recup_landsat_scene.py -o scene -a 2013 -d 360 -f 365 -s 199030"
    print "exemple (liste): python recup_landsat_scene.py -o date -l /home/hagolle/DOCS/TAKE5/liste_landsat8_site.txt"
    sys.exit(-1)
else:
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--option", dest="option", action="store", type="choice", \
                      help="scene ou liste", choices=['scene','liste'],default=None)
    parser.add_option("-l", "--liste", dest="fic_liste", action="store", type="string", \
                      help="nom du fichier liste",default=None)
    parser.add_option("-s", "--scene", dest="scene", action="store", type="string", \
                      help="coordonnees WRS2 de la scene (ex 198030)", default=None)
    parser.add_option("-a", "--annee", dest="annee", action="store", type="int", \
                      help="annee")
    parser.add_option("-d", "--doy_deb", dest="doy_deb", action="store", type="int", \
                      help="premier jour dans l'annee")
    parser.add_option("-f","--doy_fin", dest="doy_fin", action="store", type="int", \
                      help="dernier jour dans l'annee")

    (options, args) = parser.parse_args()
    parser.check_required("-o")
    if options.option=='scene':
        parser.check_required("-d")
        parser.check_required("-a")
        parser.check_required("-f")
        parser.check_required("-s")
    elif options.option=='date' :
        parser.check_required("-l")

rep='/to/be/changed/'

############Telechargement des produits par scene
if options.option=='scene':
    produit='LC8'
    station='LGN'
    path=options.scene[0:3]
    row=options.scene[3:6]

    rep_scene="%s/SCENES/%s_%s/GZ"%(rep,path,row)
    print rep_scene
    if not(os.path.exists(rep_scene)):
        os.makedirs(rep_scene)
    if produit.startswith('LC8'):repert='4923'
    if produit.startswith('LE7'):repert='3373'

    doy=options.doy_deb

    while (doy < options.doy_fin) and (doy < 366) :
        date_asc="%04d%03d"%(options.annee,doy)
        doy+=16
        for version in ['00','01']:
            nom_prod=produit+options.scene+date_asc+station+version
            url="http://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE"%(repert,nom_prod)
            print url
            if not(os.path.exists(rep_scene+'/'+nom_prod+'.tgz')):
                try:
                    connect_earthexplorer_proxy()
                    #connect_earthexplorer_no_proxy()
                    downloadChunks(url,"%s"%rep_scene,nom_prod+'.tgz')
                except TypeError:
                    print '   produit %s non trouve'%nom_prod
            else :
                print '   produit %s deja telecharge'%nom_prod
                break

############Telechargement par liste
if options.option=='liste':
    with file(options.fic_liste) as f:
        lignes=f.readlines()
    for ligne in lignes:
        (site,nom_prod)=ligne.split(' ')
        nom_prod=nom_prod.strip()
        if nom_prod.startswith('LC8'):repert='4923'
        if nom_prod.startswith('LE7'):repert='3373'

        if not os.path.exists(rep+'/'+site):
            os.mkdir('/home/vortex/Desktop/SITES/'+site)
        url="http://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE"%(repert,nom_prod)
        try:
            connect_earthexplorer_proxy()
            #connect_earthexplorer_proxy()
            downloadChunks(url,rep+'/'+site,nom_prod+'.tgz')
        except TypeError:
            print 'produit %s non trouve'%nom_prod

