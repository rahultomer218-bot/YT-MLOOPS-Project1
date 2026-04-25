from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """
    यह फंक्शन requirements.txt फाइल से लाइब्रेरीज की लिस्ट लोड करता है।
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        # अगर requirements.txt में '-e .' है, तो उसे लिस्ट से हटा दें
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name="mlops_project",
    version="0.0.1",
    author="Rahul",
    author_email="rahultomer218@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)