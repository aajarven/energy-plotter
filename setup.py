import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="energy-plotter",
    version="0.1",
    author="Anni Järvenpää",
    author_email="anni.jarvenpaa@gmail.com",
    description="Plotting tool for energy consumption data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aajarven/energy-plotter.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib",
        "sortedcontainers",
        ],
)
