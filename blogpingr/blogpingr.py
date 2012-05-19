#!/usr/bin/env python
#
# Copyright (C) 2007 Borislav Gizdov a.k.a. PoisoneR
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

import sys
import socket
import xmlrpclib
from optparse import OptionParser

__version__ = '0.1.0'
__author__ = 'Borislav Gizdov a.k.a. PoisoneR'
__progname__ = 'blogpingr'
__homepage__ = ''

# TODO
# install conf in /etc

class BlogPingr:
	"""Weblogs pinger"""

	def __init__(self):
		self.rpcServer = ''
		self.rpcServers = []
		self.replyError = False
		self.replyMessage = ''
		self.blogName = ''
		self.blogUrl = ''
		self.loadServers()
		socket.setdefaulttimeout(10)

	def ping(self):
		"""Ping self.rpcServer"""
		
		reply = {}
		try:
			rpc = xmlrpclib.Server(self.rpcServer)
			reply = rpc.weblogUpdates.ping(self.blogName, self.blogUrl)
			self.replyError = reply['flerror']
			self.replyMessage = reply['message']
		
		except socket.error, msg:
			self.replyError = True
			self.replyMessage = 'Socket error'#msg[1]
		
		except xmlrpclib.ProtocolError, inst:
			self.replyError = True
			self.replyMessage = 'Protocol error: %s : %s : %s' % (inst.errcode, inst.errmsg, inst.url)
		except xmlrpclib.Fault, inst:
			self.replyError = True
			self.replyMessage = inst.faultString
		
		except:
			self.replyError = True
			self.replyMessage = 'Unknown error occured'
	
	def loadServers(self):
		"""Load list with all rpc servers"""
		
		fp = open('/etc/blogpingr.conf')
		self.rpcServers = fp.readlines()
		fp.close()
	
	def pingAll(self):
		"""Ping all loaded rpc servers"""
		
		for server in self.rpcServers:
			self.setRpcServer(server.strip())
			self.ping()
			self.replyInfo()

	def setRpcServer(self, rpcServer):
		self.rpcServer = rpcServer

	def getReplyError(self):
		return self.replyError

	def printPingInfo(self):
		"""Print what we will ping"""
		
		print '* Pinging %s %s' % (self.blogName, self.blogUrl)

	def replyInfo(self):
		"""Print replay info from last ping"""
		
		if (self.getReplyError()):
			print '* Ping Fail:', self.rpcServer.strip()
		else:
			print '* Ping OK:', self.rpcServer.strip()

		print '\t' + self.replyMessage

	def setBlogName(self, blogName):
		self.blogName = blogName

	def setBlogUrl(self, blogUrl):
		self.blogUrl = blogUrl

	def usage(self):
		"""Usage"""
		
		usage = '\n\t%prog [options] <BlogUrl> <BlogName>\n\n'
		usage += 'example:\n\t%prog http://www.myblog.bg/ "My Blog"\n'
		usage += '\t%prog -c http://rpc.service.com/ http://www.myblog.bg/ "My Blog"'
		return usage

	def ver(self, option, opt_str, value, parser):
		"""print version and exit"""
		
		print __progname__ + ' ' + __version__
		sys.exit()

	def parseOptions(self):
		"""Class method for parsing command line arguments"""
		
		usage = self.usage() 
		parser = OptionParser(usage=usage)
		parser.add_option('-v', '--version',
			help="print version",
			action='callback',
			callback=self.ver
			)

		parser.add_option('-c', '--custom',
			metavar='rpc_server',
			dest='custom',
			default=None,
			help='ping custom xml-rpc service')
		
		(options, args) = parser.parse_args()
		
		if options.custom:
			if len(args) == 2:
				self.setRpcServer(options.custom)
				self.setBlogUrl(args[0])
				self.setBlogName(args[1])
				self.printPingInfo()
				self.ping()
				self.replyInfo()
			else:
				parser.error('Invalid arguments count')
		else:
			if len(args) == 2:
				self.setBlogUrl(args[0])
				self.setBlogName(args[1])
				self.printPingInfo()
				self.pingAll()
			elif len(args) == 0:
				parser.print_help()
			else:
				parser.error('Invalid arguments count')


