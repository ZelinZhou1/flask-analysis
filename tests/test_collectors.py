# -*- coding: utf-8 -*-
"""
Tests for collectors module.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.collectors.pydriller_collector import PyDrillerCollector


@pytest.fixture
def mock_commit():
    """Create a mock commit object."""
    commit = MagicMock()
    commit.hash = "abc1234"
    commit.msg = "test commit"
    commit.author.name = "Test Author"
    commit.author.email = "test@example.com"
    commit.author_date = datetime(2023, 1, 1, 12, 0, 0)
    commit.committer.name = "Test Author"
    commit.committer.email = "test@example.com"
    commit.committer_date = datetime(2023, 1, 1, 12, 0, 0)
    commit.lines = 10
    commit.insertions = 5
    commit.deletions = 5
    commit.modified_files = []
    commit.dmm_unit_size = 0.5
    commit.dmm_complexity = 0.5
    commit.dmm_interfacing = 0.5
    return commit


def test_collect_commits(mock_commit):
    """Test collecting commits."""
    with patch("src.collectors.pydriller_collector.Repository") as MockRepo:
        # Setup mock
        instance = MockRepo.return_value
        instance.traverse_commits.return_value = [mock_commit]

        collector = PyDrillerCollector("/path/to/repo")
        commits = list(collector.collect_commits())

        assert len(commits) == 1
        assert commits[0]["hash"] == "abc1234"
        assert commits[0]["author_name"] == "Test Author"

        # Verify Repository was called with correct path
        MockRepo.assert_called_with(path_to_repo="/path/to/repo")


def test_collect_commits_with_branch(mock_commit):
    """Test collecting commits from a specific branch."""
    with patch("src.collectors.pydriller_collector.Repository") as MockRepo:
        instance = MockRepo.return_value
        instance.traverse_commits.return_value = [mock_commit]

        collector = PyDrillerCollector("/path/to/repo", branch="develop")
        commits = list(collector.collect_commits())

        MockRepo.assert_called_with(
            path_to_repo="/path/to/repo", only_in_branch="develop"
        )
        assert len(commits) == 1


def test_collect_commits_by_author(mock_commit):
    """Test filtering commits by author."""
    with patch("src.collectors.pydriller_collector.Repository") as MockRepo:
        instance = MockRepo.return_value
        instance.traverse_commits.return_value = [mock_commit]

        collector = PyDrillerCollector("/path/to/repo")

        # Match
        commits = collector.collect_commits_by_author("Test")
        assert len(commits) == 1

        # No match (mocking a second call needs reset or just understanding the mock returns the same iterator)
        # Re-mock for fresh iterator
        instance.traverse_commits.return_value = [mock_commit]
        commits_no_match = collector.collect_commits_by_author("Unknown")
        assert len(commits_no_match) == 0
