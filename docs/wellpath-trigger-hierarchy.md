# WellPath Simple Trigger Hierarchy - MVP Implementation Guide

## Overview

This document outlines the simplified trigger hierarchy system for WellPath, designed for MVP launch with future AI agent capabilities. The system manages 26 operators across 126 trigger conditions using a clean two-level priority system: macro-level groups and micro-level individual priorities.

## Problem Statement

**Original Issue:** Multiple adherence triggers (7-day, 14-day, 21-day streaks) fire simultaneously, creating notification spam without proper interaction logic.

**Solution:** Simple two-tier hierarchy system with macro-level trigger groups for category prioritization and micro-level individual priorities within groups, all managed in Airtable as the single source of truth.

## Database Structure

### Base Information
- **Base ID:** `appy3YQaPkXp7asjj`
- **Base Name:** WellPath Content System

### Core Tables

#### `trigger_conditions` Table - Main trigger logic

**Essential Fields (KEEP):**

| Field Name | Type | Purpose | Example Values |
|------------|------|---------|----------------|
| `ID` | Single Line Text | Trigger identifier | TC0012, TC0019, TC0027 |
| `name` | Single Line Text | Human readable name | "5 of 7 days on target" |
| `Description` | Long Text | What this trigger does | Detailed trigger description |
| `operator_definitions` | Link | Links to standardized operators | Links to 26 operators |
| `operator_parameters` | Long Text (JSON) | Operator configuration | `{"target_days": 5, "window_days": 7}` |
| `priority_level` | Number | Micro-level priority (1-10) | 1, 3, 5, 8 |
| `trigger_group` | Link | Macro-level group assignment | Links to trigger_groups |
| `cooldown_hours` | Number | Optional individual cooldown override | 24, 48, 168 |
| `ai_context_tags` | Long Text | Machine-readable tags for AI | "celebration, achievement, recovery" |
| `max_per_day` | Number | Daily firing limit per user | 1, 3, 5 |

**Content Relationship Fields (KEEP):**
- `Nudges`, `Challenges`, `Check-ins`, `Education Modules`, `nudges_generated`, `checkins_v2 (2)`

**Fields to DELETE (manually in Airtable):**
- `suppression_logic` - Over-complex JSON rules
- `trigger_execution_log` & `trigger_execution_log 2` - Links to deleted tables
- `this_trigger_suppresses` & `this_trigger_suppressed_by` - Over-engineered relationships
- `applicable_suppression_rules` - Links to deleted table
- `simple_suppression_rules` - Redundant text rules

#### `trigger_groups` Table - Macro-level organization

**Table ID:** `tblk5FFRzJDLTzE7W`

| Field Name | Type | Purpose | Example Values |
|------------|------|---------|----------------|
| `group_name` | Single Line Text | Primary identifier | behavioral_recovery, adherence_streaks |
| `description` | Long Text | What this group does | "Re-engagement after setbacks" |
| `default_priority_range` | Single Line Text | Suggested priority levels | "1-3", "4-6", "7-9" |
| `typical_cooldown_hours` | Number | Default cooldown for group | 24, 48, 168 |
| `group_category` | Single Select | Visual/priority organization | Critical, Performance, Engagement, Contextual |
| `trigger_conditions` | Link | Auto-linked triggers in group | Shows all triggers in this group |

**Fields to DELETE from trigger_groups (manually):**
- `suppression_rules` & `suppression_rules 2` - Links to deleted table

### Tables to DELETE (manually in Airtable)

1. **`suppression_rules`** (tblQr3DSlFeyT1YLb) - Over-engineered rule system
2. **`trigger_execution_log`** (tbljyIVnRDUYyJLRw) - Nice to have, not MVP essential

## Two-Tier Priority System

### Macro-Level: Group Categories (Primary Sort)

| Category | Priority | Purpose | Example Groups |
|----------|----------|---------|----------------|
| **Critical Interventions** | 1 | High-priority behavioral recovery | behavioral_recovery |
| **Performance Milestones** | 2 | Achievement celebrations | adherence_streaks, performance_milestones |
| **Contextual** | 3 | Time-based interventions | contextual_timing |
| **Engagement** | 4 | Basic engagement monitoring | input_detection, random_engagement |

