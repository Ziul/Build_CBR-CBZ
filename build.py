#!/usr/bin/python
#  -*- coding: utf-8 -*-

''' Will run de default rotine and build a <path>.cbr and/ou a <path>.cbr on the directory.
	By default will search for *.jpg or *.png on this directory.
	The user can parse a list of files/directories.'''

__author__ = "Luiz Fernando Gomes de Oliveira"
__version__ = '0.8'
__license__ = 'MIT'

from multiprocessing import Process
from os import  environ, path, pathsep,walk
from subprocess import call, PIPE, STDOUT
from distutils import spawn
from glob import glob
from sys import argv
from warnings import warn

import optparse
_parser = optparse.OptionParser(
		usage = "python %prog [[options] [-o output file] [local of files]]",
		description = "Build a CBR/CBZ file with selected files",
		version = __version__
		)
#quiet options
_parser.add_option("-q", "--quiet",
	dest = "verbose",
	action = "store_false",
	help = "suppress non error messages",
	default = True
)
#output options
_parser.add_option("-o", "--output",
	dest = "output",
	action = "store",
	help = "force a name to output file. \
Default is the name of this directory [%s]"%(path.realpath('.').split('/')[-1]),
	default = path.realpath('.').split('/')[-1]
)
#Choose type of output
_parser.add_option("-t", "--type",
	dest = "extension",
	action = "store",
	help = "Choose between CBR or CBZ. By default will create both outputs.",
	default = 'both'
)
#get parser
(_options, args) = _parser.parse_args()
_options.extension = _options.extension.lower()

def make_cbr(output, files = '*.jpg *.JPG *.png *.PNG'):
	''' Make a <output>.cbr file in this directory with all *.jpg and *.png files'''
	rename_file_on_dir()
	call (['rm %s.cbr -f'%(output)],shell=True)
	if files[-1] == '*':
		files = files[:-1]
	if files[-1] == '/':
		files += '*'
	if _options.verbose:
		print '\n$ rar a -v -m0 -mt5 %s.cbr %s'%(output,files)
		call( ['rar a -v -m0 -mt5 %s.cbr %s'%(output,files)], shell=True,stdout=None)
	else:
		call( ['rar a -v -m0 -mt5 %s.cbr %s'%(output,files)], shell=True,stdout=PIPE)


def make_cbz(output, files = '*.jpg *.JPG *.png *.PNG'):
	''' Make a <output>.cbz file in this directory with all *.jpg and *.png files'''
	rename_file_on_dir()
	if files[-1] == '/':
		files = files[:-1]
	call (['rm %s.cbz -f'%(output)],shell=True)
	if _options.verbose:
		print '\n$ 7z a %s.zip %s'%(output,files)
		call( ['7z a %s.zip %s'%(output,files)], shell=True,stdout=None)
		call( ['mv %s.zip %s.cbz -vf'%(output,output)], shell=True)
	else:
		call( ['7z a %s.zip %s'%(output,files)], shell=True,stdout=PIPE)
		call( ['mv %s.zip %s.cbz -f'%(output,output)], shell=True)


def rename_file_on_dir():
	'''CBR/CBZ files have some problens on sorting the files when the name is just
	the number. a way to sove this problem is puting the numbers with the exactly 
	decimal.
	ex:
		['1.jpg', '23.jpg'] ----> ['0001.jpg','0023.jpg']
	With this the CBR/CBZ will sorte the files correctly'''
	if _options.verbose:
		print "Checking needs for rename files:"
	from shutil import move,copy
	for root, dirs, files in walk(argv[1]):
		for f in files:
			try:
				if root[-1] == '/':
					root = root[:-1]
				if _options.verbose:
					print root + "/%s -> %s/%04.0f.%s"%( f , root,int(f.split('.')[0]) ,f.split('.')[1])
				move(root + '/' + f, root + '/' +"%04.0f.%s"%(int(f.split('.')[0]) ,f.split('.')[1]) )
			except ValueError:
				print "%s/%s"%(root,f) + '\t\t=> ready to cbr file'.ljust(30)
			except Exception, e:
				raise e


def _main():
	''' Will run de default rotine and build a <path>.cbr and/ou a <path>.cbr on the directory.
	By default will search for *.jpg or *.png on this directory.
	The user can parse a list of files/directories.'''
	#check if rar is instaled
	if spawn.find_executable("rar") == None:
		print "The program 'rar' is currently not installed.  You can install it by typing:\n\tsudo apt-get install rar"
		return False
	#check if 7z is instaled
	if spawn.find_executable("7z") == None:
		print "The program '7z' is currently not installed.  You can install it by typing:\n\tsudo apt-get install 7z"
		return False

	if len(args)==[]:
		# No list of files...get them all
		files = glob('*.jpg') # look for *.jpg here
		files.extend(glob('*.png')) # look for *.png here
	else:
		#A directory of files
		if len(args)>1:
			warn("You are not passing a directory, but a list of files.", Warning)
			# Warning: Sometimes raise some syntax problems
			files = args
		else:
			files = args
		#print files
	if files:
		files = sorted(files )	#order them
		#print files
		files = ' '.join(files) #formating string with files
		if _options.extension == 'cbz':
			make_cbz(_options.output,files)
		elif _options.extension == 'cbr':
			make_cbr(_options.output,files)
		elif _options.extension != 'both':
			warn("You have passed a not supported extension.", Warning)			
		else:
			make_cbz(_options.output,files)
			make_cbr(_options.output,files)
	else:
		print "Put some *.jpg or *.png on " + path.realpath('.')


if __name__ == '__main__':
	_main()

