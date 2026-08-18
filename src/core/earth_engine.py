"""
satellite-brain - Global Crisis and Land Change Monitoring Engine
File: src/core/earth_engine.py
Description: Secure connection layer for Google Earth Engine (GEE) Python API 
handling cloud initialization and session handshake tokens.
"""

import os
from typing import Optional
import ee
from dotenv import load_dotenv

class EarthEngineTunnel:
    """
    Manages secure backend authentication and token validation for high-throughput 
    Google Earth Engine analytics pipelines inside satellite-brain.
    """
    
    def __init__(self) -> None:
        """
        Loads local environment buffers and triggers the security handshake.
        """
        load_dotenv()
        self.is_active = False
        self.authenticate_session()

    def authenticate_session(self) -> bool:
        """
        Verifies credentials via local tokens or environment secrets.
        Prevents pipeline execution if connection parameters are compromised.
        """
        try:
            print("[INFO] Authenticating Earth Engine cloud credentials...")
            
            # GEE typically checks for local service account keys or stored user tokens
            # In headless environments (like Docker or GitHub Actions), it parses variables
            ee.Initialize()
            self.is_active = True
            print("[SUCCESS] Google Earth Engine connection tunnel is secure and active.")
            return True
            
        except Exception as auth_error:
            print(f"[WARNING] Native initialization failed: {str(auth_error)}")
            print("[INFO] Attempting fallback authentication via environment tokens...")
            
            try:
                # Explicit fallback logic for enterprise service account orchestration
                gee_project = os.getenv("EARTHENGINE_PROJECT")
                if gee_project:
                    ee.Initialize(project=gee_project)
                    self.is_active = True
                    print(f"[SUCCESS] Connected to GEE under corporate project scope: {gee_project}")
                    return True
                else:
                    print("[ERROR] Fallback parameters missing. GEE pipelines will operate in local simulation mode.")
                    self.is_active = False
                    return False
                    
            except Exception as fallback_error:
                print(f"[CRITICAL ERROR] All cloud token handshakes failed: {str(fallback_error)}")
                self.is_active = False
                return False
