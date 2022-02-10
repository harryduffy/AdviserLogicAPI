from distutils.core import setup

setup(
   name='AdviserLogicAPI',
   package_dir = {'': 'AdviserLogicAPI'},
   packages=['AdviserLogicAPI'],
   url='https://github.com/harryduffy/AdviserLogicAPI',
   license='',
   version='1.0',
   description='API for Morningstar\'s AdviserLogic software.',
   author='Harry Duffy, Alexander Morton',
   install_requires=['pandas', 'python-dotenv', 'requests', 'setuptools', 'SharePlum']
)