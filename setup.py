from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='recommendation-system',
    version='1.0',
    author='Zubair Farahi',
    packages=find_packages(),
    install_requires=requirements
)