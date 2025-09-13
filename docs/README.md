# WellPath Data Documentation

## Getting Started

This documentation describes the WellPath health data system architecture, similar to Apple's HealthKit framework but designed for comprehensive wellness tracking and adherence scoring.

## Documentation Structure

### 📖 [Overview](overview/)
- **[Introduction](overview/introduction.md)** - System overview and core concepts
- **[Data Architecture](overview/data-architecture.md)** - How data types relate to each other
- **[Getting Started](overview/getting-started.md)** - Quick start guide

### 📚 [Reference](reference/)
- **[Metric Types](reference/metric-types/)** - Complete catalog of trackable data
- **[Algorithm Types](../algorithms/)** - Scoring algorithm reference
- **[Units System](reference/units/)** - Standardized measurements and conversions
- **[Data Sources](reference/data-sources/)** - Source options and validation
- **[Compliance Rules](reference/compliance/)** - Health screening requirements

### 🛠 [Developer Guides](guides/)
- **[Data Modeling](guides/data-modeling.md)** - Designing new metrics and algorithms
- **[Algorithm Implementation](guides/algorithm-implementation.md)** - Creating custom scoring algorithms
- **[Configuration Schema](guides/configuration-schema.md)** - Understanding config structure
- **[Testing Framework](guides/testing-framework.md)** - Validating implementations

### 🔧 [API Reference](api-reference/)
- **[Algorithms API](api-reference/algorithms.md)** - Algorithm classes and methods
- **[Data Types API](api-reference/data-types.md)** - Metric and unit classes
- **[Configuration API](api-reference/configuration.md)** - Config generation and validation

## Quick Links

### For Developers
- [Algorithm Types Overview](../algorithms/algorithm-types.md) - Complete algorithm reference
- [Implementation Guide](guides/algorithm-implementation.md) - Build custom algorithms
- [Testing Your Changes](guides/testing-framework.md) - Validate implementations

### For Health Professionals
- [Metric Types Catalog](reference/metric-types/) - Available health metrics
- [Compliance Requirements](reference/compliance/) - Health screening rules
- [Data Sources Guide](reference/data-sources/) - Understanding data inputs

### For Researchers
- [Data Architecture](overview/data-architecture.md) - System design principles
- [Algorithm Research](../WellPath-Adherence-Scoring-Implementation-Guide.md) - Adherence scoring methodology

## System Overview

WellPath provides a comprehensive framework for:

- **📊 Health Data Tracking**: 100+ standardized health metrics
- **🎯 Adherence Scoring**: 10 algorithm types for behavior assessment
- **🔄 Real-time Processing**: Progressive scoring with immediate feedback
- **📱 Integration Ready**: HealthKit-compatible data types and units

## Getting Help

- **Issues**: Report bugs and request features on our [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: Join the community on [GitHub Discussions](https://github.com/your-repo/discussions)
- **Contributing**: See our [Contributing Guide](../CONTRIBUTING.md)

---

*Documentation version 1.0 | Last updated: January 2025*