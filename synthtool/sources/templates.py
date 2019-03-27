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

from typing import Union
from pathlib import Path

import jinja2

from synthtool import log
from synthtool import tmp


PathOrStr = Union[str, Path]


def _make_env(location):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(location)),
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters["release_quality_badge"] = release_quality_badge
    env.filters["language_pretty"] = language_pretty
    env.filters["syntax_highlighter"] = syntax_highlighter
    return env


def _render_to_path(env, template_name, dest, params):
    template = env.get_template(template_name)

    output = template.stream(**params)

    if template_name.endswith(".j2"):
        template_name = template.name[:-3]

    dest = dest / template_name
    dest.parent.mkdir(parents=True, exist_ok=True)

    with dest.open("w") as fh:
        output.dump(fh)

    # Copy file mode over
    source_path = Path(template.filename)
    mode = source_path.stat().st_mode
    dest.chmod(mode)

    return dest


class Templates:
    def __init__(self, location: PathOrStr) -> None:
        self.env = _make_env(location)
        self.source_path = Path(location)
        self.dir = tmp.tmpdir()

    def render(self, template_name: str, **kwargs) -> Path:
        return _render_to_path(self.env, template_name, self.dir, kwargs)


class TemplateGroup:
    def __init__(self, location: PathOrStr) -> None:
        self.env = _make_env(location)
        self.dir = tmp.tmpdir()
        self.excludes = []

    def render(self, **kwargs) -> Path:
        for template_name in self.env.list_templates():
            if template_name not in self.excludes:
                print(f"Rendering: {template_name}")
                _render_to_path(self.env, template_name, self.dir, kwargs)
            else:
                print(f"Skipping: {template_name}")

        return self.dir


#
# Generates a markdown badge for displaying a "Release Quality'.
#
def release_quality_badge(input):
    if not input:
        log.error(f"ensure you pass a string 'quality' to release_quality_badge")
        return

    release_quality = input.upper()
    badge = ""

    if release_quality == "GA":
        badge = "general%20availability%20%28GA%29-brightgreen"
    elif release_quality == "BETA":
        badge = "beta-yellow"
    elif release_quality == "ALPHA":
        badge = "alpha-orange"
    elif release_quality == "EAP":
        badge = "EAP-yellow"
    elif release_quality == "DEPRECATED":
        badge = "deprecated-red"
    else:
        log.error(
            "Expected 'release_quality' to be one of: (ga, beta, alpha, eap, deprecated)"
        )
        return
    return f"[![release level](https://img.shields.io/badge/release%20level-{badge}.svg?style=flat)](https://cloud.google.com/terms/launch-stages)"


#
# .repo-metadata.json language field to pretty language.
#
def language_pretty(input):
    if input == "nodejs":
        return "Node.js"
    return input


#
# .repo-metadata.json language field to syntax highlighter name.
#
def syntax_highlighter(input):
    if input == "nodejs":
        return "javascript"
    return input
