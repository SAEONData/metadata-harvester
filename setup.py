from setuptools import find_packages
from setuptools import setup

setup(
    name='Metadata Harvesting Agent',
    version='0.1',
    description='An agent that harvests metadata files into a DataCite json format',
    url='',
    author='Mike Metcalfe',
    author_email='mike@webtide.co.za',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'cherrypy',
        'mako',
        'declxml',
    ],
    python_requires='>=3',
    tests="tests",
)
