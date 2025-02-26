import setuptools_scm
from setuptools import find_packages, setup

setup(
    name="{{cookiecutter.project_name}}",
    version=setuptools_scm.get_version(),
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=["setuptools>=42", "setuptools_scm"],
)
