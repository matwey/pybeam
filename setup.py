from setuptools import setup

setup(name='pybeam',
      version='0.3.2',
      description='Python module to parse Erlang BEAM files',
      url='http://github.com/matwey/pybeam',
      author='Matwey V. Kornilov',
      author_email='matwey.kornilov@gmail.com',
      license='MIT',
      packages=['pybeam'],
      test_suite = 'test',
      install_requires=['construct'], 
      zip_safe=False)