### Micro-Level: Individual Priority (Secondary Sort)

Within each group category, triggers are ranked 1-10:
- **1-3**: Highest priority within group
- **4-6**: Medium priority within group  
- **7-10**: Lower priority within group

### Current Trigger Groups

| Group Name | Category | Priority Range | Cooldown | Purpose |
|------------|----------|----------------|----------|---------|
| `behavioral_recovery` | Critical Interventions | 1-3 | 48-72 hours | Re-engagement after setbacks |
| `adherence_streaks` | Performance Milestones | 4-6 | 168+ hours (7+ days) | Celebrating consistency patterns |
| `performance_milestones` | Performance Milestones | 4-6 | 168+ hours (7+ days) | Achievement celebrations |
| `contextual_timing` | Contextual | 6-8 | 12 hours | Time-based interventions |
| `input_detection` | Engagement | 7-9 | 24 hours | Basic engagement monitoring |
| `random_engagement` | Engagement | 8-10 | 72 hours | Variety and surprise triggers |

## Cooldown Logic for Assessment-Based Triggers

### **Systematic Cooldown Formula: Assessment Period × 2 × 24**

This creates a predictable, non-annoying notification rhythm while ensuring fresh assessment windows.

**Formula:** `Cooldown Hours = Assessment Days × 2 × 24`

**Examples:**
- **1-day assessment:** 1 × 2 × 24 = **48 hours** → User sees content every 3 days max
- **7-day assessment:** 7 × 2 × 24 = **336 hours (14 days)** → User sees content every 21 days max  
- **14-day assessment:** 14 × 2 × 24 = **672 hours (28 days)** → User sees content every 42 days max

**Example - TC0012: "5 of 7 days on target"**
- **Day 7**: Trigger fires (user hit 5 of 7 days)
- **Days 8-21**: Cooldown period (7 × 2 × 24 = 336 hours)
- **Day 22+**: Fresh 7-day window evaluation begins

**Why This Formula Works:**
```javascript
// 1-DAY ASSESSMENT TRIGGER:
// Day 1: Fire trigger ("No input today")
// Days 2-3: 48-hour cooldown 
// Day 4: Can evaluate again → 3-day rhythm

// 7-DAY ASSESSMENT TRIGGER:
// Day 7: Fire trigger ("5 of 7 days met")
// Days 8-21: 336-hour cooldown (14 days)
// Day 22: Fresh 7-day window starts → 21-day rhythm
```

### **Updated Cooldown Guidelines by Assessment Period**

| Assessment Period | Cooldown Formula | Hours | Example Triggers |
|-------------------|------------------|-------|------------------|
| **1 day** | 1 × 2 × 24 = **48 hours** | 48h | "No input today", "Missed daily goal" |
| **3 days** | 3 × 2 × 24 = **144 hours** | 144h | "3-day streak broken" |
| **7 days** | 7 × 2 × 24 = **336 hours** | 336h | "5 of 7 days", "Weekly milestone" |
| **14 days** | 14 × 2 × 24 = **672 hours** | 672h | "Bi-weekly achievements" |
| **30 days** | 30 × 2 × 24 = **1440 hours** | 1440h | "Monthly milestones" |

### **Implementation Function**

