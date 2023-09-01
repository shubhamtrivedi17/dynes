from setuptools import setup, find_packages

setup(    
    name="dynes",
    version = "0.1",
    author = "Shubham Trivedi",
    author_email = "shubham.king.007@gmail.com",
    description = "Module to perform non-linear site response analysis with Ishihara-Yoshida model in the time domain",
    long_description = "file: README.md",
    long_description_content_type = "text/markdown",
    # url = "https://github.com/arup-group/optif",
    # project_urls = {
    #     "Bug Tracker" : "https://github.com/arup-group/optif/issues"},

    classifiers =
        ["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],

    packages=find_packages("."),
    package_dir={'': '.'},
    python_requires = ">=3.7",

    install_requires = [
        "numpy",
        "pandas",
        "fortranformat",
        "matplotlib"],

    entry_points={
        "console_scripts": [
            "dynes=dynes.scripts.dynes:main"
            ]
        }

)
