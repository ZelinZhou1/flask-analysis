# -*- coding: utf-8 -*-
"""
Tests for analyzers module.
"""

import pytest
import os
from unittest.mock import MagicMock, patch
from src.analyzers.stats import CodeStats
from src.analyzers.complexity_analyzer import ComplexityAnalyzer

# --- CodeStats Tests ---


def test_count_lines():
    """Test line counting logic."""
    stats = CodeStats()
    content = """
    def hello():
        print("world")
    
    # This is a comment
    
    """
    # Total lines: 6
    # Empty lines: 2 (line 4 and 6, assuming splitlines includes empty strings if they exist, or just check split logic)
    # Comment lines: 1
    # Code lines: 3

    result = stats.count_lines(content)
    assert result["total"] == 6
    assert result["empty"] == 2
    assert result["comment"] == 1
    assert result["code"] == 3


def test_analyze_file_stats(tmp_path):
    """Test analyzing a single file."""
    f = tmp_path / "test.py"
    f.write_text("print('hello')", encoding="utf-8")

    stats = CodeStats()
    result = stats.analyze_file_stats(str(f))

    assert result["extension"] == ".py"
    assert result["line_stats"]["total"] == 1
    assert result["size_bytes"] > 0


# --- ComplexityAnalyzer Tests ---


@patch("src.analyzers.complexity_analyzer.radon_cc.cc_visit")
def test_analyze_file_complexity(mock_cc_visit, tmp_path):
    """Test complexity analysis for a file."""
    # Mock Radon block
    block = MagicMock()
    block.complexity = 5
    block.name = "test_func"
    block.lineno = 1
    block.endline = 5
    block.classname = None

    mock_cc_visit.return_value = [block]

    f = tmp_path / "complex.py"
    f.write_text("def test_func(): pass", encoding="utf-8")

    analyzer = ComplexityAnalyzer(str(tmp_path))
    result = analyzer.analyze_file(str(f))

    assert result["average_complexity"] == 5
    assert result["max_complexity"] == 5
    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "test_func"


def test_analyze_repository_complexity(tmp_path):
    """Test repository wide complexity analysis."""
    # Create a dummy python file
    d = tmp_path / "src"
    d.mkdir()
    f = d / "test.py"
    f.write_text("def foo():\n    pass\n", encoding="utf-8")

    # We need to mock analyze_file or let it run.
    # Since we depend on radon, and we don't want to install it if not present (but requirements said it is),
    # let's try to let it run if simple.
    # But for safety, let's mock analyze_file of the instance.

    with patch.object(ComplexityAnalyzer, "analyze_file") as mock_analyze:
        mock_analyze.return_value = {
            "average_complexity": 5,
            "max_complexity": 15,
            "functions": [{"name": "complex_func", "complexity": 15, "lineno": 1}],
        }

        analyzer = ComplexityAnalyzer(str(tmp_path))
        stats = analyzer.analyze_repository()

        # It should find the file and aggregate
        # Wait, analyze_repository uses rglob("*.py").
        # So we need at least one file on disk, which we created.

        assert stats["total_complexity"] == 15
        assert stats["total_functions"] == 1
        assert len(stats["high_complexity_functions"]) == 1
        assert stats["high_complexity_functions"][0]["name"] == "complex_func"
