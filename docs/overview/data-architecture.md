# WellPath Data Architecture

## System Design Principles

WellPath follows a three-tier architecture similar to Apple's HealthKit, ensuring scalability, consistency, and real-time performance for health data tracking and adherence scoring.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    WellPath Data System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────┐ │
│  │   Data Layer    │    │ Processing Layer │    │ Score Layer │ │
│  │                 │────│                  │────│             │ │
│  │ • Raw Metrics   │    │ • Calculated     │    │ • Algorithm │ │
│  │ • Data Sources  │    │   Metrics        │    │   Engines   │ │
│  │ • Validation    │    │ • Aggregation    │    │ • Real-time │ │
│  │ • Storage       │    │ • Transformation │    │   Scoring   │ │
│  └─────────────────┘    └──────────────────┘    └─────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Types Hierarchy

### Raw Metrics (Tier 1)
**Direct measurements from devices or user input**

- **Instantaneous**: Single point-in-time measurements
  - `step_taken` - Individual step from accelerometer
  - `heart_rate_reading` - BPM measurement at specific time
  - `glucose_reading` - Blood glucose level reading

- **Event-based**: Discrete occurrences with timestamps
  - `meal_logged` - Food intake entry
  - `medication_taken` - Drug administration record
  - `symptom_reported` - User-reported health event

- **Duration-based**: Time period measurements
  - `sleep_session` - Sleep start/end times
  - `exercise_session` - Workout duration and intensity
  - `meditation_session` - Mindfulness practice period

### Calculated Metrics (Tier 2)
**Derived values computed from raw data**

- **Daily Aggregates**: 24-hour summaries
  - `daily_steps` - Total steps from `step_taken` events
  - `daily_calories` - Energy expenditure from various sources
  - `daily_water_intake` - Fluid consumption total

- **Weekly Patterns**: 7-day analysis
  - `weekly_exercise_minutes` - Total workout time
  - `weekly_medication_adherence` - Compliance percentage
  - `weekly_sleep_consistency` - Schedule regularity score

- **Derived Insights**: Complex calculations
  - `sleep_duration` - Hours between sleep_start and sleep_end
  - `resting_heart_rate` - Baseline HR from continuous monitoring
  - `activity_intensity_distribution` - Exercise zone analysis

## Data Flow Architecture

### 1. Ingestion Pipeline

```
Raw Data Sources → Validation → Normalization → Storage
     ↓               ↓             ↓            ↓
• Devices        • Schema      • Unit         • Time-series
• Manual Entry   • Range       • Conversion   • Database
• API Import     • Type        • Formatting   • Indexing
```

### 2. Processing Pipeline

```
Raw Metrics → Calculation Engine → Calculated Metrics
     ↓              ↓                    ↓
• Individual    • Aggregation        • Daily totals
• Events        • Transformation     • Weekly patterns
• Sessions      • Derived values     • Consistency scores
```

### 3. Scoring Pipeline

```
Calculated Metrics → Algorithm Engine → Adherence Scores
        ↓                  ↓                 ↓
• Target values       • 10 Algorithm      • Real-time
• Frequency data      • Types             • Progressive
• Time windows        • Configuration     • Weekly final
```

## Algorithm Integration

### Algorithm Types and Data Requirements

| Algorithm Type | Input Data | Output Format | Real-time |
|----------------|------------|---------------|-----------|
| **Binary Threshold** | Single daily value | Pass/Fail (0/100) | ✅ Yes |
| **Proportional** | Progress toward target | 0-100% scale | ✅ Yes |
| **Zone-Based** | Measured value | Zone score (0-100) | ✅ Yes |
| **Minimum Frequency** | Weekly pattern | Frequency achievement | ⏱️ End of week |
| **Composite Weighted** | Multiple metrics | Weighted average | ✅ Yes |

### Progressive Scoring System

```
Day 1: [Raw Data] → [Algorithm] → [Progressive Score 1]
Day 2: [Raw Data] → [Algorithm] → [Progressive Score 2]
Day 3: [Raw Data] → [Algorithm] → [Progressive Score 3]
...
Day 7: [Raw Data] → [Algorithm] → [Final Weekly Score]
```

**Key Principles:**
- Users see daily progress updates
- Scores evolve as more data arrives
- Final weekly assessment provides complete picture
- No retroactive score changes

