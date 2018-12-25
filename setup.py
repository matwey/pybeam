from setuptools import setup
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

name="pybeam"
version="0.4.1"

setup(name=name,
	version=version,
	description='Python module to parse Erlang BEAM files',
	url='http://github.com/matwey/pybeam',
	author='Matwey V. Kornilov',
	author_email='matwey.kornilov@gmail.com',
	license='MIT',
	packages=['pybeam'],
	test_suite='test',
	install_requires=['construct>=2.8,<2.9', 'six'],
	command_options={
		'build_sphinx': {
			'project': ('setup.py', name),
			'version': ('setup.py', version),
			'release': ('setup.py', version),
			'source_dir': ('setup.py', 'doc')
		}
	},
	zip_safe=False)
