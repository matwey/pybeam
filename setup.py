from setuptools import find_packages, setup, Command

name="pybeam"
version="0.5"
test_suite="test"

class BuildSphinx(Command):
	description = 'Build Sphinx documentation'
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		import sphinx.cmd.build as scb
		scb.build_main(['-b', 'html',
			'-D', 'project=' + name,
			'-D', 'version=' + version,
			'-D', 'release=' + version,
			'./doc', './build/html'])

setup(name=name,
	version=version,
	description='Python module to parse Erlang BEAM files',
	url='http://github.com/matwey/pybeam',
	author='Matwey V. Kornilov',
	author_email='matwey.kornilov@gmail.com',
	license='MIT',
	packages=find_packages(exclude=(test_suite,)),
	test_suite=test_suite,
	install_requires=['construct>=2.9,<2.10', 'six'],
	cmdclass = {'build_sphinx': BuildSphinx},
	zip_safe=False)
