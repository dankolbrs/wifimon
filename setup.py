from setuptools import setup

setup(
    name='wifimon',
    version='0.0.1',
    description='Script to report available WAP strengths and qualities',
    author='Dan Kolb',
    author_email='dan@dankolb.net',
    packages=['wifimon'],
    url='https://github.com/dankolbrs/wifimon.git',
    install_requires=open('requirements.txt').read(),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Operating System :: POSIX',
            'Programming Language :: Python'
        ],
    entry_points={
        'console_scripts': [
            'wifimon = wifimon.scanwifi:main'
        ]
    }
)
