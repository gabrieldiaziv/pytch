#!/bin/env sh

git clone -n --depth=1 --filter=tree:0 \
  https://github.com/gabrieldiaziv/pytch pytch
cd pytch-test
git sparse-checkout set --no-cone tracker/analytics
git checkout

mv tracker/analytics ./analytics
rm -rf .git tracker

touch main.py
echo """ # Example Viz Implementation
import json

from analytics.engine import Viz
from analytics.types import Match

import plotly.graph_objects as go

class CustomViz(Viz):
    @property
    def name(self) -> str:
        return 'custom_viz'

    @property
    def description(self) -> str:
        return 'Description of your custom visualization.'

    def generate(self, match: Match) -> go.Figure:
        # Your implementation goes here
        pass

if __name__ == '__main__':

     with open(PATH_TO_MATCH) as match_file:

        match = json.load(match_file)
        match = Match.from_dict(match)

        my_viz = CustomViz()
        my_viz.generate(match).show()

""" >> main.py  

