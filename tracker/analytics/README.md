# Custom Viz Implementation Guide

## Introduction

Welcome to the Viz library, a tool for creating visualizations of sports matches! This guide will walk you through the process of creating your own visualization by implementing the `Viz` abstract class.

## Getting Started

1. **Use Pytch to Download Match File"**
    - Log in to pytch account and go to your dashboard, select a match, and download the match file.
    ![Download Button](https://raw.githubusercontent.com/GabrielDiazIV/pytch/docs/docs/imgs/download-img.png)

1. **Install the Viz Library:**
   - To install the Viz library, run the following command in your terminal:

     ```bash
     curl https://raw.githubusercontent.com/GabrielDiazIV/pytch/main/install.sh | sh
     ```

2. **Navigate to the Viz Directory:**
   - Change to the Viz library directory:

     ```bash
     cd pytch
     ```

3. **Install Dependencies:**
   - Install the required dependencies by running the following command:

     ```bash
     pip install -r analytics/requirements.txt
     ```

4. **Understanding the Abstract Class:**
   - Take a look at the `Viz` abstract class in `engine.py`. This class provides a template for creating visualizations.

## Implementing Your Viz

1. **Open `main.py`:**
   - Open the `main.py` file in your preferred text editor or IDE. This file contains the main logic and serves as a starting point for implementing your custom visualization.

4. **Implement Properties:**
   - Implement the `name` and `description` properties, providing a unique name and a brief description of your visualization.

5. **Implement the `generate` Method:**
   - Implement the `generate` method to create the actual visualization. Use the `match` parameter, which represents the sports match data.

6. **Testing Your Viz:**
   - Test your visualization by instantiating your class, passing a `Match` instance, and generating the visualization.

7. **Documentation:**
   - Document any additional features or customization options in your class.

## Example Implementation

```python
# Example Viz Implementation

from .engine import Viz
from .types import Match

class CustomViz(Viz):
    @property
    def name(self) -> str:
        return 'custom_viz'

    @property
    def description(self) -> str:
        return 'Description of your custom visualization.'

    def generate(self, match: Match):
        # Your implementation goes here
        pass
```

## Contributing

Feel free to contribute to the library by creating new visualizations or improving existing ones. Submit a pull request to share your work with the community!

## Explore Existing Visualizations for Inspiration

For inspiration, explore the existing visualizations in the analytics/ directory. Take a look at the variety of visualizations created by the community to spark ideas for your own custom visualization.

