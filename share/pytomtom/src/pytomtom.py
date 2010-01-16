#/usr/bin/python
# -*- coding:utf-8 -*-
#----------------------------------------------- ENTETE DE DEFINITION DE L'APPLICATION ---------------------------------------
##
## pyTOMTOM version 0.4b (2010) - Gerez votre TomTom sous Linux !
##
## http://tomonweb.2kool4u.net/pytomtom/
##
## auteur : Thomas LEROY
##
## remerciements à Philippe (toto740), Sunil, Chamalow, Exzemat, GallyHC, Pascal

#----------------------------------------------- DEFINITION DES REGLES DE DEVELOPPEMENT --------------------------------------
## Regles de developpement
##   - Utilisation de la langue anglaise pour le nom des variables et des fonctions (pas de melange)
##   - Les noms des fonctions commencent par une majuscule, avec une majuscule a chaque nouveau mot
##   ( - les noms de fonctions commencent par une majuscule avec _ pour separer les mots )
##   - Les variables commencent par une minuscule, avec une majuscule a chaque nouveau mot
##   ( - pas de distinction entre le nom d'une variable et le nom d'une fonction )
##   - Les fonctions ont toujours une entete definissant l'utilite de la fonction, ...
##   - Le nom d'une classe s'ecrit comme le nom d'une fonction
##   - tous les textes s'utilisent avec la fonction _() afin de rendre l'application internationnale
##   - tout code ecrit deux fois est mis dans une fonction, jamais copie
##   - tous les commentaires ne sont pas ecrits avec des accents (internationalisation de l'application)
##   - pas d'espace avant (, mais un espace apres
##   - un espace avant ), mais pas d'espace apres
##   - pas d'espace avant : qui demarre un ensemble
##   - un espace avant et un apres + (concatenation de chaine)
##   - un espace apres une virgule
##   - les fonctions internes commencent par _

#----------------------------------------------- IMPORT DES LIBRAIRIES UTILES ------------------------------------------------
## TODO : Utile ? import pygtk
import gtk

## Utilise pour recuperer les fichiers cab pour le GPSFix
import urllib2
## Utilise pour lancer des sous-programmes (tar, cabextract, df, ...)
import subprocess
## Utilise pour copier les fichiers et supprimer des repertoires
import shutil
## Utilise pour recuperer les variables d'environnement et faire des manipulations sur les dossiers et fichiers
import os
## Utilise pour recuperer des informations sur les fichiers et les dossiers
import os.path
## Utilise pour voir la date du jour
from datetime import date
## Utilise pour recuperer les options fournies en argument
import getopt
## Utilise pour utiliser les systemes
import sys
## Utilise pour traduire le texte
import gettext
## Utilise pour creer des repertoires et des fichiers temporaires
import tempfile
## Utilise pour creer un timeout
import gobject
## Utilise pour creer un nouveau fichier de sauvegarde avec un chiffre aleatoire
import random
## Utilise pour connaitre la taille du terminal lancant le logiciel
import termios, fcntl, struct

#----------------------------------------------- DEFINITION GLOBALES ---------------------------------------------------------
## Definition du nom et de la version de l'application
App = "pyTOMTOM"
Ver = "0.4b"
Dev = "Thomas LEROY"
Transl = "Pascal MALAISE"

## Creation d'un racourci pour utiliser _ comme fonction de traduction
_ = gettext.gettext

## TODO : en mode texte non lance par un terminal, un message d'erreur arrive, il n'empeche pas le lancement
##        du logiciel ni ses actions, mais il serait plus propre de ne pas l'avoir

#----------------------------------------------- VERIFICATIONS DES PRE-REQUIS ------------------------------------------------
## Verification d'etre sous Linux - du moins un systeme posix
if( os.name != "posix" ):
	print _( "Vous n'êtes pas sous un système Linux" )
	sys.exit( 2 )
## TODO : Utile ? Verification de python en version 2.0 minimum
##pygtk.require('2.0')

