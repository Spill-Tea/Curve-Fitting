"""Setuptools script for building package."""


# Python Dependencies
from os import path
from setuptools import setup
from setuptools import find_packages


here = path.abspath(path.dirname(__file__))
PACKAGE_NAME = "CurveFitting"


def get_version(rel_path):
    """Function to read the __version__ from the init.
    This lets us define the version in a single location.

    Args:
        rel_path (str): Path from here defined above.

    Returns:
        Version string.

    """
    def read(x):
        with open(path.join(here, x), "r") as fp:
            return fp.read()

    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name=PACKAGE_NAME,  # Required
    version=get_version(f"{PACKAGE_NAME}/__init__.py"),
    description="Curve Fitting",
    long_description=long_description,

    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/Spill-Tea/Curve-Fitting",
    author="Jason C Del Rio",
    author_email="spillthetea917@gmail.com",

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Informaticians",
        "Topic :: Chem/Bio Informatics :: Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],

    # Note that this is a string of words separated by whitespace, not a list.
    keywords="Curve Fitting",

    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    # package_dir={"": ""},  # Optional
    # package_data={PACKAGE_NAME: [""]},

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=["tests", "dist"]),  # Required

    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.8, <4",
    install_requires=[
        "numpy",
        "plotly",
        "scipy",
        "sympy",
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={  # Optional
    #     "dev": ["check-manifest"],
    #     "test": ["coverage"],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    # package_data={  # Optional
    #
    # },

    # Although "package_data" is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, "data_file" will be installed into "<sys.prefix>/my_data"
    # data_files=[("my_data", ["data/clustering_analysis.yml"])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional

    },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    # project_urls={  # Optional
    #     "Bug Reports": "https://github.com/pypa/sampleproject/issues",
    #     "Funding": "https://donate.pypi.org",
    #     "Say Thanks!": "http://saythanks.io/to/example",
    #     "Source": "https://github.com/pypa/sampleproject/",
    # },
)