## Data Consistency and Validation

### Schema Enforcement

```json
{
  "metric_id": "daily_steps",
  "data_type": "calculated",
  "unit": "count",
  "valid_range": [0, 100000],
  "source_metrics": ["step_taken"],
  "calculation_method": "sum",
  "update_frequency": "real_time"
}
```

### Validation Rules

1. **Range Validation**: Ensure values fall within biological/logical limits
2. **Type Validation**: Enforce correct data types (integer, float, timestamp)
3. **Source Validation**: Verify data source authenticity and reliability
4. **Temporal Validation**: Check timestamp consistency and chronological order

## Storage Architecture

### Time-Series Database Design

```
┌─────────────────┐
│ Metrics Table   │
├─────────────────┤
│ • timestamp     │
│ • user_id       │
│ • metric_id     │
│ • value         │
│ • unit          │
│ • source        │
│ • quality_score │
└─────────────────┘
```

### Indexing Strategy

- **Primary Index**: `(user_id, metric_id, timestamp)`
- **Secondary Index**: `(metric_id, timestamp)` for population analysis
- **Composite Index**: `(user_id, timestamp)` for user timeline queries

## Real-time Processing

### Event-Driven Architecture

1. **Data Ingestion**: New metric arrives
2. **Validation**: Schema and range checks
3. **Storage**: Persist to time-series database
4. **Calculation Trigger**: Update dependent calculated metrics
5. **Scoring Trigger**: Recalculate adherence scores
6. **Notification**: Push updates to user interface

### Performance Optimization

- **Caching**: Store frequently accessed calculations
- **Batch Processing**: Group related updates
- **Incremental Updates**: Only recalculate affected metrics
- **Async Processing**: Non-blocking score calculations

## Data Quality and Reliability

### Quality Scoring System

Each data point receives a quality score (0-100) based on:
- **Source Reliability**: Device accuracy, manual entry validation
- **Temporal Consistency**: Expected timing patterns
- **Value Plausibility**: Biological/behavioral reasonableness
- **Completeness**: Missing data indicators

### Error Handling

```python
# Example error handling workflow
if data_quality_score < 70:
    flag_for_review()
    exclude_from_high_stakes_calculations()
    notify_user_of_potential_inaccuracy()
```

## Integration Patterns

### HealthKit Compatibility

WellPath maintains compatibility with Apple HealthKit data types:

| WellPath Metric | HealthKit Equivalent | Unit |
|-----------------|---------------------|------|
| `daily_steps` | `HKQuantityTypeIdentifierStepCount` | count |
| `sleep_duration` | `HKCategoryTypeIdentifierSleepAnalysis` | hours |
| `heart_rate` | `HKQuantityTypeIdentifierHeartRate` | bpm |

### API Standards

- **REST API**: Standard HTTP methods for data operations
- **WebSocket**: Real-time score updates
- **Webhook**: Event notifications for external systems
- **GraphQL**: Flexible data querying for complex applications

## Security and Privacy

### Data Protection

- **Encryption**: AES-256 for data at rest, TLS 1.3 for transit
- **Access Control**: Role-based permissions (read/write/admin)
- **Audit Logging**: Complete trail of data access and modifications
- **Data Retention**: Configurable retention policies per metric type

### Privacy by Design

- **Data Minimization**: Only collect necessary metrics
- **Purpose Limitation**: Use data only for stated health tracking purposes
- **User Control**: Complete ownership and deletion rights
- **Anonymization**: Remove identifying information for population studies

## Scalability Considerations

### Horizontal Scaling

- **Sharding Strategy**: Partition by user_id for even distribution
- **Load Balancing**: Distribute API requests across multiple instances
- **Caching Layer**: Redis/Memcached for frequently accessed data
- **CDN Integration**: Serve static documentation and assets globally

### Performance Metrics

- **Ingestion Rate**: Target 10,000+ metrics per second
- **Query Response**: <100ms for real-time score calculations
- **Data Consistency**: Eventual consistency acceptable for non-critical metrics
- **Availability**: 99.9% uptime target with graceful degradation

---

**Next Steps**: [Getting Started Guide](getting-started.md) | [Algorithm Types](../../algorithms/algorithm-types.md)