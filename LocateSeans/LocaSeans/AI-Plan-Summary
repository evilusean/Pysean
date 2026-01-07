### Summary: The "Homestead Hunter" Concept
The goal is to build a **Site Suitability Analysis** tool. Instead of browsing real estate listings manually, this script scans the physical geography of Canada to find land that meets the specific "Permaculture Gold Mine" criteria.

The script identifies "pixels" on a map that satisfy four key requirements:
1.  **Hydraulic Head:** A significant elevation drop over a short distance along a waterway for micro-hydro power.
2.  **Permanent Flow:** Reliable water sources (perennial streams) identified through hydrographic datasets.
3.  **Solar Aspect:** South-facing slopes (135° to 225°) to maximize garden productivity and passive solar gain.
4.  **Infrastructure Proximity:** Proximity to existing roads to minimize the cost of development.

---

### Technical Stack & Languages

#### Primary Language
* **Python 3.x:** The industry standard for Geospatial Data Science and automation.

#### Core Libraries
* **`geemap` / `Google Earth Engine (GEE)`:** Allows for server-side processing of massive satellite and elevation datasets (SRTM/LiDAR) without downloading terabytes of data.
* **`GeoPandas`:** Handles vector data like property boundaries and river lines as tabular data frames.
* **`PySheds`:** Used specifically for hydrological modeling to determine watershed boundaries and flow accumulation.
* **`Rasterio`:** For manipulating "Raster" data (elevation maps and slope heatmaps).
* **`Folium`:** For rendering the final results onto an interactive, clickable leaflet map.

---

### Databases & Data Sources (Canada)

To get high-resolution results in Canada, the script should query the following open-data repositories:

| Data Type | Source Name | Description |
| :--- | :--- | :--- |
| **Waterways** | [CanVec Series](https://open.canada.ca/data/en/dataset/8ba2aa2a-7bb9-4448-b4d7-f164409fe056) | Topographic data including every river, stream, and lake in Canada. |
| **Elevation** | [HRDEM (CanElevation)](https://open.canada.ca/data/en/dataset/957782bf-847c-4644-a757-e383c0057995) | High-Resolution Digital Elevation Models (LiDAR) providing 1-2m accuracy for slope/head. |
| **Agriculture** | [AAFC Crop Inventory](https://open.canada.ca/data/en/dataset/ba264537-4288-461e-bd72-460ce9a633c8) | Identifies land cover types (forest vs. field) and soil suitability. |
| **Roads/Access** | [OpenStreetMap (OSM)](https://download.geofabrik.de/north-america/canada.html) | The most up-to-date database for rural roads and access trails. |

---

### Logic Workflow
1.  **Step 1 (The Sun):** Calculate the **Aspect** from the Elevation Model. Filter for pixels facing South.
2.  **Step 2 (The Water):** Buffer the **CanVec River** lines (e.g., 50m). Intersect this buffer with the South-facing pixels.
3.  **Step 3 (The Power):** Within those intersected areas, calculate the **Slope**. A steep drop next to a high-flow stream indicates micro-hydro potential.
4.  **Step 4 (The Output):** Export coordinates where all conditions overlap as a CSV or GeoJSON for use in Google Maps/Google Earth.
