from setuptools import setup
from setuptools import find_packages

setup(
    name='maps',
    version='4.2.0',
    author='Pratik Hublikar, Kristoffer Snabb',
    packages=find_packages(),
    include_package_data=True,
    package_data = {
	"maps": [
	    "templates/*",
            "fixtures/*"
	    ]
        },
    zip_safe=False,
    install_requires=[
       'django'
    ]
)
