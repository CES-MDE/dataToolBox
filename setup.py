from setuptools import setup, find_packages

setup(
    name='dataToolBox',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    ],
    author='Quentin Samudio',
    author_email='quentin.samudio@minesparis.psl.eu',
    description='Librairie pour manipuler des données sous formes de dataframe.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CES-MDE/dataToolBox',  # Lien vers votre repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