```javascript
function calculateCooldownHours(assessmentDays) {
  return assessmentDays * 2 * 24;
}

// Usage examples:
const dailyTriggerCooldown = calculateCooldownHours(1);    // 48 hours
const weeklyTriggerCooldown = calculateCooldownHours(7);   // 336 hours  
const monthlyTriggerCooldown = calculateCooldownHours(30); // 1440 hours

## Implementation Code

### Core Trigger Selection Logic (MVP)

```javascript
// Simple, clean trigger selection for MVP
function selectTriggersForUser(userId, availableTriggers) {
  const now = new Date();
  
  return availableTriggers
    .filter(trigger => {
      // Check daily limit
      const todayCount = getTriggerCountToday(trigger.ID, userId);
      const maxDaily = trigger.max_per_day || 3;
      if (todayCount >= maxDaily) return false;
      
      // Check cooldown (each trigger has its own calculated cooldown)
      const cooldownHours = trigger.cooldown_hours || 48; // Default fallback
      if (isInCooldown(trigger.ID, userId, cooldownHours)) {
        return "SKIP_EVALUATION"; // Don't evaluate during cooldown
      }
      
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

## AI Agent Preparation

### AI Context Tags (Keep as Text Field)

The `ai_context_tags` field uses comma-separated text for maximum flexibility:

**Why not a separate table?**
- **Flexible combinations**: One trigger can have multiple tag types
- **AI learning**: Let AI discover which tag patterns work best  
- **Simple maintenance**: Easy to add/edit tags without table management
- **Avoid over-engineering**: Keep the system simple for MVP

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

### AI-Ready Trigger Evaluation (Future)

```javascript
// Future: AI-powered trigger selection
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

## Current Example Configurations

### Configured Triggers

**TC0012 - "5 of 7 days on target"**
- Priority: 5
- Group: adherence_streaks (Performance Milestones)
- Cooldown: **168 hours (7 days)** - Prevents re-evaluation during assessment window
- Max per day: 1
- AI Tags: "celebration, achievement, positive_reinforcement"
- **Logic**: Fire Day 7 → Skip Days 8-14 → Evaluate again Day 15+

**TC0019 - "No input today"**
- Priority: 8
- Group: input_detection (Engagement)
- Cooldown: 24 hours - Daily reminders still effective
- Max per day: 3
- AI Tags: "reminder, engagement, input_detection, gentle_nudge"

**TC0027 - "Streak Broken After 3+ Days"**
- Priority: 3
- Group: behavioral_recovery (Critical Interventions)
- Cooldown: **48 hours** - Prevents multiple recovery messages while allowing urgent intervention
- Max per day: 1
- AI Tags: "recovery, critical_intervention, behavioral_reset, high_priority"
- **Logic**: After firing, wait 48 hours before checking for new streak breaks

**TC0009 - "3 of 7 days hitting target"**
- Priority: 5
- Group: adherence_streaks (Performance Milestones)
- Cooldown: **168 hours (7 days)** - Matches 7-day assessment window
- Max per day: 1
- AI Tags: "celebration, achievement, progress_recognition, positive_reinforcement"

**TC0010 - "<3 of 7 days hitting target"**
- Priority: 1
- Group: behavioral_recovery (Critical Interventions)
- Cooldown: **336 hours (14 days)** - Longer recovery period for performance crisis
- Max per day: 1
- AI Tags: "recovery, critical_intervention, performance_crisis, high_priority"

## Implementation Phases

### Phase 1: MVP Implementation (Week 1-2)
1. **Clean up Airtable structure** - Delete over-engineered fields and tables
2. **Configure trigger groups** - Set up the 6 core groups with proper categories
3. **Assign triggers to groups** - Categorize all 126 triggers
4. **Set priority levels** - Assign 1-10 priorities within each group
5. **Implement basic selection logic** - Deploy the simple filtering algorithm

### Phase 2: Optimization (Week 3-4)  
1. **Configure AI context tags** - Add meaningful tags to all triggers
2. **Set daily limits** - Configure max_per_day for each trigger based on usage
3. **Fine-tune cooldowns** - Adjust cooldown_hours for triggers that need special timing
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

## Key Benefits

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

## Contact & Support

This simplified system provides a clean foundation for MVP launch while preparing for future AI agent capabilities. The two-tier priority system (macro groups + micro priorities) gives you the control you need now and the structure an AI agent can easily understand and optimize later.

For implementation questions:
- Reference the simple selection algorithm above
- Use trigger groups for macro-level organization  
- Set individual priorities for fine-tuning within groups
- Prepare AI context tags for future agent integration