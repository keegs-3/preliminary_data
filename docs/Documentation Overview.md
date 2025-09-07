# Documentation Overview

This document provides a quick reference guide to the four core WellPath system documentation files and their contents.

## Document Structure

### 1. [Complete User Guide.md](./Complete%20User%20Guide.md)
**Purpose:** End-to-end workflow documentation for using the WellPath system  
**Audience:** Data scientists, researchers, implementation teams

**Contents:**
- **Quick Start Guide** - Step-by-step instructions from data generation to final impact scoring
- **Data Format Requirements** - Exact specifications for biomarker (89 columns) and survey (320 columns) data
- **Processing Pipeline** - Complete workflow through all 7 processing steps
- **File Structure & Outputs** - Directory organization and expected output files
- **Troubleshooting** - Common issues, error resolution, validation steps
- **Configuration** - Pillar weights, directory paths, system settings
- **Airtable Integration** - Excel-to-JSON recommendation data management

**Key Use Cases:**
- Setting up the system for first time
- Processing real patient data
- Generating synthetic data for testing
- Updating recommendation configurations
- Debugging processing issues

---

### 2. [WellPath Check-In System.md](./WellPath%20Ckeck-In%20System.md)
**Purpose:** Technical architecture for the user feedback and questionnaire system  
**Audience:** Backend developers, database architects, product managers

**Contents:**
- **Database Architecture** - Complete table structure (checkins_v2, checkin_questions_v2, response_options_v2, etc.)
- **Trigger System Integration** - How check-ins connect to the WellPath trigger system
- **Data Flow & Execution Logic** - From trigger conditions to user responses to data correlation
- **Check-in Categories** - Data entry, reflection, experience tracking, pattern monitoring examples
- **Implementation Guidelines** - Naming conventions, design principles, quality assurance
- **Advanced Features** - AI-enhanced check-ins, response pattern analysis
- **Technical Implementation** - Response validation, performance considerations, scalability design

**Key Use Cases:**
- Building check-in functionality in apps
- Designing questionnaire databases
- Implementing trigger-driven user engagement
- Creating adaptive user feedback systems

---

### 3. [WellPath Survey Scoring System.md](./WellPath%20Survey%20Scoring%20System.md)
**Purpose:** Technical documentation for sophisticated survey response scoring algorithms  
**Audience:** Backend developers, data scientists, health analytics teams

**Contents:**
- **Custom Scoring Functions** - Biomarker-dependent personalized scoring (protein, calories, movement, etc.)
- **Complex Logic Implementation** - Multi-factor movement scoring, sleep issue analysis, stress management
- **Backend Integration Strategy** - Database schema, API design, scoring engine architecture
- **Question ID Architecture** - Mapping custom logic to specific question identifiers
- **Enhanced Substance Scoring** - Time-since-quit bonuses, usage trend analysis
- **Configuration Management** - Dynamic scoring updates, A/B testing support
- **Migration Paths** - From Python implementation to production backends

**Key Use Cases:**
- Implementing sophisticated health survey scoring
- Building personalized nutrition/fitness assessments
- Creating evidence-based wellness algorithms
- Integrating complex scoring into existing systems

---

### 4. [WellPath Trigger System.md](./WellPath%20Trigger%20System.md)
**Purpose:** Foundational behavioral intervention platform architecture  
**Audience:** Backend developers, AI/ML engineers, behavioral health specialists

**Contents:**
- **Two-Tier Priority System** - Macro-level trigger groups and micro-level individual priorities
- **Operator Categories** - 26 standardized operators (input detection, performance, mathematical, etc.)
- **Database Structure** - trigger_conditions, trigger_groups, operator_definitions tables
- **Cooldown & Rate Limiting** - Assessment period-based formulas, daily firing limits
- **AI Agent Preparation** - Context tags, future AI-powered trigger selection
- **Content Integration** - How triggers connect to check-ins, nudges, challenges, education
- **Implementation Code** - JavaScript examples for trigger selection logic

**Key Use Cases:**
- Building behavioral intervention systems
- Implementing smart notification logic
- Creating adaptive user engagement platforms
- Designing AI-ready trigger systems

---

## Document Relationships

```
Complete User Guide ──────► Practical implementation using all systems
         │
         ├─► WellPath Check-In System ──► User feedback collection
         │
         ├─► WellPath Survey Scoring ───► Health assessment algorithms  
         │
         └─► WellPath Trigger System ───► Behavioral intervention logic
```

## Usage Recommendations

**For System Implementation:**
1. Start with **Complete User Guide** to understand overall workflow
2. Reference **WellPath Trigger System** for notification/intervention logic
3. Use **WellPath Check-In System** for user feedback architecture
4. Implement **WellPath Survey Scoring** for health assessment algorithms

**For Specific Tasks:**
- **Data Processing**: Complete User Guide
- **Database Design**: Check-In System + Trigger System
- **Health Algorithms**: Survey Scoring System
- **User Engagement**: Trigger System + Check-In System
- **Troubleshooting**: Complete User Guide

**For Different Roles:**
- **Product Managers**: Complete User Guide + Check-In System
- **Backend Developers**: All four documents
- **Data Scientists**: Complete User Guide + Survey Scoring System
- **AI/ML Engineers**: Trigger System + Survey Scoring System
- **Health Analytics Teams**: Survey Scoring System + Complete User Guide

Each document is designed to be comprehensive and self-contained while working together as part of the complete WellPath system architecture.
