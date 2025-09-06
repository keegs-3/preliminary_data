# WellPath Trigger System Architecture - Updated

## System Overview

The WellPath trigger system is the foundational behavioral intervention platform that manages **126 trigger conditions** across **26 standardized operators**. This system serves as the execution engine for **check-ins, nudges, challenges, and educational content delivery** across the entire WellPath ecosystem.

## Problem Statement & Solution

**Original Issue:** Multiple adherence triggers (7-day, 14-day, 21-day streaks) fire simultaneously, creating notification spam without proper interaction logic.

**Solution:** Simple two-tier hierarchy system with macro-level trigger groups for category prioritization and micro-level individual priorities within groups, all managed in Airtable as the single source of truth.

---

## Core Database Structure

### Base Information
- **Base ID:** `appy3YQaPkXp7asjj`
- **Base Name:** WellPath Content System

### Primary Tables

#### `trigger_conditions` Table - Main Trigger Logic
**Table ID:** `tblrqKOn9Jok1Dt9m`

**Essential Fields:**

| Field Name | Type | Purpose | Example Values |
|------------|------|---------|----------------|
| `ID` | Single Line Text | Trigger identifier | TC0012, TC0019, TC0027 |
| `name` | Single Line Text | Human readable name | "5 of 7 days on target" |
| `Description` | Long Text | What this trigger does | Detailed trigger description |
| `operator_definitions` | Link | Links to standardized operators | Links to 26 operators |
| `operator_parameters` | Long Text (JSON) | Operator configuration | `{"target_days": 5, "window_days": 7}` |
| `priority_level` | Number | Micro-level priority (1-10) | 1, 3, 5, 8 |
| `trigger_group` | Link | Macro-level group assignment | Links to trigger_groups |
| `assessment_period_days` | Number | Evaluation window length | 1, 7, 14, 30, 60 |
| `cooldown_hours` | Formula | Hours between re-evaluations | 24, 168, 336 |
| `max_per_day` | Number | Daily firing limit per user | 1, 3, 5, 999 |
| `ai_context_tags` | Long Text | Machine-readable tags for AI | "celebration, achievement, recovery" |

**Content Relationship Fields:**
- `Nudges` → nudges table (legacy)
- `nudges_generated` → nudges_v2 table  
- `Challenges` → challenges table
- `Check-ins` → check_ins table
- `checkins_v2 (2)` → checkins_v2 table
- `Education Modules` → education_modules table

#### `trigger_groups` Table - Macro-Level Organization
**Table ID:** `tblk5FFRzJDLTzE7W`

| Field Name | Type | Purpose | Example Values |
|------------|------|---------|----------------|
| `group_name` | Single Line Text | Primary identifier | behavioral_recovery, adherence_streaks |
| `description` | Long Text | What this group does | "Re-engagement after setbacks" |
| `default_priority_range` | Single Line Text | Suggested priority levels | "1-3", "4-6", "7-9" |
| `typical_cooldown_hours` | Number | Default cooldown for group | 24, 48, 168 |
| `group_category` | Single Select | Visual/priority organization | Critical, Performance, Engagement, Contextual |
| `trigger_conditions` | Link | Auto-linked triggers in group | Shows all triggers in this group |

#### `operator_definitions` Table - Standardized Logic Operators
**Table ID:** `tblGmoQqYZwynqejS`

| Field Name | Type | Purpose | Example Values |
|------------|------|---------|----------------|
| `operator_id` | Single Line Text | Logical identifier | no_input_detected, streak_met |
| `display_name` | Single Line Text | Human readable name | "No Input Detected", "Streak Achievement" |
| `category` | Single Line Text | Operator classification | Input Detection, Performance, Mathematical |
| `description` | Long Text | What this operator does | "Fires when no tracked input has been logged" |
| `parameter_schema` | Long Text (JSON) | Required parameters schema | `{"time_window": "string", "threshold_hours": "number"}` |
| `active` | Checkbox | Whether operator is available | ✓ |

---

## Two-Tier Priority System

### Macro-Level: Group Categories (Primary Sort)

