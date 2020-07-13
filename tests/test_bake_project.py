# coding: utf-8

"""
Unit Tests for cookie cutter template

Copyright (c) Audrey Roy Greenfeld and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Audrey Roy Greenfeld nor the names of its
       contributors may be used to endorse or promote products derived from this
       software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import datetime
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager
from types import ModuleType
from typing import Any, Dict, Iterable, Iterator, Optional, Tuple

# import yaml
from py._path.local import LocalPath  # Decprecated(?): replace with pathlib later.
from pytest import mark
from pytest_cookies.plugin import Cookies, Result

from helper_functions import bake_in_temp_dir, project_info, run_inside_dir


def test_year_compute_in_license_file(cookies: Cookies) -> None:
    with bake_in_temp_dir(cookies) as result:
        license_file_path: LocalPath = result.project.join("LICENSE")
        now: datetime.datetime = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def test_bake_with_defaults(cookies: Cookies) -> None:
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "setup.py" in found_toplevel_files
        assert "tox.ini" in found_toplevel_files
        assert "docs" in found_toplevel_files
        assert "src" in found_toplevel_files
        assert "tests" in found_toplevel_files
        assert "interview_practice" in os.listdir(
            os.path.join(str(result.project), "src")
        )


def test_bake_without_author_file(cookies: Cookies) -> None:
    with bake_in_temp_dir(cookies, extra_context={"create_author_file": "n"}) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "AUTHORS.rst" not in found_toplevel_files
        # doc_files = [f.basename for f in result.project.join('docs').listdir()]
        # assert 'authors.rst' not in doc_files

        # # Assert there are no spaces in the toc tree
        # docs_index_path = result.project.join('docs/index.rst')
        # with open(str(docs_index_path)) as index_file:
        #     assert 'contributing\n   history' in index_file.read()

        # # Check that
        # manifest_path = result.project.join('MANIFEST.in')
        # with open(str(manifest_path)) as manifest_file:
        #     assert 'AUTHORS.rst' not in manifest_file.read()


# def test_make_help(cookies):
#     with bake_in_temp_dir(cookies) as result:
#         # The supplied Makefile does not support win32
#         if sys.platform != "win32":
#             output = check_output_inside_dir('make help', str(result.project))
#             assert b"check code coverage quickly with the default Python" in output


@mark.parametrize(
    "license_info",
    [
        ("MIT", "MIT"),
        ("Apache 2.0 License", "Licensed under the Apache License, Version 2.0"),
    ],
)
def test_bake_selecting_license(
    cookies: Cookies, license_info: Tuple[str, str]
) -> None:
    license: str
    target_string: str
    result: Result

    license, target_string = license_info
    with bake_in_temp_dir(cookies, extra_context={"license": license}) as result:
        assert target_string in result.project.join("LICENSE").read()
        assert license in result.project.join("setup.py").read()


def test_bake_other_license(cookies: Cookies) -> None:
    result: Result
    with bake_in_temp_dir(cookies, extra_context={"license": "Other"}) as result:
        found_toplevel_files: Iterable[str] = [
            f.basename for f in result.project.listdir()
        ]
        assert "setup.py" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in result.project.join("README.markdown").read()


def test_bake_no_cli(cookies: Cookies) -> None:
    result: Result
    with bake_in_temp_dir(cookies) as result:
        project_path, _, project_dir = project_info(result)
        found_project_files: Iterable[str] = os.listdir(project_dir)
        assert "cli.py" not in found_project_files

        setup_path: str = os.path.join(project_path, 'setup.py')
        with open(setup_path, 'r') as setup_file:
            assert "entry_points" not in setup_file.read()


def test_bake_sphinx(cookies: Cookies) -> None:
    result: Result
    with bake_in_temp_dir(cookies) as result:
        project_path: str = project_info(result)[0]
        root_files: Iterable[str] = os.listdir(project_path)

        assert "Pipfile" in root_files
        with open(os.path.join(project_path, "Pipfile"), 'r') as pipfile:
            lines: Iterable[str] = pipfile.read().splitlines()
            assert 'mkdocs = "*"' not in lines

            assert 'sphinx = "*"' in lines
            assert 'sphinx-autodoc-typehints = "*"' in lines
            assert 'sphinx-rtd-theme = "*"' in lines

        assert "docs" in root_files
        assert "source" in os.listdir(os.path.join(project_path, "docs"))
        docs_source_dir_name: str = os.path.join(project_path, "docs", "source")
        docs_source_dir: Iterable[str] = os.listdir(docs_source_dir_name)

        assert "index.rst" in docs_source_dir
        assert "index.markdown" not in docs_source_dir

        assert "conf.py" in docs_source_dir
        with open(os.path.join(docs_source_dir_name, "conf.py"), 'r') as docs_setup:
            lines = docs_setup.read().splitlines()

            for extension in ["autodoc", "coverage", "viewcode", "napoleon"]:
                assert next((s for s in lines if extension in s), None)

            rtd_theme_init_line: Optional[str] = next(
                (s for s in lines if "sphinx_autodoc_typehints" in s), None
            )
            rtd_theme_set_line: str = 'html_theme = "sphinx_rtd_theme"'
            assert (
                rtd_theme_init_line is not None
                and rtd_theme_init_line != rtd_theme_set_line
            )
            assert rtd_theme_set_line in lines

            assert next((s for s in lines if "sphinx_autodoc_typehints" in s), None)


@mark.slow
@mark.parametrize(
    "context", [{}, {"full_name": 'name "quote" name'}, {"full_name": "O'connor"},],
)
def test_bake_and_run_tests(cookies: Cookies, context: Dict[str, str]) -> None:
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        assert result.project.isdir()
        test_file_path = result.project.join("tests/test_interview_practice.py")
        assert "import pytest" in test_file_path.read()

        assert run_inside_dir("tox", str(result.project)) == 0
