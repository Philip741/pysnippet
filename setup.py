from setuptools import setup, find_packages

setup(
    name='pysnippet',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'prompt-toolkit',
        'pygments',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'mycommand=myproject.cli:main'
        ]
    }
)
