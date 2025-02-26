from setuptools import find_packages, setup

_ = setup(
    name="{{cookiecutter.project_name}}",
    use_scm_version=True,
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude={"test*", "testing*", "tests*"}),
    # cmdclass={"build_py": my_build_py},  # noqa: F821
    # include_package_data=True,
    # package_data={PACKAGE_DIR_NAME: ["*.zip", ".gz"]},
)
