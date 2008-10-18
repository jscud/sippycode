#!/bin/bash

mkdir -p sippy_twitter/sippycode/twitter/
mkdir -p sippy_twitter/sippycode/auth/
mkdir -p sippy_twitter/sippycode/http/
cp ../sippycode/twitter/sippy_twitter.py sippy_twitter/
cp ../sippycode/__init__.py sippy_twitter/sippycode/__init__.py
cp ../sippycode/twitter/__init__.py sippy_twitter/sippycode/twitter/__init__.py
cp ../sippycode/twitter/core.py sippy_twitter/sippycode/twitter/core.py
cp ../sippycode/auth/__init__.py sippy_twitter/sippycode/auth/__init__.py
cp ../sippycode/auth/core.py sippy_twitter/sippycode/auth/core.py
cp ../sippycode/http/__init__.py sippy_twitter/sippycode/http/__init__.py
cp ../sippycode/http/core.py sippy_twitter/sippycode/http/core.py
zip -r sippy_twitter-0.1.zip sippy_twitter