#----------------------------------------------- DEFINITION DE LA CLASSE PRINCIPALE ------------------------------------------
class NotebookTomtom:

    ##------------------------------------------ DEFINITION DES VARIABLES GLOBALES -------------------------------------------
    ## Definition du repertoire contenant les donnees du logiciel
    dir = os.getenv( "HOME" ) + "/." + App
    ## Nom du fichier de configuration du logiciel
    configFile = App + ".cfg"
    ## Dossier de destination pour le GpsQuickFix sur le point de montage, 
    dest = "/ephem"
    ## Definition du fichier permettant de valider la presence d'un tomtom
    ttgo = "/ttgo.bif"
    ## Dossier contenant les images du logiciel
    dirPix = "../share/pytomtom/pix/"
    ## Definition par defaut du point de montage, vide veut dire que le point de montage n'a pas ete fourni
    ptMount = False
    ## Taille en octets du point de montage sélectionné
    ptMountSize = -1
    ## Liste des points de montage possibles, par defaut aucun
    ptMounts = []
    ## Definition par defaut du modele, vide veut dire que le modele n'a pas ete fourni
    model = False
    ## Choix de l'onglet affiché au démarrage de l'application, 3 par defaut (About)
    ## 0=options, 1=GPSQuickFix, 2=Save&Restore, 3=apropos, 4=quitter
    boxInit = 3
    ## liste des modeles avec une puce siRFStarIII
    siRFStarIII = ["Carminat",
	"GO 510 - 710 - 910",
	"GO 520 - 720 - 920 T",
	"GO 530 - 630 - 730 - 930 T",
	"One 1st edition",
	"Rider",
	"Rider 2nd edition"]
    ## liste des modeles avec une puce globalLocate
    globalLocate = ["GO 740 Live - 940 Live",
	"GO 750 Live - 950 Live",
	"One 3rd edition",
	"One 30 Series - New One 2008 - One v4",
	"One IQ Routes",
	"One XL",
	"One XL 2008",
	"One XL IQ Routes",
	"One XL Live",
	"Start"]
    ## liste de tous les modeles, somme des modeles
    ## TODO : ne pas utiliser append, mais extend ?
    models = []
    for model in siRFStarIII:
	models.append( model )
    for model in globalLocate:
	models.append( model )

    ## Niveau de debugage, 1 par defaut, seules les informations de debugage de niveau inferieur ou egal seront vues
    debug = 1

    ## Fichier de log, sys.stdout pour l'equivalent d'un print
    logFileName = dir + "/" + os.path.basename( sys.argv[ 0 ] ) + ".log"
    ## ex : logFile = open( logFileName, "w" ) ## ecriture dans un fichier de log avec suppression de l'existant
    ## ex : logFile = open( logFileName, "a" ) ## ecriture dans un fichier de log avec conservation de l'existant
    logFile = sys.stdout ## equivalent d'un print

    ## Par defaut le fichier de log n'est pas ecrase, cette option permet de l'ecraser
    overwriteLog = False
    ## lancement sans le gui pour le cas d'un script, faux par defaut
    noGui = False
    ## lancement de l'application sans lancement des actions exterieures (pour debuggage) a savoir gpsfix, backup, restore
    noExec = False
    ## Lancement de l'action GPSFix
    doGpsFix = False
    ## Lancement de l'action de backup
    doBackup = False
    ## Lancement de l'action de sauvegarde de la configuration
    doSave = False
    ## Lancement de l'action de restauration
    doRestore = False
    ## Processus du Backup ou Restore, une fois celui-ci lance
    procBackup = None
    ## Nom du fichier pour l'action de restauration ou de sauvegarde
    fileName = False
    ## Barre de progression
    progressionBar = None
    ## Taille de la barre de progression pour le mode graphique (pour le mode texte, la taille est calculee en fonction de la taille du terminal)
    progressionBarSize = 120
    ## Affichage du temps estime restant dans la barre de progression
    configTimeRemind = True
    ## Affichage du temps passe dans la barre de progression
    configTimePassed = False
    ## Affichage du temps estime total dans la barre de progression
    configTimeTot = True
    ## minuteur pour la barre de progression
    tempo = None
    ## delai de rafraichissement de la barre de progression
    tempoDelay = 3000
    ## timestamp de demarrage du minuteur, pour le calcul du temps estime restant et total
    tempoStartTime = None
    ## minuteur pour le refraichissement du combo contenant la liste des points de montages
    tempoCombo = None
    ## Verification de la possibilite d'effectuer le GPSFix (presence de cabextract)
    couldGpsFix = True
    ## Verification de la possibilite d'effectuer le backup (presence de tar)
    couldBackup = True
    ## Si l'utilisateur veut quitter avant la fin d'un sous-processus, la sauvegarde ou la restauration finissent puis l'application quitte
    quit = False

    ## objet graphique window
    window = None
    ## objet graphique de la liste des points de montage
    ptCombo = None

    ##------------------------------------------ DEFINITION DES FONCTIONS DE LA CLASSE ---------------------------------------
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction d'affichage des informations
    def Debug( self, niveau, text ):

	## Affichage uniquement si le niveau general de debug est superieur au niveau du debug fourni
	if( niveau <= self.debug ):
		## Ecriture dans le fichier de log
		self.logFile.write( str( date.today() ) + " " + text + "\n" )
		## flush pour un affichage immediat
		self.logFile.flush()
	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction d'affichage du nom et de la version de l'application
    def PrintVersion( self ):

	print( "" )
	print( App )
	print( Ver )

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction d'affichage de l'utilisation des options
    def Usage(self):
	## Utilisation de sysr.argv[ 0 ] afin d'avoir toujours le bon nom de l'executable
	print( "" )
	print( _( "utilisation : " ) + "python " + os.path.basename( sys.argv[ 0 ] ) + " [option]" )
	print( "" )
	print( "    -h, --help                                 " + _( "Cette aide" ) )
	print( "    -V, --version                              " + _( "Affichage du nom et de la version de l'application" ) )
	print( "    -d, --debug         niv                    " + _( "Niveau de déboggage valeur entre 0 et 9" ) )
	print( "    -l, --log-file      file-to-log            " + _( "Nom du fichier d'enregistrement des traces de l'application" ) )
	print( "    -x, --overwrite-log                        " + _( "Ecraser le ficher des traces, mode ajout par défaut" ) )
	print( "        --no-exec                              " + _( "Ne pas executer les commandes, juste afficher ce qui doit être fait" ) )
	print( "        --print-time-passed                    " + _( "Afficher le temps passé dans la barre de progression" ) )
	print( "        --print-time-remind                    " + _( "Afficher le temps estimé restant dans la barre de progression" ) )
	print( "        --print-time-tot                       " + _( "Afficher le temps estimé total dans la barre de progression" ) )
	print( "    -n, --no-gui                               " + _( "Utilisation en mode texte" ) )
	print( "    -s, --save-config                          " + _( "Lancer la sauvegarde du fichier de configuration" ) )
	print( "    -g, --do-gpsfix                            " + _( "Lancer la mise a jour GPSFix" ) )
	print( "    -b, --do-backup                            " + _( "Lancer le backup dans le fichier " )
		+ self.dir + "/sv-[date-du-jour]-[model].tar[.gz|.bz] "
		+ _( "\n                                               ou fourni par -f" ) )
	print( "    -r, --do-restore                           " + _( "Lancer la restauration du fichier " )
		+ self.dir + "/sv-[date-du-jour]-[model].tar[.gz|.bz]"
		+ _( "\n                                               ou fourni par -f" ) )
	print( "    -f, --file          file-to-save           " + _( "Emplacement du fichier de sauvegarde ou de restauration" ) )
	print( "    -p, --ptmount       dir                    " + _( "Point de montage du TomTom" ) )
	print( "    -m, --model         model                  " + _( "Modele du TomTom dans la liste :" ) )
	## Liste des modeles
	for model in self.models:
		print( "                                                     '" + model + "'" )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de recuperation des options
    def GetOpts( self ):

	## initialisation des variables
	ptMount = False
	model = False
	debug = False
	err = False
	logFile = None

	## On teste la recuperation des arguments
	try:
		## getopt.getopt decoupe la ligne (l'ensemble des arguments : sys.argv[1:]) en deux variables, les options et les arguments de la commande
		##        l'ordre des options importe peu pour la technique, cependant, afin de ne pas mettre deux fois la meme lettre, il est plus
                ##        simple de respecter l'ordre alphabetique
		opts, args = getopt.getopt( sys.argv[1:], "bd:f:ghl:m:np:rsxV",
			[ "do-backup", "debug=", "file=", "do-gpsfix", "help", "log-file=", "model=", "no-gui", "ptmount=", "do-restore",
				"save-config", "overwrite-log", "version",
				"no-exec", "print-time-passed", "print-time-remind", "print-time-tot" ] )
	## Si le test ne fonctionne pas
	except getopt.GetoptError, err:
		## affichage de l'erreure
		self.Debug( 0, str( err ) ) ## Affichera quelque chose comme "option -a not recognized"
		## Affichage de l'utilisation des options
		self.Usage()
		sys.exit( 2 )

	## Pour chaque option et ses arguments de la liste des options
	for opt, argument in opts:
		if opt in ( "-b", "--do-backup" ):
			self.doBackup = True
			self.Debug( 5, _( "Backup à effectuer" ) )
		elif opt in ( "-d", "--debug" ):
			## Verification de l'option fournie faite a la fin
			debug = argument
		elif opt in ( "-f", "--file" ):
			self.fileName = os.path.realpath( argument )
			self.Debug( 5, _( "Nom du fichier fourni : " ) + self.fileName )
		elif opt in ( "-g", "--do-gpsfix" ):
			self.doGpsFix = True
			self.Debug( 5, _( "GpsFix à executer" ) )
		elif opt in ( "-h", "--help" ):
			self.Usage()
			sys.exit()
		elif opt in ( "-l", "--log-file" ):
			logFile = argument
		elif opt in ( "-m", "--model" ):
			## Verification du bon choix du modele faite a la fin
			model = argument
		elif opt in ( "-n", "--no-gui" ):
			self.noGui = True
			self.Debug( 5, _( "Mode script activé" ) )
		elif opt in ( "-p", "--ptmount" ):
			## Verification du bon choix du point de montage faite a la fin
			ptMount = argument
		elif opt in ( "-r", "--do-restore" ):
			self.doRestore = True
			self.Debug( 5, _( "Restauration à effectuer" ) )
		elif opt in ( "-s", "--save-config" ):
			self.doSave = True
			self.Debug( 5, _( "Sauvegarde de la configuration à effectuer" ) )
		elif opt in ( "-x", "--overwrite-log" ):
			self.overwriteLog = True
			self.Debug( 5, _( "Ecrasement du fichier de configuration" ) )
		elif opt in ( "-V", "--version" ):
			self.PrintVersion()
			sys.exit()
		elif opt in ( "--no-exec" ):
			self.noExec = True
			self.Debug( 5, _( "Mode sans execution" ) )
		elif opt in ( "--print-time-passed" ):
			self.configTimePassed = True
			self.Debug( 5, _( "Affichage du temps passé dans la barre de progression" ) )
		elif opt in ( "--print-time-remind" ):
			self.configTimeRemind = True
			self.Debug( 5, _( "Affichage du temps restant dans la barre de progression" ) )
		elif opt in ( "--print-time-tot" ):
			self.configTimeTot = True
			self.Debug( 5, _( "Affichage du temps total dans la barre de progression" ) )
		else:
			## Si l'option est mise dans getopt mais n'est pas traite ici
			self.Debug( 0, _( "Option sans action" ) )

	## Verifications diverses

	## Changement de fichier de log
	if( logFile != None ):
		## Choix du mode d'ecriture du fichier de log, par defaut en ajout, si l'option est fournie, on passe en ecrasement
		if( self.overwriteLog == True ):
			option = "a"
		else:
			option = "w"

		## On test l'ecriture dans le nouveau fichier de log
		try:
			## Pour ne pas perdre l'ancien fichier, on ouvre le nouveau dans une nouvelle variable
			logFile = open( logFile, option )
			## Si tout s'est bien passe, on ferme l'ancien fichier (sauf s'il s'agit de stdout)
			if( self.logFile != sys.stdout ):
				self.logFile.close()
			## Puis on rattache le nouveau fichier a la variable globale
			self.logFile = logFile
		except:
			## S'il y a une erreur, on affiche un message d'erreur (dans l'ancien fichier de log)
			self.Debug( 1, _( "Impossible de changer de fichier de traces" ) )
	else:
		## S'il n'y a pas de demande de nouveau fichier mais simplement d'excrasement du fichier de log (et qu'il ne s'agit pas
		## de stdout, et re-ouvre (fermeture puis re-ouverture) le fichier de log en ecrasement
		if( self.logFile != sys.stdout and self.overwriteLog == True ):
			self.logFile.close()
			self.logFile = open( self.logFileName, "w" )
		
	## Si les options de sauvegarde et de restauration sont founies en meme temps, il y a erreur
	if( self.doBackup and self.doRestore ):
		self.Debug( 0, _( "Option -b et -r fournies en meme temps" ) )
		## Afin que toutes les options soient testees plutot que de stopper sur la premiere puis la seconde...
		err = True

	## Verification que le modele donne fait partie de la liste des modeles existants
	if not( model == False ):
		if( model in self.models ):
			self.model = model
			self.Debug( 5, _( "Modele fourni : " ) + self.model )
		else:
			self.Debug( 0, _( "Mauvais choix de modèle " ) + str( model ) )
			## Afin que toutes les options soient testees plutot que de stopper sur la premiere puis la seconde...
			err = True

	## Verification du point de sauvegarde
	if not( ptMount == False ):
		if( self.IsPtMount( ptMount ) ):
			self.ptMount = ptMount
			self.Debug( 5, _( "Point de montage fourni : " ) + self.ptMount )
		else:
			self.Debug( 0, _( "Mauvais argument pour le point de montage : " ) + ptMount )
			## Afin que toutes les options soient testees plutot que de stopper sur la premiere puis la seconde...
			err = True

	## Verification que le niveau de debug est compris entre 0 et 9
	if not( debug == False ):
		try:
			if( int( debug ) >= 0 and int( debug ) <= 9 ):
				self.debug = int( debug )
				self.Debug( 5, _( "Argument pour l'option de deboggage " ) + str( int( debug ) ) )
			else:
				self.Debug( 1, _( "Mauvais argument pour l'option de deboggage " ) + str( int( debug ) ) )
		except:
			self.Debug( 1, _( "Argument pour l'option de deboggage non entier " ) + debug )

	## Si on a une erreur, on arrete le programme
	if( err ):
		self.Usage()
		sys.exit( 2 )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de lecture des variables d'environnement
    def GetVariables( self ):

	## Lecture du point de montage (variable PYTOMTOM_PTMOUNT)
	env = os.getenv( "PYTOMTOM_PTMOUNT", False )
	if not( env == False ):
		self.ptMount = str( env )
		self.Debug( 5, _( "Point de montage fourni : " ) + str( env ) )

	## Lecture du modele PYTOMTOM_MODELE
	env = os.getenv( "PYTOMTOM_MODELE", False )
	if not( env == False ):
		self.model = str( env )
		self.Debug( 5, _( "Modele fourni : " ) + str( env ) )

	## Lecture de l'affichage de la barre de progression
	env = os.getenv( "PYTOMTOM_CONFIG_TIME_PASSED", False )
	if not( env == False ):
		if( env == "False" ):
			self.configTimePassed = False
		elif( env == "True" ):
			self.configTimePassed = True
		self.Debug( 5, _( "Affichage du temps passé : " ) + str( env ) )

	## Lecture de l'affichage de la barre de progression
	env = os.getenv( "PYTOMTOM_CONFIG_TIME_REMIND", False )
	if not( env == False ):
		if( env == "False" ):
			self.configTimeRemind = False
		elif( env == "True" ):
			self.configTimeRemind = True
		self.Debug( 5, _( "Affichage du temps restant : " ) + str( env ) )

	## Lecture de l'affichage de la barre de progression
	env = os.getenv( "PYTOMTOM_CONFIG_TIME_TOT", False )
	if not( env == False ):
		if( env == "False" ):
			self.configTimeTot = False
		elif( env == "True" ):
			self.configTimeTot = True
		self.Debug( 5, _( "Affichage du temps total : " ) + str( env ) )

	## Afin de valider le mode graphique, on verifie la variable d'environnement DISPLAY
	env = os.getenv( "DISPLAY", False )
	if( env == False or env == "" ):
		self.noGui = True
		self.Debug( 5, _( "Mode script activé" ) )

	return True
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de lecture des donnees de configuration
    def GetConfig( self ):

	## La lecture du fichier de configuration, puis des options et enfin des variables d'environnement
	## permet de definir l'ordre de preference des donnees si les donnees sont fournies sous differentes formes

	## Verification de l'existence du repertoire de configuration
	if not( os.path.exists( self.dir ) ):
		## Creation du repertoire si inexistant
		os.mkdir( self.dir )
		## Verification apres creation afin de valider le systeme
		if not( os.path.exists( self.dir ) ):
			self.Debug( 0, _( "Creation du dossier de configuration impossible " ) + self.dir )
			sys.exit( 2 )
	else:
		## Verification que le dossier de configuration en est bien un
		## TODO : verification en cas de lien vers un dossier plutot qu'un dossier
		if( os.path.isdir( self.dir ) ):
			## Verification de l'existence du fichier de configuration
			if( os.path.exists( self.dir + "/" + self.configFile ) ):
				## Ouverture du fichier de configuration en lecture
				with open( self.dir + "/" + self.configFile, "rb" ) as config:
					## Lecture des lignes
					line = config.readline()
					while( line ):
						## suppression des \n de fin de ligne
						line = line[:-1]
						## Le fichier se presente sous la forme nom=valeur, on decoupe selon le =
						line = line.split( '=' )
						## Suppression des espaces inutiles en debut et fin de mot
						name = line[ 0 ].strip()
						## On traite en deux cas, soit le parametre est un string, soit un bouleen
						if( name in ( "ptMount", "model" ) ):
							## setattr permet d'associer la valeur a l'attribut fourni par son nom au format str
							## On supprime naturellement les espaces inutiles en debut et fin de mot
							setattr( self, name, line[ 1 ].strip() )
						##      deuxieme cas, s'il s'agit d'un bouleen
						elif( name in ( "configTimePassed", "configTimeRemind", "configTimeTot" ) ):
							if( line[ 1 ].strip() == "True" ):
								setattr( self, name, True )
							else:
								setattr( self, name, False )

						## lecture de la prochaine ligne
						line = config.readline()
				## Fermeture du fichier de configuration
				config.close()
		else:
			self.Debug( 0, _( "Le dossier de configuration n'est pas un dossier " ) + self.dir )
			sys.exit( 2 )

	## Lecture des options
	self.GetOpts()
	## Lecture des variables d'environnement
	self.GetVariables()

	## Si le point de montage ou le modele n'est pas defini, il faut le definir -> passage sur la fenetre de gestion des options
	##       de meme si le point de montage n'est pas valide
	if( self.ptMount == False or self.IsPtMount( self.ptMount ) == False or self.model == False ):
		self.boxInit = 0

	## Validation des possibilites de l'application (verification des dependances externes)
	## Lancement de la commande which cabextract qui precise l'emplacement de cabextract, renvoi 0 si trouve, 1 sinon
	p = subprocess.Popen( "which cabextract > /dev/null", shell=True )
	if( p.wait() != 0 ):
		self.Debug( 1, _( "cabextract n'est pas installé" ) )
		self.couldGpsFix = False

	## Lancement de la commande which tar qui precise l'emplacement de cabextract, renvoi 0 si trouve, 1 sinon
	p = subprocess.Popen( "which tar > /dev/null", shell=True )
	if( p.wait() != 0 ):
		self.Debug( 1,_( "tar n'est pas installé" )  )
		self.couldBackup = False

	## Affichage des informations de deboggage
	self.Debug( 1, _( "Application : " ) + App + _( " - Version : " ) + Ver )
	self.Debug( 1, _( "Point de montage utilisé : " ) + str( self.ptMount ) )
	self.Debug( 1, _( "Modèle utilisé : " ) + str( self.model ) )

	return True
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de mise a jour et d'enregistrement des options par le formulaire
    def OnUpdate( self, entry ):
	
	## Recuperation des differents parametres du formulaire
	model = self.modeleCombo.get_model()
        index = self.modeleCombo.get_active()
	self.model = str( model[ index ][ 0 ] )
	## Pas de verification du modele puisque le choix s'effectue a partir d'une liste fournie par l'application, aucun risque d'erreur

	ptMount = self.ptCombo.get_model()
	index = self.ptCombo.get_active()
	if( self.IsPtMount( str( ptMount[ index ][ 0 ] ) ) ):
		self.ptMount = str( ptMount[ index ][ 0 ] )

	## Enregistrment des options
	self.PutConfig()

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de sauvegarde de la configuration
    def PutConfig( self ):
	
	## Verification des donnees a sauvegarder
	if not( self.ptMount and self.model ):
		self.Debug( 0, _( "Les données ne peuvent être enregistrées : " ) + _( "point de montage = '" ) + str( self.ptMount )
			+ _( "' - modèle = '" ) + str( self.model ) + "'" )
		sys.exit(2)

	## Sauvegarde des donnees dans le fichier de configuration
	try:
		configFile = open( self.dir + "/" + self.configFile, "wb" )
		## L'enregistrement des options s'effectue sous le forme nom=valeur
		## getattr permet de recuperr la valeur de l'attribut fourni par son nom au format str
		for option in ( "ptMount", "model", "configTimePassed", "configTimeRemind", "configTimeTot" ):
			configFile.write( option + "=" + str( getattr( self, option ) ) + "\n" )
	finally:
		## Fermeture du fichier, qu'il y ait une erreur ou non
		configFile.close()

	## Affichage des informations de deboggage
	self.Debug( 1, _( "TomTom : " ) + str( self.model ) + _( " ::enregistré::" ) )
	self.Debug( 1, _( "Point de montage : " ) + str( self.ptMount ) + _( " ::enregistré::" ) )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de recherche des points de montage disponibles
    def GetPtMounts(self):

	## Mise a zero de la liste
	self.ptMounts = []
	## Recuperation de la liste des points de montage de type vfat, avec leur taille
	ptMounts = self.GetPtWithSize( "vfat" )
	## Pour chaque point de montage
	for ptMountSize, ptMount in ptMounts:
		if( ptMountSize == -1 ):
			self.Debug( 5, _( "Aucun point de montage" ) )
			return True

		## Validation du point de montage
		if( self.IsPtMount( ptMount ) ):
			self.ptMounts.append( [ ptMountSize, ptMount ] )

	## Affichage des informations de deboggage
	self.Debug( 5, _( "Liste de points de montage " ) + str( self.ptMounts ) )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de validation du point de montage
    def IsPtMount(self, mountPoint):

	## Si le point de montage n'est pas fourni ou est faux
	if( mountPoint == False ):
		return False

	## Verification de l'existence du fichier ttgo.bif pour valider qu'il s'agit bien d'un point de montage d'un tomtom
	self.Debug( 6, _( "Test du point de montage " ) + mountPoint )
	if( os.path.exists( mountPoint + self.ttgo ) ):
		self.Debug( 5, _( "Point de montage valide : " ) + mountPoint )
		return True

	## Dans tous les autres cas, le point de montage n'est pas valide
	return False

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## fonction GPSQUICKFIX, mise a jour des donnees de l'emplacement des satellites (a effectuer une fois par semaine)
    def GpsQuickFix(self, widget):
	
	## Si cabextract n'existe pas, on ne fait rien
	if( self.couldGpsFix == False ):
		return False

	## Verification du point de montage
	if not( self.IsPtMount( self.ptMount ) ):
		self.Debug( 1, _( "Point de montage non valide : " + self.ptMount ) )
		return False

	## Aucune verification du modele car il provient d'une liste pre-definie

	## Definition du dossier de destination
	dir = str( self.ptMount + self.dest )
	
	if self.model in self.siRFStarIII: ## si le tomtom possede un chipset SiRFStarIII
		url = "http://home.tomtom.com/download/Ephemeris.cab?type=ephemeris&amp;eeProvider=SiRFStarIII&amp;devicecode=2"
		self.Debug( 6, "chipset SiRFStarIII : " + url )
	else: ## sinon (si le tomtom possede un chipset globalLocate)
		url = "http://home.tomtom.com/download/Ephemeris.cab?type=ephemeris&amp;eeProvider=globalLocate&amp;devicecode=1"
		self.Debug( 6, "chipset globalLocate : " + url )

	## Definition d'une requete
	request = urllib2.Request( url, None )
	## Ouverture de la requete
	try:
		## Si l'on veut l'execution, on lance la recuperation de l'url
		if( self.noExec == False ):
			urlFile = urllib2.urlopen( request )
	except:
		self.Debug( 1, _( "Impossible de récupérer l'url : " ) + url )
		return False

	## Autant de try imbrique afin de fournir des messages justes, et de supprimer correctement les fichiers et dossiers temporaires
	## Le cab est recupere dans un fichier temporaire, puis extrait dans un dossier temporaire
	try:
		## Creation d'un repertoire temporaire pour extraire le cab telecharge
		tempDirName = tempfile.mkdtemp()
		self.Debug( 5, _( "Création du dossier temporaire : " ) + tempDirName )
		try:
			## Creation d'un fichier temporaire pour le telechargement du cab
			tempFile = tempfile.NamedTemporaryFile()
			self.Debug( 5, _( "Création du fichier temporaire : " ) + tempFile.name )
			try:
				self.Debug( 5, _( "Récupération des données : " ) + url )
				## Si l'on veut une execution, on telecharge le cab
				if( self.noExec == False ):
					tempFile.write( urlFile.read() )
					tempFile.flush()
					urlFile.close()
				try:
					## Extraction du cab seulement si l'on veut l'execution, sinon un simple affichage de ce que l'on aurait fait
					if( self.noExec == False ):
						cmd = ( "cabextract -d " + tempDirName
                        				+ " " + tempFile.name + "; touch " + tempDirName + "/*" )
					else:
						cmd = ( "echo cabextract -d " + tempDirName
                        				+ " " + tempFile.name + "; echo touch " + tempDirName + "/*" )
					self.Debug( 5, _( "Lancement de la commande " ) + cmd )
					## Lancement du processus
					p = subprocess.Popen( cmd, shell=True )
					p.wait()
					try:
						## Deplacement de tous les fichiers du cab vers la destination
						##     Ceci evite de faire une difference entre les deux modeles de chipset
						files = os.listdir( tempDirName )
						for file in files:
							self.Debug( 5, _( "Deplacement des fichiers vers leur destination finale : " )
								+ tempDirName + "/" + file + " -> " + self.ptMount + self.dest + "/" + file )
							## ATTENTION : si le fichier destination est un repertoire, et que le fichier existe
							##             shutil.move fait une erreur, il faut donc preciser le fichier de destination
							##             pour l'ecraser, et non simplement le repertoire de destination
							shutil.move( tempDirName + "/" + file, self.ptMount + self.dest + "/" + file )
					except:
						self.Debug( 0, _( "Impossible de déplacer les données" ) )
				except:
					self.Debug( 0, _( "Impossible d'extraire les données" ) )
			except:
				self.Debug( 0, _( "Impossible de récupérer les données" ) )
		except:
			self.Debug( 0, _( "Impossible de créer un fichier temporaire" ) )
		finally:
			## Fermeture propre du fichier temporaire (avec sa suppression) dans tous les cas (meme si un probleme survient)
			tempFile.close()
	except:
		self.Debug( 0, _( "Impossible de créer un répertoire temporaire" ) )
	finally:
		## Suppression du dossier temporaire dans tous les cas (meme si un probleme survient)
		shutil.rmtree( tempDirName )

	## Affichage de la fin de l'execution, en popup si l'on est pas en mode script
	if( self.noGui == False ):
		self.Popup( _( "GPSQuickFix terminé" ) )
	self.Debug( 1, _( "GPSQuickFix terminé" ) )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de recuperation du nom et de la taille des partitions locales montees, limite par un type de systeme, ou/et un point de montage
    def GetPtWithSize( self, type = None, ptMount = None ):
	
	## Ecriture de la commande, df pour lister,
	##     -t pour specifier le type selectionne,
	##     -T pour afficher le type du systeme de fichier
	##     -l pour lister uniquement les systemes de fichiers locaux
	##     -P pour avoir le format posix
	##     --output-delimiter pour s'assurer le delimiteur final avant traitement (commande split)
	##     -B 1 pour utiliser une taille de 1 octet pour l'affichage
	##     Si la commande ne liste aucun systeme de fichier, un message d'erreur est fourni, on re-dirige donc les erreurs sur /dev/null
	##     La commande df affiche une entete inutile, d'ou le tail -n +2 (on commence a la deuxieme ligne)
	##     Afin de pouvoir decouper facilement la ligne, on remplace les ensembles d'espace par un unique espace - commande tr -s
	##     Afin de ne retenir que les donnees utiles, on recupere les champs 4 et 7 - commande cut
	cmd = "df -B 1 -TlP"
	if not( type == None ):
		cmd += "t " + type + " "
	if not( ptMount == None ):
		cmd += " \"" + ptMount + "\""
	cmd += " 2> /dev/null | tail -n +2 | tr -s ' ' | cut -d ' ' -f 4,7 --output-delimiter=,"

	## Lancement de la commande, avec recuperation du stdout dans le processus actuel
	self.Debug( 5, _( "Lancement de la commande : " ) + cmd )
	p = subprocess.Popen( cmd, stdout = subprocess.PIPE, shell=True )
	res = []
	## Lecture du resultat
	for line in p.stdout:
		## Suppression du \n de la ligne
		line = line[ : -1 ]
		## Grace a l'option --output-delimiter, on lance split
		line = line.split( ',', 2 )
		self.Debug( 5, _( "Résultat de la commande : " ) + str( int( line[0 ] ) ) + " -> " + line[ 1 ] )
		res.append( [ int( line[ 0 ] ), line[ 1 ] ] )
	p.wait()

	if( res == [] ):
		## le resultat de la fonction est une liste de liste contenant la taille et le nom du point de montage
		return( [ [ -1, None ] ] )

	## Renvoi des donnees collectees
	return res

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de recherche d'un enfant de self.window, le nom fourni sous la forme nom_frame.nom_box....
    def SearchObj( self, name ):

	## TODO : existe-t-il deja une fonction plus rapide ?
	## Decoupage du nom par le separateur "."
	name = name.split( '.' )

	## On commence au niveau self.window
	objParent = self.window
	self.Debug( 7, _( "Objet recherché : " ) + str( name ) )

	## Pour tous les niveaux du nom fourni
	for i in range( 0, len( name ) - 1, 1 ):
		self.Debug( 7, _( "Parcours niveau : " ) + str( i ) )

		## Enfant non trouve
		find = False

		## Pour chaque enfant
		for objChild in objParent:
			self.Debug( 7, _( "     Objet parcouru : " ) + objChild.get_name() )
			## Si le nom correspond
			if( objChild.get_name() == name[ i ] ):
				self.Debug( 7, _( "Objet trouvé" ) )
				## Le parent devient l'enfant pour continuer la recherche au niveau suivant
				objParent = objChild
				## On a bien trouve l'enfant
				find = True
				break

		## Si l'enfant n'est pas trouve a ce niveau, on arrete tout
		if( find == False ):
			return None

	## retour de l'enfant, comme le parent est devenu l'enfant, il suffit de retourner le parent (on est sur qu'il est defini)
	return objParent
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## fonction de remplacement image de demarrage avec toutes les verifications utiles
    def ChangeStartImg( self, widget ):
		## TODO : mettre en place la reconnaissance des noms des images a remplacer
		if ( os.path.exists( self.ptMount +"/splash.bmp" ) ):
			return True ##ecran normal n
		else: 
			if ( os.path.exists( self.ptMount +"/splashw.bmp" ) ): ##elif ??
				return True ##ecran widescreen w

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de creation d'un nom de fichier de sauvegarde
    def GetNewFileName( self, uniq = False ):

	## si l'option uniq est fournie, on ajoute un nombre aleatoire
	if( uniq == False ):
		return( self.dir + "/sv-" + str( date.today() ) + "-" + self.model + ".tar" )
	else:
		return( self.dir + "/sv" + str( random.randint( 1, 50 ) ) + "-" + str( date.today() ) + "-" + self.model + ".tar" )

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## fonction de lancement du Backup et de la restauration avec toutes les verifications utiles
    def BackupRestoreGPS( self, widget, type ):

	## Verification du point de montage
	if not( self.IsPtMount( self.ptMount ) ):
		self.Debug( 1, _( "Point de montage non valide : " + self.ptMount ) )
		return False

	## Recuperation du nom du fichier de sauvegarde
	files = self.saveFileCombo.get_model()
	index = self.saveFileCombo.get_active()
	if( files[ index ][ 0 ] == "" ):
		self.Debug( 2, _( "Mauvaise selection du fichier de " ) + _( type ) )
		return False
	self.fileName = files[ index ][ 0 ]
	self.Debug( 1, _( "Fichier de " ) + _( type ) + " : " + self.fileName )

	if( type == "restore" ):
		##TODO a corriger si le fichier n'existe pas !!! et non l'inverse...
		if not( os.path.exists( self.fileName ) ):
			self.Debug( 1, _( "Archive inexistante" ) )
			return False

	if( self.noGui == False ):
		obj = self.SearchObj( "notebook.frameSaveRestore.boxSaveRestore.btnSave" )
		if( obj != None ):
			obj.set_sensitive( False )
		obj = self.SearchObj( "notebook.frameSaveRestore.boxSaveRestore.btnRestore" )
		if( obj != None ):
			obj.set_sensitive( False )

	## Verification de l'espace disponible par rapport a l'espace initial,

	## Recuperation d'un tableau de toutes les partitions de type
	##     les donnees sont sur la ligne 0 puisque nous n'avons qu'une seule ligne
	self.ptMountSize = self.GetPtWithSize( "vfat", self.ptMount )
	## Recuperation du nom de la partition impactee,
	##     en effet, si l'on fournit /boot, on retrouve / car /boot n'est pas monte et fait partie du systeme /
	self.ptMount = self.ptMountSize[ 0 ][ 1 ]
	## Recuperation de la taille de la partition
	self.ptMountSize = self.ptMountSize[ 0 ][ 0]

	if( self.ptMountSize == -1 ):
		self.Debug( 1, _( "Taille du systeme de fichier impossible a calculer" ) )
		return False
	self.Debug( 5, _( "Taille du point de montage : " ) + self.ptMount  + " -> " + str( self.ptMountSize ) )

	## Recuperation de la taille de la partition hote du fichier de sauvegarde
	size = self.GetPtWithSize( None, os.path.dirname( os.path.realpath( self.fileName ) ) )
	size = size[ 0 ][ 0 ]
	self.Debug( 5, _( "Taille de la partition de sauvegarde : " ) + str( size ) )

	## Attention, si la taille de la partition de la sauvegarde est trop petite
	if( self.ptMountSize > size ):
		self.Debug( 1, _( "Espace disque insuffisant : " ) + str( size ) + _( " pour " ) + str( self.ptMountSize ) )
		return False

	## ajout d'affichage supplementaire de la commande tar si le debug est suffisament important
	option = ""
	if( self.debug >= 4 ):
		option += "v"

	## Choix de la commande s'il faut faire un backup ou une restauration, choix du texte a afficher dans la barre de progression
	if( type == "backup" ):
		option += "c"
		text = _( "Création" )
	elif( type == "restore" ):
		option += "x"
		text = _( "Restauration" )

	## Si le processus precedent n'a pas ete lance ou n'est pas fini (ex : poll = None), on attend
	if( self.procBackup == None or self.procBackup.poll() != None ):
		## -u pour creer ou mettre a jour une archive
		## -f pour preciser le nom de l'archive plutot que sur le stdout
		## Execution de la commande seuleument si l'on veut, sinon affichage de ce que l'on aurait fait
		if( self.noExec == False ):
			cmd = "cd " + self.ptMount + "; tar -" + option + "f \"" + self.fileName + "\" ." 
		else:
			cmd = "cd " + self.ptMount + "; echo tar -" + option + "f \"" + self.fileName + "\" ." 
		self.Debug( 5, _( "Lancement de la commande : " ) + cmd )
		self.procBackup = subprocess.Popen( cmd, shell=True )

		## verification de la fin du processus
		if( self.procBackup.poll() != None ):
			## Si l'on est pas en mode script, on affiche un popup de fin de processus
			if( self.noGui == False ):
				self.Popup( text + _( " terminée" ) )
			self.Debug( 5, text + _( " terminée" ) )

		## Lancement de la barre de progression
		self.Debug( 5, _( "Lancement du test de " ) + text + _( " d'archive toutes les secondes" ) )
		## Supression du tempo avant sa re-utilisation
		if( self.tempo != None ):
			gobject.source_remove( self.tempo )
		## Saut de ligne pour etre sur d'afficher correctement la barre de progression
        	sys.stdout.write( "\n" )
		sys.stdout.flush()
		## Creation d'un timeout toutes les n ms, lancement de la fonction self.Progress avec ces parametres
		self.tempo = gobject.timeout_add( self.tempoDelay, self.Progress, 100, 100,
				text + _( " de l'archive" ), self._BackupRestoreGPSEnd, text )

		return False

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de calcul et de mise en forme des temps estimes restant, total et du temps passe
    def GetTimeDelay( self, percent ):

	## Calcul du temps passe (en secondes) depuis le lancement de la sauvegarde
	secondsPass = gobject.get_current_time() - self.tempoStartTime
	## Calcul du temps estime total (en secondes) - en supposant que le temps passe est lineaire par rapport au travail effectue
	##      pour le tar, ce n'est pas le cas, rapide jusqu'a 11%, puis apparement lineaire, tres proche a partir de 40% - 37mn pour 1,6Go
	##      pour le bzip2, on l'est quasiment, à 2% on est tres proche - 22mn pour 1,6Go compresse en 1,5Go soit 98% - inutile !!!
	##      pour le bunzip2, il faut 8mn
	secondsTot = secondsPass / percent
	## Calcul du temps estime restant (en secondes)
	secondsRemind = secondsTot - secondsPass

	## Calcul du nombre d'heures passe (pour l'affichage)
	hoursPass = str( int( secondsPass / 3600 ) )
	## Calcul du nombre de minutes estimees au total, sans les heures calculees auparavant (pour l'affichage)
	minutesPass = str( int( ( secondsPass / 60 ) % 60 ) )
	## Calcul du nombre de secondes estimees au total, sans les heures et les minutes calculees auparavant (pour l'affichage)
	secondsPass = str( int( secondsPass % 60 ) )

	## Calcul du nombre d'heures estimees au total (pour l'affichage)
	hoursTot = str( int( secondsTot / 3600 ) )
	## Calcul du nombre de minutes estimees au total, sans les heures calculees auparavant (pour l'affichage)
	minutesTot = str( int( ( secondsTot / 60 ) % 60 ) )
	## Calcul du nombre de secondes estimees au total, sans les heures et les minutes calculees auparavant (pour l'affichage)
	secondsTot = str( int( secondsTot % 60 ) )

	## Calcul du nombre d'heures estimees restantes (pour l'affichage)
	hoursRemind = str( int( secondsRemind / 3600 ) )
	## Calcul du nombre de minutes estimees restantes, sans les heures calculees auparavant (pour l'affichage)
	minutesRemind = str( int( ( secondsRemind / 60 ) % 60 ) )
	## Calcul du nombre de secondes estimees restantes, sans les heures et les minutes calculees auparavant (pour l'affichage)
	secondsRemind = str( int( secondsRemind % 60 ) )

	## Mise en place de l'affichage du temps a afficher, en fonction des options fournies
	timeToPrint = ""
	if( self.configTimePassed == True ):
		timeToPrint += hoursPass + ":" + minutesPass + ":" + secondsPass + " -> "
	if( self.configTimeRemind == True ):
		timeToPrint += hoursRemind + ":" + minutesRemind + ":" + secondsRemind
	if( self.configTimeTot == True ):
		timeToPrint += " / " + hoursTot + ":" + minutesTot + ":" + secondsTot

	## Renvoi du texte a afficher
	return timeToPrint

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## fonction de validation du processus apres sa fin
    def _BackupRestoreGPSEnd( self, type ):

	## Test de la valeur retournee pour valider ou non la tache finie
	if( self.procBackup.poll() != 0 ):
		type += _( " non réussie" )
	else:
		type += _( " terminée avec succès !" )

	self.Debug( 1, type + _( " : " ) + str( self.procBackup.poll() ) )

	## Si l'on est pas en mode script, on re-active les boutons de lancement des taches
	if( self.noGui == False ):
		## Recherche du bouton btnSave
		obj = self.SearchObj( "notebook.frameSaveRestore.boxSaveRestore.btnSave" )
		if( obj != None ):
			## Activation du bouton (de-sactive auparavant)
			obj.set_sensitive( True )
		## TODO : Quand la restauration pourra etre lance, supprimer les # devant les 3 lignes suivantes
		obj = self.SearchObj( "notebook.frameSaveRestore.boxSaveRestore.btnRestore" )
		if( obj != None ):
			obj.set_sensitive( True )
		## Affichage du resultat par un popup
		self.Popup( type )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction d'affichage de la barre de progression
    def Progress( self, percentMin, percentMax, text, functEnd, paramEnd ):

	## TODO : possibilite de mettre en pause
	## La premiere fois que la fonction est lancee, l'application a deja ete lancee il y a self.tempoDelay secondes
	if( self.tempoStartTime == None ):
		self.tempoStartTime = gobject.get_current_time() - self.tempoDelay

	## Si le processus est fini
	if( self.procBackup.poll() != None ):

		## Recuperation du temps a afficher, etant arrive a 1, soit 100% (le processus est fini)
		timeToPrint = self.GetTimeDelay( 1 )
		## Creation du texte de la barre de progression
		text = '%s : 100%% - %s' % ( text, timeToPrint )
		## Taille de la barre en mode texte
		try:
			barSize = struct.unpack( "HH", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, struct.pack( "HH", 0, 0 ) ) )[ 1 ] - len( text ) - 5
		except:
			barSize = 120
		
		## Affichage de la barre de progression en mode texte
        	out = '\r [%s] %s\n' % ( '=' * barSize, text )
        	sys.stdout.write( out )
		sys.stdout.flush()
		
		## Si l'on est en mode graphique
		if( self.noGui == False ):
			## Centrage du texte sur une taille de self.progressionBarSize (permettant d'avoir une barre de progression toujours a la meme taille
			textToPrint = text.center( self.progressionBarSize )
			## Affichage de la barre de progression (la valeur doit etre inferieure ou egale a 1
			self.progressionBar.set_fraction( 1 )
			## Affichage du texte sur la barre de progression
			self.progressionBar.set_text( textToPrint )
		
		## Lancement de la fonction de validation du processus
		functEnd( paramEnd )

		## Suppression du minuteur et de la date de debut du processus
		gobject.source_remove( self.tempo )
		self.tempo = None
		self.tempoStartTime = None
		
		## Si on a deja voulu quitter, on quitte a la fin du processus
		if( self.quit == True ):
			self.Debug( 5, _( "On quitte suite à la demande" ) )
			self.Delete( None )

		## Pour arreter le minuteur, il faut renvoyer False
		return False

	## Le processus n'est pas fini, il faut calculer et afficher la barre de progression
	## Initialisation du type de la nouvelle valeur, un nombre flottant a 2 valeurs apres la virgule
	newVal = round( float( 0.01 ), 2 )
	## Recuperation de la taille du fichier de destination
	newSize = os.path.getsize( self.fileName )
	self.Debug( 7, _( "Taille du fichier : " )  + self.fileName + " -> " + str( newSize ) + " / " + str( self.ptMountSize ) )

	## On estime que la taille du fichier finale sera percentMin, mais qu'au maximum le fichier aura une taille de percentMax
	## On calcul donc le pourcentage estime entre ces deux valeurs, avec des sauts de 10 pourcent
	for percent in range( percentMin, percentMax + 10, 10 ):
		## Si la taille du fichier est inferieur au pourcentage de la taille du fichier original, on calcule la nouvelle
		## valeur de la barre de progression comprise entre 0,00 et 1
		if( newSize <= self.ptMountSize * percent / 100 ):
			self.Debug( 7, "<" + str( percent ) )
			newVal = round( float( newSize / float( self.ptMountSize * percent / 100 ) ), 2 )
			break
		## Si toutefois on depasse le pourcentage maximum, la valeur restera a 1 (soit 100%)
		elif( percent > percentMax ):
			newVal = 1

	## Au depart, pas d'idees sur le temps restant, il vient au fur et a mesure
	timeToPrint = ""
	if( newVal >= 0.01 ):
		## Recuperation de l'affichage du temps estime restant, total et du temps passe
		timeToPrint = self.GetTimeDelay( newVal )

	## Remise sous la forme 100%, soit un entier compris entre 0 et 100
	newVal = int( 100 * newVal )
	## Presentation avec le texte, le pourcentage et le temps a afficher
	text = '%s : %3d %% - %8s' % ( text, newVal, timeToPrint )
	## Taille de la barre en mode texte
	try:
		barSize = struct.unpack( "HH", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, struct.pack( "HH", 0, 0 ) ) )[ 1 ] - len( text ) - 5
	except:
		barSize = 120

	if( self.noGui == False ):
		## Ajustement de la taille de la progress barre à 120 caracteres avec centrage du texte
		textToPrint = text.center( self.progressionBarSize )
		## Affichage de la barre de progression (la valeur doit etre inferieure a 1)
		self.progressionBar.set_fraction( round( float( newVal ) / 100, 2 ) )
		## Affichage du texte sur la barre de progression
		self.progressionBar.set_text( textToPrint )

	## Pour l'affichage en mode texte, calcul de la valeur par rapport a la taille de la barre en mode texte
	newVal = newVal * barSize / 100
	## Affichage de la barre de progression
        out = '\r [%s%s] %s' % ( '=' * newVal, ' ' * ( barSize - newVal ), text )
        sys.stdout.write( out )
	sys.stdout.flush()

	## Pour continuer la barre de progression, il faut renvoyer la valeur True
	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction pour quitter l'application
    def Delete( self, widget, event = None ):

	## Afin de ne pas quitter sauvagement les processus en cours de sauvegarde ou de restauration, on ne quitte que si
	##     le processus est termine, il faut donc revenir, d'ou l'enregistrement de self.quit pour revenir a la fin du processus
	self.quit = True

	## Supression de la mise a jour automatique du combo de la liste des points de montage
	if( self.tempoCombo != None ):
		gobject.source_remove( self.tempoCombo )

	## On ne quitte que si le sous-processus est fini
	if( self.tempo != None ):
		self.Debug( 1, _( "En attente de fin de sous-processus" ) )
		return False

	## Fermeture du fichier de log, si ce n'est pas stdout
	if( self.logFile != sys.stdout ):
		self.logFile.close()

	## Si l'on est pas en mode script, fermeture de gtk
	if not( self.noGui ):
		gtk.main_quit()
	## Sinon, sortie par le mode sys
	else:
		sys.exit( 0 )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de creation et d'affichage d'un onglet
    def CreateCustomTab( self, text, notebook, frame ):

	##On crée une eventbox
        eventBox = gtk.EventBox()
	##On crée une boite horizontale
        tabBox = gtk.HBox( False, 2 )
	##On crée un label "text" (text donné en attribut)
        tabLabel = gtk.Label( text )
                
        eventBox.show()
        tabLabel.show()
	##On attache tablabel
        tabBox.pack_start( tabLabel, False )       

        tabBox.show_all()
	##On ajoute la boite à l'eventbox
        eventBox.add( tabBox )

        return eventBox


    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction d'affichage d'un popup
    def Popup( self, text ):

	## Creation d'un popup
	dialog = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, text )
	## Affichage du popup
	dialog.run()
	## Suppression du popup
	dialog.destroy()

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction d'affichage et de mise a jour du combo des points de montage
    def MakeCombo( self ):

	## Recuperation des points de montage potentiels
	self.GetPtMounts()

	## Creation du combo s'il n'existe pas
	if( self.ptCombo == None ):
		self.ptCombo = gtk.combo_box_new_text()
		## Affichage d'une ligne vide, afin de forcer le choix s'il n'a pas ete fait auparavant
		self.ptCombo.append_text( '' )

	## Recuperation des donnees du combo
	combo = self.ptCombo.get_model()

	## --------- Premiere etape, ajout des points de montage inexistants ---------

	## Pour chaque point de montage
	for ptMountSize, ptMount in self.ptMounts:
		## Par defaut on a pas trouve
		found = False
		## Pour chaque element du combo (on commence a 1 puisqu'on a un element vide)
		for i in range( 1, len( combo ), 1 ):
			## Si l'on trouve le point de montage, on arrete le parcours
			if( ptMount == combo[ i ][ 0 ] ):
				found = True
				break
		## Si l'on est arrive au bout du combo, on a pas trouve le point de montage
		if( found == False ):
			## On ajoute le point de montage
			self.ptCombo.append_text( str( ptMount ) )
			if( ptMount == self.ptMount ):
				## Si le point de montage est enregistre, on selectionne ce point de montage dans le combo
				self.ptCombo.set_active( len( combo ) - 1 )

	## --------- Deuxieme etape, supression des points de montage n'existant plus ---------
	## Pour chaque element du combo (on commence a 1 puisqu'on a un element vide)
	for i in range( 1, len( combo ), 1 ):
		## Par defaut, on a pas trouve l'element
		found = False
		## Pour chaque point de montage
		for ptMountSize, ptMount in self.ptMounts:
			## Si on trouve le point de montage
			if( ptMount == combo[ i ][ 0 ] ):
				found = True
		## Si le point de montage n'a pas ete trouve, on le supprime
		if( found == False ):
			self.ptCombo.remove_text( i )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de mise a jour de la variable associee a chaque case a cocher pour l'affichage des temps restant, total, passe
    def UpdateConfigTime( self, widget ):

	## Recuperation du nom de la case a cocher
	name = widget.get_name()
	## Modification de la variable associee (meme nom)
	setattr( self, name, widget.get_active())

	return True

    ##------------------------------------------ DEFINITION DES FONCTIONS D'AFFICHAGE ----------------------------------------
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de creation de la frame des options
    def FrameOption( self, notebook ):

	##--------------------------------------
	## Onglet OPTIONS
	##--------------------------------------
        frame = gtk.Frame( _( "Options" ) )
        frame.set_border_width( 10 )
        frame.show()
	
	##On crée une boite horizontale
        tabBox = gtk.VBox( False, 2) 	
        frame.add( tabBox )
        tabBox.show()

        label = gtk.Label( _( '''Indiquez le point de montage de votre TomTom :
(généralement /media/INTERNAL ou /media/disk)''' ) )
	label.set_justify( gtk.JUSTIFY_CENTER )
        tabBox.pack_start( label, True, False, 2 )
	
	## bouton parcourir
