#!/bin/bash
# Copyright 2021 Google LLC
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
# limitations under the License.

set -eo pipefail

# Use synthtool templates at this commit hash
export SYNTHTOOL_TEMPLATES="`pwd`/synthtool/gcp/templates"

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Add github to known hosts.
mkdir "$HOME/.ssh"
ssh-keyscan github.com >> "$HOME/.ssh/known_hosts"

# Kokoro exposes this as a file, but the scripts expect just a plain variable.
export GITHUB_TOKEN=$(cat ${KOKORO_KEYSTORE_DIR}/73713_yoshi-automation-github-key)

# Setup git credentials
echo "https://${GITHUB_TOKEN}:@github.com" >> ~/.git-credentials
git config --global credential.helper 'store --file ~/.git-credentials'

python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade --quiet -r requirements.txt
export PYTHONPATH=`pwd`
python3 -m autosynth.multi --config ${MULTISYNTH_CONFIG}
