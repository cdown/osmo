#!/usr/bin/env python

import os
import osmo.succor as s
import shutil
import tempfile

def test_listdir_full():
    temp_dir = tempfile.mkdtemp(prefix="osmo-test-_listdir_full")
    file_names = { "x", "y", "z" }

    for file_name in file_names:
        open(os.path.join(temp_dir, file_name), "w+").close()

    file_names_list = set(os.listdir(temp_dir))
    file_names_path_list = set(s._listdir_full(temp_dir))

    assert file_names_list == file_names
    assert file_names_path_list == { os.path.join(temp_dir, file_name) for file_name in file_names_list }

    shutil.rmtree(temp_dir)
