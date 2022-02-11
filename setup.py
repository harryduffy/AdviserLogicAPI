from distutils.core import setup

setup(
   name='AdviserLogicAPI',
   packages=['AdviserLogicAPI', 'Exceptions'],
   url='https://github.com/harryduffy/AdviserLogicAPI',
   license='',
   version='1.0',
   description='API for Morningstar\'s AdviserLogic software.',
   author='Harry Duffy, Alexander Morton',
   install_requires=['pandas', 'python-dotenv', 'requests', 'setuptools', 'SharePlum']
)