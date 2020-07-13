#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
from glob import iglob
from os.path import basename, splitext

from setuptools import find_packages, setup  # type: ignore

long_description: str
with open("README.markdown", encoding='utf-8') as f:
    long_description = f.read()
    print(long_description)

{%- set license_classifiers = {
    "MIT License": "License :: OSI Approved :: MIT License",
    "Apache 2.0 License": "License :: OSI Approved :: Apache Software License",
} %}

setup(
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
    {%- if cookiecutter.license in license_classifiers %}
        "{{ license_classifiers[cookiecutter.license] }}",
    {%- endif %}
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
{%- if cookiecutter.license in license_classifiers %}
    license="{{ cookiecutter.license }}",
{%- endif %}
    author="{{ cookiecutter.full_name }}",
    description="{{ cookiecutter.project_short_description }}",
    include_package_data=True,
    keywords="",
    long_description_content_type='text/markdown',
    long_description=long_description,
    name="{{ cookiecutter.project_slug }}",
    package_dir={"": "src"},
    packages=find_packages("src"),
    py_modules=[splitext(basename(path))[0] for path in iglob("src/*.py")],
    python_requires=">=3.6",
    test_suite="tests",
    url="",
    version="{{ cookiecutter.version }}",
    zip_safe=False,
)
