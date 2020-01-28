from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='getcontent',
    version='0.1.0',
    description='Get content from reddit top news stories',
    long_description=readme,
    author='Niall Crowley',
    author_email='',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['Cython',
                      'jinja2',
                      'pandas',
                      'pandas-datareader',
                      'pathlib',
                      'praw',
                      'newspaper3k',
                      'requests',
                      'nltk']
)
