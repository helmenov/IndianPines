# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indianpines']

package_data = \
{'': ['*'], 'indianpines': ['resource/*']}

install_requires = \
['numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'requests>=2.28.0,<3.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'tifffile>=2022.5.4,<2023.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'indianpines',
    'version': '0.1.0',
    'description': 'Indian Pines datasets for scikit-learn',
    'long_description': 'None',
    'author': 'Kotaro SONODA',
    'author_email': 'kotaro1976@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