##        p = gtk.Button( _( "Sélectionner le point de montage du TomTom..." ) )
##	tabBox.pack_start( p, True, False, 2 )
##        p.connect( "clicked", self.parcourir_gps )

	## Liste des points de montage possibles
	self.MakeCombo()
	tabBox.pack_start( self.ptCombo, True, False, 0 )
	## Lancement de la mise a jour automatiquement toutes les 2 secondes
	self.tempoCombo = gobject.timeout_add( 2000, self.MakeCombo )
		
	## separator
        hs = gtk.HSeparator()
        tabBox.pack_start( hs, False, False, 2 )

	## Liste des modeles
	self.modeleCombo = gtk.combo_box_new_text()
	i = 0
	for text in self.models:
		self.modeleCombo.append_text( str( text ) )
		if( text == self.model ):
			self.modeleCombo.set_active( i )
		i += 1
        ##self.modeleCombo.connect( 'changed', self.OnUpdate ) 
	tabBox.pack_start( self.modeleCombo, True, False, 0 )
	
        hs = gtk.HSeparator()
        tabBox.pack_start( hs, False, False, 2 )

	label = gtk.Label( _( "Pendant la sauvegarde ou la restauration, afficher :" ) )
	label.set_justify( gtk.JUSTIFY_CENTER )
        tabBox.pack_start( label, True, False, 2 )

	## Case a cocher pour l'affichage du temps passe dans la barre de progression
	button = gtk.CheckButton( _( "le temps passé" ), False )
	button.set_name( "configTimePassed" )
	button.connect( "clicked", self.UpdateConfigTime )
	if( self.configTimePassed == True ):
		button.set_active( True )
	tabBox.pack_start( button, True, False, 0 )

	## Case a cocher pour l'affichage du temps estime restant dans la barre de progression
	button = gtk.CheckButton( _( "le temps restant" ), False )
	button.set_name( "configTimeRemind" )
	button.connect( "clicked", self.UpdateConfigTime )
	if( self.configTimeRemind == True ):
		button.set_active( True )
	tabBox.pack_start( button, True, False, 0 )

	## Case a cocher pour l'affichage du temps estime total dans la barre de progression
	button = gtk.CheckButton( _( "le temps total" ), False )
	button.set_name( "configTimeTot" )
	button.connect( "clicked", self.UpdateConfigTime )
	if( self.configTimeTot == True ):
		button.set_active( True )
	tabBox.pack_start( button, True, False, 0 )
	
	## separator
        hs = gtk.HSeparator()
        tabBox.pack_start( hs, True, False, 2 )
	
	button = gtk.Button( stock = gtk.STOCK_SAVE )
	tabBox.pack_start( button, True, False, 0 )

	## Connexion du signal "clicked" du GtkButton
	button.connect( "clicked", self.OnUpdate )
	
        eventBox = self.CreateCustomTab( _( "Options" ), notebook, frame )
        notebook.append_page( frame, eventBox )

	return True
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de creation de la frame du GPSFix
    def FrameGPSQuickFix( self, notebook ):

	##--------------------------------------
	## Onglet GPSQuickFix
	##--------------------------------------
        frame = gtk.Frame( _( "GPSQuickFix" ) )
        frame.set_border_width( 10 )
        frame.show()
	
	## on cree une boite pour contenir les widgets
	vbox = gtk.VBox( False, 10 )
	frame.add( vbox )
	vbox.show()
	
	## label
        label = gtk.Label( _( '''Cette mise-à-jour détermine les dernières positions connues des satellites.
Elle permet donc de trouver votre position initiale en moins de 30 secondes
et de commencer à naviguer plus rapidement... 

Assurez-vous d\'avoir correctement paramétré votre GPS dans les options.''' ) )
	## On centre le texte
	label.set_justify( gtk.JUSTIFY_CENTER )
        vbox.pack_start( label, True, False, 2 )
	
	## bouton maj quickfix
	if( self.couldGpsFix ):
		btn_csi = gtk.Button( _( "Lancer la mise-à-jour GPSQuickfix" ) )
		vbox.pack_start( btn_csi, True, False, 2 )
		## On connecte le signal "clicked" du bouton a la fonction qui lui correspond
        	btn_csi.connect( "clicked", self.GpsQuickFix )
	else:
		btn_csi = gtk.Button( _( "Impossible de lancer la mise-à-jour GPSQuickfix (cabextract absent)" ) )
		btn_csi.set_sensitive( False )
		vbox.pack_start( btn_csi, True, False, 2 )
		## On ne connecte à aucune fonction
           
        eventBox = self.CreateCustomTab( _( "GPSQuickFix" ), notebook, frame )
        notebook.append_page( frame, eventBox )

	return True
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de creation de la frame de lancement du backup et de la restauration
    def FrameBackupRestore( self, notebook ):

	##---------------------------------------------------------------------
	## Onglet SAUVEGARDE ET RESTAURATION
	##---------------------------------------------------------------------
	
	frame = gtk.Frame( _( "Sauvegarde et restauration" ) )
        frame.set_border_width( 10 )
	frame.set_name( "frameSaveRestore" )
        frame.show()
	
	## on crée une boite pour contenir les widgets
	vbox = gtk.VBox( False, 10 )
	vbox.set_name( "boxSaveRestore" )
	frame.add( vbox )
	vbox.show()

	## Text pour le choix du fichier de sauvegarde
        label = gtk.Label( _( "Fichier de sauvegarde:" ) )
	label.set_justify( gtk.JUSTIFY_CENTER )
        vbox.pack_start( label, True, False, 2 )
	
	## Liste des fichiers de sauvegarde existant et un nouveau
	self.saveFileCombo = gtk.combo_box_new_text()
	## recuperation du nom d'un fichier
	file = self.GetNewFileName()
	## Si le fichier existe, recuperation d'un nom presque certainement inexistant
	if( os.path.exists( file ) ):
		file = self.GetNewFileName( True )

	## Creation d'un combo contenant la liste des fichiers de sauvegarde
	## Ajout du nom de fichier nouveau (si l'on veut en creer un nouveau)
	self.saveFileCombo.append_text( file )
	## Ajout d'une ligne vide
	self.saveFileCombo.append_text( "" )

	## Si le nom du fichier a ete fourni, ajout du nom du fichier, et selection du fichier dans le combo
	if( self.fileName != False ):
		self.saveFileCombo.append_text( os.path.realpath( self.fileName ) )
		self.saveFileCombo.set_active( 2 )
	## Sinon selection du nouveau fichier
	else:
		self.saveFileCombo.set_active( 0 )

	## Ajout de tous les anciens fichiers de sauvegarde
	## Ouverture du dossier de sauvegarde
	files = os.listdir( self.dir )
	## Pour chaque fichier
	for file in files:
		## Recuperation de l'extension du fichier pour savoir s'il s'agit d'une sauvegarde
		f, extension = os.path.splitext( file )
		## Ajout du fichier de sauvegarde, s'il s'agit d'une sauvegarde, et qu'il ne s'agit pas du fichier fourni en option
		if( extension == ".tar" and ( self.fileName == False or os.path.realpath( self.dir + "/" + file ) != os.path.realpath( self.fileName ) ) ):
			self.saveFileCombo.append_text( self.dir + "/" + file )

	vbox.pack_start( self.saveFileCombo, True, False, 0 )

	## Mise en place de la barre de progression
	self.progressionBar = gtk.ProgressBar()

	## Affichage du texte dans la barre de progression pour avoir une taille precise de la barre
	text = "";
	self.progressionBar.set_text( text.center( self.progressionBarSize ) )
	align = gtk.Alignment( 0.5, 0.5, 0, 0 )
	vbox.pack_start( align, False, False, 10 )
	align.show()
	align.add( self.progressionBar )
	self.progressionBar.show()

	## Affichage d'information de la duree
        label = gtk.Label( _( '''Pour effectuer ces opérations, ''' ) + App + _( ''' prend du temps et de l'espace. 
Pour info, 25 minutes et 1GB sur le disque dur pour un One Series 30''' ) )
	label.set_justify( gtk.JUSTIFY_CENTER )
        vbox.pack_start( label, True, False, 2 )
	
	## separator
        hs = gtk.HSeparator()
        vbox.pack_start( hs, True, False, 2 )
	
	## bouton sauvegarde
	## Si la commande tar n'existe pas, la sauvegarde ne peut etre lancee, l'affichage change et le bouton ne peut
	##     etre clique
	if( self.couldBackup ):
		btnSave = gtk.Button( _( "Lancer la sauvegarde..." ) )
		btnSave.props.name = "btnSave"
		vbox.pack_start( btnSave, True, False, 2 )
		## On connecte le signal "clicked" du bouton a la fonction qui lui correspond
        	btnSave.connect( "clicked", self.BackupRestoreGPS, "backup" )
	else:
		btnSave = gtk.Button( _( "Impossible de lancer la sauvegarde... (tar absent)" ) )
		btnSave.set_sensitive( False )
		btnSave.props.name = "btnSave"
		vbox.pack_start( btnSave, True, False, 2 )
		## On connecte le signal "clicked" du bouton a rien
		
	## separator
        hs = gtk.HSeparator()
        vbox.pack_start( hs, True, False, 2 )
	
	## bouton RESTAURATION
	## Si la commande tar n'existe pas, la sauvegarde ne peut etre lancee, l'affichage change et le bouton ne peut
	##     etre clique
	if( self.couldBackup ):
		btnRestore = gtk.Button( _( "Lancer la restauration..." ) )
		btnRestore.set_name( "btnRestore" )
		vbox.pack_start( btnRestore, True, False, 2 )
		## On connecte le signal "clicked" du bouton a la fonction qui lui correspond
        	btnRestore.connect( "clicked", self.BackupRestoreGPS, "restore" )
	else:
		btnRestore = gtk.Button( _( "Impossible de lancer la restauration... (tar absent)" ) )
		btnRestore.set_sensitive( False )
		btnRestore.set_name( "btnRestore" )
		vbox.pack_start( btnRestore, True, False, 2 )
		## On connecte le signal "clicked" du bouton a rien
	
	label = gtk.Label( _( '''N\'utilisez la restauration qu\'en cas d\'absolue nécessité !''' ) )
	label.set_justify( gtk.JUSTIFY_CENTER )
	vbox.pack_start( label, True, False, 2 )

	## Creation et affichage de la frame
        eventBox = self.CreateCustomTab( _( "Sauvegarde et Restauration" ), notebook, frame )
        notebook.append_page( frame, eventBox )

	return True
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de creation de la frame PERSONNALISER
    def FrameBonus( self, notebook ):

	##--------------------------------------
	## Onglet PERSONNALISER
	##--------------------------------------
        frame = gtk.Frame( _( "Personnaliser son GPS" ) )
        frame.set_border_width( 10 )
        frame.show()
	##On crée une boite horizontale
        tabBox = gtk.VBox( False, 2 )
        frame.add( tabBox )
        tabBox.show()
	
	## label
        label = gtk.Label( _( "Remplacez l\'écran de démarrage de votre GPS par la photo de votre choix" ) )
       	tabBox.pack_start( label, True, False, 2 )
	##TODO verifier presence ImageMagick
	## subprocess.call( [ "convert image.jpg -resize 320x240 -background black -gravity center -extent 320x240 splash.bmp" ], shell = True )
	## bouton 
        b = gtk.Button( _( "texte bouton" ) )
	tabBox.pack_start( b, True, False, 2 )
        b.connect( "clicked", self.Delete )

        eventBox = self.CreateCustomTab( _( "Personnaliser" ), notebook, frame )
	
	notebook.append_page( frame, eventBox )
	

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de creation de la frame a propos
    def FrameAbout( self, notebook ):

	##--------------------------------------
	## Onglet A PROPOS
	##--------------------------------------
        frame = gtk.Frame( _( "A propos" ) )
        frame.set_border_width( 10 )
        frame.show()
	
	##On crée une boite horizontale
        tabBox = gtk.VBox( False, 2 )	
        frame.add( tabBox )
        tabBox.show()
		
	## image	
	image = gtk.Image()
	image.set_from_file( self.dirPix + "pytomtom.png" )
	tabBox.pack_start( image, True, False, 2 )
	
	##On crée un label "text" (text donné en attribut)
        tabLabel = gtk.Label( _( '''version ''' ) + Ver + _( '''
	
	http://tomonweb.2kool4u.net/pytomtom/
	''' ) )
	tabLabel.set_justify( gtk.JUSTIFY_CENTER )
	tabLabel.show()
	##On attache label dans la boite
        tabBox.pack_start( tabLabel, True, False, 2 )
	
        eventBox = self.CreateCustomTab( _( "A propos" ), notebook, frame )
        notebook.append_page( frame, eventBox )

	return True
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de creation de la frame quit
    def FrameQuit( self, notebook ):

	##--------------------------------------
	## Onglet QUITTER
	##--------------------------------------
        frame = gtk.Frame( _( "Quitter ?" ) )
        frame.set_border_width( 10 )
        frame.show()
	
	##On crée une boite horizontale
        tabBox = gtk.VBox( False, 2 )	
        frame.add( tabBox )
        tabBox.show()
	
	## label
        label = gtk.Label( _( "N\'oubliez pas d\'éjecter proprement votre TomTom !" ) )
       	label.show()
	tabBox.pack_start( label, True, False, 2 )
	
	## bouton quitter
        b = gtk.Button( stock = gtk.STOCK_QUIT )
	b.show()
	tabBox.pack_start( b, True, False, 2 )
        b.connect( "clicked", self.Delete )
	
        eventBox = self.CreateCustomTab( _( "Quitter" ), notebook, frame )
        notebook.append_page( frame, eventBox )

	return True

    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## fonction parcourir pour selectionner un dossier / conservation en cas de besoin def parcourir_gps( self,entry ):
    def selectFolder( self,entry ):
	
	self.window = gtk.FileChooserDialog( _( "Ouvrir..." ), gtk.Window( gtk.WINDOW_TOPLEVEL ),
		gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK ) );

	if( self.window.run() == gtk.RESPONSE_OK ):
		dossier = self.window.get_filename()
		self.Debug( 5, dossier )
		self.labelfolder.set_text( dossier )
		self.window.destroy()

	return True
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## fonction parcourir pour selectionner un fichier
    def selectFile( self,entry ):
	
	self.window = gtk.FileChooserDialog( _( "Ouvrir..." ), gtk.Window(gtk.WINDOW_TOPLEVEL), 
		gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK));

	if( self.window.run() == gtk.RESPONSE_OK ):
		file = self.window.get_filename()
		self.Debug( 5, file )
		self.labelfile.set_text( file )
		self.window.destroy()
		
	return True
	
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Fonction de demarrage de la classe
    def __init__( self ):

	## Definition du repertoire contenant les donnees d'internationalisation
	gettext.bindtextdomain( App, '.' )
	## Recuperation de la configuration
	self.GetConfig()

	## Si on est pas en mode script
	if( self.noGui == False ):
		##On cree la fenetre principale
        	self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
		## En cas de fermeture de la fenetre, on appel la fonction Delete
        	self.window.connect( "delete_event", self.Delete )
        	self.window.set_border_width( 10 )
		self.window.set_title( App )
		## centrage de la fenetre 
		self.window.set_position( gtk.WIN_POS_CENTER )
		##*************************************************************************************************************
        	##On cree un nouveau notebook
        	notebook = gtk.Notebook()
		notebook.set_name( "notebook" )
        	self.window.add( notebook )
        	notebook.show()
		##*************************************************************************************************************
		## Construction des onglets de la fenetre principale
		self.FrameOption( notebook )
		self.FrameGPSQuickFix( notebook )
		self.FrameBackupRestore( notebook )
		##TODO decommenter la ligne suivante pour affichage
		##self.FrameBonus( notebook )
		self.FrameAbout( notebook )
		self.FrameQuit( notebook )
		##*************************************************************************************************************
		## Onglet que nous verrons à l'ouverture
        	notebook.set_current_page( self.boxInit )
		## Affichage de l'ensemble
        	self.window.show_all()

	## Lancement des actions

	## Si l'option a ete fournie, lancement de la sauvegarde de la configuration
	if( self.doSave ):
		self.PutConfig()

	## Si l'option a ete fournie, lancement du GpsFix
	if( self.doGpsFix ):
		self.Debug( 1, _( "Lancement de GpsQuickFix" ) )
		self.GpsQuickFix( None )

	## Si l'option a ete fournie, lancement du Backup
	if( self.doBackup ):
		self.Debug( 1, _( "Lancement de la Sauvegarde" ) )
		self.BackupRestoreGPS( None, "backup" )

	## Si l'option a ete fournie, lancement de la restauration
	if( self.doRestore ):
		self.Debug( 1, _( "Lancement de la Restauration" ) )

	## Si on est en mode script, fermeture de l'application
	if( self.noGui == True ):
		self.Delete( None )
		return None

	return None


#----------------------------------------------- DEFINITION DES FONCTIONS GLOBALES -------------------------------------------
def main():
    gtk.main()
    return 0

#----------------------------------------------- LANCEMENT DE L'APPLICATION --------------------------------------------------
if __name__ == "__main__":
    NotebookTomtom()
    main()
