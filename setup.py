from distutils.core import setup

setup(
   name='AdviserLogicAPI',
   packages=['API', 'Exceptions', 'Abstractions'],
   url='https://github.com/harryduffy/AdviserLogicAPI',
   license='MIT',
   version='1.0',
   description='API for Morningstar\'s AdviserLogic software.',
   author='Harry Duffy, Alexander Morton',
   install_requires=['pandas', 'python-dotenv', 'requests', 'setuptools', 'SharePlum']
)