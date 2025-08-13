import setuptools

with open("README.md", "r", errors="replace") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libgen_api_refhub",
    packages=["libgen_api_refhub"],
    version="1.0.0.2",
    description="Search Library genesis by Title or Author",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Merkousha/libgen-api-refhub",
    author="Massoud Beygi",
    author_email="merkousha.net@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
    ],
    keywords=["libgen search", "libgen api", "search libgen", "search library genesis"],
    install_requires=["bs4", "requests", "lxml"],
    python_requires=">=3.7",
)
