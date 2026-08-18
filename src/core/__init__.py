"""
satellite-brain - Global Crisis and Land Change Monitoring Engine
File: src/core/__init__.py
Description: Exposes all cloud geospatial data connectors and authentication 
tunnels directly to the analytics modules.
"""

from src.core.stac_client import StacClient
from src.core.earth_engine import EarthEngineTunnel

# Declaring open public endpoints for clean imports across the platform
__all__ = ["StacClient", "EarthEngineTunnel"]
