"""
Configuration & Constants for Nassau Candy Decision Intelligence System
Author: Anushka Roy
Unified Mentor Machine Learning Internship
"""

import os

# Base paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "Nassau Candy Distributor.csv.xls")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

# 1. Five Master Manufacturing Hubs with GPS Coordinates & Rated Capacities
FACTORIES = {
    "Lot's O' Nuts": {
        "latitude": 32.881893,
        "longitude": -111.768036,
        "state": "Arizona",
        "city": "Casa Grande",
        "region_hub": "West / Pacific",
        "rated_capacity_orders": 3500,
        "max_utilization_threshold": 1.0,
        "description": "Primary western manufacturing facility specializing in nut confection lines."
    },
    "Wicked Choccy's": {
        "latitude": 32.076176,
        "longitude": -81.088371,
        "state": "Georgia",
        "city": "Savannah",
        "region_hub": "Southeast / Atlantic",
        "rated_capacity_orders": 3500,
        "max_utilization_threshold": 1.0,
        "description": "East Coast port-adjacent manufacturing hub for flagship solid chocolates."
    },
    "Sugar Shack": {
        "latitude": 48.119140,
        "longitude": -96.181150,
        "state": "Minnesota",
        "city": "Thief River Falls",
        "region_hub": "Upper Midwest / Interior",
        "rated_capacity_orders": 600,
        "max_utilization_threshold": 1.0,
        "description": "Northern facility handling hard candies, gummies, and seasonal sugar lines."
    },
    "Secret Factory": {
        "latitude": 41.446333,
        "longitude": -90.565487,
        "state": "Illinois",
        "city": "Rock Island",
        "region_hub": "Central Midwest / Interior",
        "rated_capacity_orders": 1800,
        "max_utilization_threshold": 1.0,
        "description": "Midwestern hub equipped for high-speed novelty and specialty confections."
    },
    "The Other Factory": {
        "latitude": 35.117500,
        "longitude": -89.971107,
        "state": "Tennessee",
        "city": "Memphis",
        "region_hub": "Mid-South / Gulf Corridor",
        "rated_capacity_orders": 1600,
        "max_utilization_threshold": 1.0,
        "description": "Centrally located multimodal logistics hub in the Mississippi Delta corridor."
    }
}

# 2. Baseline Legacy Product-to-Factory Mapping (15 SKUs)
PRODUCT_FACTORY_MAP = {
    # Chocolate Division
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar - Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",  # Address data whitespace variation
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    
    # Sugar Division
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    
    # Other Division
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

# 3. Product Division Classification
PRODUCT_DIVISION_MAP = {
    "Wonka Bar - Nutty Crunch Surprise": "Chocolate",
    "Wonka Bar - Fudge Mallows": "Chocolate",
    "Wonka Bar - Scrumdiddlyumptious": "Chocolate",
    "Wonka Bar -Scrumdiddlyumptious": "Chocolate",
    "Wonka Bar - Milk Chocolate": "Chocolate",
    "Wonka Bar - Triple Dazzle Caramel": "Chocolate",
    "Laffy Taffy": "Sugar",
    "SweeTARTS": "Sugar",
    "Nerds": "Sugar",
    "Fun Dip": "Sugar",
    "Everlasting Gobstopper": "Sugar",
    "Hair Toffee": "Sugar",
    "Fizzy Lifting Drinks": "Other",
    "Lickable Wallpaper": "Other",
    "Wonka Gum": "Other",
    "Kazookles": "Other"
}

# 4. Regional Groupings
REGION_STATE_MAP = {
    'Pacific': ['California', 'Washington', 'Oregon', 'Nevada', 'Arizona', 'Idaho', 'Utah', 'Alaska', 'Hawaii'],
    'Atlantic': ['New York', 'Pennsylvania', 'New Jersey', 'Massachusetts', 'Virginia', 'North Carolina', 
                 'South Carolina', 'Georgia', 'Maryland', 'Connecticut', 'Delaware', 'District of Columbia', 
                 'Maine', 'New Hampshire', 'Rhode Island', 'Vermont', 'West Virginia'],
    'Gulf': ['Texas', 'Florida', 'Louisiana', 'Alabama', 'Mississippi'],
    'Interior': ['Illinois', 'Ohio', 'Michigan', 'Indiana', 'Wisconsin', 'Minnesota', 'Missouri', 'Tennessee', 
                 'Kentucky', 'Colorado', 'Iowa', 'Kansas', 'Arkansas', 'Oklahoma', 'Nebraska', 'New Mexico', 
                 'South Dakota', 'North Dakota', 'Montana', 'Wyoming']
}

# 5. Delivery Logistics & Economic Modeling Parameters
DEFAULT_FREIGHT_RATE_PER_MILE = 1.75   # USD per mile standard freight rate
FREIGHT_UNIT_SCALING = 0.05            # Marginal volume scaling factor for multi-unit orders
DEFAULT_WEIGHT_DISTANCE = 0.50         # Distance reduction priority (0.0 to 1.0)
DEFAULT_WEIGHT_COST = 0.30             # Freight cost/profit priority (0.0 to 1.0)
DEFAULT_WEIGHT_CAPACITY = 0.20         # Workload balance priority (0.0 to 1.0)

# 6. Bespoke Executive Design Tokens (Clean Corporate Architecture)
THEME_TOKENS = {
    "bg_dark": "#0F141C",
    "sidebar_bg": "#131926",
    "surface": "#171E2B",
    "surface_card": "#1C2433",
    "surface_elevated": "#222C3D",
    "border": "#263147",
    "border_light": "#334155",
    "border_active": "#3B82F6",
    "text_primary": "#FFFFFF",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "accent_primary": "#2563EB",    # Corporate Cobalt
    "accent_success": "#059669",    # Sage Emerald (Optimal/Savings)
    "accent_danger": "#BE123C",     # Deep Crimson (Baseline/Bottleneck)
    "accent_warning": "#D97706",    # Warm Ochre (Capacity Warning)
    "accent_steel": "#475569"       # Neutral Steel
}
