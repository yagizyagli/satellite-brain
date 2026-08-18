"""
satellite-brain - Global Crisis and Land Change Monitoring Engine
File: src/analyzers/base_analyzer.py
Description: Abstract base class that defines the core structure for all environmental 
and emergency satellite imagery analyzers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import geopandas as gpd


class BaseAnalyzer(ABC):
    """
    Abstract Base Class for all satellite data analyzers.
    Every specific hazard or environmental tracking module must inherit from this class.
    """

    def __init__(self, provider_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initializes the base analyzer with cloud provider configurations.
        
        Args:
            provider_config (dict): API keys, tokens, or endpoints for STAC / GEE.
        """
        self.provider_config = provider_config or {}
        self.is_connected = False
        self._initialize_connection()

    @abstractmethod
    def _initialize_connection(self) -> None:
        """
        Establishes secure connection to the satellite data provider (e.g., GEE, Microsoft Planetary Computer).
        Must be implemented by the child class or a core connection mixin.
        """
        pass

    @abstractmethod
    def fetch_data(self, roi: gpd.GeoDataFrame, start_date: str, end_date: str) -> Any:
        """
        Queries and filters satellite assets without downloading the whole heavy dataset.
        
        Args:
            roi (gpd.GeoDataFrame): Region of Interest (bounding box or polygon).
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.
            
        Returns:
            Cloud metadata links or on-the-fly virtual raster arrays.
        """
        pass

    @abstractmethod
    def run_analysis(self, pre_event_data: Any, post_event_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the primary change detection or classification algorithm.
        
        Args:
            pre_event_data: Baseline satellite imagery layer.
            post_event_data: Post-disaster or target time-series imagery layer.
            
        Returns:
            Dict[str, Any]: Metrics, change logs, and risk scores.
        """
        pass

    @abstractmethod
    def generate_outputs(self, analysis_results: Dict[str, Any], output_path: str) -> bool:
        """
        Saves lightweight results into geospatial vector formats (GeoJSON/Shapefile) 
        and extracts key metrics.
        
        Args:
            analysis_results (dict): The results dictionary from run_analysis.
            output_path (str): File system directory to save the output.
            
        Returns:
            bool: True if generation was successful, False otherwise.
        """
        pass

    def execute_pipeline(self, roi: gpd.GeoDataFrame, pre_start: str, pre_end: str, 
                         post_start: Optional[str] = None, post_end: Optional[str] = None, 
                         output_path: str = "data/processed/") -> Dict[str, Any]:
        """
        Standardized execution workflow for all crisis events.
        Orchestrates fetching, analyzing, and saving data smoothly.
        """
        print(f"[INFO] Starting analysis pipeline for {self.__class__.__name__}...")
        
        # 1. Fetch baseline data
        pre_data = self.fetch_data(roi, pre_start, pre_end)
        post_data = None
        
        # 2. Fetch post-event data if it's an acute emergency (like earthquake/flood)
        if post_start and post_end:
            print("[INFO] Fetching post-event satellite assets...")
            post_data = self.fetch_data(roi, post_start, post_end)
            
        # 3. Process the imagery on-the-fly
        results = self.run_analysis(pre_data, post_data)
        
        # 4. Export lightweight metrics and maps
        success = self.generate_outputs(results, output_path)
        
        if success:
            print(f"[SUCCESS] Pipeline completed. Outputs saved to {output_path}")
        else:
            print("[ERROR] Pipeline failed during output generation.")
            
        return results
