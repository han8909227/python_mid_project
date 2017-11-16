import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid >= 1.9a',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    'ipython',
    'pyramid_ipython',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'psycopg2',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
    'tox',
    'nltk',
    'scrapy',
    'plotly'
]

setup(
    name='TechLurker',
    version='0.0',
    description='TechLurker',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Han Bao, Brian Wheeler, Max Wolf, Phil Werner',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = TechLurker:main',
        ],
        'console_scripts': [
            'initdb = TechLurker.scripts.initializedb:main',
        ],
    },
)
