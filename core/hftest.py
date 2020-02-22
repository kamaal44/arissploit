#!/usr/bin/env python3

#            ---------------------------------------------------
#                           Arissploit Framework                                 
#            ---------------------------------------------------
#                Copyright (C) <2019-2020>  <Entynetproject>
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <http://www.gnu.org/licenses/>.

from core import colors
import traceback, sys, os
import glob
import py_compile
from core import getpath
import importlib

def check_modules():
	modules = glob.glob(getpath.modules()+"*.py")

	for module in modules:
		module = module.replace(getpath.modules(), '').replace('.py', '')
		if module != '__init__':
			modadd = importlib.import_module("modules."+module)
			check_module(modadd)

def check_module(modadd):
	print(colors.yellow+'checking',modadd.conf["name"]+colors.green)
	module = modadd.__name__.replace("modules.", "")
	if modadd.conf["name"] != module:
		print("["+colors.bold+colors.red+"err"+colors.end+"] \nmodules name doesn't match")
	modadd.conf["version"]
	if modadd.conf["shortdesc"] == 'none':
		print(colors.red+'\ndesc variable has default value'+colors.green)
		testfailed()
	if modadd.conf["github"] == 'none':
		 print(colors.red+'\ngithub variable has default value'+colors.green)
		 testfailed()
	if modadd.conf["author"] == 'none':
		print(colors.red+'\ncreatedby variable has default value'+colors.green)
		testfailed()
	if modadd.conf["email"] == 'none':
		print(colors.red+'\nemail variable has default value'+colors.green)
		testfailed()

	if modadd.conf["initdate"] == "none":
		print(colors.red+'\ninitdate variable has default value'+colors.green)
		testfailed()

	if modadd.conf["lastmod"] == "none":
		print(colors.red+'\nlastmod variable has default value'+colors.green)
		testfailed()

	try:
		if modadd.conf["dependencies"][0] == None:
			print("["+colors.bold+colors.red+"err"+colors.end+"] \ndependencies has default value")
			testfailed()
	except KeyError:
		pass

	modadd.variables.items()

	modadd.conf["apisupport"]
	modadd.changelog
	modadd.run
	try:
		modadd.customcommands
		check_customcommands(modadd)
	except AttributeError:
		pass


def check_customcommands(modadd):

	f = open(modadd.__file__, "r")
	for line in f:
		for c in modadd.customcommands:
			if c in line and "def" in line and "#" not in line and "args" not in line:
				print("["+colors.bold+colors.red+"err"+colors.end+"] custom command function doesn't have args argument"+colors.end)
				testfailed()
	f.close()


def compile_core():
	core = glob.glob(getpath.core()+"*.py")

	print(colors.green+'\ntesting core...\n'+colors.green)

	for item in core:
		print(colors.yellow+'compiling',item+colors.green)
		py_compile.compile(item)

def compile_lib():
	print(colors.green+'\ntesting libraries...\n'+colors.green)
	for file in glob.iglob(getpath.lib()+'/**/*.py', recursive=True):
		print(colors.yellow+'compiling',file+colors.green)
		py_compile.compile(file)
	
def check_cmethods():

	print(colors.green+"\ntesting cmethods...\n"+colors.end)

	fcm = open(getpath.core()+"cmethods.py", "r")

	linenum = 1

	for line in fcm:
		if "self" not in line and "def " in line or "args" not in line and "def " in line:
			if "__init__" not in line and "mcu" not in line and "#" not in line:
				print("["+colors.bold+colors.red+"err"+colors.end+"] error in line "+str(linenum)+":\n"+colors.end)
				print(colors.red+line+colors.end)
				testfailed()
		linenum += 1

def compile_api():
	print(colors.green+"compiling api...\n"+colors.end)
	py_compile.compile("api.py")

def challenge():
	try:
		print(colors.green+"\nstarting challenge"+colors.green)
		print(colors.green+"\ntesting modules\n"+colors.green)

		check_modules()
		compile_core()		
		compile_lib()
		check_cmethods()
		compile_api()

		print(colors.green+"test passed!"+colors.end)

		sys.exit(0)

	except SystemExit as e:
		sys.exit(e)

	except:
		print("["+colors.bold+colors.red+"err"+colors.end+"] \ntest not passed!\n")
		traceback.print_exc()
		print(colors.end)
		sys.exit(1)

def testfailed():
	print("["+colors.bold+colors.red+"err"+colors.end+"] \ntest not passed!\n"+colors.end)
	sys.exit(1)
