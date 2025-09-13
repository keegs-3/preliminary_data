# Source Options Reference

**Standardized food source categorization for quality-based health tracking**

| **Total Sources** | **Categories** | **Quality Scoring** | **Integration** |
|-------------------|----------------|---------------------|-----------------|
| **51 sources** | **6 categories** | **0.2-1.0 range** | **Quality algorithms** |

## Overview

Source options provide granular food quality tracking by categorizing the **types and quality** of food sources within major nutritional categories. Unlike basic nutrition tracking that only measures quantities, source options enable assessment of **food quality patterns** and **nutritional diversity**.

## Quick Reference

### 🍎 **Fruit Sources** (8 types)
**Metric:** `fruit_source_type` | **Best:** Berries (1.0) | **Range:** 0.5-1.0

| Source | Quality Score | Examples |
|--------|---------------|----------|
| **Berries** | 1.0 | Blueberries, strawberries, raspberries |
| **Citrus** | 0.9 | Oranges, lemons, grapefruits |
| **Stone Fruits** | 0.8 | Peaches, plums, cherries |
| **Dried Fruits** | 0.5 | Raisins, dates (no added sugar) |

### ☕ **Caffeine Sources** (7 types)
**Metric:** `caffeine_source` | **Best:** Coffee (1.0) | **Range:** 0.2-1.0

| Source | Quality Score | Examples |
|--------|---------------|----------|
| **Coffee** | 1.0 | Brewed coffee, espresso |
| **Tea** | 0.9 | Black, green, white, oolong |
| **Energy Drinks** | 0.2 | Energy drinks and shots |
| **Soda** | 0.3 | Caffeinated soft drinks |

### 🌱 **Fiber Sources** (7 types)  
**Metric:** `fiber_source` | **Best:** Legumes (1.0) | **Range:** 0.6-1.0

| Source | Quality Score | Examples |
|--------|---------------|----------|
| **Legumes** | 1.0 | Beans, lentils, chickpeas |
| **Whole Grains** | 0.9 | Oats, quinoa, brown rice |
| **Vegetables** | 0.9 | Broccoli, Brussels sprouts |
| **Psyllium** | 0.6 | Psyllium husk supplement |

### 🥬 **Vegetable Sources** (9 types)
**Metric:** `vegetable_source` | **Best:** Leafy Greens & Cruciferous (1.0) | **Range:** 0.5-1.0

| Source | Quality Score | Examples |
|--------|---------------|----------|
| **Leafy Greens** | 1.0 | Spinach, kale, arugula |
| **Cruciferous** | 1.0 | Broccoli, cauliflower, Brussels sprouts |
| **Colorful Peppers** | 0.9 | Red, yellow, orange bell peppers |
| **Starchy Vegetables** | 0.5 | Potatoes, corn, peas |

### 🌾 **Whole Grain Sources** (9 types)
**Metric:** `whole_grain_source` | **Best:** Oats & Quinoa (1.0) | **Range:** 0.7-1.0

| Source | Quality Score | Examples |
|--------|---------------|----------|
| **Oats** | 1.0 | Steel-cut, rolled oats |
| **Quinoa** | 1.0 | All varieties |
| **Brown Rice** | 0.9 | Brown, wild, black rice |
| **Whole Grain Bread** | 0.7 | 100% whole grain products |

### 🫘 **Legume Sources** (10 types)
**Metric:** `legume_source` | **Best:** Lentils & Chickpeas (1.0) | **Range:** 0.7-1.0

| Source | Quality Score | Examples |
|--------|---------------|----------|
| **Lentils** | 1.0 | Red, green, brown, black |
| **Chickpeas** | 1.0 | Garbanzo beans, hummus |
| **Black Beans** | 0.9 | Black turtle beans |
| **Green Peas** | 0.7 | Fresh or frozen |

---

## Complete Source Categories

### 🍎 Fruit Sources (8 sources)
*Maps to: `fruit_source_type` metric*

| ID | Name | Score | Description |
|----|------|-------|-------------|
| `berries` | **Berries** | 1.0 | Blueberries, strawberries, raspberries, blackberries |
| `citrus` | **Citrus Fruits** | 0.9 | Oranges, lemons, limes, grapefruits, tangerines |
| `apples_pears` | **Apples & Pears** | 0.8 | Apples, pears, and similar pome fruits |
| `stone_fruits` | **Stone Fruits** | 0.8 | Peaches, plums, apricots, cherries, nectarines |
| `tropical` | **Tropical Fruits** | 0.7 | Bananas, mangoes, pineapples, kiwi, papaya |
| `melons` | **Melons** | 0.7 | Watermelon, cantaloupe, honeydew |
| `grapes` | **Grapes** | 0.6 | Red, green, or purple grapes |
| `dried_fruits` | **Dried Fruits** | 0.5 | Raisins, dates, dried apricots, prunes (no added sugar) |

