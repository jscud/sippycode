#!/bin/bash

mkdir -p mashupcamp_editor/static
cp ../mashpcamp_editor/app.yaml mashupcamp_editor/
cp ../mashpcamp_editor/article.py mashupcamp_editor/
cp ../mashpcamp_editor/article.html mashupcamp_editor/
cp ../mashpcamp_editor/main.py mashupcamp_editor/
cp ../mashpcamp_editor/static/json.js mashupcamp_editor/static
cp ../mashpcamp_editor/static/q12-min.js mashupcamp_editor/static
zip -r mashupcamp_editor-0.1.zip mashupcamp_editor
