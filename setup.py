from setuptools import setup


setup(
    name='jobappmgr',
    version='0.1.0',
    packages=['jobappmgr'],
    entry_points={
        'console_scripts': [
            'jobappmgr = jobappmgr.cli:cli'
        ]
    },
    install_requires=[
        'click',
        'pyyaml',
        'python-docx'
    ]
)