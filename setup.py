from setuptools import setup

setup(name='pybeam',
      version='0.1',
      description='Python module to parse Erlang BEAM files',
      url='http://github.com/matwey/pybeam',
      author='Matwey V. Kornilov',
      author_email='matwey.kornilov@gmail.com',
      license='MIT',
      packages=['pybeam'],
      install_requires=['construct'], 
      zip_safe=False)

