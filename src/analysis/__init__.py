"""
Brent Oil Price Analysis Module

This module provides tools for analyzing Brent oil prices using Bayesian change point analysis
and event correlation studies.
"""

from .change_point import ChangePointAnalyzer
from .event_research import EventResearch
from .impact_analysis import ImpactAnalyzer

__all__ = ['ChangePointAnalyzer', 'EventResearch', 'ImpactAnalyzer']
