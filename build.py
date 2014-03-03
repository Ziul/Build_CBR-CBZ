#!/usr/bin/python
#  -*- coding: utf-8 -*-

""" This routine will make a CBR file with the same name 
of the directory where is called with all the *.jpg and *.png files on it. """

__author__ = "Luiz Fernando Gomes de Oliveira"
__version__ = '0.7'
__license__ = 'MIT'

from multiprocessing import Process
from os import  environ, path, pathsep,walk
from subprocess import call, PIPE, STDOUT
from distutils import spawn
from glob import glob
from sys import argv

import optparse
_parser = optparse.OptionParser(
		usage = "python %prog [[options] [-o output file] [local of files]]",
		description = "Build a CBR/CBZ file with selected files",
		version = __version__
		)
_parser.add_option("-q", "--quiet",
	dest = "verbose",
	action = "store_false",
	help = "suppress non error messages",
	default = True
)

_parser.add_option("-o", "--output",
	dest = "output",
	action = "store",
	help = "force a name to output file. \
Default is the name of this directory [%s]"%(path.realpath('.').split('/')[-1]),
	default = path.realpath('.').split('/')[-1]
)


(_options, args) = _parser.parse_args()
#print args

def make_cbr(output, files = '*.jpg *.JPG *.png *.PNG'):
	''' Make a <output>.cbr file in this directory with all *.jpg and *.png files'''
	call (['rm %s.cbr -f'%(output)],shell=True)
	if files[-1] == '*':
		files = files[:-1]
	if _options.verbose:
		print 'rar a -v -m0 -mt5 %s.cbr %s'%(output,files)
		call( ['rar a -v -m0 -mt5 %s.cbr %s'%(output,files)], shell=True,stdout=None)
	else:
		call( ['rar a -v -m0 -mt5 %s.cbr %s'%(output,files)], shell=True,stdout=PIPE)
	

def make_cbz(output, files = '*.jpg *.JPG *.png *.PNG'):
	''' Make a <output>.cbr file in this directory with all *.jpg and *.png files'''
	if files[-1] == '/':
		files = files[:-1]
	call (['rm %s.cbz -f'%(output)],shell=True)
	if _options.verbose:
		print '7z a %s.zip %s'%(output,files)
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


def main():
	''' Will run de default rotine and build a <path>.cbr on the directory with 
		all the *.jpg or *.png files in this directory'''
	#if not  is_tool('rar'):
	if spawn.find_executable("rar") == None:
		print "The program 'rar' is currently not installed.  You can install it by typing:\n\tsudo apt-get install rar"
		return False

	if len(args)==[]:
		# No list of files...get them all
		files = glob('*.jpg') # look for *.jpg here
		files.extend(glob('*.png')) # look for *.png here
	else:
		#A directory of files
		if len(args)>1:
			print "You are not passing a directory, but a list of files"
			files = args
		else:
			files = args
			rename_file_on_dir()
		#print files
	if files:
		#files = sorted(files, key=lambda x: int(x.split('.')[0])  )	#order them
		files = sorted(files )	#order them
		#print files
		files = ' '.join(files) #formating string with files
		make_cbz(_options.output,files)
		make_cbr(_options.output,files)
	else:
		print "Put some *.jpg or *.png on " + path.realpath('.')


if __name__ == '__main__':
	main()

