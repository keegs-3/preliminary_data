import os
import pandas as pd
import numpy as np

# ========================
# CONFIG: markers and metrics (ADD YOUR FULL CONFIG BELOW)
# ========================

MARKER_CONFIG = {
    "total_cholesterol": {
        "name": "Total Cholesterol",
        "units": "mg/dL",
        "pillar_weights": {
        "Healthful Nutrition": 2,
        "Movement + Exercise": 0,
        "Restorative Sleep": 0,
        "Stress Management": 0,
        "Cognitive Health": 0,
        "Connection + Purpose": 0,
        "Core Care": 7
        },
        "subs": [
            {
                # All patients (no gender split)
                "ranges": [
                    {
                        "label": "optimal",
                        "min": 0,
                        "max": 200,
                        "score_type": "fixed",
                        "score": 10
                    },
                    {
                        "label": "borderline_high",
                        "min": 200.01,
                        "max": 239.99,
                        "score_type": "linear",
                        "score_start": 7,
                        "score_end": 0
                    },
                    {
                        "label": "high",
                        "min": 240,
                        "max": 720,
                        "score_type": "fixed",
                        "score": 0
                    }
                ]
            }
        ]
    },

    "ldl": {
        "name": "LDL",
        "units": "mg/dL",
        "pillar_weights": {
        "Healthful Nutrition": 8,
        "Movement + Exercise": 3,
        "Restorative Sleep": 0,
        "Stress Management": 0,
        "Cognitive Health": 7,
        "Connection + Purpose": 0,
        "Core Care": 8
        },
        "subs": [
            {
                "ranges": [
                    {
                        "label": "optimal",
                        "min": 0,
                        "max": 70,
                        "score_type": "fixed",
                        "score": 10
                    },
                    {
                        "label": "near_optimal",
                        "min": 70,
                        "max": 99.99,
                        "score_type": "linear",
                        "score_start": 7,
                        "score_end": 5.25
                    },
                    {
                        "label": "borderline_high",
                        "min": 100,
                        "max": 129.99,
                        "score_type": "linear",
                        "score_start": 5.25,
                        "score_end": 3.5
                    },
                    {
                        "label": "high",
                        "min": 130,
                        "max": 159.99,
                        "score_type": "linear",
                        "score_start": 3.5,
                        "score_end": 1.75
                    },
                    {
                        "label": "very_high",
                        "min": 160,
                        "max": 189.99,
                        "score_type": "linear",
                        "score_start": 1.75,
                        "score_end": 0
                    },
                    {
                        "label": "critically_high",
                        "min": 190,
                        "max": 570,
                        "score_type": "fixed",
                        "score": 0
                    }
                ]
            }
        ]
    },

    "hdl": {
        "name": "HDL",
        "units": "mg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 4,
            "Restorative Sleep": 0,
            "Stress Management": 0,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 6
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {
                        "label": "critically_low",
                        "min": 0,
                        "max": 40,
                        "score_type": "fixed",
                        "score": 0
                    },
                    {
                        "label": "suboptimal_low",
                        "min": 40,
                        "max": 59.99,
                        "score_type": "linear",
                        "score_start": 0,
                        "score_end": 7
                    },
                    {
                        "label": "optimal",
                        "min": 60,
                        "max": 79.99,
                        "score_type": "fixed",
                        "score": 10
                    },
                    {
                        "label": "suboptimal_high",
                        "min": 80,
                        "max": 99.99,
                        "score_type": "linear",
                        "score_start": 7,
                        "score_end": 0
                    },
                    {
                        "label": "critically_high",
                        "min": 100,
                        "max": 300,
                        "score_type": "fixed",
                        "score": 0
                    }
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {
                        "label": "critically_low",
                        "min": 0,
                        "max": 50,
                        "score_type": "fixed",
                        "score": 0
                    },
                    {
                        "label": "suboptimal_low",
                        "min": 50,
                        "max": 59.99,
                        "score_type": "linear",
                        "score_start": 0,
                        "score_end": 7
                    },
                    {
                        "label": "optimal",
                        "min": 60,
                        "max": 99.99,
                        "score_type": "fixed",
                        "score": 10
                    },
                    {
                        "label": "suboptimal_high",
                        "min": 100,
                        "max": 119.99,
                        "score_type": "linear",
                        "score_start": 7,
                        "score_end": 0
                    },
                    {
                        "label": "critically_high",
                        "min": 120,
                        "max": 360,
                        "score_type": "fixed",
                        "score": 0
                    }
                ]
            }
        ]
    },
    
    "lp(a)": {
        "name": "Lp(a)",
        "units": "nmol/L",
        "pillar_weights": {
            "Healthful Nutrition": 10,
            "Movement + Exercise": 2,
            "Restorative Sleep": 0,
            "Stress Management": 0,
            "Cognitive Health": 4,
            "Connection + Purpose": 0,
            "Core Care": 9
        },
        "subs": [
            {
                "ranges": [
                    {"label": "optimal", "min": 0, "max": 30, "score_type": "fixed", "score": 10},
                    {"label": "borderline_high", "min": 30, "max": 49.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "high", "min": 50, "max": 119.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "very_high", "min": 120, "max": 360, "score_type": "fixed", "score": 0},
                ]
            }
        ]
    },

    "triglycerides": {
        "name": "Triglycerides",
        "units": "mg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 5,
            "Restorative Sleep": 0,
            "Stress Management": 0,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "optimal", "min": 0, "max": 80, "score_type": "fixed", "score": 10},
                    {"label": "near_optimal", "min": 80, "max": 99.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "borderline_high", "min": 100, "max": 149.99, "score_type": "linear", "score_start": 5.25, "score_end": 3.5},
                    {"label": "high", "min": 150, "max": 199.99, "score_type": "linear", "score_start": 3.5, "score_end": 1.75},
                    {"label": "very_high", "min": 200, "max": 499.99, "score_type": "linear", "score_start": 1.75, "score_end": 0},
                    {"label": "critically_high", "min": 500, "max": 1500, "score_type": "fixed", "score": 0},
                ]
            }
        ]
    },

    "apob": {
        "name": "ApoB",
        "units": "mg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 10,
            "Movement + Exercise": 4,
            "Restorative Sleep": 0,
            "Stress Management": 0,
            "Cognitive Health": 5,
            "Connection + Purpose": 0,
            "Core Care": 8
        },
        "subs": [
            {
                "ranges": [
                    {"label": "optimal", "min": 0, "max": 80, "score_type": "fixed", "score": 10},
                    {"label": "borderline_high", "min": 80, "max": 89.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "high", "min": 90, "max": 99.99, "score_type": "linear", "score_start": 5.25, "score_end": 3.5},
                    {"label": "very_high", "min": 100, "max": 119.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "critically_high", "min": 120, "max": 360, "score_type": "fixed", "score": 0},
                ]
            }
        ]
    },

    "omega3_index": {
        "name": "Omega-3 Index",
        "units": "%",
        "pillar_weights": {
            "Healthful Nutrition": 8,
            "Movement + Exercise": 0,
            "Restorative Sleep": 0,
            "Stress Management": 0,
            "Cognitive Health": 6,
            "Connection + Purpose": 0,
            "Core Care": 7
        },
        "subs": [
            {
                "ranges": [
                    {"label": "critically_low", "min": 0, "max": 4, "score_type": "fixed", "score": 0},
                    {"label": "suboptimal", "min": 4, "max": 7.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "optimal", "min": 8, "max": 12, "score_type": "fixed", "score": 10},
                ]
            }
        ]
    },

    "rdw": {
        "name": "RDW",
        "units": "%",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 0,
            "Restorative Sleep": 4,
            "Stress Management": 3,
            "Cognitive Health": 3,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "critically_low", "min": 0, "max": 11, "score_type": "fixed", "score": 0},
                    {"label": "suboptimal_low", "min": 11, "max": 11.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "optimal", "min": 12, "max": 13.5, "score_type": "fixed", "score": 10},
                    {"label": "suboptimal_high", "min": 13.51, "max": 14.5, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "high", "min": 14.51, "max": 15.5, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "critically_high", "min": 15.5, "max": 46.5, "score_type": "fixed", "score": 0},
                ]
            }
        ]
    },
    "magnesium_rbc": {
        "name": "Magnesium (RBC)",
        "units": "mg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 0,
            "Restorative Sleep": 6,
            "Stress Management": 4,
            "Cognitive Health": 7,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "severe_deficiency", "min": 0, "max": 3.5, "score_type": "fixed", "score": 0},
                    {"label": "suboptimal", "min": 3.5, "max": 4.19, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "in_range", "min": 4.2, "max": 5.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 6, "max": 7.5, "score_type": "fixed", "score": 10}
                ]
            }
        ]
    },

    # Matches: "vitamin_d" in generator
    "vitamin_d": {
        "name": "Vitamin D",
        "pillar_weights": {
            "Healthful Nutrition": 8,
            "Movement + Exercise": 0,
            "Restorative Sleep": 6,
            "Stress Management": 0,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "units": "ng/mL",
        "subs": [
            {
                "ranges": [
                    {"label": "deficient", "min": 0, "max": 20, "score_type": "fixed", "score": 0},
                    {"label": "insufficient", "min": 20, "max": 29.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "sufficient", "min": 30, "max": 39.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 40, "max": 59.99, "score_type": "fixed", "score": 10},
                    {"label": "elevated", "min": 60, "max": 79.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "high", "min": 80, "max": 99.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "toxic", "min": 100, "max": 300, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    # Matches: "serum_ferritin" in generator
    "serum_ferritin": {
        "name": "Serum Ferritin",
        "units": "ng/mL",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 0,
            "Restorative Sleep": 5,
            "Stress Management": 4,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "deficient", "min": 0, "max": 30, "score_type": "fixed", "score": 0},
                    {"label": "suboptimal_low", "min": 30, "max": 49.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "optimal", "min": 50, "max": 99.99, "score_type": "fixed", "score": 10},
                    {"label": "suboptimal_high", "min": 100, "max": 149.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "high", "min": 150, "max": 199.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "excess", "min": 200, "max": 600, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    # Matches: "total_iron_binding_capacity" in generator
    "total_iron_binding_capacity": {
        "name": "Total Iron Binding Capacity (TIBC)",
        "units": "µg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 0,
            "Restorative Sleep": 4,
            "Stress Management": 0,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "low", "min": 0, "max": 199.99, "score_type": "fixed", "score": 0},
                    {"label": "borderline_low", "min": 200, "max": 239.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "in_range_low", "min": 240, "max": 249.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 250, "max": 309.99, "score_type": "fixed", "score": 10},
                    {"label": "in_range_high", "min": 310, "max": 449.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "borderline_high", "min": 450, "max": 469.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "high", "min": 470, "max": 1410, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    # Matches: "transferrin_saturation" in generator
    "transferrin_saturation": {
        "name": "Transferrin Saturation",
        "units": "%",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 0,
            "Restorative Sleep": 3,
            "Stress Management": 0,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "low", "min": 0, "max": 15, "score_type": "fixed", "score": 0},
                    {"label": "borderline_low", "min": 15, "max": 19.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "in_range_low", "min": 20, "max": 24.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 25, "max": 34.99, "score_type": "fixed", "score": 10},
                    {"label": "in_range_high", "min": 35, "max": 39.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "borderline_high", "min": 40, "max": 49.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "high", "min": 50, "max": 150, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "hscrp": {
        "name": "hsCRP",
        "units": "mg/L",
        "pillar_weights": {
            "Healthful Nutrition": 8,
            "Movement + Exercise": 0,
            "Restorative Sleep": 4,
            "Stress Management": 6,
            "Cognitive Health": 0,
            "Connection + Purpose": 2,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "optimal", "min": 0, "max": 0.29, "score_type": "fixed", "score": 10},
                    {"label": "low_risk", "min": 0.3, "max": 0.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "moderate_risk", "min": 1, "max": 2.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "high_risk", "min": 3, "max": 9.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "very_high_risk", "min": 10, "max": 30, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "wbc": {
        "name": "White Blood Cell Count",
        "units": "Billion/L",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 3,
            "Restorative Sleep": 2,
            "Stress Management": 5,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 4
        },
        "subs": [
            {
                "ranges": [
                    {"label": "significantly_low", "min": 0, "max": 3, "score_type": "fixed", "score": 0},
                    {"label": "mildly_low", "min": 3, "max": 3.59, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "in_range_lower", "min": 3.6, "max": 3.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 4, "max": 6.99, "score_type": "fixed", "score": 10},
                    {"label": "in_range_upper", "min": 7, "max": 9.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "mildly_elevated", "min": 10, "max": 11.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "significantly_high", "min": 12, "max": 36, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "neutrophils": {
        "name": "Neutrophils",
        "units": "Billion/L",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 1,
            "Restorative Sleep": 0,
            "Stress Management": 5,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "severe_neutropenia", "min": 0, "max": 0.99, "score_type": "fixed", "score": 0},
                    {"label": "mild_neutropenia", "min": 1, "max": 1.79, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "in_range_lower", "min": 1.8, "max": 2.49, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 2.5, "max": 5.49, "score_type": "fixed", "score": 10},
                    {"label": "in_range_upper", "min": 5.5, "max": 6.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "mild_neutrophilia", "min": 7, "max": 9.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "severe_neutrophilia", "min": 10, "max": 30, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "lymphocytes": {
        "name": "Lymphocytes",
        "units": "Billion/L",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 1,
            "Restorative Sleep": 0,
            "Stress Management": 2,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "severe_lymphopenia", "min": 0, "max": 0.49, "score_type": "fixed", "score": 0},
                    {"label": "mild_lymphopenia", "min": 0.5, "max": 0.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "in_range_low", "min": 1, "max": 1.49, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 1.5, "max": 3.49, "score_type": "fixed", "score": 10},
                    {"label": "in_range_high", "min": 3.5, "max": 4.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "elevated", "min": 4.5, "max": 5.59, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "critically_elevated", "min": 5.5, "max": 16.5, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "neut_lymph_ratio": {
        "name": "Neutrocyte/Lymphocyte Ratio",
        "units": "unitless",
        "pillar_weights": {
            "Healthful Nutrition": 4,
            "Movement + Exercise": 3,
            "Restorative Sleep": 2,
            "Stress Management": 6,
            "Cognitive Health": 5,
            "Connection + Purpose": 0,
            "Core Care": 4
        },
        "subs": [
            {
                "ranges": [
                    {"label": "critically_low", "min": 0, "max": 0.49, "score_type": "fixed", "score": 0},
                    {"label": "mildly_low", "min": 0.5, "max": 0.79, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "in_range_low", "min": 0.8, "max": 0.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 1, "max": 2.49, "score_type": "fixed", "score": 10},
                    {"label": "in_range_high", "min": 2.5, "max": 3.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "mildly_elevated", "min": 3.5, "max": 4.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "critically_elevated", "min": 5, "max": 15, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "eosinophils": {
        "name": "Eosinophils",
        "units": "Per Microliter (/µL)",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 1,
            "Restorative Sleep": 0,
            "Stress Management": 2,
            "Cognitive Health": 0,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "very_low", "min": 0, "max": 49.99, "score_type": "fixed", "score": 0},
                    {"label": "in_range_low", "min": 50, "max": 99.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "optimal", "min": 100, "max": 299.99, "score_type": "fixed", "score": 10},
                    {"label": "in_range_high", "min": 300, "max": 499.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "mild_eosinophilia", "min": 500, "max": 1499.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "moderate_eosinophilia", "min": 1500, "max": 4999.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "severe_eosinophilia", "min": 5000, "max": 15000, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "hba1c": {
        "name": "HbA1c",
        "units": "%",
        "pillar_weights": {
            "Healthful Nutrition": 8,
            "Movement + Exercise": 5,
            "Restorative Sleep": 3,
            "Stress Management": 5,
            "Cognitive Health": 7,
            "Connection + Purpose": 0,
            "Core Care": 8
        },
        "subs": [
            {
                "ranges": [
                    {"label": "critically_low", "min": 0, "max": 4.19, "score_type": "fixed", "score": 0},
                    {"label": "suboptimal_low", "min": 4.2, "max": 4.59, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "optimal", "min": 4.6, "max": 5.19, "score_type": "fixed", "score": 10},
                    {"label": "in_range_high", "min": 5.2, "max": 5.59, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "prediabetes", "min": 5.6, "max": 6.4, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "diabetes", "min": 6.5, "max": 19.5, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "fasting_glucose": {
        "name": "Fasting Glucose",
        "units": "mg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 4,
            "Movement + Exercise": 7,
            "Restorative Sleep": 0,
            "Stress Management": 4,
            "Cognitive Health": 5,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "critically_low", "min": 0, "max": 59.99, "score_type": "fixed", "score": 0},
                    {"label": "suboptimal_low", "min": 60, "max": 69.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "in_range_low", "min": 70, "max": 84.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "optimal", "min": 85, "max": 89.99, "score_type": "fixed", "score": 10},
                    {"label": "in_range_high", "min": 90, "max": 99.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "impaired_fasting_glucose", "min": 100, "max": 124.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "diabetes", "min": 150, "max": 450, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "fasting_insulin": {
        "name": "Fasting Insulin",
        "units": "µU/mL",
        "pillar_weights": {
            "Healthful Nutrition": 3,
            "Movement + Exercise": 7,
            "Restorative Sleep": 0,
            "Stress Management": 5,
            "Cognitive Health": 6,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "critically_low", "min": 0, "max": 0.99, "score_type": "fixed", "score": 0},
                    {"label": "suboptimal_low", "min": 1, "max": 1.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "optimal", "min": 2, "max": 5.99, "score_type": "fixed", "score": 10},
                    {"label": "in_range", "min": 6, "max": 9.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "elevated", "min": 10, "max": 14.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "high", "min": 15, "max": 24.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "severe_elevation", "min": 25, "max": 75, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "homa_ir": {
        "name": "HOMA-IR",
        "units": "",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 7,
            "Restorative Sleep": 0,
            "Stress Management": 5,
            "Cognitive Health": 7,
            "Connection + Purpose": 0,
            "Core Care": 0
        },
        "subs": [
            {
                "ranges": [
                    {"label": "critically_low", "min": 0, "max": 0.5, "score_type": "fixed", "score": 0},
                    {"label": "suboptimal_low", "min": 0.5, "max": 0.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "optimal", "min": 1, "max": 1.79, "score_type": "fixed", "score": 10},
                    {"label": "mild_resistance", "min": 1.8, "max": 2.49, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "moderate_resistance", "min": 2.5, "max": 3.49, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "significant_resistance", "min": 3.5, "max": 3.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "diabetes_risk", "min": 4, "max": 12, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "alt": {
        "name": "ALT",
        "units": "U/L",
        "pillar_weights": {
            "Healthful Nutrition": 3,
            "Core Care": 5
        },
        "subs": [
            {
                "sex": "Male",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 9.99, "score_type": "fixed", "score": 0},
                    {"label": "Optimal", "min": 10, "max": 24.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range", "min": 25, "max": 39.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Mild Elevation", "min": 40, "max": 64.99, "score_type": "linear", "score_start": 5.25, "score_end": 3.5},
                    {"label": "Moderate Elevation", "min": 65, "max": 99.99, "score_type": "linear", "score_start": 3.5, "score_end": 1.75},
                    {"label": "Severe Elevation", "min": 100, "max": 119.99, "score_type": "linear", "score_start": 1.75, "score_end": 0},
                    {"label": "Critically High", "min": 120, "max": 360, "score_type": "fixed", "score": 0}
                ]
            },
            {
                "sex": "Female",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 6.99, "score_type": "fixed", "score": 0},
                    {"label": "Optimal", "min": 7, "max": 19.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range", "min": 20, "max": 29.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Mild Elevation", "min": 30, "max": 49.99, "score_type": "linear", "score_start": 5.25, "score_end": 3.5},
                    {"label": "Moderate Elevation", "min": 50, "max": 79.99, "score_type": "linear", "score_start": 3.5, "score_end": 1.75},
                    {"label": "Severe Elevation", "min": 80, "max": 99.99, "score_type": "linear", "score_start": 1.75, "score_end": 0},
                    {"label": "Critically High", "min": 100, "max": 300, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "ggt": {
        "name": "GGT",
        "units": "U/L",
        "pillar_weights": {
            "Healthful Nutrition": 3,
            "Core Care": 4
        },
        "subs": [
            {
                "sex": "Male",
                "ranges": [
                    {"label": "Very High", "min": 100, "max": 300, "score_type": "fixed", "score": 0},
                    {"label": "High", "min": 70, "max": 99.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Moderately Elevated", "min": 50, "max": 69.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "Mildly Elevated", "min": 25, "max": 49.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 10, "max": 24.99, "score_type": "fixed", "score": 10}
                ]
            },
            {
                "sex": "Female",
                "ranges": [
                    {"label": "Very High", "min": 100, "max": 300, "score_type": "fixed", "score": 0},
                    {"label": "High", "min": 70, "max": 99.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Moderately Elevated", "min": 50, "max": 69.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "Mildly Elevated", "min": 25, "max": 49.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 10, "max": 24.99, "score_type": "fixed", "score": 10}
                ]
            }
        ]
    },

    "testosterone": {
        "name": "Testosterone",
        "units": "ng/dL",
        "pillar_weights": {
            "Healthful Nutrition": 1,
            "Movement + Exercise": 7,
            "Restorative Sleep": 3,
            "Stress Management": 3,
            "Core Care": 6
        },
        "subs": [
            {
                "sex": "Male",
                "ranges": [
                    {"label": "Severely Low", "min": 0, "max": 263.99, "score_type": "fixed", "score": 0},
                    {"label": "Borderline Low", "min": 264, "max": 299.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 300, "max": 399.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 400, "max": 799.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 800, "max": 899.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "Borderline High", "min": 900, "max": 999.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Excessively High", "min": 1000, "max": 3000, "score_type": "fixed", "score": 0}
                ]
            },
            {
                "sex": "Female",
                "ranges": [
                    {"label": "Severely Low", "min": 0, "max": 5.99, "score_type": "fixed", "score": 0},
                    {"label": "Borderline Low", "min": 6, "max": 9.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 15, "max": 49.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 50.01, "max": 59.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "Borderline High", "min": 60.01, "max": 69.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Excessively High", "min": 70, "max": 210, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "uric_acid": {
        "name": "Uric Acid",
        "units": "mg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 2
        },
        "subs": [
            {   # Male
                "sex": "Male",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 1.99, "score_type": "fixed", "score": 0},
                    {"label": "Low Uric Acid", "min": 2, "max": 2.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 3, "max": 3.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 4, "max": 4.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 5, "max": 6.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "Mild Hyperuricemia", "min": 6.5, "max": 7.19, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Severe Hyperuricemia", "min": 7.2, "max": 21.6, "score_type": "fixed", "score": 0}
                ]
            },
            {   # Female
                "sex": "Female",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 1.49, "score_type": "fixed", "score": 0},
                    {"label": "Low Uric Acid", "min": 1.5, "max": 1.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 2, "max": 2.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 3, "max": 4.49, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 4.5, "max": 5.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "Mild Hyperuricemia", "min": 5.5, "max": 5.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Severe Hyperuricemia", "min": 6, "max": 18, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "alkaline_phosphatase": {
        "name": "Alkaline Phosphatase",
        "units": "U/L",
        "pillar_weights": {
            "Healthful Nutrition": 2
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 19.99, "score_type": "fixed", "score": 0},
                    {"label": "Suboptimal Low", "min": 20, "max": 39.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 40, "max": 89.99, "score_type": "fixed", "score": 10},
                    {"label": "Mildly Elevated", "min": 90, "max": 119.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Moderately Elevated", "min": 120, "max": 149.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "High", "min": 150, "max": 179.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Critically High", "min": 180, "max": 540, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "albumin": {
        "name": "Albumin",
        "units": "g/dL",
        "pillar_weights": {
            "Healthful Nutrition": 3
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Severe Hypoalbuminemia", "min": 0, "max": 2.49, "score_type": "fixed", "score": 0},
                    {"label": "Hypoalbuminemia", "min": 2.5, "max": 2.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Mildly Low", "min": 3, "max": 3.49, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "In-Range (Low)", "min": 3.5, "max": 3.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 4, "max": 4.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 5, "max": 5.49, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Very High", "min": 5.5, "max": 16.5, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "serum_protein": {
        "name": "Serum Protein",
        "units": "g/dL",
        "pillar_weights": {
            "Healthful Nutrition": 3
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Severe Hypoproteinemia", "min": 0, "max": 5, "score_type": "fixed", "score": 0},
                    {"label": "Mildly Low", "min": 5, "max": 5.49, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 5.5, "max": 5.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Normal", "min": 6, "max": 6.79, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 6.8, "max": 7.49, "score_type": "fixed", "score": 10},
                    {"label": "High Normal", "min": 7.5, "max": 8.29, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Hyperproteinemia", "min": 8.3, "max": 24.9, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "hemoglobin": {
        "name": "Hemoglobin",
        "units": "g/dL",
        "pillar_weights": {
            "Healthful Nutrition": 4,
            "Stress Management": 3
        },
        "subs": [
            {
                "sex": "Male",
                "ranges": [
                    {"label": "Severe Anemia", "min": 0, "max": 10.99, "score_type": "fixed", "score": 0},
                    {"label": "Mild Anemia", "min": 11, "max": 12.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range", "min": 13, "max": 13.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 14, "max": 15.49, "score_type": "fixed", "score": 10},
                    {"label": "High-Normal", "min": 15.5, "max": 16.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessively High Hgb", "min": 17, "max": 51, "score_type": "fixed", "score": 0}
                ]
            },
            {
                "sex": "Female",
                "ranges": [
                    {"label": "Severe Anemia", "min": 0, "max": 9.99, "score_type": "fixed", "score": 0},
                    {"label": "Mild Anemia", "min": 10, "max": 11.49, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range", "min": 11.5, "max": 11.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 12, "max": 14.49, "score_type": "fixed", "score": 10},
                    {"label": "High-Normal", "min": 14.5, "max": 15.49, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessively High Hgb", "min": 15.5, "max": 46.5, "score_type": "fixed", "score": 0}
                ]
            },
        ]
    },
    "hematocrit": {
        "name": "Hematocrit",
        "units": "%",
        "pillar_weights": {
        "Healthful Nutrition": 4,
        "Stress Management": 3,
        "Core Care": 5
        },
        "subs": [
            # MALE
            {
                "sex": "male",
                "ranges": [
                    {"label": "Severe Anemia", "min": 0, "max": 30, "score_type": "fixed", "score": 0},
                    {"label": "Mild Anemia", "min": 30, "max": 37.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 38, "max": 39.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 40, "max": 44.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 45, "max": 49.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "High Hct", "min": 15, "max": 150, "score_type": "fixed", "score": 0}
                ]
            },
            # FEMALE
            {
                "sex": "female",
                "ranges": [
                    {"label": "Severe Anemia", "min": 0, "max": 27.99, "score_type": "fixed", "score": 0},
                    {"label": "Mild Anemia", "min": 28, "max": 34.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 35, "max": 36.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 37, "max": 41.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 42, "max": 45.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "High Hct", "min": 46, "max": 138, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "vitamin_b12": {
        "name": "Vitamin B12",
        "units": "pg/mL",
        "pillar_weights": {
        "Healthful Nutrition": 4,
        "Cognitive Health": 8
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Severe Deficiency", "min": 0, "max": 149.99, "score_type": "fixed", "score": 0},
                    {"label": "Mild Deficiency", "min": 150, "max": 199.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 200, "max": 399.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 400, "max": 799.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 800, "max": 899.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "High", "min": 900, "max": 999.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Excessively High", "min": 1000, "max": 3000, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "folate_serum": {
        "name": "Folate Serum",
        "units": "ng/mL",
        "pillar_weights": {
        "Healthful Nutrition": 4,
        "Cognitive Health": 6
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Severe Deficiency", "min": 0, "max": 2.99, "score_type": "fixed", "score": 0},
                    {"label": "Mild Deficiency", "min": 3, "max": 4.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 5, "max": 7.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 8, "max": 14.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 15, "max": 29.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive Folate", "min": 30, "max": 90, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "folate_rbc": {
        "name": "Folate (RBC)",
        "units": "ng/mL",
        "pillar_weights": {
        "Healthful Nutrition": 4,
        "Cognitive Health": 7
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Severe Deficiency", "min": 0, "max": 99.99, "score_type": "fixed", "score": 0},
                    {"label": "Mild Deficiency", "min": 100, "max": 249.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 250, "max": 399.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 400, "max": 999.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 1000, "max": 1499.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive Folate", "min": 1500, "max": 4500, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "egfr": {
        "name": "eGFR",
        "units": "mL/min/1.73 m²",
        "pillar_weights": {
        "Healthful Nutrition": 1,
        "Core Care": 5
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Kidney Failure (ESRD)", "min": 0, "max": 14.99, "score_type": "fixed", "score": 0},
                    {"label": "Severe Kidney Dysfunction", "min": 15, "max": 29.99, "score_type": "linear", "score_start": 0, "score_end": 1.75},
                    {"label": "Moderate Kidney Dysfunction", "min": 30, "max": 44.99, "score_type": "linear", "score_start": 1.75, "score_end": 3.5},
                    {"label": "Mild Kidney Dysfunction", "min": 45, "max": 59.99, "score_type": "linear", "score_start": 3.5, "score_end": 5.25},
                    {"label": "In-Range", "min": 60, "max": 89.99, "score_type": "linear", "score_start": 5.25, "score_end": 7},
                    {"label": "Optimal", "min": 90, "max": 270, "score_type": "fixed", "score": 10}
                ]
            }
        ]
    },
    "cystatin_c": {
        "name": "Cystatin C",
        "units": "mg/L",
        "pillar_weights": {
        "Healthful Nutrition": 1,
        "Core Care": 5
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Very High Cystatin C", "min": 2, "max": 6, "score_type": "fixed", "score": 0},
                    {"label": "Moderate-Severe Kidney Dysfunction", "min": 1.5, "max": 1.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Mild Elevation", "min": 1.2, "max": 1.49, "score_type": "linear", "score_start": 5.25, "score_end": 3.5},
                    {"label": "In-Range", "min": 0.9, "max": 1.19, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 0.6, "max": 0.89, "score_type": "fixed", "score": 10},
                    {"label": "Low", "min": 0.5, "max": 0.59, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Excessively Low", "min": 0, "max": 0.49, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "bun": {
        "name": "BUN",
        "units": "mg/dL",
        "pillar_weights": {
        "Movement + Exercise": 3,
        "Core Care": 7
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Critically High BUN", "min": 60, "max": 180, "score_type": "fixed", "score": 0},
                    {"label": "Significantly Elevated", "min": 40, "max": 59.99, "score_type": "linear", "score_start": 2.65, "score_end": 0},
                    {"label": "Mildly Elevated BUN", "min": 25, "max": 39.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.65},
                    {"label": "In-Range (High)", "min": 20, "max": 24.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 10, "max": 19.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (low)", "min": 7, "max": 9.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Low", "min": 3, "max": 6.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Excessively Low", "min": 0, "max": 2.99, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "creatinine": {
        "name": "Creatinine",
        "units": "mg/dL",
        "pillar_weights": {
        "Healthful Nutrition": 3
        },
        "subs": [
            # Male, 18-59
            {
                "sex": "male",
                
                "age_high": 59.99,
                "ranges": [
                    {"label": "Low", "min": 0, "max": 0.61, "score_type": "fixed", "score": 0},
                    {"label": "In-Range (low)", "min": 0.62, "max": 0.73, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 0.74, "max": 1.1, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (high)", "min": 1.11, "max": 1.27, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 1.28, "max": 3.84, "score_type": "fixed", "score": 0}
                ]
            },
            # Male, 60+
            {
                "sex": "male",
                "age_low": 60,
                "age_high": 150,
                "ranges": [
                    {"label": "Low", "min": 0, "max": 0.69, "score_type": "fixed", "score": 0},
                    {"label": "In-Range (low)", "min": 0.7, "max": 0.73, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 0.74, "max": 1.1, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (high)", "min": 1.11, "max": 1.27, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 1.28, "max": 3.84, "score_type": "fixed", "score": 0}
                ]
            },
            # Female, 18-59
            {
                "sex": "female",
                
                "age_high": 59.99,
                "ranges": [
                    {"label": "Low", "min": 0, "max": 0.49, "score_type": "fixed", "score": 0},
                    {"label": "In-Range (low)", "min": 0.5, "max": 0.58, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 0.59, "max": 0.9, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (high)", "min": 0.91, "max": 0.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 1, "max": 3, "score_type": "fixed", "score": 0}
                ]
            },
            # Female, 60+
            {
                "sex": "female",
                "age_low": 60,
                "age_high": 150,
                "ranges": [
                    {"label": "Low", "min": 0, "max": 0.56, "score_type": "fixed", "score": 0},
                    {"label": "In-Range (low)", "min": 0.57, "max": 0.58, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 0.59, "max": 0.9, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (high)", "min": 0.91, "max": 0.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 1, "max": 3, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "homocysteine": {
        "name": "Homocysteine",
        "units": "µmol/L",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Cognitive Health": 8,
            "Core Care": 3
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Extremely High", "min": 30, "max": 90, "score_type": "fixed", "score": 0},
                    {"label": "Moderate Elevation", "min": 15, "max": 29.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Mild Elevation", "min": 12, "max": 14.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "In-Range", "min": 10, "max": 11.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 5, "max": 9.99, "score_type": "fixed", "score": 10},
                    {"label": "Low", "min": 3, "max": 4.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Extremely Low", "min": 0, "max": 2.99, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "cortisol_morning": {
        "name": "Cortisol (Morning)",
        "units": "µg/dL",
        "pillar_weights": {
            "Movement + Exercise": 2,
            "Restorative Sleep": 5,
            "Stress Management": 8,
            "Cognitive Health": 6,
            "Connection + Purpose": 5
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Extremely Low", "min": 0, "max": 1.99, "score_type": "fixed", "score": 0},
                    {"label": "Low Morning Cortisol", "min": 2, "max": 4.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 5, "max": 7.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 8, "max": 15.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 16, "max": 17.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High Morning Cortisol", "min": 18, "max": 19.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Extremely High", "min": 20, "max": 60, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "estradiol": {
        "name": "Estradiol",
        "units": "pg/mL",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Stress Management": 3
        },
        "subs": [
            # Premenopausal - Follicular
            {
                "sex": "female",
                "cycle_stage": "follicular",
                "menopausal_status": "premenopausal",
                "ranges": [
                    {"label": "Low", "min": 0, "max": 29.99, "score_type": "fixed", "score": 0},
                    {"label": "Suboptimal", "min": 30, "max": 49.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 50, "max": 99.99, "score_type": "fixed", "score": 10},
                    {"label": "Elevated", "min": 100, "max": 149.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive", "min": 150, "max": 450, "score_type": "fixed", "score": 0}
                ]
            },
            # Premenopausal - Ovulatory
            {
                "sex": "female",
                "cycle_stage": "ovulatory",
                "menopausal_status": "premenopausal",
                "ranges": [
                    {"label": "Low", "min": 0, "max": 99.99, "score_type": "fixed", "score": 0},
                    {"label": "Suboptimal", "min": 100, "max": 199.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 200, "max": 399.99, "score_type": "fixed", "score": 10},
                    {"label": "Elevated", "min": 400, "max": 499.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive", "min": 500, "max": 1500, "score_type": "fixed", "score": 0}
                ]
            },
            # Premenopausal - Luteal
            {
                "sex": "female",
                "cycle_stage": "luteal",
                "menopausal_status": "premenopausal",
                "ranges": [
                    {"label": "Low", "min": 0, "max": 59.99, "score_type": "fixed", "score": 0},
                    {"label": "Suboptimal", "min": 60, "max": 99.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 100, "max": 249.99, "score_type": "fixed", "score": 10},
                    {"label": "Elevated", "min": 250, "max": 299.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive", "min": 300, "max": 900, "score_type": "fixed", "score": 0}
                ]
            },
            # Postmenopausal
            {
                "sex": "female",
                "menopausal_status": "postmenopausal",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 4.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 5, "max": 9.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 10, "max": 19.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 20, "max": 39.99, "score_type": "fixed", "score": 10},
                    {"label": "Elevated", "min": 40, "max": 59.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive", "min": 60, "max": 180, "score_type": "fixed", "score": 0}
                ]
            },
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Very Low", "min": 0, "max": 4.99, "score_type": "fixed", "score": 0},
                    {"label": "In-Range (Low)", "min": 5, "max": 9.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 10, "max": 39.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 40, "max": 59.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Elevated", "min": 60, "max": 180, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "progesterone": {
        "name": "Progesterone",
        "units": "ng/mL",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Stress Management": 3
        },
        "subs": [
            # Premenopausal - Follicular
            {
                "sex": "female",
                "cycle_stage": "follicular",
                "menopausal_status": "premenopausal",
                "ranges": [
                    {"label": "Expected Low", "min": 0, "max": 0.49, "score_type": "fixed", "score": 10},
                    {"label": "Unusually High", "min": 0.5, "max": 1.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "High (Misaligned Phase?)", "min": 2, "max": 6, "score_type": "fixed", "score": 0}
                ]
            },
            # Premenopausal - Ovulatory
            {
                "sex": "female",
                "cycle_stage": "ovulatory",
                "menopausal_status": "premenopausal",
                "ranges": [
                    {"label": "Suboptimal", "min": 0, "max": 1.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 2, "max": 4.99, "score_type": "fixed", "score": 10},
                    {"label": "Elevated", "min": 5, "max": 6.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive", "min": 7, "max": 21, "score_type": "fixed", "score": 0}
                ]
            },
            # Premenopausal - Luteal
            {
                "sex": "female",
                "cycle_stage": "luteal",
                "menopausal_status": "premenopausal",
                "ranges": [
                    {"label": "Low", "min": 0, "max": 9.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 10, "max": 24.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 25, "max": 29.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive", "min": 30, "max": 90, "score_type": "fixed", "score": 0}
                ]
            },
            # Postmenopausal
            {
                "sex": "female",
                "menopausal_status": "postmenopausal",
                "ranges": [
                    {"label": "Very Low", "min": 0, "max": 0.09, "score_type": "fixed", "score": 0},
                    {"label": "Suboptimal", "min": 0.1, "max": 0.49, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 0.5, "max": 1.49, "score_type": "fixed", "score": 10},
                    {"label": "Elevated", "min": 1.5, "max": 2.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Excessive", "min": 3, "max": 9, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "tsh": {
        "name": "TSH",
        "units": "mIU/L",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Restorative Sleep": 4,
            "Stress Management": 4,
            "Cognitive Health": 5,
            "Core Care": 8
        },
        "subs": [
            # General (non-elderly)
            {
                "age_low": 0,
                "age_high": 74.99,
                "ranges": [
                    {"label": "Clinical Hyperthyroid", "min": 0, "max": 0.09, "score_type": "fixed", "score": 0},
                    {"label": "Subclinical Hyperthyroid", "min": 0.1, "max": 0.49, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 0.5, "max": 0.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 1, "max": 2.49, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 2.5, "max": 4.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "Subclinical Hypothyroid", "min": 4.5, "max": 9.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Clinical Hypothyroid", "min": 10, "max": 30, "score_type": "fixed", "score": 0}
                ]
            },
            # Elderly (75+)
            {
                "age_low": 75,
                "age_high": 150,
                "ranges": [
                    {"label": "Clinical Hyperthyroid", "min": 0, "max": 0.09, "score_type": "fixed", "score": 0},
                    {"label": "Subclinical Hyperthyroid", "min": 0.1, "max": 1.19, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "In-Range (Low)", "min": 1.2, "max": 1.49, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 1.5, "max": 2.99, "score_type": "fixed", "score": 10},
                    {"label": "In-Range (High)", "min": 3, "max": 4.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "Subclinical Hypothyroid", "min": 4.5, "max": 10, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Clinical Hypothyroid", "min": 10, "max": 30, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "calcium_serum": {
        "name": "Calcium (Serum)",
        "units": "mg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 4
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low Serum Calcium", "min": 0, "max": 7.99, "score_type": "fixed", "score": 0},
                    {"label": "Mildly Low Serum Calcium", "min": 8, "max": 8.49, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal Serum Calcium", "min": 8.8, "max": 10.19, "score_type": "fixed", "score": 10},
                    {"label": "Mildly Elevated Serum Calcium", "min": 10.2, "max": 10.49, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High Serum Calcium", "min": 10.5, "max": 31.5, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "calcium_ionized": {
        "name": "Calcium (Ionized)",
        "units": "mg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 4
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low Ionized Calcium", "min": 0, "max": 3.99, "score_type": "fixed", "score": 0},
                    {"label": "Mildly Low Ionized Calcium", "min": 4, "max": 4.49, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal Ionized Calcium", "min": 4.5, "max": 5.29, "score_type": "fixed", "score": 10},
                    {"label": "Mildly Elevated Ionized Calcium", "min": 5.3, "max": 5.69, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High Ionized Calcium", "min": 5.7, "max": 17.1, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "dhea_s": {
        "name": "DHEA-S",
        "units": "µg/dL",
        "pillar_weights": {
            "Stress Management": 5,
            "Connection + Purpose": 3
        },
        "subs": [
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Critically Low DHEA-S", "min": 0, "max": 29.99, "score_type": "fixed", "score": 0},
                    {"label": "Mildly Low DHEA-S", "min": 30, "max": 274.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 275, "max": 399.99, "score_type": "fixed", "score": 10},
                    {"label": "Mildly Elevated DHEA-S", "min": 400, "max": 449.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High DHEA-S", "min": 450, "max": 1350, "score_type": "fixed", "score": 0}
                ]
            },
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Critically Low DHEA-S", "min": 0, "max": 149.99, "score_type": "fixed", "score": 0},
                    {"label": "Mildly Low DHEA-S", "min": 150, "max": 349.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 350, "max": 499.99, "score_type": "fixed", "score": 10},
                    {"label": "Mildly Elevated DHEA-S", "min": 500, "max": 699.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High DHEA-S", "min": 700, "max": 2100, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "ast": {
        "name": "AST",
        "units": "U/L",
        "pillar_weights": {
            "Healthful Nutrition": 5
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Critically High", "min": 1000, "max": 3000, "score_type": "fixed", "score": 0},
                    {"label": "Severely Elevated", "min": 500, "max": 999.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Moderately Elevated", "min": 80, "max": 499.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "Mildly Elevated", "min": 25, "max": 79.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 10, "max": 24.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal Low", "min": 7, "max": 9.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Critically Low", "min": 0, "max": 6.99, "score_type": "fixed", "score": 0}
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Critically High", "min": 1000, "max": 3000, "score_type": "fixed", "score": 0},
                    {"label": "Severely Elevated", "min": 80, "max": 999.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Moderately Elevated", "min": 40, "max": 79.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "Mildly Elevated", "min": 20, "max": 39.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 10, "max": 19.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal Low", "min": 7, "max": 9.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Critically Low", "min": 0, "max": 6.99, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "ck": {
        "name": "Creatine Kinase",
        "units": "U/L",
        "pillar_weights": {
            "Movement + Exercise": 5,
            "Stress Management": 3
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Critically High", "min": 1000, "max": 3000, "score_type": "fixed", "score": 0},
                    {"label": "Severely Elevated", "min": 550, "max": 999.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Moderately Elevated", "min": 350, "max": 549.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "Mildly Elevated", "min": 200, "max": 349.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 50, "max": 199.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal Low", "min": 30, "max": 49.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Critically Low", "min": 0, "max": 29.99, "score_type": "fixed", "score": 0}
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Critically High", "min": 1000, "max": 3000, "score_type": "fixed", "score": 0},
                    {"label": "Severely Elevated", "min": 450, "max": 999.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Moderately Elevated", "min": 300, "max": 449.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "Mildly Elevated", "min": 150, "max": 299.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 40, "max": 149.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal Low", "min": 25, "max": 39.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Critically Low", "min": 0, "max": 24.99, "score_type": "fixed", "score": 0}
                ]
            },
            # Athlete (sex-agnostic, flagged by context)
            {
                "unique_condition": "athlete",
                "ranges": [
                    {"label": "Critically High", "min": 1200, "max": 3600, "score_type": "fixed", "score": 0},
                    {"label": "Severely Elevated", "min": 800, "max": 1199.99, "score_type": "linear", "score_start": 2.625, "score_end": 0},
                    {"label": "Moderately Elevated", "min": 600, "max": 799.99, "score_type": "linear", "score_start": 5.25, "score_end": 2.625},
                    {"label": "Mildly Elevated", "min": 400, "max": 599.99, "score_type": "linear", "score_start": 7, "score_end": 5.25},
                    {"label": "Optimal", "min": 100, "max": 399.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal Low", "min": 70, "max": 99.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Critically Low", "min": 0, "max": 69.99, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "sodium": {
        "name": "Sodium",
        "units": "mmol/L",
        "pillar_weights": {
            "Healthful Nutrition": 3
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Severe Hyponatremia", "min": 0, "max": 129.99, "score_type": "fixed", "score": 0},
                    {"label": "Mild Hyponatremia", "min": 130, "max": 134.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 135, "max": 135.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 136, "max": 141.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 142, "max": 143.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "Mild Hypernatremia", "min": 143.5, "max": 144.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Severe Hypernatremia", "min": 145, "max": 435, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "potassium": {
        "name": "Potassium",
        "units": "mmol/L",
        "pillar_weights": {
            "Healthful Nutrition": 3
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Severe Hypokalemia", "min": 0, "max": 2.99, "score_type": "fixed", "score": 0},
                    {"label": "Mild Hypokalemia", "min": 3, "max": 3.49, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 3.5, "max": 3.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 4, "max": 4.69, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 4.7, "max": 5.19, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "Mild Hyperkalemia", "min": 5.2, "max": 5.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Severe Hyperkalemia", "min": 6, "max": 18, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "ferritin": {
        "name": "Ferritin",
        "units": "ng/mL",
        "pillar_weights": {
            "Healthful Nutrition": 4,
            "Stress Management": 4,
            "Core Care": 4
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 14.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 15, "max": 29.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 30, "max": 39.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 40, "max": 99.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 100, "max": 149.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 150, "max": 199.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 200, "max": 600, "score_type": "fixed", "score": 0}
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 9.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 10, "max": 19.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 20, "max": 39.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 40, "max": 99.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 100, "max": 124.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 125, "max": 149.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 150, "max": 450, "score_type": "fixed", "score": 0}
                ]
            },
            # Athlete (context flagged)
            {
                "unique_condition": "athlete",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 19.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 20, "max": 29.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 30, "max": 34.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 35, "max": 99.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 100, "max": 124.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 125, "max": 149.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 150, "max": 450, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "iron": {
        "name": "Iron",
        "units": "µg/dL",
        "pillar_weights": {
            "Healthful Nutrition": 5
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 39.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 40, "max": 54.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 55, "max": 79.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 80, "max": 129.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 130, "max": 149.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 150, "max": 174.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 175, "max": 525, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "mch": {
        "name": "Mean Corpuscular Hemoglobin (MCH)",
        "units": "pg/cell",
        "pillar_weights": {
            "Healthful Nutrition": 4
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 23.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 24, "max": 26.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 27, "max": 29.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 30, "max": 32.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 33, "max": 34.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 34.5, "max": 35.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 36, "max": 108, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "mchc": {
        "name": "Mean Corpuscular Hemoglobin Concentration (MCHC)",
        "units": "g/dL",
        "pillar_weights": {
            "Healthful Nutrition": 3
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 29.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 30, "max": 31.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 32, "max": 33.49, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 33.5, "max": 35.49, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 35.5, "max": 36.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 36.5, "max": 37.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 38, "max": 114, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "mcv": {
        "name": "Mean Corpuscular Volume",
        "units": "fL",
        "pillar_weights": {
            "Healthful Nutrition": 4
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 69.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 70, "max": 79.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 80, "max": 84.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 85, "max": 94.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 95, "max": 99.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 100, "max": 104.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 105, "max": 315, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "rbc": {
        "name": "Red Blood Cell Count",
        "units": "million/µL",
        "pillar_weights": {
            "Healthful Nutrition": 2
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 3.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 4, "max": 4.39, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 4.4, "max": 4.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 5, "max": 5.69, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 5.7, "max": 5.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 6, "max": 6.49, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 6.5, "max": 19.5, "score_type": "fixed", "score": 0}
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 3.79, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 3.8, "max": 4.19, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 4.2, "max": 4.59, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 4.6, "max": 5.29, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 5.3, "max": 5.49, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 5.5, "max": 5.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 6, "max": 18, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "platelet": {
        "name": "Platelet Count",
        "units": "x 10⁹/L",
        "pillar_weights": {
            "Healthful Nutrition": 3
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 99.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 100, "max": 149.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 150, "max": 199.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 200, "max": 299.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 300, "max": 399.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 400, "max": 499.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 500, "max": 1500, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "free_testosterone": {
        "name": "Free Testosterone",
        "units": "ng/dL",
        "pillar_weights": {
            "Healthful Nutrition": 3,
            "Movement + Exercise": 3,
            "Restorative Sleep": 3
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 4.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 5, "max": 7.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Normal", "min": 8, "max": 11.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 12, "max": 19.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 20, "max": 29.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High", "min": 30, "max": 90, "score_type": "fixed", "score": 0}
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 0.49, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 0.5, "max": 0.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 1, "max": 1.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 2, "max": 2.49, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High", "min": 2.5, "max": 7.5, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "shbg": {
        "name": "SHBG",
        "units": "nmol/L",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Stress Management": 4
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 9.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 10, "max": 17.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 18, "max": 34.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 35, "max": 54.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High", "min": 55, "max": 175, "score_type": "fixed", "score": 0}
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 19.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 20, "max": 39.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 40, "max": 79.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 80, "max": 124.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High", "min": 125, "max": 375, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "vo2_max": {
        "name": "VO2 Max",
        "units": "ml/kg/min",
        "pillar_weights": {
            "Movement + Exercise": 8,
            "Cognitive Health": 4
        },
        "subs": [
            # Male - 20s
            {
                "sex": "male", "age_low": 20, "age_high": 29.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 34.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 35, "max": 41.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 42, "max": 49.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 50, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Male - 30s
            {
                "sex": "male", "age_low": 30, "age_high": 39.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 32.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 33, "max": 39.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 40, "max": 46.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 47, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Male - 40s
            {
                "sex": "male", "age_low": 40, "age_high": 49.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 29.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 30, "max": 35.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 36, "max": 43.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 44, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Male - 50s
            {
                "sex": "male", "age_low": 50, "age_high": 59.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 27.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 28, "max": 33.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 34, "max": 39.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 40, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Male - 60s
            {
                "sex": "male", "age_low": 60, "age_high": 69.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 24.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 25, "max": 29.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 30, "max": 35.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 36, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Male - 70s
            {
                "sex": "male", "age_low": 70, "age_high": 79.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 21.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 22, "max": 27.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 28, "max": 31.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 32, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Male - 80s
            {
                "sex": "male", "age_low": 80, "age_high": 89.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 19.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 20, "max": 21.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 22, "max": 24.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 25, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Male - 90s
            {
                "sex": "male", "age_low": 90, "age_high": 99.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 17.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 18, "max": 19.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 20, "max": 22.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 23, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },

            # Female - 20s
            {
                "sex": "female", "age_low": 20, "age_high": 29.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 29.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 30, "max": 36.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 37, "max": 44.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 45, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Female - 30s
            {
                "sex": "female", "age_low": 30, "age_high": 39.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 27.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 28, "max": 34.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 35, "max": 41.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 42, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Female - 40s
            {
                "sex": "female", "age_low": 40, "age_high": 49.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 25.66, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 26, "max": 32.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 33, "max": 38.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 39, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Female - 50s
            {
                "sex": "female", "age_low": 50, "age_high": 59.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 23.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 24, "max": 29.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 30, "max": 35.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 36, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Female - 60s
            {
                "sex": "female", "age_low": 60, "age_high": 69.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 21.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 22, "max": 26.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 27, "max": 31.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 32, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Female - 70s
            {
                "sex": "female", "age_low": 70, "age_high": 79.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 19.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 20, "max": 25.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 26, "max": 27.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 28, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Female - 80s
            {
                "sex": "female", "age_low": 80, "age_high": 89.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 15.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 16, "max": 17.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 18, "max": 20.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 21, "max": 100, "score_type": "fixed", "score": 10}
                ]
            },
            # Female - 90s
            {
                "sex": "female", "age_low": 90, "age_high": 99.99,
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 13.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 14, "max": 15.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal", "min": 16, "max": 18.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 19, "max": 100, "score_type": "fixed", "score": 10}
                ]
            }
        ]
    },
    "percent_body_fat": {
        "name": "% Bodyfat",
        "units": "%",
        "pillar_weights": {
            "Healthful Nutrition": 7,
            "Movement + Exercise": 6,
            "Restorative Sleep": 4,
            "Stress Management": 4,
            "Cognitive Health": 5
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Excessively Low", "min": 0, "max": 4.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 5, "max": 9.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 10, "max": 14.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 15, "max": 19.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 20, "max": 24.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 25, "max": 29.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Excessively High", "min": 30, "max": 100, "score_type": "fixed", "score": 0}
                ]
            },
            # Female - Premenopausal
            {
                "sex": "female", "menopausal_status": "premenopausal",
                "ranges": [
                    {"label": "Excessively Low", "min": 0, "max": 12.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 13, "max": 17.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 18, "max": 22.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 23, "max": 27.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 28, "max": 32.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 33, "max": 37.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Excessively High", "min": 38, "max": 100, "score_type": "fixed", "score": 0}
                ]
            },
            # Female - Postmenopausal
            {
                "sex": "female", "menopausal_status": "postmenopausal",
                "ranges": [
                    {"label": "Excessively Low", "min": 0, "max": 14.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 15, "max": 19.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 20, "max": 24.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 25, "max": 29.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 30, "max": 34.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 35, "max": 39.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Excessively High", "min": 40, "max": 100, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "smm_to_ffm": {
        "name": "Skeletal Muscle Mass to Fat-Free Mass",
        "units": "%",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 4,
            "Restorative Sleep": 3,
            "Stress Management": 3
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 64.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 65, "max": 69.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 70, "max": 74.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 75, "max": 89, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 89, "max": 91.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 92, "max": 94.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 95, "max": 200, "score_type": "fixed", "score": 0}
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 59.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 60, "max": 64.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 65, "max": 69.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 70, "max": 84.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 85, "max": 87.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 88, "max": 89.99, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 90, "max": 200, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "hip_to_waist": {
        "name": "Hip-to-Waist Ratio",
        "units": "",
        "pillar_weights": {
            "Healthful Nutrition": 6,
            "Movement + Exercise": 6,
            "Restorative Sleep": 4,
            "Stress Management": 4,
            "Cognitive Health": 4
        },
        "subs": [
            # Male
            {
                "sex": "male",
                "ranges": [
                    {"label": "Excessively Low", "min": 0, "max": 0.79, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 0.8, "max": 0.84, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 0.85, "max": 0.89, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 0.9, "max": 0.94, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 0.95, "max": 0.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 1, "max": 1.09, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Excessively High", "min": 1.1, "max": 2, "score_type": "fixed", "score": 0}
                ]
            },
            # Female
            {
                "sex": "female",
                "ranges": [
                    {"label": "Excessively Low", "min": 0, "max": 0.64, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 0.65, "max": 0.69, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 0.7, "max": 0.74, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 0.75, "max": 0.79, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 0.8, "max": 0.84, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 0.85, "max": 0.89, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Excessively High", "min": 0.9, "max": 2, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "bmi": {
        "name": "BMI",
        "units": "kg/m2",
        "pillar_weights": {
            "Healthful Nutrition": 7,
            "Movement + Exercise": 7,
            "Restorative Sleep": 5,
            "Stress Management": 4,
            "Cognitive Health": 6
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 16.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 17, "max": 18.49, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Suboptimal Low", "min": 18.5, "max": 21.49, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 21.5, "max": 24.99, "score_type": "fixed", "score": 10},
                    {"label": "Suboptimal High", "min": 25, "max": 27.99, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High", "min": 28, "max": 29.9, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "Critically High", "min": 30, "max": 100, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "resting_heart_rate": {
        "name": "Resting Heart Rate",
        "units": "bpm",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 3,
            "Restorative Sleep": 2,
            "Stress Management": 4
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Critically Low", "min": 0, "max": 39.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 40, "max": 49.99, "score_type": "linear", "score_start": 0, "score_end": 7},
                    {"label": "Optimal", "min": 50, "max": 64.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 66, "max": 79.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High", "min": 80, "max": 200, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "blood_pressure_systolic": {
        "name": "Blood Pressure - Systolic",
        "units": "mmHg",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 5,
            "Restorative Sleep": 3,
            "Stress Management": 4,
            "Core Care": 8
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Optimal", "min": 0, "max": 119.99, "score_type": "fixed", "score": 10},
                    {"label": "Elevated", "min": 120, "max": 129, "score_type": "linear", "score_start": 7, "score_end": 3.5},
                    {"label": "High (Stage 1)", "min": 130, "max": 139, "score_type": "linear", "score_start": 3.5, "score_end": 0},
                    {"label": "High (Stage 2)", "min": 140, "max": 300, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "blood_pressure_diastolic": {
        "name": "Blood Pressure - Diastolic",
        "units": "mmHg",
        "pillar_weights": {
            "Healthful Nutrition": 5,
            "Movement + Exercise": 5,
            "Restorative Sleep": 3,
            "Stress Management": 3,
            "Core Care": 8
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Optimal", "min": 0, "max": 79.99, "score_type": "fixed", "score": 10},
                    {"label": "High (Stage 1)", "min": 80, "max": 89.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "High (Stage 2)", "min": 90, "max": 300, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "visceral_fat": {
        "name": "Visceral Fat",
        "units": "",
        "pillar_weights": {
            "Healthful Nutrition": 2
        },
        "subs": [
            {
                "ranges": [
                    {"label": "Optimal", "min": 0, "max": 9.99, "score_type": "fixed", "score": 10},
                    {"label": "Elevated", "min": 10, "max": 14.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "High", "min": 15, "max": 200, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
    "grip_strength": {
        "name": "Grip Strength",
        "units": "kg",
        "pillar_weights": {
            "Movement + Exercise": 7,
            "Cognitive Health": 5
        },
        "subs": [
            # Males, age bands
            {"sex": "male", "age_low": 20, "age_high": 29.99,
            "ranges": [
                {"label": "Optimal", "min": 48, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 42, "max": 47.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 41.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "male", "age_low": 30, "age_high": 39.99,
            "ranges": [
                {"label": "Optimal", "min": 46, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 40, "max": 45.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 39.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "male", "age_low": 40, "age_high": 49.99,
            "ranges": [
                {"label": "Optimal", "min": 44, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 38, "max": 43.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 37.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "male", "age_low": 50, "age_high": 59.99,
            "ranges": [
                {"label": "Optimal", "min": 42, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 36, "max": 41.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 35.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "male", "age_low": 60, "age_high": 69.99,
            "ranges": [
                {"label": "Optimal", "min": 40, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 34, "max": 39.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 33.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "male", "age_low": 70, "age_high": 79.99,
            "ranges": [
                {"label": "Optimal", "min": 38, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 32, "max": 37.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 31.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "male", "age_low": 80, "age_high": 89.99,
            "ranges": [
                {"label": "Optimal", "min": 28, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 23, "max": 27.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 22.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "male", "age_low": 90, "age_high": 99.99,
            "ranges": [
                {"label": "Optimal", "min": 22, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 18, "max": 21.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 17.99, "score_type": "fixed", "score": 0}
            ]},

            # Females, age bands
            {"sex": "female", "age_low": 20, "age_high": 29.99,
            "ranges": [
                {"label": "Optimal", "min": 28, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 22, "max": 27.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 21.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "female", "age_low": 30, "age_high": 39.99,
            "ranges": [
                {"label": "Optimal", "min": 26, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 20, "max": 25.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 19.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "female", "age_low": 40, "age_high": 49.99,
            "ranges": [
                {"label": "Optimal", "min": 24, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 18, "max": 23.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 17.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "female", "age_low": 50, "age_high": 59.99,
            "ranges": [
                {"label": "Optimal", "min": 22, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 16, "max": 21.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 15.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "female", "age_low": 60, "age_high": 69.99,
            "ranges": [
                {"label": "Optimal", "min": 20, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 14, "max": 19.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 13.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "female", "age_low": 70, "age_high": 79.99,
            "ranges": [
                {"label": "Optimal", "min": 18, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 12, "max": 17.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 11.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "female", "age_low": 80, "age_high": 89.99,
            "ranges": [
                {"label": "Optimal", "min": 17, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 13, "max": 15.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 12.99, "score_type": "fixed", "score": 0}
            ]},
            {"sex": "female", "age_low": 90, "age_high": 99.99,
            "ranges": [
                {"label": "Optimal", "min": 14, "max": 200, "score_type": "fixed", "score": 10},
                {"label": "Moderate", "min": 11, "max": 13.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                {"label": "Low", "min": 0, "max": 10.99, "score_type": "fixed", "score": 0}
            ]}
        ]
    },
    "hrv": {
        "name": "HRV",
        "units": "",
        "pillar_weights": {
            "Movement + Exercise": 2,
            "Restorative Sleep": 6,
            "Stress Management": 6,
            "Cognitive Health": 8
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Critically Low", "min": 0.00, "max": 19.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 20.00, "max": 39.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Moderate", "min": 40.00, "max": 59.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 60.00, "max": 180.00, "score_type": "fixed", "score": 10}
                ]
            }
        ]
    },

    "rem_sleep": {
        "name": "REM Sleep",
        "units": "minutes",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 2,
            "Restorative Sleep": 7,
            "Stress Management": 6,
            "Cognitive Health": 6
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Critically Low", "min": 0.00, "max": 59.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 60.00, "max": 89.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Moderate", "min": 90.00, "max": 119.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 120.00, "max": 149.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 150.00, "max": 179.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High", "min": 180.00, "max": 540.00, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },

    "deep_sleep": {
        "name": "Deep Sleep",
        "units": "minutes",
        "pillar_weights": {
            "Healthful Nutrition": 2,
            "Movement + Exercise": 2,
            "Restorative Sleep": 7,
            "Stress Management": 6,
            "Cognitive Health": 7
        },
        "subs": [
            {
                
                
                
                "ranges": [
                    {"label": "Critically Low", "min": 0.00, "max": 39.99, "score_type": "fixed", "score": 0},
                    {"label": "Low", "min": 40.00, "max": 59.99, "score_type": "linear", "score_start": 0, "score_end": 3.5},
                    {"label": "Moderate", "min": 60.00, "max": 89.99, "score_type": "linear", "score_start": 3.5, "score_end": 7},
                    {"label": "Optimal", "min": 90.00, "max": 119.99, "score_type": "fixed", "score": 10},
                    {"label": "High", "min": 120.00, "max": 149.99, "score_type": "linear", "score_start": 7, "score_end": 0},
                    {"label": "Critically High", "min": 150.00, "max": 450.00, "score_type": "fixed", "score": 0}
                ]
            }
        ]
    },
}

import os
import pandas as pd

def select_sub(marker_subs, patient):
    for sub in marker_subs:
        match = True
        for key, val in sub.items():
            if key == "ranges":
                continue
            # Age low/high/min/max
            if key in {"age_low", "age_min"}:
                try:
                    if float(patient.get("age", -999)) < val:
                        match = False
                        break
                except Exception:
                    match = False
                    break
                continue
            if key in {"age_high", "age_max"}:
                try:
                    if float(patient.get("age", 9999)) > val:
                        match = False
                        break
                except Exception:
                    match = False
                    break
                continue
            # Wildcard in config
            if val in ("all", None):
                continue
            # Only match on keys that exist in the patient
            if key not in patient:
                continue
            patient_val = patient.get(key)
            # String case-insensitive
            if isinstance(val, str) and isinstance(patient_val, str):
                if patient_val.lower() != val.lower():
                    match = False
                    break
            else:
                if patient_val != val:
                    match = False
                    break
        if match:
            return sub

    print("No matching sub found!")
    print("Patient:", patient)
    print("All subs for this marker:")
    for sub in marker_subs:
        print(sub)

    return None

def find_band(ranges, value):
    """
    Find which scoring band applies for a value.
    """
    for band in ranges:
        if band["min"] <= value <= band["max"]:
            return band
    return None

def get_score_from_band(band, value):
    if band["score_type"] == "fixed":
        return band["score"] / 10  # Divide by 10 here
    elif band["score_type"] == "linear":
        rng = band["max"] - band["min"]
        if rng == 0:
            return band.get("score_start", 0) / 10  # And here
        score = band["score_start"] + ((value - band["min"]) / rng) * (band["score_end"] - band["score_start"])
        return score / 10  # And here
    else:
        return None

def get_max_score_for_sub(sub):
    max_score = 0
    for band in sub["ranges"]:
        if band["score_type"] == "fixed":
            max_score = max(max_score, band.get("score", 0) / 10)  # Divide by 10
        elif band["score_type"] == "linear":
            max_score = max(max_score, band.get("score_start", 0) / 10, band.get("score_end", 0) / 10)  # Divide by 10
    return max_score

def score_marker(marker, value, patient):
    config = MARKER_CONFIG.get(marker)
    if not config:
        return {"marker": marker, "error": f"Marker {marker} not defined."}
    sub = select_sub(config["subs"], patient)
    if not sub:
        return {"marker": marker, "error": f"No sub-config for marker {marker} and this patient context."}
    band = find_band(sub["ranges"], value)
    if not band:
        return {
            "marker": marker,
            "name": config["name"],
            "units": config["units"],
            "value": value,
            "label": "out_of_range",
            "score": 0,
            "range_min": None,
            "range_max": None,
            "score_type": None
        }
    score = get_score_from_band(band, value)
    return {
        "marker": marker,
        "name": config["name"],
        "units": config["units"],
        "value": value,
        "label": band["label"],
        "score": score,
        "range_min": band["min"],
        "range_max": band["max"],
        "score_type": band["score_type"]
    }

def compute_pillar_scores(patient_row, marker_config):
    """
    For a given patient_row (from df), compute raw and normalized pillar scores.
    Returns: dict {pillar: (raw_sum, max_sum, normalized_score)}
    """
    pillar_sums = {}
    pillar_max = {}

    # Build a patient dict (for sex, menopause, etc.)
    patient = {k: str(patient_row.get(k, "")).lower() for k in ["sex", "menopausal_status", "age", "cycle_stage", "unique_condition"]}

    for marker_key, config in marker_config.items():
        value = patient_row.get(marker_key)
        if value is None or pd.isnull(value):
            continue
        sub = select_sub(config["subs"], patient)
        if not sub:
            continue
        band = find_band(sub["ranges"], value)
        if not band:
            continue
        score = get_score_from_band(band, value)
        max_score = get_max_score_for_sub(sub)
        for pillar, weight in config.get("pillar_weights", {}).items():
            if weight and weight > 0:
                pillar_sums.setdefault(pillar, 0)
                pillar_max.setdefault(pillar, 0)
                pillar_sums[pillar] += score * weight
                pillar_max[pillar] += max_score * weight

    # Build output dict with normalized pillar scores (0–1 or None if not possible)
    pillar_results = {}
    for pillar in pillar_sums:
        total = pillar_sums[pillar]
        max_total = pillar_max[pillar]
        normalized = total / max_total if max_total > 0 else None
        pillar_results[pillar] = {
            "raw_sum": total,
            "max_sum": max_total,
            "score": normalized
        }
    return pillar_results

def calculate_precise_phenoage(row):
    """Calculate PhenoAge and DNAm PhenoAge from lab markers"""
    try:
        albumin = row['albumin'] * 10
        creatinine = row['creatinine'] * 88.4
        glucose = row['fasting_glucose'] * 0.0555
        crp = row['hscrp'] * 0.1
        lymph_pct = row['lymphocyte_percent']
        rdw = row['rdw']
        alk_phos = row['alkaline_phosphatase']
        wbc = row['wbc']
        age = row['age']
        mcv = row['mcv']

        xb = (
            -19.9067
            + (albumin * -0.0336)
            + (creatinine * 0.0095)
            + (glucose * 0.1953)
            + (np.log(max(crp, 0.001)) * 0.0954)
            + (lymph_pct * -0.012)
            + (rdw * 0.3306)
            + (alk_phos * 0.0019)
            + (wbc * 0.0554)
            + (age * 0.0804)
            + (mcv * 0.0268)
        )

        # Now match the Excel mortality score!
        numerator = np.exp(xb) * (np.exp(0.0076927 * 120) - 1)
        denominator = 0.0076927
        mort_score = 1 - np.exp(-numerator / denominator)
        mort_score = min(mort_score, 1 - 1e-10)

        phenoage = 141.50225 + np.log(-0.00553 * np.log(1 - mort_score)) / 0.09165

        denom = 1 + 1.28047 * np.exp(0.0344329 * (-182.344 + phenoage))
        dnam_phenoage = phenoage / denom

        return phenoage, dnam_phenoage
    except Exception as e:
        print("Precise PhenoAge calculation error:", e)
        return np.nan, np.nan

# ========================
# MAIN SCRIPT
# ========================

if __name__ == "__main__":

    # Use relative paths from the script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "dummy_lab_results_full.csv")
    
    # Use your existing folder structure
    markers_output_dir = os.path.join(base_dir, "WellPath_Score_Markers")
    
    # Updated output paths
    out_path = os.path.join(markers_output_dir, "scored_lab_results.csv")
    pillar_out_path = os.path.join(markers_output_dir, "pillar_scores.csv")

    # Check if data file exists
    if not os.path.exists(data_path):
        print(f"⚠️  Data file not found: {data_path}")
        print("Please place your data file in the data/ folder and run again.")
        exit(1)

    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)

    results = []
    pillar_results_list = []
    all_scores = []

    # --- First Pass: Per-marker scoring (raw + weighted + max) ---
    print("Processing patient scores...")
    for idx, row in df.iterrows():
        # --- Context for marker scoring ---
        patient = {
            "sex": str(row.get("sex", "")).lower(),
            "age": float(row.get("age", -999)),
            "menopausal_status": str(row.get("menopausal_status", "")).lower() if "menopausal_status" in row else None,
            "cycle_stage": str(row.get("cycle_stage", "")).lower() if "cycle_stage" in row else None,
            "unique_condition": str(row.get("unique_condition", "")).lower() if "unique_condition" in row else None,
        }
        patient_id = row.get("patient_id", f"row_{idx}")

        patient_result = {"patient_id": patient_id}

        # Score all markers for this patient (original approach for detailed results)
        for marker in MARKER_CONFIG:
            value = row.get(marker, None)
            if pd.isnull(value):
                continue
            result = score_marker(marker, value, patient)
            result["patient_id"] = patient_id
            results.append(result)

        # Score all markers with max calculations for gap analysis
        for marker in MARKER_CONFIG:
            value = row.get(marker, None)
            config = MARKER_CONFIG[marker]
            
            # Calculate max possible score for this marker and patient context
            sub = select_sub(config["subs"], patient)
            max_possible_score = 0
            if sub:
                max_possible_score = get_max_score_for_sub(sub)
            
            # Score the actual marker value
            if pd.isnull(value):
                # If no value, set actual scores to 0 but keep max
                score = 0
            else:
                result = score_marker(marker, value, patient)
                score = result.get("score", 0)
            
            # Add to patient result for each pillar this marker contributes to
            for pillar, weight in config.get("pillar_weights", {}).items():
                if weight and weight > 0:
                    patient_result[f"{marker}_{pillar}_raw"] = score
                    patient_result[f"{marker}_{pillar}_weighted"] = score * weight
                    patient_result[f"{marker}_{pillar}_max"] = max_possible_score * weight

        all_scores.append(patient_result)

        # Calculate per-pillar scores for this patient (original approach)
        per_pillar = compute_pillar_scores(row, MARKER_CONFIG)
        per_pillar_out = {"patient_id": patient_id}
        for pillar, vals in per_pillar.items():
            per_pillar_out[f"{pillar}_score"] = vals["score"]
            per_pillar_out[f"{pillar}_raw"] = vals["raw_sum"]
            per_pillar_out[f"{pillar}_max"] = vals["max_sum"]

        # --- Calculate PhenoAge and DNAm PhenoAge (ONCE PER PATIENT) ---
        phenoage, dnam_phenoage = calculate_precise_phenoage(row)
        per_pillar_out["phenoage"] = phenoage
        per_pillar_out["dnam_phenoage"] = dnam_phenoage

        pillar_results_list.append(per_pillar_out)

    # --- Create detailed marker scoring DataFrame ---
    df_debug = pd.DataFrame(all_scores).fillna(0)
    df_debug.to_csv(os.path.join(markers_output_dir, "scored_markers_with_max.csv"), index=False)
    print("✓ Per-marker raw, weighted, and max scores saved to WellPath_Score_Markers/scored_markers_with_max.csv")

    # --- Second Pass: Aggregate pillar scores and calculate percentages ---
    pillar_names = [
        "Healthful Nutrition", "Movement + Exercise", "Restorative Sleep", 
        "Cognitive Health", "Stress Management", "Connection + Purpose", "Core Care"
    ]

    for pillar in pillar_names:
        # Sum weighted scores
        weighted_cols = [col for col in df_debug.columns if col.endswith(f'_{pillar}_weighted')]
        if weighted_cols:
            df_debug[f"{pillar}_Total"] = df_debug[weighted_cols].sum(axis=1)
        else:
            df_debug[f"{pillar}_Total"] = 0
        
        # Sum max scores  
        max_cols = [col for col in df_debug.columns if col.endswith(f'_{pillar}_max')]
        if max_cols:
            df_debug[f"{pillar}_Max"] = df_debug[max_cols].sum(axis=1)
        else:
            df_debug[f"{pillar}_Max"] = 0
        
        # Calculate percentages
        df_debug[f"{pillar}_Pct"] = (df_debug[f"{pillar}_Total"] / df_debug[f"{pillar}_Max"] * 100).fillna(0)

    # --- Create gap analysis export with relative impact ---
    gap_analysis = []
    for idx, row in df_debug.iterrows():
        patient_id = row['patient_id']
        
        # Get pillar totals for relative impact calculation
        pillar_totals = {}
        pillar_maxes = {}
        for pillar in pillar_names:
            pillar_totals[pillar] = row.get(f"{pillar}_Total", 0)
            pillar_maxes[pillar] = row.get(f"{pillar}_Max", 1)  # Avoid division by zero
        
        # Extract all weighted, max, and raw columns
        weighted_cols = [col for col in df_debug.columns if col.endswith('_weighted')]
        
        for weighted_col in weighted_cols:
            # Parse the column name to get marker and pillar
            base_name = weighted_col.replace('_weighted', '')
            max_col = f"{base_name}_max"
            raw_col = f"{base_name}_raw"
            
            if max_col in df_debug.columns:
                actual_weighted = row[weighted_col]
                max_weighted = row[max_col]
                actual_raw = row.get(raw_col, 0)
                
                # Calculate gaps
                weighted_gap = max_weighted - actual_weighted
                weighted_gap_pct = (weighted_gap / max_weighted * 100) if max_weighted > 0 else 0
                
                # Parse marker and pillar from column name
                if '_' in base_name:
                    parts = base_name.rsplit('_', 1)  # Split from right to handle multi-word markers
                    if len(parts) == 2:
                        marker_name = parts[0]
                        pillar_short = parts[1]
                    else:
                        marker_name = base_name
                        pillar_short = "Unknown"
                else:
                    marker_name = base_name
                    pillar_short = "Unknown"
                
                # Map short pillar name to full pillar name
                pillar_full_name = None
                for full_name in pillar_names:
                    # Check if the short name matches part of the full name
                    if pillar_short == "Healthful Nutrition" or (pillar_short == "Nutrition" and "Nutrition" in full_name):
                        pillar_full_name = "Healthful Nutrition"
                    elif pillar_short == "Movement + Exercise" or (pillar_short == "Exercise" and "Exercise" in full_name):
                        pillar_full_name = "Movement + Exercise"
                    elif pillar_short == "Restorative Sleep" or (pillar_short == "Sleep" and "Sleep" in full_name):
                        pillar_full_name = "Restorative Sleep"
                    elif pillar_short == "Cognitive Health" or (pillar_short == "Cognitive" and "Cognitive" in full_name):
                        pillar_full_name = "Cognitive Health"
                    elif pillar_short == "Stress Management" or (pillar_short == "Stress" and "Stress" in full_name):
                        pillar_full_name = "Stress Management"
                    elif pillar_short == "Connection + Purpose" or (pillar_short == "Connection" and "Connection" in full_name):
                        pillar_full_name = "Connection + Purpose"
                    elif pillar_short == "Core Care" or (pillar_short == "CoreCare" and "Core Care" in full_name):
                        pillar_full_name = "Core Care"
                
                # Calculate relative impact - what % improvement this would give to the pillar
                relative_impact_pct = 0
                current_pillar_pct = 0
                pillar_max = 0
                
                if pillar_full_name and pillar_maxes.get(pillar_full_name, 0) > 0:
                    pillar_max = pillar_maxes[pillar_full_name]
                    relative_impact_pct = (weighted_gap / pillar_max) * 100
                    current_pillar_pct = (pillar_totals[pillar_full_name] / pillar_max) * 100
                
                gap_analysis.append({
                    'patient_id': patient_id,
                    'marker': marker_name,
                    'pillar_short': pillar_short,
                    'pillar_full_name': pillar_full_name,
                    'actual_raw_score': actual_raw,
                    'actual_weighted_score': actual_weighted,
                    'max_weighted_score': max_weighted,
                    'weighted_gap': weighted_gap,
                    'weighted_gap_percent': weighted_gap_pct,
                    'absolute_impact': weighted_gap,  # Same as weighted_gap, for clarity
                    'relative_impact_percent': relative_impact_pct,  # % improvement to pillar
                    'current_pillar_percent': current_pillar_pct,
                    'pillar_max_possible': pillar_max
                })

    # Create gap analysis DataFrame
    gap_df = pd.DataFrame(gap_analysis)

    # Filter out rows with 0 gaps (already optimal)
    gap_df = gap_df[gap_df['weighted_gap'] > 0]

    # Create two sorted versions
    gap_df_absolute = gap_df.sort_values(['patient_id', 'absolute_impact'], ascending=[True, False])
    gap_df_relative = gap_df.sort_values(['patient_id', 'relative_impact_percent'], ascending=[True, False])

    # Save both analyses
    gap_df_absolute.to_csv(os.path.join(markers_output_dir, "marker_gap_analysis_absolute.csv"), index=False)
    gap_df_relative.to_csv(os.path.join(markers_output_dir, "marker_gap_analysis_relative.csv"), index=False)

    print("✓ Marker gap analysis saved:")
    print("  - marker_gap_analysis_absolute.csv (sorted by absolute point impact)")
    print("  - marker_gap_analysis_relative.csv (sorted by relative % impact to pillar)")

    # Final output with pillar summaries
    summary_cols = ["patient_id"] + [f"{pillar}_Total" for pillar in pillar_names] + \
                   [f"{pillar}_Max" for pillar in pillar_names] + \
                   [f"{pillar}_Pct" for pillar in pillar_names]

    summary_df = df_debug[summary_cols]
    summary_df.to_csv(os.path.join(markers_output_dir, "marker_pillar_summary.csv"), index=False)
    print("✓ Marker pillar summary saved to WellPath_Score_Markers/marker_pillar_summary.csv")

    # --- Create simple normalized scores export ---
    print("Creating simple normalized scores export...")
    
    # Get all marker names from config
    marker_names = list(MARKER_CONFIG.keys())
    
    # Create a DataFrame with just patient_id and normalized scores (0-1)
    simple_scores_data = []
    
    for idx, row in df.iterrows():
        patient_id = row.get("patient_id", f"row_{idx}")
        
        # Build patient context for scoring
        patient = {
            "sex": str(row.get("sex", "")).lower(),
            "age": float(row.get("age", -999)),
            "menopausal_status": str(row.get("menopausal_status", "")).lower() if "menopausal_status" in row else None,
            "cycle_stage": str(row.get("cycle_stage", "")).lower() if "cycle_stage" in row else None,
            "unique_condition": str(row.get("unique_condition", "")).lower() if "unique_condition" in row else None,
        }
        
        # Start with patient ID
        patient_data = {"patient_id": patient_id}
        
        # Add each marker's normalized score with display name from config
        for marker_key in marker_names:
            config = MARKER_CONFIG[marker_key]
            display_name = config["name"]  # Use the "name" field from config
            
            # Get the raw value from the original data
            raw_value = row.get(marker_key, None)
            
            if pd.isnull(raw_value):
                normalized_score = None
            else:
                # Score the marker to get 0-1 normalized score
                result = score_marker(marker_key, raw_value, patient)
                normalized_score = result.get("score", None)
            
            # Add to patient data with the display name as column header
            patient_data[display_name] = normalized_score
        
        simple_scores_data.append(patient_data)
    
    # Create DataFrame and save
    simple_scores_df = pd.DataFrame(simple_scores_data)
    simple_scores_path = os.path.join(markers_output_dir, "normalized_marker_scores.csv")
    simple_scores_df.to_csv(simple_scores_path, index=False)
    
    print(f"✅ Normalized marker scores exported to WellPath_Score_Markers/normalized_marker_scores.csv")
    print(f"   Contains {len(marker_names)} markers with scores normalized to 0-1 scale")
    
    # Create DataFrame and save
    simple_df = pd.DataFrame(simple_export_data)
    simple_export_path = os.path.join(markers_output_dir, "raw_marker_values.csv")
    simple_df.to_csv(simple_export_path, index=False)
    
    print(f"✅ Raw marker values exported to WellPath_Score_Markers/raw_marker_values.csv")
    print(f"   Contains {len(marker_names)} markers with display names as column headers")
    
    # Optional: Show top improvement opportunities per patient (both perspectives)
    print("\nTop 5 marker improvement opportunities per patient:")
    for patient_id in gap_df['patient_id'].unique()[:3]:  # Show first 3 patients as example
        print(f"\nPatient {patient_id}:")
        
        print("  By Absolute Impact:")
        patient_gaps_abs = gap_df_absolute[gap_df_absolute['patient_id'] == patient_id].head(5)
        for _, gap_row in patient_gaps_abs.iterrows():
            print(f"    {gap_row['marker']} ({gap_row['pillar_short']}): {gap_row['absolute_impact']:.1f} points")
        
        print("  By Relative Impact:")
        patient_gaps_rel = gap_df_relative[gap_df_relative['patient_id'] == patient_id].head(5)
        for _, gap_row in patient_gaps_rel.iterrows():
            print(f"    {gap_row['marker']} ({gap_row['pillar_short']}): {gap_row['relative_impact_percent']:.1f}% pillar improvement")



