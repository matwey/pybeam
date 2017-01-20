from setuptools import setup

setup(name='pybeam',
      version='0.4',
      description='Python module to parse Erlang BEAM files',
      url='http://github.com/matwey/pybeam',
      author='Matwey V. Kornilov',
      author_email='matwey.kornilov@gmail.com',
      license='MIT',
      packages=['pybeam'],
      test_suite = 'test',
      install_requires=['construct>=2.8'], 
      zip_safe=False)
