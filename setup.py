from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='nsga2',
    version='0.0.1',
    description='Nondominated Sort Genetic Algorithm 2',
    long_description=readme,
    author='Rikuo Hasegawa',
    author_email='rikuo.hase1997@gmail.com',
    install_requires=[
        'numpy',
        'deap',
        'matplotlib'],
    url='https://github.com/Spaghet/nsga2',
    license=None,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)
