# Copyright 2018 Google LLC
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

import os
import platform
import tempfile

from synthtool import cache
from synthtool import log
from synthtool import shell

ARTMAN_VERSION = os.environ.get("SYNTHTOOL_ARTMAN_VERSION", "latest")


class Artman:
    def __init__(self):
        # Docker on mac by default cannot use the default temp file location
        # # instead use the more standard *nix /tmp location\
        if platform.system() == "Darwin":
            tempfile.tempdir = "/tmp"
        self._ensure_dependencies_installed()
        self._install_artman()

    def run(self, image, root_dir, config, *args):
        """Executes artman command in the artman container.
          Args:
              root_dir: The input directory that will be mounted to artman docker
                  container as local googleapis directory.
          Returns:
              The output directory with artman-generated files.
          """
        container_name = "artman-docker"
        output_dir = root_dir / "artman-genfiles"

        docker_cmd = [
            "docker",
            "run",
            "--name",
            container_name,
            "--rm",
            "-i",
            "-e",
            f"HOST_USER_ID={os.getuid()}",
            "-e",
            f"HOST_GROUP_ID={os.getgid()}",
            "-e",
            "RUNNING_IN_ARTMAN_DOCKER=True",
            "-v",
            f"{root_dir}:{root_dir}",
            "-v",
            f"{output_dir}:{output_dir}",
            "-w",
            root_dir,
            image,
            "/bin/bash",
            "-c",
        ]

        artman_command = " ".join(
            map(str, ["artman", "--local", "--config", config, "generate"] + list(args))
        )

        cmd = docker_cmd + [artman_command]

        shell.run(cmd, cwd=root_dir)

        return output_dir

    def _ensure_dependencies_installed(self):
        log.debug("Ensuring dependencies.")

        dependencies = ["docker", "git"]
        failed_dependencies = []
        for dependency in dependencies:
            return_code = shell.run(["which", dependency], check=False).returncode
            if return_code:
                failed_dependencies.append(dependency)

        if failed_dependencies:
            raise EnvironmentError(
                f"Dependencies missing: {', '.join(failed_dependencies)}"
            )

    def _install_artman(self):
        log.debug("Pulling artman image.")
        shell.run(["docker", "pull", f"googleapis/artman:{ARTMAN_VERSION}"])
