# WellPath Check-in System - Unified Architecture

## System Overview
The check-in system is a highly configurable framework for collecting user feedback through structured questionnaires. It supports everything from simple data entry to complex behavioral assessments, with intelligent triggering powered by the **WellPath Trigger System**.

## Purpose & Capabilities

The check-in system enables:
- **Subjective data collection** for metrics that can't be automatically tracked
- **Pattern recognition** through structured behavioral assessments  
- **User engagement** via meaningful reflection and feedback opportunities
- **Adaptive personalization** based on user responses and patterns
- **Gap filling** for objective data collection

---

## Core Database Architecture

### Base Information
- **Base ID:** `appy3YQaPkXp7asjj`
- **Base Name:** WellPath Content System

### Primary Tables & Relationships

#### `checkin_types_v2` - Check-in Categories
**Table ID:** `tblJG8ZprK9mMOOz3`
```
Primary Key: type_id (CT001, CT002, etc.)
Purpose: Defines behavioral categories and default scheduling patterns
```

**Key Fields:**
- `purpose`: Categorical classification
  - **Options**: data-entry, reflection, insight-generation, behavior-tracking, experience-tracking, pattern-monitoring, body-awareness, work-wellness, nutrition-awareness
- `default_frequency`: Base scheduling template
  - **Options**: Daily, Weekly, Multiple Daily, User-initiated, Conditional, End-of-Challenge, Mid-Challenge, One-time
- `description`: What this check-in type accomplishes

**Usage:** Templates for check-in behavior and default triggering patterns

---

#### `checkins_v2` - Check-in Instances  
**Table ID:** `tblAjjUE7bQ21mYyf`
```
Primary Key: checkin_id (CK-XXX-XXX-001 format)
Purpose: Individual check-in configurations
```

**Core Configuration Fields:**
- `checkin_type` → checkin_types_v2: Inherits behavioral template
- `checkin_name`: Human-readable identifier
- `description`: What this check-in accomplishes
- `help_text`: User guidance and context

**Relationship Fields:**
- `trigger_conditions` → trigger_conditions: **Defines WHEN to fire** (powered by Trigger System)
- `tracked_metrics` → tracked_metrics: Data correlation targets
- `recommendations_targeted` → recommendations: Improvement focus areas

**Computed Fields:**
- `frequency`: Inherited from checkin_type
- `Pillar(s)`: Rolled up from targeted recommendations  
- `Response_Types`: Aggregated from all questions

---

#### `checkin_questions_v2` - Individual Questions
**Table ID:** `tblNGXf7FRJ8eYCmA`
```
Primary Key: question_id (Q-XXX-001 format)  
Purpose: Atomic question units within check-ins
```

**Key Fields:**
- `parent_checkin` → checkins_v2: Container relationship
- `question_text`: The actual question asked to user
- `question_order`: Sequence within check-in (1, 2, 3...)
- `response_options_v2` → response_options_v2: Answer structure and validation
- `help_text`: Additional context or guidance for user

**Computed Fields:**
- `tracked_metrics`: Inherited from parent check-in
- `Response_Types`: Inherited from response_options

---

#### `response_options_v2` - Specific Answer Sets
**Table ID:** `tblr3Y4xvBT7dYKbI`
```
Primary Key: option_id (RO-XXX-XXX format)
Purpose: Concrete answer choices and validation for questions
```

**Core Fields:**
- `response_choices`: JSON array of selectable options
- `min_value`/`max_value`: Validation bounds for numerical inputs
- `scoring_map`: JSON mapping for analytics and data processing
- `Response_Types` → response_types_v2: UI component reference

**Usage:** Specific answer sets like `["1: Struggling", "2: Getting by", "3: Okay", "4: Good", "5: Great"]`

---

#### `response_types_v2` - Response Input Methods
**Table ID:** `tblQr7KM5e2vYkv8L`
```
Primary Key: type_id (RT001, RT002, etc.)
Purpose: Generic response mechanisms and UI components
```

**Key Fields:**
- `response_type`: UI component type
  - **Options**: Boolean, Scale 1-3/1-5/1-10, Multiple Choice, Free Text, Numerical, Time Entry, Date Entry
- `options_config`: JSON configuration for UI behavior and validation
- `description`: When to use this response type

**Usage:** Reusable UI templates linked to specific response_options_v2 instances

---

