from setuptools import setup, find_packages

setup(
    name='ArucoCam',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'glob2',
    ],
)
