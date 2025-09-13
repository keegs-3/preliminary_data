#!/usr/bin/env python3
"""
Config Demo Test

Shows realistic weekly sample data for each REC config and what the algorithm outputs.
This gives you a clear view of what each config actually does with real data.

Focus: Demo each config with sample data rather than pass/fail testing.
"""

import sys
import os
import glob
import json
import random
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Union
from dataclasses import dataclass
import traceback

# Add src to path for algorithm imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

@dataclass
class ConfigDemo:
    """Demo showing what a config does with sample data"""
    config_name: str
    rec_id: str
    algorithm_type: str
    recommendation_text: str
    sample_data: List[float]
    data_description: str
    daily_scores: List[float]
    weekly_score: float
    unit: str
    target_info: str
    error_message: Optional[str] = None
    sleep_composite_data: Optional[List[Dict[str, float]]] = None

class RealisticDataGenerator:
    """Generates realistic weekly data that makes sense for each recommendation"""
    
    def __init__(self, config_data: Dict[str, Any]):
        self.config_data = config_data
        self.schema = config_data.get('configuration_json', {}).get('schema', {})
        self.algorithm_type = config_data.get('scoring_method', 'unknown')
        self.rec_text = config_data.get('metadata', {}).get('recommendation_text', '')
        
    def generate_weekly_demo_data(self) -> Tuple[List[float], str, str]:
        """Generate one realistic weekly scenario with description and target info"""
        
        if self.algorithm_type == 'proportional':
            return self._generate_proportional_demo()
        elif self.algorithm_type == 'binary_threshold':
            return self._generate_binary_demo()
        elif self.algorithm_type == 'minimum_frequency':
            return self._generate_frequency_demo()
        elif self.algorithm_type == 'weekly_elimination':
            return self._generate_elimination_demo()
        elif self.algorithm_type == 'zone_based':
            return self._generate_zone_demo()
        elif self.algorithm_type == 'constrained_weekly_allowance':
            return self._generate_allowance_demo()
        elif self.algorithm_type == 'proportional_frequency_hybrid':
            return self._generate_hybrid_demo()
        elif self.algorithm_type == 'sleep_composite':
            return self._generate_sleep_demo()
        elif self.algorithm_type == 'categorical_filter_threshold':
            return self._generate_categorical_demo()
        elif self.algorithm_type == 'composite_weighted':
            return self._generate_composite_demo()
        else:
            return [1.0] * 7, "Generic test data", "Unknown algorithm"
    
    def _generate_proportional_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic proportional scoring demo"""
        target = self.schema.get('target', 5.0)
        unit = self.schema.get('unit', 'units')
        evaluation_period = self.schema.get('evaluation_period', 'daily')
        frequency_requirement = self.schema.get('frequency_requirement', 'daily')
        
        # Check if this is weekly evaluation
        is_weekly = 'weekly' in evaluation_period.lower() or 'weekly' in frequency_requirement.lower()
        
        if is_weekly:
            # Weekly target - distribute across workout days
            if 'cardio' in self.rec_text.lower() or 'exercise' in self.rec_text.lower():
                # Cardio/exercise - realistic workout distribution
                data = [30, 0, 45, 0, 15, 0, 0]  # Total = 90 minutes across 3 days
                desc = f"Weekly workout distribution - {sum(data)} total minutes across workout days"
            elif 'zone' in self.rec_text.lower():
                # Zone 2 cardio pattern
                data = [35, 0, 40, 0, 15, 0, 0]  # 90 minutes total
                desc = f"Zone 2 cardio sessions - {sum(data)} total minutes per week"
            else:
                # Generic weekly target - spread across days
                daily_avg = target / 7
                data = [daily_avg * 2, 0, daily_avg * 2.5, daily_avg * 0.5, daily_avg * 2, 0, 0]
                desc = f"Weekly total distribution - {sum(data):.0f} total {unit}"
            
            target_info = f"Weekly Target: {target} {unit}/week (sum of daily values)"
        else:
            # Daily target - existing logic
            if 'fiber' in self.rec_text.lower():
                # Fiber sources - dynamic realistic eating pattern
                data = []
                for day in range(7):
                    # Generate around target with realistic variation
                    base_intake = random.uniform(target * 0.4, target * 1.3)
                    data.append(round(base_intake, 1))
                desc = "Daily fiber source intake - dynamic variation around target"
            elif 'water' in self.rec_text.lower():
                # Water - dynamic hydration pattern
                data = []
                for day in range(7):
                    # Weekends tend to be lower, weekdays higher
                    if day in [5, 6]:  # Weekend
                        multiplier = random.uniform(0.6, 0.9)
                    else:  # Weekday
                        multiplier = random.uniform(0.8, 1.2)
                    daily_intake = target * multiplier
                    data.append(round(daily_intake, 1))
                desc = "Daily water intake - dynamic with weekend/weekday patterns"
            elif 'step' in self.rec_text.lower():
                # Steps - dynamic activity pattern
                data = []
                for day in range(7):
                    if day in [5, 6]:  # Weekend - lower activity
                        multiplier = random.uniform(0.6, 0.9)
                    else:  # Weekday - higher activity
                        multiplier = random.uniform(0.9, 1.3)
                    daily_steps = target * multiplier
                    data.append(round(daily_steps, 0) if target >= 1000 else round(daily_steps, 1))
                desc = "Daily steps - dynamic with higher midweek, lower weekend activity"
            elif 'protein' in self.rec_text.lower() or 'serving' in self.rec_text.lower():
                # Protein servings - dynamic meal-based pattern
                data = []
                for day in range(7):
                    # Realistic variation in meal planning
                    multiplier = random.uniform(0.6, 1.3)
                    daily_servings = target * multiplier
                    data.append(round(daily_servings, 1))
                desc = "Daily protein servings - dynamic meal planning variation"
            else:
                # Generic daily target - dynamic
                data = []
                for day in range(7):
                    multiplier = random.uniform(0.5, 1.4)
                    daily_value = target * multiplier
                    data.append(round(daily_value, 1))
                desc = f"Daily values with dynamic variation around {target} target"
            
            target_info = f"Daily Target: {target} {unit}/day"
        
        return data, desc, target_info
    
    def _generate_binary_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic binary threshold demo with dynamic variance"""
        threshold = self.schema.get('threshold', 1.0)
        operator = self.schema.get('comparison_operator', '>=')
        unit = self.schema.get('unit', 'units')
        
        # Generate realistic success/failure patterns dynamically
        scenario_type = random.choice(['high_success', 'moderate_success', 'struggling', 'inconsistent'])
        data = []
        
        if 'vitamin' in self.rec_text.lower() or 'supplement' in self.rec_text.lower():
            # Binary vitamin/supplement - 0 or 1 with realistic adherence patterns
            success_rates = {
                'high_success': 0.85,
                'moderate_success': 0.65, 
                'struggling': 0.45,
                'inconsistent': 0.55
            }
            success_rate = success_rates[scenario_type]
            
            for day in range(7):
                data.append(1 if random.random() < success_rate else 0)
            desc = f"Daily supplement taking - {scenario_type} adherence pattern"
            target_info = f"Goal: {operator}{threshold} {unit} daily"
            
        elif 'workout' in self.rec_text.lower() or 'exercise' in self.rec_text.lower():
            # Exercise with realistic patterns
            if threshold >= 20:  # Minutes threshold
                for day in range(7):
                    if scenario_type == 'high_success':
                        # Usually exceed threshold, occasional rest
                        if random.random() < 0.85:
                            data.append(random.uniform(threshold * 1.1, threshold * 2.0))
                        else:
                            data.append(random.uniform(0, threshold * 0.3))  # Rest day
                    elif scenario_type == 'moderate_success':
                        # Mix of good days and rest days
                        if random.random() < 0.6:
                            data.append(random.uniform(threshold * 0.9, threshold * 1.5))
                        else:
                            data.append(random.uniform(0, threshold * 0.7))
                    elif scenario_type == 'struggling':
                        # Often fall short or skip
                        if random.random() < 0.4:
                            data.append(random.uniform(threshold * 0.5, threshold * 1.1))
                        else:
                            data.append(random.uniform(0, threshold * 0.6))
                    else:  # inconsistent
                        # Very variable - great days mixed with off days
                        if random.random() < 0.3:
                            data.append(random.uniform(threshold * 1.5, threshold * 2.5))  # Great days
                        elif random.random() < 0.6:
                            data.append(random.uniform(0, threshold * 0.4))  # Off days
                        else:
                            data.append(random.uniform(threshold * 0.7, threshold * 1.2))  # Average days
                desc = f"Daily exercise minutes - {scenario_type} pattern"
            else:
                # Binary exercise completion
                success_rates = {
                    'high_success': 0.9,
                    'moderate_success': 0.65,
                    'struggling': 0.4,
                    'inconsistent': 0.55
                }
                success_rate = success_rates[scenario_type]
                for day in range(7):
                    data.append(1 if random.random() < success_rate else 0)
                desc = f"Daily exercise completion - {scenario_type} pattern"
            target_info = f"Goal: {operator}{threshold} {unit} daily"
            
        else:
            # Generic binary threshold with realistic variance
            threshold_val = float(threshold)
            for day in range(7):
                if operator in ['>=', '>']:
                    # Need to meet or exceed threshold
                    if scenario_type == 'high_success' and random.random() < 0.8:
                        # Usually exceed
                        data.append(random.uniform(threshold_val * 1.1, threshold_val * 2.0))
                    elif scenario_type == 'moderate_success' and random.random() < 0.6:
                        # Sometimes meet
                        data.append(random.uniform(threshold_val * 0.9, threshold_val * 1.4))
                    elif scenario_type == 'struggling' and random.random() < 0.35:
                        # Often fall short
                        data.append(random.uniform(threshold_val * 0.8, threshold_val * 1.2))
                    else:
                        # Below threshold
                        data.append(random.uniform(threshold_val * 0.2, threshold_val * 0.9))
                else:  # <= or <
                    # Need to stay under threshold
                    if scenario_type == 'high_success' and random.random() < 0.8:
                        # Usually stay under
                        data.append(random.uniform(threshold_val * 0.3, threshold_val * 0.9))
                    elif scenario_type == 'moderate_success' and random.random() < 0.6:
                        # Sometimes succeed
                        data.append(random.uniform(threshold_val * 0.6, threshold_val * 1.1))
                    elif scenario_type == 'struggling' and random.random() < 0.35:
                        # Sometimes succeed
                        data.append(random.uniform(threshold_val * 0.7, threshold_val * 1.2))
                    else:
                        # Over threshold - failed day
                        data.append(random.uniform(threshold_val * 1.1, threshold_val * 2.0))
            desc = f"Daily values relative to {threshold} threshold - {scenario_type} pattern"
            target_info = f"Goal: {operator}{threshold} {unit} daily"
        
        return data, desc, target_info
    
    def _generate_frequency_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic frequency requirement demo"""
        daily_threshold = self.schema.get('daily_threshold', 1.0)
        required_days = self.schema.get('required_days', 3)
        comparison = self.schema.get('daily_comparison', '>=')
        unit = self.schema.get('unit', 'units')
        
        if isinstance(daily_threshold, str) and ':' in daily_threshold:
            # Time-based (like caffeine cutoff) - dynamic scenarios
            hour = float(daily_threshold.split(':')[0]) if ':' in str(daily_threshold) else 14
            scenario_type = random.choice(['mostly_compliant', 'struggling', 'inconsistent', 'barely_passing'])
            data = []
            
            for day in range(7):
                if scenario_type == 'mostly_compliant':
                    # Usually succeed, occasional slip
                    if random.random() < 0.85:
                        data.append(round(random.uniform(hour - 3, hour - 0.2), 1))  # Before threshold
                    else:
                        data.append(round(random.uniform(hour + 0.5, hour + 3), 1))  # After threshold
                elif scenario_type == 'struggling':
                    # Often fail to meet cutoff
                    if random.random() < 0.4:
                        data.append(round(random.uniform(hour - 2, hour - 0.1), 1))  # Before threshold
                    else:
                        data.append(round(random.uniform(hour + 0.3, hour + 4), 1))  # After threshold
                elif scenario_type == 'inconsistent':
                    # Very variable pattern
                    if random.random() < 0.5:
                        data.append(round(random.uniform(hour - 4, hour - 0.3), 1))  # Well before
                    else:
                        data.append(round(random.uniform(hour + 0.2, hour + 2), 1))  # After
                else:  # barely_passing
                    # Just meets minimum requirement
                    passing_days = 0
                    target_passing = required_days
                    if day < 6:
                        # For first 6 days, decide if this should pass
                        need_to_pass = (target_passing - passing_days) > (6 - day)
                        if need_to_pass or (passing_days < target_passing and random.random() < 0.6):
                            data.append(round(random.uniform(hour - 2, hour - 0.1), 1))
                            passing_days += 1
                        else:
                            data.append(round(random.uniform(hour + 0.2, hour + 2), 1))
                    else:
                        # Last day - ensure we meet minimum
                        if passing_days < target_passing:
                            data.append(round(random.uniform(hour - 2, hour - 0.1), 1))
                        else:
                            data.append(round(random.uniform(hour + 0.2, hour + 2), 1))
                            
            if '14:00' in str(daily_threshold):
                desc = f"Last caffeine time each day (decimal hours) - {scenario_type} pattern"
            else:
                desc = f"Daily times around {daily_threshold} threshold - {scenario_type} pattern"
            target_info = f"Goal: {comparison}{daily_threshold} on ≥{required_days} days/week"
        else:
            # Numeric threshold - check if this is a weekly frequency pattern
            threshold = float(daily_threshold) if daily_threshold else 1.0
            
            # Special handling for weekly frequency patterns like "X times per week" or "X meals per week"
            if threshold == 1.0 and ('times per week' in self.rec_text.lower() or 'sessions per week' in self.rec_text.lower() or 'meals per week' in self.rec_text.lower()):
                # This is a weekly frequency pattern - generate distributed data
                weekly_target = required_days  # required_days is actually the weekly target
                return self._generate_weekly_frequency_data(weekly_target, unit)
            
            # Handle edge case where required_days > 7 (impossible daily requirement)
            if threshold == 1.0 and required_days > 7:
                # This is a weekly frequency pattern - generate distributed data
                weekly_target = required_days  # required_days is actually the weekly target
                return self._generate_weekly_frequency_data(weekly_target, unit)
            
            scenario_type = random.choice(['exactly_meets', 'exceeds_requirement', 'struggling', 'inconsistent'])
            data = []
            
            if 'exercise' in self.rec_text.lower() or 'workout' in self.rec_text.lower():
                # Exercise frequency with realistic workout patterns
                for day in range(7):
                    if scenario_type == 'exactly_meets':
                        # Just meets minimum requirement with strategic rest days
                        passing_chance = 0.7 if day < 5 else (0.9 if sum(1 for x in data if x >= threshold) < required_days else 0.2)
                        if random.random() < passing_chance:
                            data.append(random.uniform(threshold, threshold * 1.8))  # Workout day
                        else:
                            data.append(0)  # Rest day
                    elif scenario_type == 'exceeds_requirement':
                        # Exceeds requirement - active lifestyle
                        if random.random() < 0.8:
                            data.append(random.uniform(threshold * 1.1, threshold * 2.5))
                        else:
                            data.append(random.uniform(0, threshold * 0.6))  # Light day
                    elif scenario_type == 'struggling':
                        # Struggles to meet requirement
                        if random.random() < 0.45:
                            data.append(random.uniform(threshold * 0.8, threshold * 1.3))
                        else:
                            data.append(random.uniform(0, threshold * 0.7))
                    else:  # inconsistent
                        # Very variable - some great days, some off days
                        if random.random() < 0.3:
                            data.append(random.uniform(threshold * 1.5, threshold * 3.0))  # Great workout
                        elif random.random() < 0.7:
                            data.append(0)  # Complete rest
                        else:
                            data.append(random.uniform(threshold * 0.5, threshold * 1.2))  # Light activity
                desc = f"Daily exercise minutes - {scenario_type} pattern"
                
            elif unit and 'serving' in unit.lower():
                # Serving-based frequency with realistic eating patterns
                for day in range(7):
                    if scenario_type == 'exactly_meets':
                        # Strategic to meet minimum
                        passing_chance = 0.6 if day < 5 else (0.9 if sum(1 for x in data if x >= threshold) < required_days else 0.3)
                        if random.random() < passing_chance:
                            data.append(random.uniform(threshold, threshold * 2.2))
                        else:
                            data.append(random.uniform(0, threshold * 0.8))
                    elif scenario_type == 'exceeds_requirement':
                        # Consistently good nutrition
                        if random.random() < 0.8:
                            data.append(random.uniform(threshold * 1.1, threshold * 2.5))
                        else:
                            data.append(random.uniform(threshold * 0.5, threshold * 0.9))
                    elif scenario_type == 'struggling':
                        # Hard to maintain good nutrition
                        if random.random() < 0.4:
                            data.append(random.uniform(threshold, threshold * 1.5))
                        else:
                            data.append(random.uniform(0, threshold * 0.8))
                    else:  # inconsistent
                        # Feast or famine pattern
                        if random.random() < 0.4:
                            data.append(random.uniform(threshold * 1.3, threshold * 3.0))  # Good days
                        else:
                            data.append(random.uniform(0, threshold * 0.6))  # Poor days
                desc = f"Daily servings - {scenario_type} nutrition pattern"
                
            else:
                # Generic frequency pattern with realistic variance
                for day in range(7):
                    if scenario_type == 'exactly_meets':
                        # Just meets requirement
                        passing_chance = 0.65 if day < 5 else (0.9 if sum(1 for x in data if x >= threshold) < required_days else 0.2)
                        if random.random() < passing_chance:
                            data.append(random.uniform(threshold, threshold * 1.6))
                        else:
                            data.append(random.uniform(threshold * 0.1, threshold * 0.9))
                    elif scenario_type == 'exceeds_requirement':
                        # Often exceeds
                        if random.random() < 0.8:
                            data.append(random.uniform(threshold * 1.1, threshold * 2.2))
                        else:
                            data.append(random.uniform(threshold * 0.3, threshold * 0.9))
                    elif scenario_type == 'struggling':
                        # Hard to meet requirement
                        if random.random() < 0.35:
                            data.append(random.uniform(threshold * 0.9, threshold * 1.4))
                        else:
                            data.append(random.uniform(threshold * 0.1, threshold * 0.8))
                    else:  # inconsistent
                        # Very variable performance
                        if random.random() < 0.35:
                            data.append(random.uniform(threshold * 1.2, threshold * 2.5))
                        else:
                            data.append(random.uniform(threshold * 0.2, threshold * 0.9))
                desc = f"Daily values - {scenario_type} achievement pattern"
            
            target_info = f"Goal: {comparison}{threshold} {unit} on ≥{required_days} days/week"
        
        return data, desc, target_info
    
    def _generate_weekly_frequency_data(self, weekly_target: int, unit: str) -> Tuple[List[float], str, str]:
        """Generate data that distributes weekly target across days realistically."""
        scenario_type = random.choice(['exactly_meets', 'exceeds_target', 'falls_short', 'inconsistent'])
        data = []
        
        if scenario_type == 'exactly_meets':
            # Distribute target realistically - allow 2-3 sessions per day
            remaining_sessions = weekly_target
            data = [0.0] * 7
            
            # Distribute sessions across days, allowing realistic daily counts (1-5 sessions)
            while remaining_sessions > 0:
                day = random.randint(0, 6)
                
                # Decide how many sessions this day - realistic meal-based activity
                max_daily = min(5, remaining_sessions)  # Up to 5 sessions per day (3 meals + 2 snacks)
                
                if max_daily >= 4 and random.random() < 0.2:
                    sessions_this_day = random.randint(3, max_daily)  # Very active day
                elif max_daily >= 3 and random.random() < 0.4:
                    sessions_this_day = random.randint(2, min(3, max_daily))  # Moderately active
                elif max_daily >= 2 and random.random() < 0.6:
                    sessions_this_day = random.randint(1, min(2, max_daily))  # Some activity
                else:
                    sessions_this_day = 1  # Minimal activity
                
                sessions_this_day = min(sessions_this_day, remaining_sessions)
                data[day] += sessions_this_day
                remaining_sessions -= sessions_this_day
            
            desc = f"Weekly target distribution - exactly meets {weekly_target} sessions"
            
        elif scenario_type == 'exceeds_target':
            # Exceed target by 1-3 sessions
            actual_target = weekly_target + random.randint(1, 3)
            remaining_sessions = actual_target
            data = [0.0] * 7
            
            # Distribute sessions allowing multiple per day
            while remaining_sessions > 0:
                day = random.randint(0, 6)
                max_daily = min(5, remaining_sessions)
                
                # Slightly higher chance of multiple sessions since exceeding target
                if max_daily >= 3 and random.random() < 0.5:
                    sessions_this_day = random.randint(2, max_daily)
                else:
                    sessions_this_day = random.randint(1, min(2, max_daily))
                
                sessions_this_day = min(sessions_this_day, remaining_sessions)
                data[day] += sessions_this_day
                remaining_sessions -= sessions_this_day
            
            desc = f"Weekly target distribution - exceeds with {actual_target} sessions"
            
        elif scenario_type == 'falls_short':
            # Fall short by 1-2 sessions
            actual_target = max(1, weekly_target - random.randint(1, 2))
            remaining_sessions = actual_target
            data = [0.0] * 7
            
            # Distribute sessions with tendency toward fewer days (clustering)
            while remaining_sessions > 0:
                day = random.randint(0, 6)
                max_daily = min(4, remaining_sessions)  # Slightly less than exceeds_target
                
                if max_daily >= 2 and random.random() < 0.4:
                    sessions_this_day = random.randint(2, max_daily)
                else:
                    sessions_this_day = 1
                
                sessions_this_day = min(sessions_this_day, remaining_sessions)
                data[day] += sessions_this_day
                remaining_sessions -= sessions_this_day
            
            desc = f"Weekly target distribution - falls short with {actual_target} sessions"
            
        else:  # inconsistent
            # Very variable - some days many sessions, some none
            remaining_sessions = weekly_target
            data = [0.0] * 7
            
            # Randomly distribute sessions with clustering
            while remaining_sessions > 0:
                day = random.randint(0, 6)
                sessions_to_add = min(remaining_sessions, random.randint(1, 3))
                data[day] += sessions_to_add
                remaining_sessions -= sessions_to_add
            desc = f"Weekly target distribution - inconsistent clustering pattern"
        
        target_info = f"Weekly Goal: {weekly_target} {unit} distributed across week"
        return data, desc, target_info
    
    def _generate_elimination_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic elimination demo"""
        threshold = self.schema.get('elimination_threshold', 0)
        unit = self.schema.get('unit', 'units')
        comparison = self.schema.get('elimination_comparison', '==')
        
        if isinstance(threshold, str) and ':' in threshold:
            # Time-based elimination (like caffeine by 2pm) - dynamic scenarios
            if '14:00' in str(threshold):
                # Generate dynamic compliance/violation scenarios
                data = []
                scenario_type = random.choice(['perfect', 'one_violation', 'multiple_violations'])
                if scenario_type == 'perfect':
                    # Perfect compliance - all before 2pm
                    for day in range(7):
                        time_before_2pm = random.uniform(10.0, 13.8)
                        data.append(round(time_before_2pm, 1))
                    desc = "Last caffeine time daily - perfect compliance week"
                elif scenario_type == 'one_violation':
                    # One violation day
                    for day in range(7):
                        if day == random.randint(0, 6):  # Random violation day
                            time_after_2pm = random.uniform(14.5, 17.0)
                            data.append(round(time_after_2pm, 1))
                        else:
                            time_before_2pm = random.uniform(10.0, 13.8)
                            data.append(round(time_before_2pm, 1))
                    desc = "Last caffeine time daily - one violation day"
                else:
                    # Multiple violations
                    for day in range(7):
                        if random.random() < 0.3:  # 30% chance of violation
                            time_after_2pm = random.uniform(14.5, 17.0)
                            data.append(round(time_after_2pm, 1))
                        else:
                            time_before_2pm = random.uniform(10.0, 13.8)
                            data.append(round(time_before_2pm, 1))
                    desc = "Last caffeine time daily - multiple violations"
            else:
                # Other time-based elimination
                base_time = float(threshold.split(':')[0]) if ':' in str(threshold) else 12
                data = []
                for day in range(7):
                    # Add some variation around the threshold time
                    if random.random() < 0.8:  # 80% compliance
                        time_val = base_time + random.uniform(-2, 0.5)
                    else:  # 20% violation
                        time_val = base_time + random.uniform(0.5, 3)
                    data.append(round(time_val, 1))
                desc = f"Dynamic compliance/violation pattern around {threshold}"
            target_info = f"Goal: {comparison}{threshold} EVERY day (zero tolerance)"
        else:
            # Numeric elimination - dynamic scenarios
            threshold_val = float(threshold) if threshold is not None else 0
            
            if threshold_val == 0:
                # Zero tolerance - generate dynamic scenarios
                scenario_type = random.choice(['perfect', 'one_violation', 'weekend_slip'])
                data = []
                
                if scenario_type == 'perfect':
                    data = [0] * 7
                    desc = "Perfect elimination - zero consumption all week"
                elif scenario_type == 'one_violation':
                    violation_day = random.randint(0, 6)
                    for day in range(7):
                        if day == violation_day:
                            data.append(random.uniform(0.5, 2.0))  # Small violation
                        else:
                            data.append(0)
                    desc = "One violation day - otherwise perfect elimination"
                else:  # weekend_slip
                    for day in range(7):
                        if day in [4, 5, 6] and random.random() < 0.4:  # Weekend slips
                            data.append(random.uniform(0.5, 1.5))
                        else:
                            data.append(0)
                    desc = "Weekend elimination challenges"
            else:
                # Non-zero threshold elimination - dynamic around threshold
                data = []
                for day in range(7):
                    if random.random() < 0.85:  # 85% compliance
                        data.append(threshold_val)
                    else:  # 15% violation
                        data.append(threshold_val + random.uniform(0.1, 1.0))
                desc = f"Dynamic compliance around {threshold_val} threshold"
            
            target_info = f"Goal: {comparison}{threshold_val} {unit} EVERY day (zero tolerance)"
        
        return data, desc, target_info
    
    def _generate_zone_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic zone-based demo with dynamic patterns"""
        zones = self.schema.get('zones', [])
        unit = self.schema.get('unit', 'hours')
        
        # Dynamic scenario generation
        scenario_type = random.choice(['mostly_optimal', 'varied_performance', 'struggling', 'inconsistent_sleeper'])
        data = []
        
        if 'sleep' in self.rec_text.lower() or unit == 'hours':
            # Sleep duration zones with realistic sleep patterns
            for day in range(7):
                if scenario_type == 'mostly_optimal':
                    # Usually in optimal 7-9h range, occasional variation
                    if random.random() < 0.7:
                        data.append(round(random.uniform(7.0, 9.0), 1))  # Optimal zone
                    elif random.random() < 0.8:
                        data.append(round(random.uniform(6.0, 7.0), 1))  # Fair zone
                    else:
                        data.append(round(random.uniform(9.0, 10.0), 1))  # Excessive zone
                elif scenario_type == 'varied_performance':
                    # Spreads across multiple zones
                    zone_choice = random.choice(['poor', 'fair', 'optimal', 'excessive'])
                    if zone_choice == 'poor':
                        data.append(round(random.uniform(4.5, 6.0), 1))
                    elif zone_choice == 'fair':
                        data.append(round(random.uniform(6.0, 7.0), 1))
                    elif zone_choice == 'optimal':
                        data.append(round(random.uniform(7.0, 9.0), 1))
                    else:  # excessive
                        data.append(round(random.uniform(9.0, 11.0), 1))
                elif scenario_type == 'struggling':
                    # Often in poor zones, struggling with sleep
                    if random.random() < 0.5:
                        data.append(round(random.uniform(4.0, 6.0), 1))  # Poor sleep
                    elif random.random() < 0.8:
                        data.append(round(random.uniform(6.0, 7.0), 1))  # Fair sleep
                    else:
                        data.append(round(random.uniform(7.0, 8.0), 1))  # Occasional good night
                else:  # inconsistent_sleeper
                    # Very variable - insomnia mixed with oversleeping
                    if random.random() < 0.3:
                        data.append(round(random.uniform(3.5, 5.5), 1))  # Insomnia nights
                    elif random.random() < 0.6:
                        data.append(round(random.uniform(9.5, 12.0), 1))  # Oversleep nights
                    else:
                        data.append(round(random.uniform(6.5, 8.5), 1))  # Normal nights
            desc = f"Daily sleep hours - {scenario_type} sleep pattern"
            target_info = "Zones: <6h(poor), 6-7h(fair), 7-9h(optimal), >9h(excessive)"
            
        elif zones and len(zones) > 0:
            # Use actual zone ranges with realistic distribution
            zone_info = []
            for day in range(7):
                if scenario_type == 'mostly_optimal':
                    # Prefer higher-scoring zones
                    optimal_zones = [z for z in zones if z.get('score', 0) >= 80]
                    if optimal_zones and random.random() < 0.7:
                        zone = random.choice(optimal_zones)
                    else:
                        zone = random.choice(zones)
                elif scenario_type == 'varied_performance':
                    # Random zone selection
                    zone = random.choice(zones)
                elif scenario_type == 'struggling':
                    # Prefer lower-scoring zones
                    poor_zones = [z for z in zones if z.get('score', 0) <= 50]
                    if poor_zones and random.random() < 0.6:
                        zone = random.choice(poor_zones)
                    else:
                        zone = random.choice(zones)
                else:  # inconsistent
                    # Extremes - very high or very low zones
                    extreme_zones = [z for z in zones if z.get('score', 0) <= 30 or z.get('score', 0) >= 90]
                    if extreme_zones and random.random() < 0.7:
                        zone = random.choice(extreme_zones)
                    else:
                        zone = random.choice(zones)
                
                zone_range = zone.get('range', [5, 6])
                min_val = zone_range[0] if len(zone_range) > 0 else 5
                max_val = zone_range[1] if len(zone_range) > 1 else min_val + 1
                data.append(round(random.uniform(min_val, max_val), 1))
                
                if day < 3:  # Collect zone info for display
                    zone_info.append(f"{zone.get('label', f'Zone{day+1}')}: {min_val}-{max_val}")
            
            desc = f"Daily values across zones - {scenario_type} pattern"
            target_info = f"Zones: {', '.join(zone_info)}..."
        else:
            # Fallback for missing zone data
            for day in range(7):
                data.append(round(random.uniform(5.0, 10.0), 1))
            desc = f"Daily values - {scenario_type} pattern (no zone data)"
            target_info = "Zone-based scoring with dynamic values"
        
        return data, desc, target_info
    
    def _generate_allowance_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic allowance demo"""
        allowance = self.schema.get('weekly_allowance', 2)
        max_days = self.schema.get('max_days_per_week')
        unit = self.schema.get('unit', 'units')
        
        if 'cheat' in self.rec_text.lower() or 'treat' in self.rec_text.lower() or unit == 'meals':
            # Cheat meals/treats - dynamic realistic pattern
            data = [0] * 7
            meals_to_distribute = random.randint(allowance - 1, allowance + 2)  # Around allowance
            days_to_use = min(random.randint(1, max_days + 1 if max_days else 4), 7)  # Vary days used
            
            # Randomly assign meals to days
            chosen_days = random.sample(range(7), days_to_use)
            for i, day in enumerate(chosen_days):
                if i == len(chosen_days) - 1:
                    data[day] = max(0, meals_to_distribute)  # Put remaining meals on last day
                else:
                    meals_this_day = random.randint(0, min(2, meals_to_distribute))
                    data[day] = meals_this_day
                    meals_to_distribute -= meals_this_day
            desc = "Daily cheat meals - varying weekend and weekday treats"
            
        elif 'alcohol' in self.rec_text.lower() or 'drink' in self.rec_text.lower():
            # Alcohol allowance - dynamic social drinking pattern
            data = [0] * 7
            
            # Generate drinks around allowance (sometimes over, sometimes under)
            total_drinks = random.choice([
                allowance - 1,     # Under limit
                allowance,         # At limit  
                allowance + 1,     # Over limit
                allowance + 2      # Well over limit
            ])
            total_drinks = max(0, total_drinks)
            
            # Generate days (sometimes violate, sometimes don't)
            if max_days:
                days_to_use = random.choice([
                    max_days - 1,      # Under day limit
                    max_days,          # At day limit
                    max_days + 1,      # Over day limit
                    max_days + 2       # Well over day limit  
                ])
                days_to_use = min(max(1, days_to_use), 7)
            else:
                days_to_use = random.randint(1, 4)
            
            # Distribute drinks across chosen days
            if days_to_use > 0:
                chosen_days = random.sample(range(7), days_to_use)
                drinks_remaining = total_drinks
                for i, day in enumerate(chosen_days):
                    if i == len(chosen_days) - 1:
                        data[day] = max(0, drinks_remaining)  # Put remaining drinks on last day
                    else:
                        drinks_this_day = random.randint(0, min(3, drinks_remaining))
                        data[day] = drinks_this_day
                        drinks_remaining -= drinks_this_day
                        
            desc = "Daily drinks - dynamic social occasions"
            
        else:
            # Generic allowance - dynamic pattern
            data = [0] * 7
            items_to_distribute = random.randint(max(0, allowance - 1), allowance + 2)
            days_to_use = random.randint(1, min(5, 7))
            
            chosen_days = random.sample(range(7), days_to_use)
            items_remaining = items_to_distribute
            for i, day in enumerate(chosen_days):
                if i == len(chosen_days) - 1:
                    data[day] = max(0, items_remaining)
                else:
                    items_this_day = random.randint(0, min(2, items_remaining))
                    data[day] = items_this_day
                    items_remaining -= items_this_day
                    
            desc = f"Dynamic weekly allowance usage pattern"
        
        total_used = sum(data)
        days_used = sum(1 for d in data if d > 0)
        target_info = f"Weekly allowance: {allowance} {unit}"
        if max_days:
            target_info += f", max {max_days} days"
        target_info += f" | Used: {total_used} {unit} on {days_used} days"
        
        return data, desc, target_info
    
    def _generate_hybrid_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic hybrid demo"""
        daily_target = self.schema.get('daily_target', 1.0)
        required_days = self.schema.get('required_qualifying_days', 2)
        unit = self.schema.get('unit', 'units')
        
        # Generate dynamic data where top N days meet target
        data = []
        for day in range(7):
            # Create mix of qualifying (≥target) and non-qualifying days
            if day < required_days + 1:  # Ensure enough qualifying days plus some
                multiplier = random.uniform(1.0, 1.5)  # Above target
            elif day == required_days + 1 and random.random() < 0.3:
                multiplier = 0  # Occasional rest day
            else:
                multiplier = random.uniform(0.4, 0.95)  # Below target
            daily_value = daily_target * multiplier
            data.append(round(daily_value, 1))
        
        # Shuffle to make realistic
        random.shuffle(data)
        
        desc = f"Mixed performance - top {required_days} days count toward weekly score"
        target_info = f"Goal: {daily_target} {unit}/day | Top {required_days} days averaged"
        
        return data, desc, target_info
    
    def _generate_sleep_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic sleep composite demo"""
        # Dynamic sleep hours with realistic variation
        data = []
        for day in range(7):
            # Mix of optimal (7-9h), short (<7h), and long (>9h) sleep
            sleep_type = random.choices(['optimal', 'short', 'long'], weights=[0.6, 0.3, 0.1])[0]
            if sleep_type == 'optimal':
                sleep_hours = random.uniform(7.0, 9.0)
            elif sleep_type == 'short':
                sleep_hours = random.uniform(5.5, 7.0)
            else:  # long
                sleep_hours = random.uniform(9.0, 10.5)
            data.append(round(sleep_hours, 1))
        desc = "Daily sleep hours - dynamic variation across sleep quality ranges"
        target_info = "Composite: duration + sleep/wake time consistency"
        return data, desc, target_info
    
    def _generate_categorical_demo(self) -> Tuple[List[float], str, str]:
        """Generate realistic categorical demo"""
        threshold = self.schema.get('threshold', 3)
        categories = self.schema.get('categories', [])
        unit = self.schema.get('unit', 'servings')
        
        # Dynamic food category servings
        data = []
        for day in range(7):
            # Mix of days meeting/not meeting threshold
            if random.random() < 0.6:  # 60% chance of meeting threshold
                daily_servings = random.uniform(threshold, threshold + 2)
            else:  # 40% chance of falling short
                daily_servings = random.uniform(threshold * 0.3, threshold * 0.9)
            data.append(round(daily_servings, 1))
        desc = f"Daily {unit} from target categories - dynamic variation"
        target_info = f"Goal: ≥{threshold} {unit} from specific categories daily"
        
        return data, desc, target_info
    
    def _generate_composite_demo(self) -> Tuple[List[Dict[str, float]], str, str]:
        """Generate realistic composite demo with component values"""
        components = self.schema.get('components', [])
        
        data = []
        if any('sleep' in str(comp).lower() for comp in components):
            # Sleep composite - generate realistic sleep data
            for day in range(7):
                component_values = {}
                for comp in components:
                    field_name = comp.get('field_name', '')
                    if not field_name:  # Handle old format
                        field_name = comp.get('metric', 'value')
                    target = comp.get('target', 1)
                    
                    if 'duration' in field_name.lower():
                        # Sleep duration: 6-9 hours with some variation
                        value = random.uniform(6.5, 8.5)
                        component_values[field_name] = round(value, 1)
                    elif 'variance' in field_name.lower() or 'consistency' in field_name.lower():
                        # Sleep/wake time variance: 15-90 minutes
                        value = random.uniform(15, 75)
                        component_values[field_name] = round(value, 1)
                    else:
                        # Generic sleep metric
                        value = random.uniform(target * 0.7, target * 1.2)
                        component_values[field_name] = round(value, 1)
                        
                data.append(component_values)
            desc = "Daily sleep metrics - duration and consistency components"
        else:
            # Generic composite - generate component values for all fields
            # Pre-generate weekly values that will be consistent across all days
            weekly_values = {}
            for comp in components:
                field_name = comp.get('field_name')
                if not field_name:
                    field_name = comp.get('metric', 'value')
                
                # If it's a weekly metric, generate once and reuse
                if 'weekly' in field_name.lower() or 'summary' in field_name.lower():
                    target = comp.get('target', comp.get('threshold', 1))
                    value = max(0, int(random.uniform(target * 0.5, target * 1.4)))
                    weekly_values[field_name] = value
            
            for day in range(7):
                component_values = {}
                for comp in components:
                    # Handle both new format (field_name) and old format (metric)
                    field_name = comp.get('field_name')
                    if not field_name:
                        field_name = comp.get('metric', 'value')
                    
                    # Use pre-generated weekly value if available
                    if field_name in weekly_values:
                        component_values[field_name] = weekly_values[field_name]
                        continue
                    
                    target = comp.get('target', comp.get('threshold', 1))
                    unit = comp.get('unit', '')
                    
                    if 'serving' in unit.lower():
                        # Food servings: realistic variation around target
                        value = max(0, random.uniform(target * 0.6, target * 1.3))
                        component_values[field_name] = round(value, 1)
                    elif 'sources' in unit.lower() or 'variety' in field_name.lower() or 'count' in field_name.lower():
                        # Variety/sources/counts: integer values 
                        value = max(0, int(random.uniform(target * 0.5, target * 1.4)))
                        component_values[field_name] = value
                    elif 'meal' in field_name.lower():
                        # Meal counts: integer values around target
                        value = max(0, int(random.uniform(target * 0.7, target * 1.2)))
                        component_values[field_name] = value
                    else:
                        # Generic numeric values
                        value = max(0, random.uniform(target * 0.7, target * 1.2))
                        component_values[field_name] = round(value, 1)
                        
                data.append(component_values)
            desc = "Daily component values - realistic dietary patterns"
        
        target_info = f"Composite of {len(components)} weighted components"
        return data, desc, target_info

