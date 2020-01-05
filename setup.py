import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    entry_points={"console_scripts": ["carboncopy = src.carboncopy.main:run"]},
    name="carboncopy",
    version="0.0.1",
    license="MIT",
    author="Marc Cataford",
    author_email="c.marcandre@gmail.com",
    description="A small CLI utility to keep your repositories up-to-date with their templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/carboncopy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    install_requires=["requests>=2.22.0", "inquirer==2.6.3"],
    python_requires=">=3.6",
    project_urls={
        "Source": "https://github.com/mcataford/carboncopy",
        "Bug Reports": "https://github.com/mcataford/carboncopy/issues",
    },
)
