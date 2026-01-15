# -*- coding: utf-8 -*-
"""
Visualizers package
Provides various visualization modules for repo analysis.
"""

from .style import apply_style, get_color, get_palette, get_cmap
from .charts import plot_bar, plot_pie, plot_horizontal_bar
from .heatmap import plot_heatmap, plot_calendar_heatmap, plot_activity_heatmap
from .trends import plot_line_chart, plot_area_chart
from .author_charts import plot_author_stats
from .file_charts import plot_file_stats
from .complexity_charts import (
    plot_complexity_distribution,
    plot_high_complexity_functions,
    plot_maintainability_index,
)
from .message_charts import (
    plot_commit_message_wordcloud,
    plot_message_type_distribution,
)
from .yearly_charts import plot_yearly_commits, plot_monthly_activity
from .dependency_charts import plot_dependency_network, plot_module_coupling
from .issues_charts import (
    plot_issue_status_distribution,
    plot_issue_labels,
    plot_issue_creation_history,
)
from .contributors_charts import (
    plot_contributors_leaderboard,
    plot_code_changes_by_author,
    plot_author_contribution_pie,
)
from .pr_charts import (
    plot_pr_size_distribution,
    plot_pr_time_to_merge,
    plot_pr_comments_vs_size,
)
from .charts_plotly import (
    plot_interactive_commit_activity,
    plot_interactive_author_timeline,
    plot_interactive_file_changes,
)
