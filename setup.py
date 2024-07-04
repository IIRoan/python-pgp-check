from setuptools import setup, find_packages

setup(
    name='python-pgp-check',
    version='0.1.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'python-pgp-check=pgp_check.cli:main',
        ],
    },
    author='IRoan',
    author_email='pypi@lunary.roan.zip',
    description='A CLI tool to verify file hashes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iiroan/python-pgp-check',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