class ConfigDemoTester:
    """Creates demos for all configs showing realistic data and outputs"""
    
    def __init__(self):
        self.src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
        if self.src_path not in sys.path:
            sys.path.insert(0, self.src_path)
    
    def create_config_demo(self, config_data: Dict[str, Any], config_name: str) -> ConfigDemo:
        """Create a demo for one config"""
        
        algorithm_type = config_data.get('scoring_method', 'unknown')
        rec_id = config_data.get('metadata', {}).get('recommendation_id', 'UNKNOWN')
        rec_text = config_data.get('metadata', {}).get('recommendation_text', '')
        schema = config_data.get('configuration_json', {}).get('schema', {})
        unit = schema.get('unit', 'units')
        
        # Generate realistic demo data
        generator = RealisticDataGenerator(config_data)
        try:
            sample_data, data_description, target_info = generator.generate_weekly_demo_data()
        except Exception as e:
            return ConfigDemo(
                config_name=config_name,
                rec_id=rec_id,
                algorithm_type=algorithm_type,
                recommendation_text=rec_text,
                sample_data=[0] * 7,
                data_description="Failed to generate data",
                daily_scores=[0] * 7,
                weekly_score=0,
                unit=unit,
                target_info="Error generating target info",
                error_message=str(e)
            )
        
        # Get algorithm output
        try:
            algorithm = self._create_algorithm_instance(algorithm_type, schema)
            daily_scores, weekly_score = self._get_algorithm_output(algorithm, sample_data, algorithm_type)
        except Exception as e:
            daily_scores = [0] * 7
            weekly_score = 0
            error_message = str(e)
        else:
            error_message = None
        
        # Get sleep composite data if available
        sleep_composite_data = getattr(self, '_sleep_composite_data', None) if algorithm_type == 'sleep_composite' else None
        
        return ConfigDemo(
            config_name=config_name,
            rec_id=rec_id,
            algorithm_type=algorithm_type,
            recommendation_text=rec_text,
            sample_data=sample_data,
            data_description=data_description,
            daily_scores=daily_scores,
            weekly_score=weekly_score,
            unit=unit,
            target_info=target_info,
            error_message=error_message,
            sleep_composite_data=sleep_composite_data
        )
    
    def _create_algorithm_instance(self, algorithm_type: str, schema: Dict[str, Any]):
        """Create algorithm instance - same logic as integration test"""
        
        if algorithm_type == 'proportional':
            from algorithms.proportional import ProportionalAlgorithm, ProportionalConfig
            from algorithms.binary_threshold import EvaluationPeriod
            
            # Map evaluation period from schema
            evaluation_period = EvaluationPeriod.DAILY
            schema_period = schema.get('evaluation_period', 'daily')
            if 'weekly' in schema_period.lower():
                evaluation_period = EvaluationPeriod.ROLLING_7_DAY
            
            config = ProportionalConfig(
                target=schema.get('target', 1.0),
                unit=schema.get('unit', 'units'),
                maximum_cap=schema.get('maximum_cap', 100),
                minimum_threshold=schema.get('minimum_threshold', 0),
                evaluation_period=evaluation_period,
                frequency_requirement=schema.get('frequency_requirement', 'daily')
            )
            return ProportionalAlgorithm(config)
            
        elif algorithm_type == 'binary_threshold':
            from algorithms.binary_threshold import BinaryThresholdAlgorithm, BinaryThresholdConfig, ComparisonOperator
            
            operator_map = {
                '>=': ComparisonOperator.GTE, '<=': ComparisonOperator.LTE,
                '>': ComparisonOperator.GT, '<': ComparisonOperator.LT, '==': ComparisonOperator.EQ
            }
            
            config = BinaryThresholdConfig(
                threshold=schema.get('threshold', 1.0),
                success_value=schema.get('success_value', 100),
                failure_value=schema.get('failure_value', 0),
                comparison_operator=operator_map.get(schema.get('comparison_operator', '>='), ComparisonOperator.GTE)
            )
            return BinaryThresholdAlgorithm(config)
            
        elif algorithm_type == 'minimum_frequency':
            from algorithms.minimum_frequency import MinimumFrequencyAlgorithm, MinimumFrequencyConfig
            
            # Convert time string to decimal hours if needed
            threshold = schema.get('daily_threshold', 1.0)
            if isinstance(threshold, str) and ':' in threshold:
                # Convert "14:00" to 14.0
                hours, minutes = threshold.split(':')
                threshold = float(hours) + float(minutes) / 60.0
            
            config = MinimumFrequencyConfig(
                daily_threshold=threshold,
                daily_comparison=schema.get('daily_comparison', '>='),
                required_days=schema.get('required_days', 3)
            )
            return MinimumFrequencyAlgorithm(config)
            
        elif algorithm_type == 'weekly_elimination':
            from algorithms.weekly_elimination import WeeklyEliminationAlgorithm, WeeklyEliminationConfig
            
            # Convert time string to decimal hours if needed
            threshold = schema.get('elimination_threshold', 0)
            if isinstance(threshold, str) and ':' in threshold:
                # Convert "14:00" to 14.0
                hours, minutes = threshold.split(':')
                threshold = float(hours) + float(minutes) / 60.0
                
            config = WeeklyEliminationConfig(
                elimination_threshold=threshold,
                elimination_comparison=schema.get('elimination_comparison', '==')
            )
            return WeeklyEliminationAlgorithm(config)
            
        elif algorithm_type == 'zone_based':
            from algorithms.zone_based import ZoneBasedAlgorithm, ZoneBasedConfig, Zone
            
            zones = schema.get('zones', [])
            if not zones:
                zones = [Zone(0, 5, 20, "Poor"), Zone(5, 7, 60, "Fair"), Zone(7, 9, 100, "Good"), Zone(9, 12, 80, "Excessive")]
            else:
                zone_objects = []
                for zone_data in zones:
                    zone_range = zone_data.get('range', [0, 1])
                    min_val = zone_range[0] if len(zone_range) > 0 else 0
                    max_val = zone_range[1] if len(zone_range) > 1 else zone_range[0]
                    zone_objects.append(Zone(
                        min_value=min_val, max_value=max_val,
                        score=zone_data.get('score', 50), label=zone_data.get('label', 'Zone')
                    ))
                zones = zone_objects
            
            config = ZoneBasedConfig(zones=zones, unit=schema.get('unit', 'units'))
            return ZoneBasedAlgorithm(config)
            
        elif algorithm_type == 'constrained_weekly_allowance':
            from algorithms.constrained_weekly_allowance import ConstrainedWeeklyAllowanceAlgorithm, ConstrainedWeeklyAllowanceConfig
            config = ConstrainedWeeklyAllowanceConfig(
                weekly_allowance=schema.get('weekly_allowance', 2),
                unit=schema.get('unit', 'units'),
                penalty_for_overage=schema.get('penalty_per_excess', 25),
                max_days_per_week=schema.get('max_days_per_week')
            )
            return ConstrainedWeeklyAllowanceAlgorithm(config)
            
        elif algorithm_type == 'proportional_frequency_hybrid':
            from algorithms.proportional_frequency_hybrid import ProportionalFrequencyHybridAlgorithm, ProportionalFrequencyHybridConfig
            config = ProportionalFrequencyHybridConfig(
                daily_target=schema.get('daily_target', 1.0),
                required_qualifying_days=schema.get('required_qualifying_days', 2),
                unit=schema.get('unit', 'units'),
                daily_minimum_threshold=schema.get('daily_minimum_threshold', 0)
            )
            return ProportionalFrequencyHybridAlgorithm(config)
            
        elif algorithm_type == 'sleep_composite':
            from algorithms.sleep_composite import SleepCompositeAlgorithm, SleepCompositeConfig
            
            # Extract components from schema
            components = schema.get('components', {})
            
            # Get weights from components
            duration_weight = components.get('sleep_duration', {}).get('weight', 0.55)
            sleep_weight = components.get('sleep_time_consistency', {}).get('weight', 0.225)
            wake_weight = components.get('wake_time_consistency', {}).get('weight', 0.225)
            
            # Get zones and thresholds from components
            duration_zones = components.get('sleep_duration', {}).get('zones', None)
            variance_thresholds = components.get('sleep_time_consistency', {}).get('variance_thresholds', None)
            
            config = SleepCompositeConfig(
                duration_weight=duration_weight,
                sleep_consistency_weight=sleep_weight,
                wake_consistency_weight=wake_weight,
                duration_zones=duration_zones,
                variance_thresholds=variance_thresholds
            )
            return SleepCompositeAlgorithm(config)
            
        elif algorithm_type == 'composite_weighted':
            from algorithms.composite_weighted import CompositeWeightedAlgorithm, CompositeWeightedConfig, Component
            
            # Extract components from schema
            components_data = schema.get('components', [])
            components = []
            
            if isinstance(components_data, list):
                # Components stored as list - handle different formats
                for comp_data in components_data:
                    # Handle both new format (field_name) and old format (metric)
                    field_name = comp_data.get('field_name')
                    if not field_name:
                        field_name = comp_data.get('metric', 'value')
                    
                    # Handle weight as percentage or decimal
                    weight = comp_data.get('weight', 1.0)
                    if isinstance(weight, (int, float)) and weight > 10:
                        weight = weight / 100.0  # Convert percentage to decimal
                    
                    component = Component(
                        name=comp_data.get('name', field_name),
                        weight=weight,
                        target=comp_data.get('target', comp_data.get('threshold', 100)),
                        unit=comp_data.get('unit', 'units'),
                        scoring_method=comp_data.get('scoring_method', comp_data.get('algorithm', 'proportional')),
                        field_name=field_name,
                        parameters=comp_data.get('parameters', {})
                    )
                    components.append(component)
            elif isinstance(components_data, dict):
                # Components stored as dictionary - convert to Component objects
                for comp_name, comp_data in components_data.items():
                    component = Component(
                        name=comp_name,
                        weight=comp_data.get('weight', 1.0),
                        target=comp_data.get('target', 100),
                        unit=comp_data.get('unit', 'units'),
                        scoring_method=comp_data.get('scoring_method', 'proportional'),
                        field_name=comp_data.get('field_name', comp_name),
                        parameters=comp_data.get('parameters', {})
                    )
                    components.append(component)
            
            if not components:
                # Default component if none found
                components = [Component(
                    name='Default Component',
                    weight=1.0,
                    target=100,
                    unit=schema.get('unit', 'score'),
                    scoring_method='proportional',
                    field_name='value'
                )]
            
            # DEBUG: Print component field names
            # print(f"DEBUG: Components for composite_weighted: {[c.field_name for c in components]}")
            
            config = CompositeWeightedConfig(
                components=components,
                minimum_threshold=schema.get('minimum_threshold', 0),
                maximum_cap=schema.get('maximum_cap', 100)
            )
            return CompositeWeightedAlgorithm(config)
        else:
            raise ValueError(f"Unsupported algorithm type: {algorithm_type}")
    
    def _get_algorithm_output(self, algorithm, sample_data: List[float], algorithm_type: str) -> Tuple[List[float], float]:
        """Get daily and weekly scores from algorithm"""
        
        try:
            if hasattr(algorithm, 'calculate_progressive_scores'):
                # Handle special data formats for certain algorithms
                if algorithm_type == 'sleep_composite':
                    # Convert to sleep composite format with realistic patterns
                    daily_sleep_data = []
                    
                    # Generate realistic sleep patterns dynamically
                    realistic_patterns = []
                    for day in range(7):
                        # Generate realistic sleep duration (mix of optimal, suboptimal, poor)
                        duration_options = [
                            random.uniform(7.0, 9.0),    # Optimal sleep (most common)
                            random.uniform(6.0, 7.0),    # Short sleep (sometimes)  
                            random.uniform(9.0, 10.0),   # Long sleep (occasionally)
                            random.uniform(5.5, 6.0)     # Poor sleep (rarely)
                        ]
                        weights = [0.6, 0.25, 0.1, 0.05]  # Mostly good sleep with some variation
                        duration = random.choices(duration_options, weights=weights)[0]
                        
                        # Generate realistic consistency variance (correlated with sleep quality)
                        if duration >= 7.0 and duration <= 9.0:
                            # Good sleep duration usually has better consistency
                            sleep_var = random.uniform(15, 45)
                            wake_var = random.uniform(20, 40)
                        elif duration < 6.5:
                            # Poor sleep often has poor consistency
                            sleep_var = random.uniform(45, 90)  
                            wake_var = random.uniform(50, 80)
                        else:
                            # Moderate consistency for other durations
                            sleep_var = random.uniform(25, 60)
                            wake_var = random.uniform(30, 55)
                        
                        realistic_patterns.append({
                            'sleep_duration': round(duration, 1),
                            'sleep_time_consistency': round(sleep_var, 0),
                            'wake_time_consistency': round(wake_var, 0)
                        })
                    
                    for i, _ in enumerate(sample_data):
                        if i < len(realistic_patterns):
                            daily_sleep_data.append(realistic_patterns[i])
                        else:
                            # Fallback for extra days
                            daily_sleep_data.append({
                                'sleep_duration': sample_data[i] if i < len(sample_data) else 7.5,
                                'sleep_time_consistency': 30,
                                'wake_time_consistency': 30
                            })
                    
                    daily_scores = algorithm.calculate_progressive_scores(daily_sleep_data)
                    
                    # Store the full sleep data for detailed output display
                    self._sleep_composite_data = daily_sleep_data
                
                elif algorithm_type == 'categorical_filter_threshold':
                    # Convert to categorical format
                    daily_data = []
                    for value in sample_data:
                        daily_data.append({'category': 'default', 'value': value})
                    daily_scores = algorithm.calculate_progressive_scores(daily_data)
                
                elif algorithm_type == 'composite_weighted':
                    # Composite weighted sample_data is already in correct format (list of component dicts)
                    daily_scores = algorithm.calculate_progressive_scores(sample_data)
                
                else:
                    # Regular format - get progressive scores for weekly calculation
                    progressive_scores = algorithm.calculate_progressive_scores(sample_data)
                    daily_scores = progressive_scores
                    
                    # For frequency/elimination algorithms, also calculate individual daily pass/fail for display
                    if algorithm_type in ['minimum_frequency', 'weekly_elimination']:
                        individual_daily_scores = []
                        for value in sample_data:
                            individual_score = self._calculate_individual_day_score(algorithm, value, algorithm_type)
                            individual_daily_scores.append(individual_score)
                        # Use individual scores for display, progressive for weekly calculation
                        display_daily_scores = individual_daily_scores
                        daily_scores = display_daily_scores  # Update for display
                
                # Calculate weekly score based on algorithm type
                if algorithm_type in ['minimum_frequency', 'weekly_elimination', 'proportional_frequency_hybrid']:
                    # Use final progressive score for weekly result
                    if algorithm_type in ['minimum_frequency', 'weekly_elimination'] and 'progressive_scores' in locals():
                        weekly_score = progressive_scores[-1] if progressive_scores else 0
                    else:
                        weekly_score = daily_scores[-1] if daily_scores else 0  # Cumulative algorithms
                else:
                    weekly_score = sum(daily_scores) / len(daily_scores) if daily_scores else 0  # Average algorithms
                
            elif hasattr(algorithm, 'calculate_score'):
                # Single score method
                if algorithm_type == 'constrained_weekly_allowance':
                    result = algorithm.calculate_score(daily_values=sample_data)
                    weekly_score = result['score'] if isinstance(result, dict) else result
                    
                    # Generate progressive daily scores showing constraint violations
                    daily_scores = []
                    cumulative_drinks = 0
                    cumulative_days = 0
                    weekly_allowance = result.get('available_allowance', 3.0)
                    max_days = result.get('max_days_allowed', 2)
                    
                    for day_value in sample_data:
                        cumulative_drinks += day_value
                        if day_value > 0:
                            cumulative_days += 1
                        
                        # Check constraints progressively  
                        if cumulative_days > max_days or cumulative_drinks > weekly_allowance:
                            daily_score = 0.0  # Constraint violated
                        else:
                            daily_score = 100.0  # Still within constraints
                            
                        daily_scores.append(daily_score)
                elif algorithm_type == 'composite_weighted':
                    # Composite weighted expects component dictionaries
                    daily_scores = []
                    for component_values in sample_data:
                        score = algorithm.calculate_score(component_values)
                        daily_scores.append(score)
                    weekly_score = sum(daily_scores) / len(daily_scores) if daily_scores else 0
                else:
                    weekly_score = algorithm.calculate_score(sample_data[0])  # Single value
                    daily_scores = [algorithm.calculate_score(val) for val in sample_data]
            else:
                daily_scores = [50] * 7
                weekly_score = 50
                
        except Exception as e:
            raise Exception(f"Algorithm execution failed: {str(e)}")
        
        return daily_scores, weekly_score
    
    def _calculate_individual_day_score(self, algorithm, value, algorithm_type):
        """Calculate individual day pass/fail score for frequency/elimination algorithms."""
        if algorithm_type == 'minimum_frequency':
            # Check if this day meets the threshold
            if algorithm.config.daily_comparison == "<=":
                day_pass = value <= algorithm.config.daily_threshold
            elif algorithm.config.daily_comparison == ">=":
                day_pass = value >= algorithm.config.daily_threshold
            else:  # "=="
                day_pass = value == algorithm.config.daily_threshold
            return 100.0 if day_pass else 0.0
        
        elif algorithm_type == 'weekly_elimination':
            # Check if this day meets the elimination threshold
            if algorithm.config.elimination_comparison == "<=":
                day_pass = value <= algorithm.config.elimination_threshold
            elif algorithm.config.elimination_comparison == ">=":
                day_pass = value >= algorithm.config.elimination_threshold
            else:  # "=="
                day_pass = value == algorithm.config.elimination_threshold
            return 100.0 if day_pass else 0.0
        
        return 50.0  # Fallback

