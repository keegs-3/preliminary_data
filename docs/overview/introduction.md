# Introduction to WellPath Data System

## Overview

WellPath is a comprehensive health and wellness data framework designed for real-time adherence tracking and behavioral assessment. Similar to Apple's HealthKit, WellPath provides standardized data types, units, and algorithms for health applications.

## Core Features

### 📊 Comprehensive Data Model
- **100+ Health Metrics**: From basic vitals to complex behavioral patterns
- **Standardized Units**: Consistent measurement across all data types
- **Source Validation**: Reliable data collection with validation rules

### 🎯 Advanced Scoring Algorithms
- **10 Algorithm Types**: Binary, proportional, zone-based, composite, and more
- **Progressive Scoring**: Real-time feedback with cumulative progress tracking
- **Behavioral Insights**: Frequency patterns, elimination tracking, weekly goals

### 🔄 Real-time Processing
- **Immediate Feedback**: Users see progress updates in real-time
- **Weekly Assessments**: Comprehensive adherence scoring over time periods
- **Flexible Evaluation**: Daily, weekly, and custom time window support

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Raw Metrics   │    │ Calculated Metrics│    │   Algorithms    │
│                 │────│                  │────│                 │
│ • Steps         │    │ • Daily Steps    │    │ • Binary        │
│ • Meals         │    │ • Weekly Cardio  │    │ • Proportional  │
│ • Sleep Times   │    │ • Sleep Duration │    │ • Zone-Based    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Key Concepts

### Data Types

**Raw Metrics**: Direct measurements from devices or user input
- `step_taken` - Individual step measurement
- `meal_logged` - Single meal entry with timestamp
- `sleep_time` - Sleep/wake time recording

**Calculated Metrics**: Derived values computed from raw data
- `daily_steps` - Total steps per day from `step_taken`
- `daily_meals` - Meal count per day from `meal_logged`
- `sleep_duration` - Hours calculated from sleep/wake times

### Algorithm Types

**Binary Threshold**: Simple pass/fail scoring
- "Drink 8 glasses of water daily" → 100% or 0%

**Proportional**: Gradual scoring based on achievement percentage
- "Work toward 10,000 steps daily" → 80% for 8,000 steps

**Zone-Based**: Multi-tier scoring with optimal ranges
- "Sleep 7-9 hours" → 100% for optimal, 60% for fair, 20% for poor

**Minimum Frequency**: Weekly patterns with minimum requirements
- "Exercise 30+ minutes on at least 3 days/week" → Binary based on frequency

## Getting Started

1. **[Quick Start Guide](getting-started.md)** - Set up your first metrics
2. **[Data Architecture](data-architecture.md)** - Understand the system design
3. **[Algorithm Types](../../algorithms/algorithm-types.md)** - Choose the right scoring method

## Use Cases

### Personal Health Tracking
- Daily activity monitoring
- Nutrition goal achievement
- Sleep quality assessment
- Medication adherence

### Clinical Applications
- Patient progress tracking
- Treatment compliance monitoring
- Behavioral intervention scoring
- Outcome measurement

### Research Studies
- Population health metrics
- Intervention effectiveness
- Adherence pattern analysis
- Longitudinal health tracking

## Next Steps

- **Developers**: Start with [Algorithm Implementation Guide](../guides/algorithm-implementation.md)
- **Health Professionals**: Explore [Metric Types Catalog](../reference/metric-types/)
- **Researchers**: Review [Data Architecture](data-architecture.md)

---

*Learn more about specific components in the [Reference Documentation](../reference/)*