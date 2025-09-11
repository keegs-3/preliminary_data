# WellPath Health Analytics System - Documentation

A comprehensive health assessment pipeline that processes biomarkers, survey responses, and education engagement to generate personalized wellness scores and algorithmic health recommendations.

## 🎯 System Overview

WellPath is designed to:
- **Process patient health data** across biomarkers, surveys, and education metrics
- **Score wellness** across 7 evidence-based health pillars using sophisticated algorithms
- **Generate personalized recommendations** with automated algorithm configuration
- **Calculate impact scores** using statistical methods for recommendation effectiveness
- **Provide comprehensive analytics** for health optimization and patient tracking

## 🏗️ Architecture Overview

### Core Processing Pipeline
```
Raw Data → Scoring Engines → Combined Analysis → Patient Reports → Impact Analysis
    ↓           ↓              ↓                ↓                ↓
Biomarkers   Survey       Integrated        Individual      Recommendation
Lab Values   Responses    Scoring           Breakdowns      Effectiveness
```

### Health Pillars Framework
WellPath evaluates health across **7 evidence-based pillars** with intelligent weighting:

| Pillar | Markers % | Survey % | Education % |
|--------|-----------|----------|-------------|
| **Healthful Nutrition** | 72% | 18% | 10% |
| **Movement + Exercise** | 54% | 36% | 10% |
| **Restorative Sleep** | 63% | 27% | 10% |
| **Cognitive Health** | 36% | 54% | 10% |
| **Stress Management** | 27% | 63% | 10% |
| **Connection + Purpose** | 18% | 72% | 10% |
| **Core Care** | 49.5% | 40.5% | 10% |

## 📚 Documentation Structure

### Core Systems
- **[Biomarker Scoring](core-systems/biomarker-scoring.md)** - Laboratory value processing and scoring
- **[Survey Scoring](core-systems/survey-scoring.md)** - Complex survey logic and custom calculations  
- **[Combined Scoring](core-systems/combined-scoring.md)** - Integrated pillar-weighted scoring
- **[Patient Reports](core-systems/patient-reports.md)** - Individual breakdown generation

### Algorithm System
- **[Algorithm Overview](algorithms/README.md)** - Recommendation algorithm framework
- **[Algorithm Types](algorithms/algorithm-types.md)** - 14 algorithm types (binary, proportional, composite, etc.)
- **[Config Generation](algorithms/config-generation.md)** - Automated configuration from natural language

### Advanced Features
- **[Adherence Tracking](advanced-systems/adherence-tracking.md)** - Check-in and compliance systems
- **[Impact Scoring](advanced-systems/impact-scoring.md)** - Statistical recommendation effectiveness
- **[Trigger System](advanced-systems/trigger-system.md)** - Intelligent notification engine

### User Guides
- **[Data Processing Guide](user-guides/data-processing-guide.md)** - End-to-end workflow
- **[Real Patient Data](user-guides/real-patient-data.md)** - Processing production data
- **[Troubleshooting](user-guides/troubleshooting.md)** - Common issues and solutions

### Technical Reference
- **[Pillar Framework](reference/pillar-framework.md)** - Detailed pillar definitions and weights
- **[Data Formats](reference/data-formats.md)** - Input/output specifications
- **[API Reference](reference/api-reference.md)** - Function and class documentation

## 🚀 Quick Start

### Basic Processing Pipeline
```bash
# 1. Survey scoring (recommended v2 implementation)
python scripts/wellpath_score_runner_survey_v2.py

# 2. Combined scoring with pillar weights  
python scripts/WellPath_score_runner_combined.py

# 3. Generate individual patient reports
python scripts/Patient_score_breakdown_generator.py
```

### Algorithm Configuration
```python
from src.recommendation_config_generator import process_recommendation

# Generate algorithm from natural language
config, path = process_recommendation(
    "Add one daily serving of fiber-rich food", 
    "REC001"
)
```

## 🔧 Key Features

### Intelligent Algorithm Selection
- **Binary Threshold**: Pass/fail scoring for strict limits and "eliminate" patterns
- **Proportional**: Partial credit scoring for target achievement
- **Zone-Based**: Tiered scoring for optimal ranges (3-tier or 5-tier)
- **Composite**: Multi-component weighted algorithms
- **Specialized**: Weekly allowances, categorical filters, sleep consistency

### Advanced Survey Logic
- **Personalized targets** based on BMR calculations
- **Multi-pillar impact** for interconnected health factors
- **Complex rollups** for exercise, sleep, and stress patterns
- **Substance use scoring** with quit-time bonuses
- **Biomarker-dependent calculations**

### Comprehensive Analytics
- **4 statistical scaling methods** for impact analysis
- **Patient-level audit trails** showing score derivation
- **Pillar contribution analysis** for targeted interventions
- **Gap analysis** identifying improvement opportunities

## 📊 System Outputs

### Generated Data Directories
- `WellPath_Score_Markers/` - Biomarker scoring results
- `WellPath_Score_Survey/` - Survey scoring with complex logic
- `WellPath_Score_Combined/` - Integrated final scores
- `WellPath_Score_Breakdown/` - Individual patient reports
- `src/generated_configs/` - Algorithm configurations

## 🤝 Contributing

The WellPath system is designed for extensibility:
- **Add new algorithms** by extending the algorithm framework
- **Enhance survey logic** through the modular scoring functions  
- **Integrate new data sources** using the pillar weighting system
- **Extend analytics** with additional statistical methods

## 📖 Getting Help

1. **Quick questions**: Check the [Troubleshooting Guide](user-guides/troubleshooting.md)
2. **Implementation details**: See component-specific documentation
3. **Algorithm customization**: Review [Algorithm Types](algorithms/algorithm-types.md)
4. **Data processing**: Follow the [Complete Processing Guide](user-guides/data-processing-guide.md)

---

**Built for health analytics teams who need sophisticated, evidence-based wellness scoring with algorithmic recommendation generation.**