## Trigger System Integration

### **trigger_conditions** - Execution Logic
**Table ID:** `tblrqKOn9Jok1Dt9m`
```
Primary Key: ID (TC0001, TC0002, etc.)
Purpose: Defines WHEN and HOW check-ins fire
```

**Core Fields:**
- `operator_definitions` → operator_definitions: Standardized logic operators
- `operator_parameters`: JSON parameters matching operator's parameter_schema
- `timing_config`: JSON scheduling and frequency configuration
- `priority_level`: Micro-level priority (1-10) within trigger groups
- `trigger_group`: Macro-level group assignment for category prioritization
- `assessment_period_days`: Evaluation window length
- `cooldown_hours`: Hours between re-evaluations
- `max_per_day`: Daily firing limit per user
- `ai_context_tags`: Machine-readable tags for AI optimization

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

## Data Flow & Execution Logic

### Check-in Execution Flow
1. **Trigger System** determines **WHEN** to fire check-in via `trigger_conditions`
2. **`operator_definitions`** + **`operator_parameters`** determine **IF conditions are met**
3. **`checkins_v2`** defines **WHAT** check-in to present
4. **`checkin_questions_v2`** defines **question sequence and content**
5. **`response_options_v2` + `response_types_v2`** define **user interface and validation**
6. **User responses** collected and processed via scoring_map
7. **Data correlation** with tracked_metrics for analysis

### Trigger Integration - Key Trigger Types for Check-ins
- **`scheduled_timepoint`**: Time-based check-ins (morning, evening, specific times)
- **`user_initiated`**: Manual check-ins triggered by user action
- **`challenge_completion`**: Check-ins after completing challenges/milestones
- **`user_struggle_detected`**: Supportive check-ins when user indicates difficulty
- **`cumulative_missing_input_screening`**: Re-engagement check-ins for inactive users

### Data Collection Flow
1. **User responses** collected via `response_options_v2` structure
2. **Response scoring** using `scoring_map` JSON for quantitative analysis
3. **Data correlation** with `tracked_metrics` for objective/subjective pattern analysis
4. **Feedback loop** into trigger system for adaptive check-in timing and content

### Content Relationship Flow
- **`recommendations_targeted`**: Links check-ins to specific improvement goals
- **`Pillar(s)`**: Automatically categorizes check-ins by health domain (Sleep, Movement, Nutrition, etc.)
- **`tracked_metrics`**: Connects subjective feedback to objective data for correlation analysis

---

## Check-in Categories & Examples

### Data Entry Check-ins
**Purpose:** Fill gaps in objective data tracking
- **Morning Sleep Quality** (CK-SLEEP-MORNING-001): Post-sleep subjective assessment
- **Evening Nutrition Reflection** (CK-NUTRITION-EVENING-001): Daily nutrition satisfaction and patterns
- **Movement Quality Assessment** (CK-MOVEMENT-QUALITY-001): Exercise effectiveness and enjoyment

### Reflection Check-ins  
**Purpose:** Pattern recognition and self-awareness building
- **Weekly Progress Reflection** (CK-WEEKLY-PROGRESS-001): Weekly wins, challenges, and insights
- **End of Day Reflection** (CK-EOD-REFLECTION-001): Daily energy, mood, and satisfaction assessment
- **Stress Pattern Analysis** (CK-STRESS-WEEKLY-001): Weekly stress trigger and coping strategy review

### Experience Tracking Check-ins
**Purpose:** Capture qualitative experiences that impact health outcomes
- **Work Energy Assessment** (CK-WORK-ENERGY-001): Daily work stress and energy patterns
- **Social Connection Quality** (CK-SOCIAL-WEEKLY-001): Weekly relationship satisfaction and loneliness assessment
- **Cognitive Function Tracking** (CK-COGNITIVE-DAILY-001): Daily mental clarity, focus, and cognitive symptoms

### Pattern Monitoring Check-ins
**Purpose:** Identify long-term trends and behavioral patterns
- **Monthly Health Review** (CK-MONTHLY-HEALTH-001): Comprehensive monthly health and progress assessment  
- **Habit Formation Progress** (CK-HABIT-PROGRESS-001): Weekly habit adoption difficulty and success tracking
- **Seasonal Pattern Recognition** (CK-SEASONAL-PATTERNS-001): Quarterly seasonal health pattern identification

---

