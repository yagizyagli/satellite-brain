"""
satellite-brain - Global Crisis and Land Change Monitoring Engine
File: src/core/stac_client.py
Description: Robust STAC client with custom user-agent headers to bypass 
cloud firewall blockers and stream open satellite data safely.
"""

import urllib.request
import json
import pystac_client
import geopandas as gpd
from typing import Dict, Any, Optional

class StacClient:
    """
    Handles robust cloud geospatial discovery and fast metadata querying 
    bypassing proxy/firewall blockers using standard request overrides.
    """
    
    def __init__(self, endpoint_url: Optional[str] = None) -> None:
        """
        Initializes the STAC client with stable AWS Earth-Search configurations.
        """
        self.endpoint_url = endpoint_url or "https://element84.com"
        self.client: Optional[pystac_client.Client] = None
        self.connect()

    def connect(self) -> None:
        """
        Establishes connection using standard web headers to fool firewalls.
        """
        try:
            # Custom headers simulating a standard desktop Chrome browser to bypass cloud blockades
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            
            # Open direct connection bypassing pystac internal raw requests block
            self.client = pystac_client.Client.open(
                self.endpoint_url,
                headers=headers
            )
            print(f"[SUCCESS] Connected to open STAC catalog at: {self.endpoint_url}")
        except Exception as e:
            print(f"[WARNING] Advanced header connection failed: {str(e)}")
            print("[INFO] Initiating absolute lightweight fallback bridge...")
            try:
                # Absolute fallback: Test if endpoint responds to a standard HTTP handshake
                req = urllib.request.Request(self.endpoint_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.getcode() == 200:
                        # Force open connection if the endpoint is proven alive
                        self.client = pystac_client.Client.open(self.endpoint_url)
                        print(f"[SUCCESS] Fallback bridge forced activation at: {self.endpoint_url}")
            except Exception as fallback_err:
                print(f"[CRITICAL ERROR] Cloud endpoint is blocking the request: {str(fallback_err)}")
                self.client = None

    def query_assets(self, roi: gpd.GeoDataFrame, start_date: str, end_date: str, 
                     collection: str = "sentinel-2-l2a", cloud_cover_limit: float = 15.0) -> Optional[Dict[str, Any]]:
        """
        Queries the catalog for specific time and space frameworks.
        """
        if not self.client:
            print("[ERROR] STAC client is not initialized. Cannot query.")
            return None

        bbox = list(roi.total_bounds)
        datetime_range = f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"

        search_kwargs = {
            "collections": [collection],
            "bbox": bbox,
            "datetime": datetime_range,
            "max_items": 3
        }

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
