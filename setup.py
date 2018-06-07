from setuptools import setup

setup(
    name='XML Harvesting Agent',
    version='0.1',
    description='An agent that harvests xml metadata files into a DataCite json format',
    url='',
    author='Mike Metcalfe',
    author_email='mike@webtide.co.za',
    license='MIT',
    packages=['agent'],
    install_requires=[
        'requests',
        'cherrypy',
        'mako',
        'declxml',
    ],
    python_requires='>=3',
)
