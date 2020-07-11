from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='unearthed-comp-model',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "scoring_function"]),
    version='0.0.1',
    description='Data Science Challenge Template',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Innovator Name',
    author_email="innovator@example.com",
    license='MIT',
    include_package_data=True,
)
