from setuptools import setup, find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="asana",
    version="1.0",
    description="Asana api wrapper by python.",
    author="subretu",
    url="https://github.com/subretu/asana-api-python",
    packages=find_packages(),
    zip_safe=False,
    install_requires=_requires_from_file("requirements.txt"),
)