| Category | Priority | Purpose | Groups |
|----------|----------|---------|--------|
| **Critical Interventions** | 1 | High-priority behavioral recovery | behavioral_recovery |
| **Performance Milestones** | 2 | Achievement celebrations | adherence_streaks, performance_milestones |
| **Contextual** | 3 | Time-based interventions | contextual_timing |
| **Engagement** | 4 | Basic engagement monitoring | input_detection, random_engagement |

### Micro-Level: Individual Priority (Secondary Sort)

Within each group category, triggers are ranked 1-10:
- **1-3**: Highest priority within group (critical interventions)
- **4-6**: Medium priority within group (achievements, milestones)
- **7-10**: Lower priority within group (routine check-ins, random content)

### Current Trigger Groups

| Group Name | Category | Priority Range | Purpose | Trigger Count |
|------------|----------|----------------|---------|---------------|
| `behavioral_recovery` | Critical Interventions | 1-3 | Re-engagement after setbacks | 12 |
| `adherence_streaks` | Performance Milestones | 4-6 | Celebrating consistency patterns | 6 |
| `performance_milestones` | Performance Milestones | 4-6 | Achievement celebrations | 8 |
| `input_detection` | Engagement | 7-9 | Basic engagement monitoring | 4 |
| `contextual_timing` | Contextual | 6-8 | Time-based interventions | 83 |
| `random_engagement` | Engagement | 8-10 | Variety and surprise triggers | 13 |

---

## Operator Categories & Definitions

### Input Detection Operators
- **`no_input_detected`**: Fires when no tracked input logged within time window
- **`check_in_missed`**: Fires when scheduled check-in not completed in timeframe
- **`first_time_entry`**: Fires when user logs first entry for specific behavior
- **`user_initiated`**: Fires when manually triggered by user action

### Performance Operators  
- **`streak_met`**: Fires when user achieves consecutive streak of hitting target
- **`below_target`**: Fires when performance below defined target threshold
- **`near_target`**: Fires when performance close to but not meeting target
- **`above_threshold`**: Fires when performance exceeds specified threshold
- **`regression_detected`**: Fires on significant decline from previous periods

### Mathematical Operators
- **`count_below_threshold`**: Fires when count of days meeting criteria below threshold
- **`average_below_percentage`**: Fires when rolling average falls below percentage of target
- **`exact_hit_days`**: Fires when user hits target on exactly specified number of days
- **`improvement_over_previous`**: Fires when current period shows improvement

### Behavioral Operators
- **`streak_broken`**: Fires when positive streak broken after achieving minimum length
- **`challenge_completion`**: Fires when user completes specific challenge or milestone
- **`challenge_initiation`**: Fires when new challenge begins or started by user

### Temporal Operators
- **`scheduled_timepoint`**: Fires at specific time or schedule (daily, weekly, monthly)
- **`weekday_range`**: Fires during specific range of weekdays
- **`week_range_scheduled`**: Fires at specific time during specific program weeks
- **`week_range_random`**: Fires at random time within specific program weeks

### Analytical Operators
- **`timing_skew_detected`**: Fires when behavior timing patterns show significant skew
- **`composite_condition`**: Fires when multiple conditions met using logical operators

### Adaptive Content Operators
- **`qualitative_recommendation_active`**: Fires when qualitative-only recommendation active
- **`randomized_rotation_trigger`**: Fires based on randomized rotation logic for variety
- **`user_struggle_detected`**: Fires when check-in indicates low confidence or difficulty

---

## Cooldown & Rate Limiting Logic

### Assessment Period-Based Cooldown Formula
**Formula:** `Cooldown Hours = Assessment Days × 2 × 24`

**Examples:**
- **1-day assessment:** 1 × 2 × 24 = **48 hours** → Content every 3 days max
- **7-day assessment:** 7 × 2 × 24 = **336 hours (14 days)** → Content every 21 days max  
- **30-day assessment:** 30 × 2 × 24 = **1440 hours (60 days)** → Content every 90 days max

### Max Per Day Logic
Controls maximum times a trigger can fire per user per day across ALL their recommendations:

