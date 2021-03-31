# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import sys
import yaml
from pathlib import Path
from typing import Any, Dict

import synthtool as s
from synthtool import log, shell, _tracked_paths
from synthtool.gcp.common import CommonTemplates
from synthtool.sources import templates


PathOrStr = templates.PathOrStr

PB2_HEADER = r"""(\# -\*- coding: utf-8 -\*-\n)(\# Generated by the protocol buffer compiler\.  DO NOT EDIT!.*?# source: .*?\.proto)"""
PB2_GRPC_HEADER = r"""(\# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!)
(import grpc)"""

LICENSE = """
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License."""

SAMPLES_VERSIONS = ["2.7", "3.6", "3.7", "3.8"]
IGNORED_VERSIONS = ["2.7"]

SAMPLES_TEMPLATE_PATH = Path(CommonTemplates()._template_root) / "python_samples"


def fix_pb2_headers(*, proto_root: str = "**/*_pb2.py") -> None:
    s.replace(
        proto_root,
        PB2_HEADER,
        fr"\g<1>{LICENSE}\n\n\g<2>",  # change order to avoid stacking replacements
        flags=re.DOTALL | re.MULTILINE,
    )


def fix_pb2_grpc_headers(*, proto_root: str = "**/*_pb2_grpc.py") -> None:
    s.replace(
        proto_root,
        PB2_GRPC_HEADER,
        fr"{LICENSE}\n\n\g<1>\n\n\g<2>",  # add line breaks to avoid stacking replacements
    )


def _get_help(filename: str) -> str:
    """Function used by sample readmegen"""
    return shell.run([sys.executable, filename, "--help"]).stdout


def _get_sample_readme_metadata(sample_dir: Path) -> dict:
    sample_readme = sample_dir / "README.rst.in"

    sample_metadata = {}
    if sample_readme.exists():
        requirements = str(Path(sample_dir / "requirements.txt").resolve())
        log.debug(
            f"Installing requirements at {requirements} to generate {sample_readme}"
        )
        shell.run([sys.executable, "-m", "pip", "install", "-r", requirements])

        with open(sample_readme) as f:
            sample_metadata = yaml.load(f, Loader=yaml.SafeLoader)
        for sample in sample_metadata["samples"]:
            # add absolute path to metadata so `python foo.py --help` succeeds
            sample["abs_path"] = Path(sample_dir / (sample["file"])).resolve()

    return sample_metadata


def py_samples(*, root: PathOrStr = None, skip_readmes: bool = False) -> None:
    """
    Find all samples projects and render templates.
    Samples projects always have a 'requirements.txt' file and may also have
    README.rst.in

    Args:
        root (Union[Path, str]): The samples directory root.
        skip_readmes (bool): If true, do not generate readmes.
    """
    in_client_library = Path("samples").exists() and Path("setup.py").exists()
    if root is None:
        if in_client_library:
            root = "samples"
        else:
            root = "."

    excludes = []

    # todo(kolea2): temporary exclusion until samples are ready to be migrated to new format
    excludes.append("README.md")

    # TODO(busunkim): Readmegen is disabled as it requires installing the sample
    # requirements in Synthtool. Sample Readmegen should be refactored to stop
    # relying on the output of `python sample.py --help`
    skip_readmes = True
    if skip_readmes:
        excludes.append("README.rst")
    t = templates.TemplateGroup(SAMPLES_TEMPLATE_PATH, excludes=excludes)

    t.env.globals["get_help"] = _get_help  # for sample readmegen

    for req in Path(root).glob("**/requirements.txt"):
        sample_project_dir = req.parent
        log.info(f"Generating templates for samples project '{sample_project_dir}'")

        excludes = ["**/*tmpl*"]  # .tmpl. files are partial templates

        sample_readme_metadata: Dict[str, Any] = {}
        if not skip_readmes:
            sample_readme_metadata = _get_sample_readme_metadata(sample_project_dir)
            # Don't generate readme if there's no metadata
            if sample_readme_metadata == {}:
                excludes.append("**/README.rst")

        if Path(sample_project_dir / "noxfile_config.py").exists():
            # Don't overwrite existing noxfile configs
            excludes.append("**/noxfile_config.py")

        result = t.render(subdir=sample_project_dir, **sample_readme_metadata)
        _tracked_paths.add(result)
        s.copy([result], excludes=excludes)


def owlbot_main():
    """Copies files from staging and template directories into current working dir.

    When there is no owlbot.py file, run this function instead.  Also, when an
    owlbot.py file is necessary, the first statement of owlbot.py should probably
    call this function.
    """

    templated_files = CommonTemplates().py_library(cov_level=99, microgenerator=True)

    # the microgenerator has a good coveragerc file
    excludes = [".coveragerc"]
    s.move(templated_files, excludes=excludes)

    s.shell.run(["nox", "-s", "blacken"], hide_output=False)


if __name__ == "__main__":
    owlbot_main()