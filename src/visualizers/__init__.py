# -*- coding: utf-8 -*-
"""
Visualizers package
Provides various visualization modules for repo analysis.
"""

from .style import apply_style, get_color, get_palette, get_cmap
from .charts import plot_bar, plot_pie, plot_horizontal_bar
from .heatmap import plot_heatmap, plot_calendar_heatmap
from .trends import plot_line_chart, plot_area_chart
from .author_charts import plot_author_stats
from .file_charts import plot_file_stats
