import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="childespy",
    version="0.0.1",
    url="https://github.com/langcog/childespy",
    author="Jessica Mankewitz",
    author_email="jmank@stanford.edu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["rpy2>=3.3.5", "numpy>=1.19.2", "pandas>=1.1.2"],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Affero General Public License v3",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
