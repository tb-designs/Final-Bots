from setuptools import find_packages, setup

setup(
    name='finalbots',
    version='1.0.0',
    author="Ryan Blais"
    author_email="ryanblais@uvic.ca"
    description="Package for Final Bots game"
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)