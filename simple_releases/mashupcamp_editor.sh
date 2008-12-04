#!/bin/bash

mkdir -p mashupcamp_editor/static
cp ../mashupcamp_editor/README.txt mashupcamp_editor/
cp ../mashupcamp_editor/app.yaml mashupcamp_editor/
cp ../mashupcamp_editor/article.py mashupcamp_editor/
cp ../mashupcamp_editor/article.html mashupcamp_editor/
cp ../mashupcamp_editor/main.py mashupcamp_editor/
cp ../mashupcamp_editor/static/json.js mashupcamp_editor/static
cp ../mashupcamp_editor/static/q12-min.js mashupcamp_editor/static
zip -r mashupcamp_editor-0.1.zip mashupcamp_editor
