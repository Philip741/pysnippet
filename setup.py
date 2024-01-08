from setuptools import setup, find_packages

setup(
    name='pysnip',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'prompt-toolkit',
        'pygments',
        'rich'
    ],
    package_data={
        "pysnip": ["pysnip.cfg"],  # Include the configuration file in the package
    },
    entry_points={
        'console_scripts': [
            'pysnip=pysnip.main:main',
        ]
    },
)