## Implementation Guidelines

### Naming Conventions
- **Check-in IDs**: `CK-[CATEGORY]-[TYPE]-###` or `CK###-[MID/END]` for recommendation-specific
- **Question IDs**: `Q[###]-[TYPE]-##`
- **Response Option IDs**: `RO###` (incremental)

### Design Principles
1. **Purpose-Driven**: Every check-in should serve a clear, specific purpose
2. **User-Centric**: Questions should be actionable and meaningful to users
3. **Data-Informed**: Responses should correlate with objective data when possible
4. **Timing-Optimal**: Check-ins should fire at moments when users can provide quality responses
5. **Minimal Friction**: Keep check-ins concise and easy to complete

### Quality Assurance Checklist
- [ ] Check-in serves clear purpose (subjective feedback/adherence support)
- [ ] Questions are specific and actionable
- [ ] Response options cover expected user responses  
- [ ] Timing makes sense for user workflow
- [ ] Links properly to relevant recommendations and metrics
- [ ] Response_types field is populated (ALWAYS REQUIRED)
- [ ] Help text provides clear guidance
- [ ] Fits within broader check-in ecosystem without overlap or redundancy

---

## Advanced Features

### Adaptive Check-in Logic
**Powered by AI Context Tags in Trigger System**

AI-enhanced check-ins can:
- **Optimize timing** based on user response patterns and quality
- **Personalize questions** based on user goals and current challenges
- **Adapt frequency** based on user engagement and data quality
- **Smart content selection** based on user context and recent activity

### Response Pattern Analysis
- **Consistency tracking** over time to identify reliability and changes
- **Correlation analysis** between subjective responses and objective metrics  
- **Trend identification** for early intervention opportunities
- **Personalization opportunities** based on individual response patterns

### Integration Points
- **Recommendations System**: Check-in responses inform recommendation adjustments
- **Nudge System**: Check-in patterns trigger supportive nudges and content
- **Challenge System**: Check-in responses unlock relevant challenges and milestones
- **Analytics Platform**: Check-in data feeds comprehensive health pattern analysis

---

## Technical Implementation Notes

### Response Validation
- **Type checking**: Ensure responses match expected format (numerical, text, selection)
- **Range validation**: Check min/max values for numerical inputs
- **Required field enforcement**: Critical questions marked as required
- **Data sanitization**: Clean and validate all user inputs before storage

### Performance Considerations
- **Lazy loading**: Load questions progressively to improve response time
- **Caching strategy**: Cache frequently accessed check-in configurations
- **Database optimization**: Index key lookup fields for fast trigger→check-in resolution
- **User experience**: Minimize loading times and provide clear progress indicators
- **Trigger evaluation**: `trigger_conditions` table must support high-frequency evaluation
- **JSON optimization**: JSON fields require indexing strategy for complex queries

### Scalability Design
- **Modular architecture**: Easy to add new check-in types and question formats
- **Flexible response options**: Support for any UI pattern via response_types linkage
- **Dynamic configuration**: Check-in behavior can be modified without code changes
- **Integration ready**: Clean APIs for integration with external health platforms
- **Operator extensibility**: Complex logic without code changes via operator_definitions

### Data Integrity Constraints
- Every `checkin_questions_v2` must link to valid `response_options_v2`
- Every `response_options_v2` must link to valid `response_types_v2`  
- `operator_parameters` JSON must validate against `operator_definitions.parameter_schema`
- `Response_types` field must always be populated

---

## Success Metrics & Validation

### User Engagement Metrics
- **Completion rates** by check-in type and timing
- **Time to completion** per check-in (target: <2 minutes)
- **Response quality** and thoughtfulness indicators
- **User retention** on different check-in frequencies

### Data Quality Metrics
- **Response consistency** over time periods
- **Correlation strength** with objective health data
- **Pattern identification** success rate for actionable insights
- **Missing data reduction** where check-ins fill objective tracking gaps

### Health Outcome Metrics
- **Subjective improvement** in user-reported ratings over time
- **Objective correlation** with measurable health improvements
- **Recommendation adherence** improvements driven by check-in insights
- **User satisfaction** with personalized insights and pattern recognition

---

This unified check-in system transforms WellPath from basic metric tracking to comprehensive lifestyle pattern recognition and personalized health optimization, powered by intelligent triggering and meaningful user engagement.