### ☕ Caffeine Sources (7 sources)
*Maps to: `caffeine_source` metric*

| ID | Name | Score | Description |
|----|------|-------|-------------|
| `coffee` | **Coffee** | 1.0 | Brewed coffee, espresso, or coffee-based drinks |
| `tea` | **Tea** | 0.9 | Black tea, green tea, white tea, or oolong tea |
| `chocolate` | **Chocolate** | 0.8 | Dark chocolate, milk chocolate, or cocoa products |
| `supplements` | **Caffeine Supplements** | 0.5 | Caffeine pills or other caffeine supplements |
| `pre_workout` | **Pre-Workout Supplements** | 0.4 | Pre-workout powders and supplements |
| `soda` | **Soda/Soft Drinks** | 0.3 | Caffeinated sodas and soft drinks |
| `energy_drink` | **Energy Drinks** | 0.2 | Energy drinks and energy shots |

### 🌱 Fiber Sources (7 sources)
*Maps to: `fiber_source` metric*

| ID | Name | Score | Description |
|----|------|-------|-------------|
| `legumes` | **Legumes** | 1.0 | Beans, lentils, chickpeas, peas |
| `whole_grains` | **Whole Grains** | 0.9 | Oats, quinoa, brown rice, whole wheat |
| `vegetables` | **Vegetables** | 0.9 | Broccoli, Brussels sprouts, artichokes, leafy greens |
| `fruits` | **Fruits** | 0.8 | Apples, pears, berries, bananas |
| `nuts_seeds` | **Nuts & Seeds** | 0.8 | Chia seeds, flax seeds, almonds, walnuts |
| `avocado` | **Avocado** | 0.7 | Fresh avocado |
| `psyllium` | **Psyllium Husk** | 0.6 | Psyllium husk supplement |

### 🥬 Vegetable Sources (9 sources)
*Maps to: `vegetable_source` metric*

| ID | Name | Score | Description |
|----|------|-------|-------------|
| `leafy_greens` | **Leafy Greens** | 1.0 | Spinach, kale, arugula, lettuce, chard |
| `cruciferous` | **Cruciferous Vegetables** | 1.0 | Broccoli, cauliflower, Brussels sprouts, cabbage |
| `colorful_peppers` | **Colorful Peppers** | 0.9 | Red, yellow, orange, and green bell peppers |
| `root_vegetables` | **Root Vegetables** | 0.8 | Carrots, beets, sweet potatoes, turnips |
| `alliums` | **Alliums** | 0.8 | Onions, garlic, leeks, shallots |
| `tomatoes` | **Tomatoes** | 0.7 | Fresh tomatoes, cherry tomatoes, roma tomatoes |
| `squash_zucchini` | **Squash & Zucchini** | 0.7 | Zucchini, yellow squash, butternut squash |
| `mushrooms` | **Mushrooms** | 0.6 | Button, shiitake, portobello, other edible mushrooms |
| `starchy_vegetables` | **Starchy Vegetables** | 0.5 | Potatoes, corn, peas (counted as vegetables) |

### 🌾 Whole Grain Sources (9 sources)
*Maps to: `whole_grain_source` metric*

| ID | Name | Score | Description |
|----|------|-------|-------------|
| `oats` | **Oats** | 1.0 | Steel-cut oats, rolled oats, oatmeal |
| `quinoa` | **Quinoa** | 1.0 | All varieties of quinoa |
| `brown_rice` | **Brown Rice** | 0.9 | Brown rice, wild rice, black rice |
| `whole_wheat` | **Whole Wheat** | 0.8 | Whole wheat bread, pasta, flour products |
| `barley` | **Barley** | 0.8 | Pearled barley, hulled barley |
| `buckwheat` | **Buckwheat** | 0.8 | Buckwheat groats, buckwheat flour |
| `farro` | **Farro** | 0.8 | Ancient wheat grain farro |
| `millet` | **Millet** | 0.7 | Whole millet grains |
| `whole_grain_bread` | **Whole Grain Bread** | 0.7 | 100% whole grain breads and products |

### 🫘 Legume Sources (10 sources)
*Maps to: `legume_source` metric*

