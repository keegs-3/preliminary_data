# WellPath Check-in System Architecture

## System Overview
The check-in system is a highly configurable framework for collecting user feedback through structured questionnaires. It supports everything from simple data entry to complex behavioral assessments with dynamic triggering logic.

## Core Tables & Relationships

### **checkin_types_v2** - Check-in Categories
```
Primary Key: type_id (CT001, CT002, etc.)
Purpose: Defines behavioral categories and default scheduling patterns
```
**Key Fields:**
- `purpose`: Categorical classification (data-entry, reflection, insight-generation, behavior-tracking, experience-tracking, pattern-monitoring, body-awareness, work-wellness, nutrition-awareness)
- `default_frequency`: Base scheduling template (Daily, Weekly, Multiple Daily, User-initiated, Conditional, End-of-Challenge, Mid-Challenge, One-time)

**Usage:** Template for check-in behavior and default triggering patterns

---

### **response_types_v2** - Response Input Methods  
```
Primary Key: option_id (RO001, RO002, etc.)
Purpose: Generic response mechanisms and UI components
```
**Key Fields:**
- `response_type`: UI component type (Boolean, Scale 1-3/1-5/1-10, Multiple Choice, Free Text, Numerical, Time Entry, Date Entry)
- `options_config`: JSON configuration for UI behavior and validation

**Usage:** Reusable UI templates linked to specific response_options_v2 instances

---

### **checkins_v2** - Check-in Instances
```
Primary Key: checkin_id (CK-XXX-XXX-001 format)
Purpose: Individual check-in configurations
```
**Key Fields:**
- `checkin_type` → checkin_types_v2: Inherits behavioral template
- `trigger_conditions` → trigger_conditions: Defines when to fire
- `tracked_metrics` → tracked_metrics: Data correlation targets
- `recommendations_targeted` → recommendations: Improvement focus areas

**Computed Fields:**
- `frequency`: Inherited from checkin_type
- `Pillar(s)`: Rolled up from targeted recommendations
- `Response_Types`: Aggregated from all questions

---

### **checkin_questions_v2** - Individual Questions
```
Primary Key: question_id (Q-XXX-001 format)
Purpose: Atomic question units within check-ins
```
**Key Fields:**
- `parent_checkin` → checkins_v2: Container relationship
- `response_options_v2` → response_options_v2: Answer structure
- `question_order`: Sequence within check-in

**Computed Fields:**
- `tracked_metrics`: Inherited from parent check-in
- `Response_Types`: Inherited from response_options

---

### **response_options_v2** - Specific Answer Sets
```
Primary Key: option_id (RO-XXX-XXX format)  
Purpose: Concrete answer choices for questions
```
**Key Fields:**
- `response_choices`: JSON array of selectable options
- `min_value`/`max_value`: Validation bounds
- `scoring_map`: JSON mapping for analytics
- `Response_Types` → response_types_v2: UI component reference

**Usage:** Specific answer sets (e.g., ["1: Struggling", "2: Getting by", "3: Okay", "4: Good", "5: Great"])

---

## Trigger System Architecture

### **trigger_conditions** - Execution Logic (Streamlined)
```
Primary Key: ID (TC0001, TC0002, etc.)
Purpose: Defines WHEN and HOW check-ins fire
```
**Core Fields:**
- `operator_definitions` → operator_definitions: Standardized logic operators
- `operator_parameters`: JSON parameters matching operator's parameter_schema
- `timing_config`: JSON scheduling and frequency configuration ⚠️ **NEEDS REWORK**

**Relationship Fields:**
- `checkins_v2`: Which check-ins use this trigger
- `nudges_v2`: Associated nudge content
- `challenges`: Challenge-related triggers

### **operator_definitions** - Standardized Logic Operators
```
Primary Key: operator_id (logical identifiers)
Purpose: Reusable logical operators with standardized parameters
```
**Key Fields:**
- `category`: Operator classification (Input Detection, Performance, Mathematical, Behavioral, Temporal, Analytical, Adaptive Content)
- `parameter_schema`: JSON schema defining required parameters
- `display_name`: Human-readable operator description

**Usage:** Provides standardized, validated logical operators for trigger conditions

---

## Data Flow & Integration Points

### **Check-in Execution Flow**
1. `trigger_conditions.timing_config` determines **when** to fire
2. `trigger_conditions.operator_definitions` + `operator_parameters` determine **if conditions are met**
3. `checkins_v2` defines **what check-in** to present
4. `checkin_questions_v2` defines **question sequence**
5. `response_options_v2` + `response_types_v2` define **user interface**

### **Data Collection Flow**
1. User responses collected via `response_options_v2` structure
2. Responses scored using `scoring_map` JSON
3. Data correlated with `tracked_metrics` for analysis
4. Results feed back into trigger system for adaptive behavior

### **Content Relationship Flow**
- `recommendations_targeted`: Links check-ins to improvement goals
- `Pillar(s)`: Automatically categorizes check-ins by health domain
- `tracked_metrics`: Connects subjective feedback to objective data

---

## Critical Implementation Notes

### **Timing_Config JSON Structure** ⚠️ **REQUIRES REWORK**
This JSON field needs to handle:
- **Scheduling patterns** (daily, weekly, multiple times per day)
- **Trigger interaction logic** (sequential, parallel, conditional)
- **Frequency management** (adaptive timing, user preference overrides)
- **Context awareness** (user timezone, behavioral patterns)

### **Performance Considerations**
- `trigger_conditions` table must support high-frequency evaluation
- JSON fields require indexing strategy for complex queries
- Lookup/rollup fields create dependency chains affecting performance

### **Scalability Design**
- Check-in types support infinite extensibility via purpose categories
- Operator definitions enable complex logic without code changes
- Response options support any UI pattern via response_types linkage

### **Data Integrity Constraints**
- Every `checkin_questions_v2` must link to valid `response_options_v2`
- Every `response_options_v2` must link to valid `response_types_v2`  
- `operator_parameters` JSON must validate against `operator_definitions.parameter_schema`

This architecture enables rapid check-in creation, complex behavioral triggers, and scalable content management while maintaining data consistency and performance.