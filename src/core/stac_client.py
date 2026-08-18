"""
satellite-brain - Global Crisis and Land Change Monitoring Engine
File: src/core/stac_client.py
Description: Fast, lightweight STAC (SpatioTemporal Asset Catalog) client to query 
and stream open-source satellite imagery (Sentinel, Landsat) on-the-fly.
"""

import pystac_client
import planetary_computer
import geopandas as gpd
from typing import Dict, Any, Optional

class StacClient:
    """
    Handles cloud authentication and fast metadata querying for petabyte-scale 
    satellite catalogs without downloading full raster files.
    """
    
    def __init__(self, endpoint_url: Optional[str] = None) -> None:
        """
        Initializes the STAC client. Defaults to Microsoft Planetary Computer.
        """
        # Defaulting to Planetary Computer as it hosts massive open-source Sentinel/Landsat archives
        self.endpoint_url = endpoint_url or "https://microsoft.com"
        self.client: Optional[pystac_client.Client] = None
        self.connect()

    def connect(self) -> None:
        """
        Establishes connection to the cloud geospatial catalog.
        """
        try:
            # Connect and automatically inject Planetary Computer signed tokens for high-speed streaming
            raw_client = pystac_client.Client.open(self.endpoint_url)
            self.client = planetary_computer.sign_inplace(raw_client)
            print(f"[SUCCESS] Connected to STAC catalog at: {self.endpoint_url}")
        except Exception as e:
            print(f"[ERROR] Failed to connect to STAC endpoint: {str(e)}")
            self.client = None

    def query_assets(self, roi: gpd.GeoDataFrame, start_date: str, end_date: str, 
                     collection: str = "sentinel-2-l2a", cloud_cover_limit: float = 15.0) -> Optional[Dict[str, Any]]:
        """
        Queries the catalog for specific time, place, and sensor. 
        Returns lightweight pointers (URLs) to cloud-optimized assets instead of heavy files.
        
        Args:
            roi (gpd.GeoDataFrame): Region of interest polygon.
            start_date (str): Start date string (YYYY-MM-DD).
            end_date (str): End date string (YYYY-MM-DD).
            collection (str): Satellite collection name (e.g., 'sentinel-2-l2a', 'sentinel-1-grd').
            cloud_cover_limit (float): Max acceptable percentage of cloud coverage for optical data.
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary containing signed item links grouped by ID.
        """
        if not self.client:
            print("[ERROR] STAC client is not initialized. Cannot query.")
            return None

        # Convert GeoDataFrame boundary to GeoJSON geometry format for the cloud API query
        bbox = list(roi.total_bounds) # [minx, miny, maxx, maxy]
        datetime_range = f"{start_date}/{end_date}"

        # Setup standard search parameters
        search_kwargs = {
            "collections": [collection],
            "bbox": bbox,
            "datetime": datetime_range,
            "max_items": 5
        }

        # Apply cloud filtering only for optical satellites (like Sentinel-2)
        if "sentinel-2" in collection or "landsat" in collection:
            search_kwargs["query"] = {"eo:cloud_cover": {"lt": cloud_cover_limit}}

        print(f"[INFO] Querying {collection} assets for period: {datetime_range}...")
        
        try:
            search = self.client.search(**search_kwargs)
            items = search.item_collection()
            
            if len(items) == 0:
                print(f"[WARNING] No satellite assets found for the specified criteria.")
                return None

            print(f"[SUCCESS] Found {len(items)} matching satellite scenes in the cloud.")
            
            # Map item IDs to their cloud-streaming asset dictionaries
            asset_map = {}
            for item in items:
                asset_map[item.id] = {
                    "datetime": item.properties.get("datetime"),
                    "cloud_cover": item.properties.get("eo:cloud_cover", 0.0),
                    "assets": {band_name: asset.href for band_name, asset in item.assets.items()}
                }
            return asset_map

        except Exception as e:
            print(f"[ERROR] Error occurred during cloud query: {str(e)}")
            return None