- **999 (No practical limit)**: Milestone achievements, one-time events that should all fire if earned
- **1 (Daily maximum)**: Critical interventions, daily scheduled check-ins, weekly patterns
- **2-3 (Moderate allowance)**: Input detection reminders, performance feedback
- **3-5 (Higher frequency)**: Micro check-ins designed for multiple daily interactions

---

## Implementation Code

### Core Trigger Selection Logic (MVP)

```javascript
function selectTriggersForUser(userId, availableTriggers) {
  const now = new Date();
  
  return availableTriggers
    .filter(trigger => {
      // Check daily limit
      const todayCount = getTriggerCountToday(trigger.ID, userId);
      const maxDaily = trigger.max_per_day || 3;
      if (todayCount >= maxDaily) return false;
      
      // Check cooldown
      const cooldownHours = trigger.cooldown_hours || 48;
      if (isInCooldown(trigger.ID, userId, cooldownHours)) return false;
      
      return true;
    })
    .sort((a, b) => {
      // Primary sort: group category priority
      const groupPriorityA = getGroupCategoryPriority(a.trigger_group?.group_category);
      const groupPriorityB = getGroupCategoryPriority(b.trigger_group?.group_category);
      if (groupPriorityA !== groupPriorityB) return groupPriorityA - groupPriorityB;
      
      // Secondary sort: individual priority within group
      return a.priority_level - b.priority_level;
    })
    .slice(0, 3); // Max 3 triggers per evaluation
}

function getGroupCategoryPriority(category) {
  switch(category) {
    case 'Critical Interventions': return 1;
    case 'Performance Milestones': return 2; 
    case 'Contextual': return 3;
    case 'Engagement': return 4;
    default: return 5;
  }
}
```

### Cooldown Check Function

```javascript
function isInCooldown(triggerId, userId, cooldownHours) {
  const lastFired = getLastTriggerTime(triggerId, userId);
  if (!lastFired) return false;
  
  const now = new Date();
  const cooldownMs = cooldownHours * 60 * 60 * 1000;
  return (now - lastFired) < cooldownMs;
}
```

### Daily Limit Check Function

```javascript
function getTriggerCountToday(triggerId, userId) {
  const today = new Date();
  const startOfDay = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  
  // Query your trigger execution log or user activity table
  return countTriggerExecutions(triggerId, userId, startOfDay);
}
```

---

## AI Agent Preparation

### AI Context Tags
The `ai_context_tags` field uses comma-separated text for maximum flexibility:

**Tag Categories:**
- **Emotional**: celebration, recovery, encouragement, gentle_nudge, motivation
- **Behavioral**: achievement, reminder, intervention, reset, habit_building
- **Timing**: morning, evening, post_workout, work_hours, weekend
- **Urgency**: critical_intervention, high_priority, routine, optional, emergency
- **Content**: educational, celebratory, corrective, informational, interactive

**Example Usage:**
```javascript
// AI parsing is simple and flexible
const tags = trigger.ai_context_tags.split(',').map(t => t.trim());
// Result: ["celebration", "achievement", "positive_reinforcement"]

// AI can group and understand patterns
const isCelebration = tags.includes('celebration');
const isHighPriority = tags.includes('high_priority'); 
const isMorningOptimal = tags.includes('morning');
```

### Future AI-Powered Trigger Selection

```javascript
async function aiSelectOptimalTriggers(eligibleTriggers, userContext) {
  const triggerContext = eligibleTriggers.map(trigger => ({
    trigger_id: trigger.ID,
    priority_level: trigger.priority_level,
    group_category: trigger.trigger_group?.group_category,
    context_tags: trigger.ai_context_tags?.split(',').map(t => t.trim()),
    max_per_day: trigger.max_per_day,
    description: trigger.Description
  }));
  
  // AI agent evaluates optimal intervention strategy
  const aiDecision = await aiAgent.evaluateOptimalInterventions({
    available_triggers: triggerContext,
    user_context: userContext,
    recent_activity: getUserRecentActivity(userContext.userId),
    current_goals: getUserGoals(userContext.userId)
  });
  
  return aiDecision.selected_triggers;
}
```

---

## Content Integration Points

