#!/usr/bin/env python

from distutils.core import setup
from blogpingr.blogpingr import __version__
setup(
        name            = 'blogpingr',
        version         = __version__,
        description     = 'pinger for xml-rpc updating services',
        author          = 'PoisoneR',
        author_email    = 'poisonertmp@gmail.com',
        url             = '',
        packages        = ['blogpingr'],
        scripts         = ['bin/blogpingr'],
        license         = 'GPL',
	data_files	= [('/etc', ['blogpingr.conf'])]
        )

