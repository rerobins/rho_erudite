from distutils.core import setup

setup(
    name='erudite',
    version='1.0.0',
    packages=['erudite',
              'erudite.components',
              'erudite.components.commands',
              ],
    url='',
    license='BSD',
    author='Robert Robinson',
    author_email='rerobins@meerkatlabs.org',
    description='Erudite bot for the Rho infrastructure',
    install_requires=['rhobot==1.0.0', ]
)