### Check-ins Integration
- **Trigger → Check-in**: `trigger_conditions.checkins_v2` links to specific check-in configurations
- **Timing**: Trigger determines WHEN to fire, check-in defines WHAT questions to ask
- **Data Flow**: Check-in responses feed back into trigger evaluation for adaptive behavior

### Nudges Integration  
- **Trigger → Nudge**: `trigger_conditions.nudges_generated` links to nudge content
- **Content Selection**: AI can choose optimal nudge based on trigger context tags
- **Personalization**: User response patterns influence future trigger→nudge selections

### Challenges Integration
- **Trigger → Challenge**: `trigger_conditions.Challenges` links to challenge content
- **Lifecycle Events**: Triggers fire at challenge start, midpoint, completion
- **Achievement Recognition**: Performance milestones celebrate challenge progress

### Education Integration
- **Trigger → Education**: `trigger_conditions.Education Modules` links to educational content
- **Contextual Learning**: Triggers deliver education at optimal moments
- **Progressive Disclosure**: Educational content complexity adapts to user progress

---

## Implementation Phases

### Phase 1: MVP Implementation
1. **Clean up Airtable structure** - Delete over-engineered fields and tables ✅
2. **Configure trigger groups** - Set up the 6 core groups with proper categories ✅
3. **Assign triggers to groups** - Categorize all 126 triggers ✅
4. **Set priority levels** - Assign 1-10 priorities within each group ✅
5. **Implement basic selection logic** - Deploy the simple filtering algorithm

### Phase 2: Optimization 
1. **Configure AI context tags** - Add meaningful tags to all triggers ✅
2. **Set daily limits** - Configure max_per_day for each trigger based on usage ✅
3. **Fine-tune cooldowns** - Adjust cooldown_hours for triggers that need special timing ✅
4. **Monitor and adjust** - Track trigger firing patterns and optimize

### Phase 3: AI Preparation (Month 2)
1. **Enhance context tags** - Refine AI tags based on usage patterns
2. **Build AI evaluation framework** - Prepare for AI agent integration
3. **Create user context system** - Build comprehensive user behavior context
4. **Test AI decision making** - A/B test AI vs rule-based selection

### Phase 4: Full AI Agent (Future)
1. **Deploy AI agent** - Replace rule-based system with AI decision making
2. **Continuous learning** - AI learns from user responses and engagement
3. **Personalization** - AI adapts trigger selection to individual user patterns
4. **Advanced optimization** - AI optimizes timing, content, and frequency

---

## Success Metrics

### Immediate MVP Metrics
1. **Notification volume** - Max 3 triggers per evaluation period
2. **User engagement** - Response rates by group category
3. **Spam prevention** - No more than max_per_day limits
4. **Priority effectiveness** - Higher priority triggers fire more often

### AI Readiness Metrics
1. **Context tag coverage** - % of triggers with meaningful AI tags
2. **Group distribution** - Balanced firing across categories
3. **User satisfaction** - Feedback on trigger relevance and timing
4. **Personalization potential** - Variability in user trigger preferences

---

## Key Benefits

### ✅ **Universal Content Engine**
- Single trigger system serves check-ins, nudges, challenges, and education
- Consistent priority and cooldown logic across all content types
- Unified user experience with coordinated interventions

### ✅ **Simple & Clean**
- Two-tier priority system is easy to understand and maintain
- No complex suppression rules to debug
- Clear macro/micro level organization

### ✅ **AI-Ready**
- Context tags prepare for future AI agent
- Priority system AI can easily understand
- User constraints (daily limits, cooldowns) clearly defined

### ✅ **Scalable**
- Easy to add new trigger groups
- Simple to categorize new triggers
- Flexible priority assignment within groups

### ✅ **Maintainable**
- All logic in Airtable as single source of truth
- Human-readable group categories and priorities
- Easy debugging with clear hierarchy

### ✅ **MVP-Focused**
- Minimal complexity for initial launch
- Proven simple filtering approach
- Room to grow into AI sophistication

---

This simplified trigger system provides a clean foundation for MVP launch while preparing for future AI agent capabilities across all WellPath content types.