def run_config_demos():
    """Generate demos for all configs showing realistic data and outputs"""
    
    print("🎯 Generating Config Demos...")
    print("Shows realistic weekly data and algorithm outputs for each REC config\n")
    
    # Discover configs  
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'generated_configs')
    pattern = os.path.join(config_dir, 'REC*.json')
    config_files = glob.glob(pattern)
    config_files.sort()
    
    print(f"📊 Found {len(config_files)} configuration files")
    
    # Generate demos
    tester = ConfigDemoTester()
    demos = []
    
    for i, config_file in enumerate(config_files, 1):
        config_name = os.path.basename(config_file)
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            demo = tester.create_config_demo(config_data, config_name)
            demos.append(demo)
            
            if i % 20 == 0:
                print(f"  Generated {i}/{len(config_files)} demos...")
                
        except Exception as e:
            print(f"  ⚠️ Failed to process {config_name}: {e}")
    
    # Generate report
    _generate_demo_report(demos)
    return demos

def _generate_demo_report(demos: List[ConfigDemo]):
    """Generate demo report showing sample data and outputs"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    output_lines = [
        "=" * 120,
        "WELLPATH CONFIG DEMO REPORT",
        f"Generated: {timestamp}",
        f"Shows realistic weekly sample data and algorithm outputs for each REC config",
        f"Total Configs: {len(demos)}",
        "=" * 120,
        ""
    ]
    
    # Count by algorithm type
    algo_counts = {}
    for demo in demos:
        algo_type = demo.algorithm_type
        algo_counts[algo_type] = algo_counts.get(algo_type, 0) + 1
    
    output_lines.extend([
        "ALGORITHM DISTRIBUTION:",
        ""
    ])
    
    for algo_type, count in sorted(algo_counts.items()):
        output_lines.append(f"  {algo_type:25} | {count:3d} configs")
    
    output_lines.extend([
        "",
        "=" * 120,
        "CONFIG DEMOS WITH SAMPLE DATA AND OUTPUTS",
        "=" * 120,
        ""
    ])
    
    # Generate detailed demos
    for i, demo in enumerate(demos, 1):
        
        status = "✅ SUCCESS" if demo.error_message is None else "❌ ERROR"
        
        output_lines.extend([
            f"📊 DEMO {i:3d}: {demo.rec_id} | {status}",
            f"Config: {demo.config_name}",
            f"Algorithm: {demo.algorithm_type}",
            f"Recommendation: {demo.recommendation_text}",
            "-" * 80,
            "",
            f"TARGET INFO: {demo.target_info}",
            f"SCENARIO: {demo.data_description}",
            ""
        ])
        
        if demo.error_message:
            output_lines.extend([
                f"❌ ERROR: {demo.error_message}",
                ""
            ])
        else:
            # Show weekly data table
            if demo.algorithm_type == 'sleep_composite':
                # Special format for sleep composite showing all three components
                output_lines.extend([
                    "WEEKLY SAMPLE DATA & ALGORITHM OUTPUTS:",
                    f"{'Day':<4} {'Duration':<9} {'Sleep Var':<10} {'Wake Var':<9} {'Score':<8}",
                    "-" * 45
                ])
                
                # Use stored sleep composite data if available
                if demo.sleep_composite_data:
                    for day, (sleep_data, score) in enumerate(zip(demo.sleep_composite_data, demo.daily_scores), 1):
                        duration = sleep_data['sleep_duration']
                        sleep_var = sleep_data['sleep_time_consistency']
                        wake_var = sleep_data['wake_time_consistency']
                        output_lines.append(f"{day:<4} {duration:<9.1f} {sleep_var:<10.0f} {wake_var:<9.0f} {score:<8.1f}%")
                else:
                    # Fallback if data not stored
                    for day, (data, score) in enumerate(zip(demo.sample_data, demo.daily_scores), 1):
                        output_lines.append(f"{day:<4} {data:<9.1f} {'--':<10} {'--':<9} {score:<8.1f}%")
                
                output_lines.extend([
                    "-" * 45,
                    f"WEEKLY SCORE: {demo.weekly_score:.1f}%",
                    "Components: Duration(55%) + Sleep Consistency(22.5%) + Wake Consistency(22.5%)",
                    ""
                ])
            else:
                # Regular format for other algorithm types
                output_lines.extend([
                    "WEEKLY SAMPLE DATA & ALGORITHM OUTPUTS:",
                    f"{'Day':<4} {'Sample Data':<12} {'Daily Score':<12} {'Unit':<10}",
                    "-" * 45
                ])
                
                for day, (data, score) in enumerate(zip(demo.sample_data, demo.daily_scores), 1):
                    if isinstance(data, dict):
                        # Composite weighted data - show component summary
                        data_str = f"{len(data)} components"
                        output_lines.append(f"{day:<4} {data_str:<12} {score:<12.1f} {demo.unit}")
                    else:
                        output_lines.append(f"{day:<4} {data:<12.2f} {score:<12.1f} {demo.unit}")
                
                output_lines.extend([
                    "-" * 45,
                    f"WEEKLY SCORE: {demo.weekly_score:.1f}%",
                    ""
                ])
        
        output_lines.extend([
            f"Reference: /src/generated_configs/{demo.config_name}",
            f"Algorithm: /src/algorithms/{demo.algorithm_type}.py",
            "",
            "=" * 80,
            ""
        ])
    
    # Summary
    successful_demos = len([d for d in demos if d.error_message is None])
    failed_demos = len(demos) - successful_demos
    
    output_lines.extend([
        "DEMO SUMMARY:",
        "=" * 40,
        f"✅ Successful demos: {successful_demos}/{len(demos)} ({successful_demos/len(demos)*100:.1f}%)",
        f"❌ Failed demos: {failed_demos}/{len(demos)} ({failed_demos/len(demos)*100:.1f}%)",
        f"📊 Algorithm types: {len(algo_counts)}",
        "",
        "This report shows what each config actually does with realistic weekly data.",
        "Use this to understand algorithm behavior and validate recommendation logic.",
        "=" * 120
    ])
    
    # Write output file
    output_file = os.path.join(os.path.dirname(__file__), "config_demo_output.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\n📄 Demo report written to: {output_file}")
    print(f"🎯 Results: {successful_demos}/{len(demos)} demos successful ({successful_demos/len(demos)*100:.1f}%)")
    
    if failed_demos > 0:
        print(f"⚠️ {failed_demos} demos failed - check report for details")

if __name__ == "__main__":
    demos = run_config_demos()
    print(f"\n📊 Generated {len(demos)} config demos")