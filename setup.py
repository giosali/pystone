import os
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

requirements = ["requests", "playsound"]

main = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(main, "pystone", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    license=about["__license__"],
    packages=setuptools.find_packages(),
    classifiers=classifiers,
    keywords=["pystone", "translation",
              "language", "python", "reverso", "deepl"],
    install_requires=requirements,
    entry_points={
        "console_scripts": ["pystone=pystone.__init__:main"]
    },
    project_urls={
        "Source": "https://github.com/GBS3/pystone"
    }
)
