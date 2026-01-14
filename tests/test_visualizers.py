# -*- coding: utf-8 -*-
"""
Tests for visualizers module.
"""

import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from src.visualizers import charts, style


@pytest.fixture
def sample_data():
    """Create sample data for plotting."""
    return pd.Series([10, 20, 30], index=["A", "B", "C"])


def test_plot_bar(sample_data, tmp_path):
    """Test generating a bar chart."""
    output = tmp_path / "bar.png"

    with (
        patch("src.visualizers.charts.plt") as mock_plt,
        patch("src.visualizers.charts.save_plot") as mock_save,
    ):
        charts.plot_bar(sample_data, "Test Title", "X", "Y", str(output))

        # Verify plotting calls
        assert mock_plt.figure.called
        assert mock_save.called
        mock_save.assert_called_with(str(output), "Test Title")


def test_plot_pie(sample_data, tmp_path):
    """Test generating a pie chart."""
    output = tmp_path / "pie.png"

    with (
        patch("src.visualizers.charts.plt") as mock_plt,
        patch("src.visualizers.charts.save_plot") as mock_save,
    ):
        charts.plot_pie(sample_data, "Test Pie", str(output))

        assert mock_plt.pie.called
        assert mock_save.called


def test_style_config():
    """Test style configuration."""
    with (
        patch("src.visualizers.style.plt") as mock_plt,
        patch("src.visualizers.style.sns") as mock_sns,
    ):
        style.apply_style()

        assert mock_sns.set_theme.called
        assert mock_plt.rcParams.update.called
