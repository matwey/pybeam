from setuptools import find_packages, setup
try:
	from sphinx.setup_command import BuildDoc
	cmdclass = {'build_sphinx': BuildDoc}
except ImportError:
	pass

name="pybeam"
version="0.7"
test_suite="test"

setup(name=name,
	version=version,
	description='Python module to parse Erlang BEAM files',
	url='http://github.com/matwey/pybeam',
	author='Matwey V. Kornilov',
	author_email='matwey.kornilov@gmail.com',
	license='MIT',
	packages=find_packages(exclude=(test_suite,)),
	test_suite=test_suite,
	install_requires=['construct>=2.9,<2.11', 'six'],
	command_options={
		'build_sphinx': {
			'project': ('setup.py', name),
			'version': ('setup.py', version),
			'release': ('setup.py', version),
			'source_dir': ('setup.py', 'doc')
		}
	},
	zip_safe=False)
