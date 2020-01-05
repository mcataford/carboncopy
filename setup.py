import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    entry_points={"console_scripts": ["carboncopy = src.carboncopy.main:run"]},
    name="carboncopy",
    version="0.0.1",
    author="Marc Cataford",
    author_email="c.marcandre@gmail.com",
    description="A small CLI utility to keep your repositories up-to-date with their templates",
    long_description=long_description,
    url="",
    packages=setuptools.find_packages(),
    classifiers=[],
    install_requires=["requests>=2.22.0"],
    python_requires=">=3.6",
)
