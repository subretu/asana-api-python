from setuptools import setup, find_packages
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="asana-api-python",
    version="1.0",
    description="Asana API Wrapper by Python.",
    author="subretu",
    url="https://github.com/subretu/asana-api-python",
    packages=find_packages(),
    zip_safe=True,
    install_requires=_requires_from_file('requirements.txt'),
)
