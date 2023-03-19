import setuptools
from pathlib import Path

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text()

setuptools.setup(
  name="openplayground-api",
  version="0.0.2",
  author="ading2210",
  description=" A reverse engineered API wrapper for OpenPlayground (nat.dev)",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent"
  ],
  python_requires=">=3.6",
  py_modules=["openplayground"],
  package_dir={"": "openplayground-api/src"},
  install_requires=[],
  url="https://github.com/ading2210/openplayground-api"
)