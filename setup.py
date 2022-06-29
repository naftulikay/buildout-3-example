#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="myeggname",  # NOTE change this to your desired project name
    version="0.0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        'setuptools',  # NOTE setuptools: this must be here
        # NOTE instead of specifying dependencies in requirements.txt, specify
        #      them here in the exact same format that would be used in
        #      requirements.txt
        'click >=8.0,<9',
        'numpy',
    ],
    entry_points={
        "console_scripts": [
            # NOTE define your exposed scripts here, i.e.
            #      {{ exec_name }} = {{ module_path }}:{{ function_name }}
            'myegg-argparse = myeggname.cli:run_argparse',
            'myegg-click = myeggname.cli:run_click',
        ]
    }
)
