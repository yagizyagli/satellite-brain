# satellite-brain 🧠

A lightweight, open-source satellite analytics engine engineered for long-term land changes and global emergency tracking. **satellite-brain** processes multi-spectral optical, radar (SAR), and atmospheric assets on-the-fly without downloading heavy geospatial data grids to local filesystems.

---

## 📂 Architecture Overview & Data Flow
The core philosophy of **satellite-brain** is a *Cloud-Native, Zero-Storage Abstract Pipeline*. The system decouples geospatial asset discovery from pixel compute matrices.

### The 4-Stage Core Pipeline:
```text
 [ GeoJSON Boundary (RoI) ]  --> Passed into targeted Disaster Module
              │
              ▼
    [ Core STAC Client ]     --> Queries Cloud Pointers & signs access tokens (On-the-fly)
              │
              ▼
 [ Remote Pixel Streaming ]  --> Fetches only relevant band masks via virtual matrix arrays
              │
              ▼
   [ Vector GeoJSON Output ] --> Saves localized crisis alert vectors directly to filesystem
```

### System Directory Structure:
```text
satellite-brain/
├── .env                     # Local secure credentials token vault (Root level)
├── .env.example             # Global environment config template blueprint
├── data/
│   ├── raw/                 # Input Region of Interest (RoI) boundaries (GeoJSON)
│   └── processed/           # Output lightweight risk vectors and maps
├── src/
│   ├── core/                # Cloud connectivity & auth tunnels (stac_client, earth_engine)
│   └── analyzers/
│       ├── base_analyzer.py # Abstract parent core framework / Project Constitution
│       ├── environment/     # Long-term slow-onset crises (Drought, Deforestation, etc.)
│       └── emergency/       # Combined acute disasters, micro-urban & humanitarian room
└── requirements.txt         # Minimum lightweight GIS dependency stack
```

---

## 🚨 Mapped Capabilities (25 Engines Included)
### ⏳ Long-Term Environmental & Slow Crises
- **`land_degradation`** (Soil erosion & desertification) | **`drought`** (NDWI moisture stress) | **`deforestation`** (Canopy tearing) | **`glacier_melt`** (Polar ice retreat) | **`urban_sprawl`** (Concrete expansion velocity).

### 🌍 Acute Emergencies & Combined Disasters Room
- **Natural Hazards:** `earthquake` (Bridge collapse) | `tsunami` (Coastal recession) | `volcano` (Lava heat) | `landslide` | `sinkhole` (InSAR subsidence) | `flood` (Radar storm masking) | `hurricane` | `tornado` | `avalanche` | `extreme_thermal` (Heat/Frost) | `storm_impact` (Hail/Grid) | `dust_storm`.
- **Micro-Urban Lifelines:** `railway_anomaly` (Metro rail buckling) | `building_collapse` (Spontaneous tilt) | `house_fire` (Industrial flaring).
- **Anthropogenic / Humanitarian Crises:** `war_damage` (City blackouts) | `refugee_camp` (Tent density growth) | `oil_spill` (Ocean slicks) | `air_pollution` (S5P gas columns) | `marine_debris` (Mucilage/Plastics) | `industrial` (Nuclear/Tailings leakage).

---

## 🛠️ Quick Start & Installation

1. **Clone the Repository:**
```bash
git clone https://github.com
cd satellite-brain
```

2. **Setup Credentials Vault:**
```bash
cp .env.example .env
# Open .env and fill in your EarthEngine project scope coordinates
```

3. **Install Lightweight Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run Verification Check inside Codespaces:**
```bash
python tests/test_core.py
```

5. **Execution Blueprint Pattern:**
```python
import geopandas as gpd
from src.analyzers.emergency.earthquake import EarthquakeAnalyzer

# 1. Define target infrastructure coordinates
roi = gpd.read_file("data/raw/target_bridge_boundary.geojson")

# 2. Fire up the processing core
brain = EarthquakeAnalyzer()

# 3. Stream and extract metrics instantly
results = brain.execute_pipeline(
    roi=roi, 
    pre_start="2026-01-01", pre_end="2026-01-10",
    post_start="2026-02-10", post_end="2026-02-18"
)
print(f"Structural Damage Detected: {results['damage_detected']}")
```

---

## 👥 Authors

- **Yağız Yağlı:** [@yagizyagli](https://github.com/yagizyagli)
- **Community Contributions:** Feel free to open an Issue or a Pull Request to scale the algorithmic resilience of the engine.

## 🤝 Scaling & Contributions
To add a new crisis tracking module, inherit from `BaseAnalyzer` inside `src/analyzers/` and override `fetch_data`, `run_analysis`, and `generate_outputs`. 

## 📄 License
This project is licensed under the terms of the open-source **MIT License**.
