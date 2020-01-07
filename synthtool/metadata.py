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

import datetime
import os
from typing import List

import google.protobuf.json_format

from synthtool import log
from synthtool.protos import metadata_pb2


_metadata = metadata_pb2.Metadata()
_track_obsolete_files = False


def reset() -> None:
    """Clear all metadata so far."""
    global _metadata
    _metadata = metadata_pb2.Metadata()


def get():
    return _metadata


def add_git_source(**kwargs) -> None:
    """Adds a git source to the current metadata."""
    _metadata.sources.add(git=metadata_pb2.GitSource(**kwargs))


def add_generator_source(**kwargs) -> None:
    """Adds a generator source to the current metadata."""
    _metadata.sources.add(generator=metadata_pb2.GeneratorSource(**kwargs))


def add_template_source(**kwargs) -> None:
    """Adds a template source to the current metadata."""
    _metadata.sources.add(template=metadata_pb2.TemplateSource(**kwargs))


def add_client_destination(**kwargs) -> None:
    """Adds a client library destination to the current metadata."""
    _metadata.destinations.add(client=metadata_pb2.ClientDestination(**kwargs))


def add_new_files(newer_than: float) -> None:
    """Searchs a directory for new files and adds them to metadata.

    Only considers files tracked by git.
    Parameters:
    newer_than: any file modified after this timestamp (from time.time())
        will be added to the metadata
    """
    for filepath in get_new_files_tracked_by_git(newer_than):
        new_file = _metadata.new_files.add()
        new_file.path = filepath


def get_new_files_tracked_by_git(newer_than: float) -> List[str]:
    """Searchs current working directory for new files.

    Only considers files tracked by git.
    Parameters:
    newer_than: any file modified after this timestamp (from time.time())
        will be added to the metadata
    Returns:
        list of new files
    """
    new_files = []
    git_output = os.popen("git ls-files").readlines()
    files_tracked_by_git = [line.strip() for line in git_output]
    for filepath in files_tracked_by_git:
        try:
            mtime = os.path.getmtime(filepath)
        except FileNotFoundError:
            log.warning(
                f"FileNotFoundError while getting modified time for {filepath}."
            )
            continue
        if mtime >= newer_than:
            new_files.append(filepath)
    return new_files


def read_or_empty(path: str = "synth.metadata"):
    """Reads a metadata json file.  Returns empty if that file is not found."""
    try:
        with open(path, "rt") as file:
            text = file.read()
        return google.protobuf.json_format.Parse(text, metadata_pb2.Metadata())
    except FileNotFoundError:
        return metadata_pb2.Metadata()


def write(outfile: str = "synth.metadata") -> None:
    """Writes out the metadata to a file."""
    _metadata.update_time.FromDatetime(datetime.datetime.utcnow())
    jsonified = google.protobuf.json_format.MessageToJson(_metadata)

    with open(outfile, "w") as fh:
        fh.write(jsonified)

    log.debug(f"Wrote metadata to {outfile}.")


def remove_obsolete_files(old_metadata):
    """Remove obsolete files from the file system.

    Call add_new_files() before this function or it will remove all generated
    files.

    Parameters:
    old_metadata:  old metadata loaded from a call to read_or_empty().
    """
    old_files = set([new_file.path for new_file in old_metadata.new_files])
    new_files = set([new_file.path for new_file in _metadata.new_files])
    obsolete_files = old_files - new_files
    for file_path in obsolete_files:
        try:
            log.info(f"Removing obsolete file {file_path}...")
            os.unlink(file_path)
        except FileNotFoundError:
            pass  # Already deleted.  That's OK.


def set_track_obsolete_files(track_obsolete_files=True):
    """Instructs synthtool to track and remove obsolete files."""
    global _track_obsolete_files
    _track_obsolete_files = track_obsolete_files


def should_track_obsolete_files():
    return _track_obsolete_files
