from setuptools import setup
from setuptools import find_packages

setup(
    name='maps',
    version='1.0.x',
    author='Pratik Hublikar',
    packages=find_packages(),
    include_package_data=True,
    package_data = {
	"maps": [
	    "templates/*",
	    ]
        },
    zip_safe=False,
    install_requires=[
       'django'
    ]
)
