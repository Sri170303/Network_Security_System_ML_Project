from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Read the requirements from a file and return them as a list."""
    requirements:List[str] = []
    try:
        with open("requirements.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements.append(requirement)
    except FileNotFoundError:
        print(f"Requirements file not found.")
    return requirements

setup(
    name="NetworkSecurity",
    author="Sri Darsan Sah",
    version="0.0.1",
    author_email="sridarsansah5907@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
