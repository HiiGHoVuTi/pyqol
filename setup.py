import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqol",
    version="0.1.1.0",
    author="Maxime",
    author_email="emixampons@gmail.com",
    description="A Pack of useful python QoL changes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://maxime.codes/Libraries/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    install_requires=[
        "fastcore"
    ]
)
