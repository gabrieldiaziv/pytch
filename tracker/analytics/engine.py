from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
import tempfile

from .types import Match

import plotly.graph_objects as go



class Viz(ABC):
    @property
    @abstractmethod
    def name(self)->str:
        ...

    @property
    @abstractmethod
    def description(self)->str:
        ...

    @abstractmethod
    def generate(self, match: Match) -> go.Figure:
        ...

@dataclass
class VizResult:
    name: str
    desc: str
    path: str


class Engine:
    def __init__(self, vizs: list[Viz]):
        self.vizs = vizs

    def compute(self, match: Match) -> list[VizResult]:
        viz_paths = []
        for viz in self.vizs:
            _, fig_path = tempfile.mkstemp(suffix=f".html")
            fig = viz.generate(match)
            fig.write_html(fig_path)

            viz_paths.append(VizResult(
                name=viz.name,
                desc=viz.description,
                path=fig_path
            ))
        return viz_paths