| ID | Name | Score | Description |
|----|------|-------|-------------|
| `lentils` | **Lentils** | 1.0 | Red, green, brown, or black lentils |
| `chickpeas` | **Chickpeas** | 1.0 | Garbanzo beans, hummus |
| `black_beans` | **Black Beans** | 0.9 | Black turtle beans |
| `kidney_beans` | **Kidney Beans** | 0.9 | Red kidney beans, white kidney beans |
| `pinto_beans` | **Pinto Beans** | 0.9 | Pinto beans, refried beans |
| `navy_beans` | **Navy Beans** | 0.9 | Small white beans |
| `split_peas` | **Split Peas** | 0.8 | Green or yellow split peas |
| `black_eyed_peas` | **Black-Eyed Peas** | 0.8 | Black-eyed peas, cowpeas |
| `edamame` | **Edamame** | 0.7 | Young soybeans |
| `green_peas` | **Green Peas** | 0.7 | Fresh or frozen green peas |

---

## Quality Scoring System

### Score Ranges by Category

| Category | Range | Methodology |
|----------|-------|-------------|
| **Caffeine Sources** | 0.2-1.0 | Natural sources score higher than processed |
| **Fruit Sources** | 0.5-1.0 | Antioxidant density and sugar content balance |
| **Fiber Sources** | 0.6-1.0 | Soluble/insoluble fiber ratio and nutrients |
| **Vegetable Sources** | 0.5-1.0 | Nutrient density and phytonutrient diversity |
| **Whole Grain Sources** | 0.7-1.0 | Processing level and nutrient retention |
| **Legume Sources** | 0.7-1.0 | Protein quality and nutrient completeness |

### Quality Scoring Principles

#### **1.0 (Optimal)**
- Minimal processing
- Maximum nutrient density
- Best bioavailability
- Comprehensive phytonutrients

#### **0.8-0.9 (Excellent)**
- Light processing
- High nutrient retention
- Good bioavailability
- Rich phytonutrient profile

#### **0.6-0.7 (Good)**
- Moderate processing
- Some nutrient loss
- Adequate bioavailability
- Limited phytonutrients

#### **0.2-0.5 (Poor)**
- Heavy processing
- Significant nutrient loss
- Added sugars/additives
- Limited health benefits

---

## Algorithm Integration

### Progressive Scoring Algorithms

Source options integrate directly into these quality-focused algorithms:

| Algorithm | Source Integration | Scoring Method |
|-----------|------------------|---------------|
| **Proportional** | Linear quality weighting | `source_score × frequency` |
| **Zone-Based** | Quality tier classification | 5-tier quality zones |
| **Composite Weighted** | Multi-factor quality scoring | Weighted quality matrices |

### Example: Fruit Source Scoring

```
If user consumes:
- 2 servings berries (score: 1.0)
- 1 serving dried fruit (score: 0.5)

Algorithm calculates:
- Total servings: 3
- Quality-weighted servings: (2×1.0) + (1×0.5) = 2.5
- Quality score: 2.5/3 = 0.83
```

### Calculated Metrics Integration

Source options generate advanced calculated metrics:

| Calculated Metric | Description |
|------------------|-------------|
| `weekly_fruit_source_diversity` | Number of different fruit types consumed |
| `weekly_vegetable_source_quality` | Average quality score of vegetable sources |
| `weekly_whole_grain_source_consistency` | Days with high-quality grain sources |
| `weekly_fiber_source_balance` | Distribution across fiber source types |

---

## Usage Examples

### Implementation Patterns

#### **1. Single Source Selection**
```json
{
  "metric": "caffeine_source",
  "timestamp": "2024-01-15T08:00:00Z",
  "source": "coffee",
  "quality_score": 1.0
}
```

#### **2. Multiple Source Events**
```json
{
  "metric": "vegetable_source", 
  "events": [
    {"timestamp": "12:00", "source": "leafy_greens", "score": 1.0},
    {"timestamp": "18:00", "source": "tomatoes", "score": 0.7}
  ],
  "daily_quality_average": 0.85
}
```

#### **3. Weekly Source Summary**
```json
{
  "metric": "fruit_source_diversity",
  "week": "2024-W03",
  "sources_consumed": ["berries", "citrus", "stone_fruits"],
  "diversity_score": 3,
  "quality_weighted_average": 0.90
}
```

---

## Integration Notes

### **HealthKit Compatibility**
Source options are **WellPath innovations** with no direct HealthKit equivalents. HealthKit tracks nutrients but not food quality or source diversity.

### **Algorithm Requirements**
- All progressive adherence algorithms support source quality weighting
- Source scores multiply base adherence scores for quality-adjusted results
- Required for accurate Zone-Based and Composite Weighted algorithm calculations

### **Data Validation**
- Each source must have valid `score` between 0.0-1.0
- `sort_order` determines UI display priority
- `source_metrics` defines which metrics use each source

---

**Next**: [Compliance Rules](../compliance-rules/) | [Algorithm Reference](../../algorithms/)