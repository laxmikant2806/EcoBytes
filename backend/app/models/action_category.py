from pydantic import BaseModel, ConfigDict


class ActionCategoryConfig(BaseModel):
    """
    Configuration for each eco-action category.
    Stored in Firestore collection 'action_categories' with document ID = category string.
    This allows admin updates without a code deploy.
    """

    model_config = ConfigDict(populate_by_name=True)

    category: str
    base_points_per_unit: float
    unit: str
    description: str


# Default seed data — used to initialise the Firestore collection on first run.
DEFAULT_CATEGORIES: list[dict] = [
    {"category": "tree_planting",       "base_points_per_unit": 100.0, "unit": "tree",    "description": "Planting trees"},
    {"category": "waste_cleanup",       "base_points_per_unit": 50.0,  "unit": "kg",      "description": "Collecting and disposing of waste"},
    {"category": "recycling",           "base_points_per_unit": 20.0,  "unit": "kg",      "description": "Recycling materials"},
    {"category": "composting",          "base_points_per_unit": 60.0,  "unit": "setup",   "description": "Setting up or maintaining a composting system"},
    {"category": "water_conservation",  "base_points_per_unit": 40.0,  "unit": "action",  "description": "Actions that reduce water usage"},
    {"category": "energy_saving",       "base_points_per_unit": 35.0,  "unit": "kWh",     "description": "Reducing energy consumption"},
    {"category": "carpooling",          "base_points_per_unit": 30.0,  "unit": "trip",    "description": "Sharing car journeys to reduce emissions"},
    {"category": "public_transport",    "base_points_per_unit": 20.0,  "unit": "trip",    "description": "Using public transport instead of private car"},
    {"category": "cycling",             "base_points_per_unit": 25.0,  "unit": "km",      "description": "Cycling instead of driving"},
    {"category": "sustainable_purchase","base_points_per_unit": 15.0,  "unit": "item",    "description": "Purchasing eco-friendly or second-hand items"},
    {"category": "other",               "base_points_per_unit": 10.0,  "unit": "action",  "description": "Other verified eco-friendly actions"},
]
