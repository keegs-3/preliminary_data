import os
import pandas as pd
import numpy as np

def create_comprehensive_patient_file():
    """
    Complete combined scoring that creates a comprehensive patient file with:
    - Each marker's raw value, score, weight, and normalized weighted contribution per pillar
    - All questionnaire responses with their scores and weights per pillar
    - INTEGRATED complex survey calculations (protein, calorie, exercise, etc.) with proper normalization
    - Education scores per pillar
    - Combined pillar scores with proper normalization
    - Relative improvement potential calculations (improvement / current_score * 100)
    - ALL original exports preserved
    """
    
    # Define pillar weights (markers + survey + education = 1.0)
    pillar_weights = {
        "Healthful Nutrition": {"markers": 0.72, "survey": 0.18, "education": 0.10},
        "Movement + Exercise": {"markers": 0.54, "survey": 0.36, "education": 0.10},
        "Restorative Sleep": {"markers": 0.63, "survey": 0.27, "education": 0.10},
        "Cognitive Health": {"markers": 0.36, "survey": 0.54, "education": 0.10},
        "Stress Management": {"markers": 0.27, "survey": 0.63, "education": 0.10},
        "Connection + Purpose": {"markers": 0.18, "survey": 0.72, "education": 0.10},
        "Core Care": {"markers": 0.495, "survey": 0.405, "education": 0.10}
    }
    
    # Use relative paths from script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input files with relative paths
    marker_detailed_file = os.path.join(base_dir, "WellPath_Score_Markers", "scored_markers_with_max.csv")
    survey_detailed_file = os.path.join(base_dir, "WellPath_Score_Survey", "per_question_scores_full_weighted.csv")
    raw_lab_data = os.path.join(base_dir, "data", "dummy_lab_results_full.csv")
    raw_survey_data = os.path.join(base_dir, "data", "synthetic_patient_survey.csv")
    
    # Authoritative max scores from runners (source of truth)
    survey_pillar_summary = os.path.join(base_dir, "WellPath_Score_Survey", "synthetic_patient_pillar_scores_survey_with_max_pct.csv")
    marker_pillar_summary = os.path.join(base_dir, "WellPath_Score_Markers", "marker_pillar_summary.csv")
    
    # Output directory with relative path
    combined_output_dir = os.path.join(base_dir, "WellPath_Score_Combined")
    os.makedirs(combined_output_dir, exist_ok=True)
    
    # Load all data
    try:
        print("Loading all data files...")
        marker_detailed_df = pd.read_csv(marker_detailed_file)
        survey_detailed_df = pd.read_csv(survey_detailed_file)
        raw_lab_df = pd.read_csv(raw_lab_data)
        raw_survey_df = pd.read_csv(raw_survey_data)
        
        # Load authoritative max scores (source of truth)
        survey_pillar_df = pd.read_csv(survey_pillar_summary)
        marker_pillar_df = pd.read_csv(marker_pillar_summary)
        
        print(f"✓ Marker detailed data: {len(marker_detailed_df)} rows")
        print(f"✓ Survey detailed data: {len(survey_detailed_df)} rows")
        print(f"✓ Survey pillar max scores: {len(survey_pillar_df)} rows")
        print(f"✓ Marker pillar max scores: {len(marker_pillar_df)} rows") 
        print(f"✓ Raw lab data: {len(raw_lab_df)} rows")
        print(f"✓ Raw survey data: {len(raw_survey_df)} rows")
        
    except FileNotFoundError as e:
        print(f"❌ Error loading files: {e}")
        print(f"   Make sure all required files exist in the expected folders")
        return None
    except Exception as e:
        print(f"❌ Unexpected error loading files: {e}")
        return None
    
    # Find common patients across all datasets
    marker_patients = set(marker_detailed_df['patient_id'])
    survey_patients = set(survey_detailed_df['patient_id']) 
    lab_patients = set(raw_lab_df['patient_id'])
    survey_raw_patients = set(raw_survey_df['patient_id'])
    
    common_patients = marker_patients & survey_patients & lab_patients & survey_raw_patients
    print(f"✓ Common patients across all datasets: {len(common_patients)}")
    
    if len(common_patients) == 0:
        print("❌ ERROR: No common patients found across all datasets!")
        return None
    
    # Get all unique markers and pillars from the detailed marker data
    marker_columns = [col for col in marker_detailed_df.columns if col.endswith('_weighted')]
    unique_markers = set()
    unique_pillars = set()
    
    for col in marker_columns:
        parts = col.replace('_weighted', '').rsplit('_', 1)
        if len(parts) == 2:
            marker, pillar = parts
            unique_markers.add(marker)
            unique_pillars.add(pillar)
    
    print(f"✓ Found {len(unique_markers)} unique markers across {len(unique_pillars)} pillars")
    
    # Create comprehensive results
    comprehensive_results = []
    pillar_names = list(pillar_weights.keys())
    
    for patient_id in common_patients:
        print(f"Processing patient {patient_id}...")
        
        # Get data for this patient from each source
        marker_rows = marker_detailed_df[marker_detailed_df['patient_id'] == patient_id]
        survey_rows = survey_detailed_df[survey_detailed_df['patient_id'] == patient_id]
        lab_row = raw_lab_df[raw_lab_df['patient_id'] == patient_id].iloc[0]
        survey_raw_row = raw_survey_df[raw_survey_df['patient_id'] == patient_id].iloc[0]
        
        # Start building comprehensive patient record
        patient_record = {
            'patient_id': patient_id,
            'age': lab_row.get('age'),
            'sex': lab_row.get('sex'),
            'weight_lb': lab_row.get('weight_lb'),
            'height_cm': lab_row.get('height_cm'),
        }
        
        # Add all raw lab marker values
        marker_raw_columns = [col for col in raw_lab_df.columns if col not in ['patient_id', 'age', 'sex', 'weight_lb', 'height_cm']]
        for col in marker_raw_columns:
            patient_record[f"raw_marker_{col}"] = lab_row.get(col)
        
        # Add ALL questionnaire responses (for UI display)
        all_survey_columns = [col for col in raw_survey_df.columns if col != 'patient_id']
        for qid in all_survey_columns:
            if qid in survey_raw_row.index:
                patient_record[f"survey_q_{qid}_response"] = survey_raw_row.get(qid)
                
                # Get the scoring details for this question if it exists in detailed survey data
                if len(survey_rows) > 0:
                    survey_row = survey_rows.iloc[0]
                    
                    # Look for any scoring columns for this question across all pillars
                    question_weighted_cols = [col for col in survey_row.index if col.startswith(f"{qid}_") and col.endswith('_weighted')]
                    
                    if question_weighted_cols:
                        # Sum across all pillars for this question to get total question score
                        total_raw_score = 0
                        total_weighted_score = 0
                        total_max_score = 0
                        
                        for weighted_col in question_weighted_cols:
                            base_name = weighted_col.replace('_weighted', '')
                            raw_col = f"{base_name}_raw"
                            max_col = f"{base_name}_max"
                            
                            total_raw_score += survey_row.get(raw_col, 0)
                            total_weighted_score += survey_row.get(weighted_col, 0)
                            total_max_score += survey_row.get(max_col, 0)
                        
                        # Store question-level totals (for UI display)
                        patient_record[f"survey_q_{qid}_raw_score"] = total_raw_score
                        patient_record[f"survey_q_{qid}_weighted_score"] = total_weighted_score
                        patient_record[f"survey_q_{qid}_max_score"] = total_max_score
                        patient_record[f"survey_q_{qid}_improvement_potential"] = total_max_score - total_weighted_score
                    else:
                        # No scoring data available for this question
                        patient_record[f"survey_q_{qid}_raw_score"] = 0
                        patient_record[f"survey_q_{qid}_weighted_score"] = 0
                        patient_record[f"survey_q_{qid}_max_score"] = 0
                        patient_record[f"survey_q_{qid}_normalized_score"] = 0
                        patient_record[f"survey_q_{qid}_improvement_potential"] = 0

        # Process individual markers with their scores and weights per pillar
        if len(marker_rows) > 0:
            marker_row = marker_rows.iloc[0]
            
            # Extract all marker scoring details
            for marker in unique_markers:
                # Store shared value/raw score once
                shared_value_key = f"marker_{marker}_value"
                shared_raw_key = f"marker_{marker}_raw_score"
                shared_set = (shared_value_key in patient_record)

                for pillar in unique_pillars:
                    # Map pillar token to full name
                    full_pillar_name = None
                    for full_name in pillar_names:
                        if pillar in full_name or full_name.replace(" ", "").replace("+", "") == pillar.replace(" ", "").replace("+", ""):
                            full_pillar_name = full_name
                            break
                    if not full_pillar_name:
                        continue

                    raw_col = f"{marker}_{pillar}_raw"
                    weighted_col = f"{marker}_{pillar}_weighted"
                    max_col = f"{marker}_{pillar}_max"

                    if weighted_col in marker_row.index:
                        raw_score = float(marker_row.get(raw_col, 0) or 0)
                        weighted_score = float(marker_row.get(weighted_col, 0) or 0)
                        max_weighted = float(marker_row.get(max_col, 0) or 0)

                        # Set shared value once
                        if not shared_set:
                            patient_record[shared_value_key] = lab_row.get(marker, np.nan)
                            patient_record[shared_raw_key] = raw_score
                            shared_set = True

                        # Store marker pillar contributions
                        patient_record[f"marker_{marker}_{full_pillar_name}_weight"] = (
                            (weighted_score / raw_score) if raw_score else 0
                        )
                        patient_record[f"marker_{marker}_{full_pillar_name}_weighted_score"] = weighted_score
                        patient_record[f"marker_{marker}_{full_pillar_name}_max_weighted"] = max_weighted
                        patient_record[f"marker_{marker}_{full_pillar_name}_improvement_potential"] = max_weighted - weighted_score

        # Process survey data using CLEAN survey_v2 output (don't recreate the logic!)
        if len(survey_rows) > 0:
            survey_row = survey_rows.iloc[0]
            
            # Extract all survey question scoring details from survey_v2 clean output
            survey_weighted_cols = [col for col in survey_row.index if col.endswith('_weighted')]
            
            for weighted_col in survey_weighted_cols:
                if pd.notna(survey_row[weighted_col]) and survey_row[weighted_col] != 0:
                    base_name = weighted_col.replace('_weighted', '')
                    raw_col = f"{base_name}_raw"
                    max_col = f"{base_name}_max"
                    
                    parts = base_name.rsplit('_', 1)
                    if len(parts) == 2:
                        question_id, pillar = parts
                        
                        # Map to full pillar name
                        full_pillar_name = None
                        for full_name in pillar_names:
                            if pillar in full_name or full_name.replace(" ", "").replace("+", "") == pillar.replace(" ", "").replace("+", ""):
                                full_pillar_name = full_name
                                break
                        
                        if full_pillar_name:
                            raw_score = survey_row.get(raw_col, 0)
                            weighted_score = survey_row.get(weighted_col, 0)
                            max_score = survey_row.get(max_col, 0)
                            
                            # Calculate the weight (from survey_v2 logic)
                            weight = weighted_score / raw_score if raw_score != 0 else 0
                            
                            # Store survey question details using CORRECT response mapping
                            # Get response from raw survey data using correct question ID
                            actual_response = survey_raw_row.get(question_id, "")
                            
                            patient_record[f"survey_{question_id}_{full_pillar_name}_response"] = actual_response
                            patient_record[f"survey_{question_id}_{full_pillar_name}_score"] = raw_score
                            patient_record[f"survey_{question_id}_{full_pillar_name}_weight"] = weight
                            patient_record[f"survey_{question_id}_{full_pillar_name}_weighted_score"] = weighted_score
                            patient_record[f"survey_{question_id}_{full_pillar_name}_max_weighted"] = max_score
                            patient_record[f"survey_{question_id}_{full_pillar_name}_improvement_potential"] = max_score - weighted_score
        
        # PROCESS COMPLEX SURVEY CALCULATIONS - INTEGRATED INTO PIPELINE
        process_complex_survey_calculations(patient_record, survey_raw_row, pillar_names, pillar_weights)
        
        # === Calculate pillar totals, normalization, and per-item normalized impact ===
        # Get patient sex for gender-specific max calculations
        sex = patient_record.get('sex', 'M')
        
        for pillar in pillar_names:
            weights = pillar_weights[pillar]

            # Pillar totals (markers / survey)
            marker_total_weighted = sum(
                float(val or 0.0) for key, val in patient_record.items()
                if key.startswith("marker_") and key.endswith(f"_{pillar}_weighted_score")
            )
            # Use gender-specific max values for markers (progesterone affects females only)
            base_max = marker_pillar_df[f"{pillar}_Max"].iloc[0]
            is_female = str(sex).lower().startswith('f')
            if pillar == "Healthful Nutrition" and is_female:
                marker_total_max = base_max + 2  # Progesterone adds 2 points for females
            elif pillar == "Stress Management" and is_female:
                marker_total_max = base_max + 3  # Progesterone adds 3 points for females
            else:
                marker_total_max = base_max

            survey_total_weighted = sum(
                float(val or 0.0) for key, val in patient_record.items()
                if key.startswith("survey_") and key.endswith(f"_{pillar}_weighted_score")
            )
            # Use authoritative max values instead of recalculating  
            survey_total_max = survey_pillar_df[f"{pillar}_Max"].iloc[0]

            # Include substance max values for Core Care
            if pillar == "Core Care":
                substance_weighted = sum(
                    float(val or 0.0) for key, val in patient_record.items()
                    if key.endswith("_CoreCare_weighted") and not key.startswith("survey_")
                )
                survey_total_weighted += substance_weighted
                
                substance_max = sum(
                    float(val or 0.0) for key, val in patient_record.items()
                    if key.endswith("_CoreCare_max") and not key.startswith("survey_")
                )
                survey_total_max += substance_max

            # Education
            education_score = calculate_education_score(patient_id, pillar)
            education_max = 100.0

            # Normalize each component to 0-1
            marker_normalized = (marker_total_weighted / marker_total_max) if marker_total_max > 0 else 0.0
            survey_normalized = (survey_total_weighted / survey_total_max) if survey_total_max > 0 else 0.0
            education_normalized = (education_score / education_max) if education_max > 0 else 0.0

            # Apply pillar allocation weights
            marker_final_weighted = marker_normalized * weights["markers"]
            survey_final_weighted = survey_normalized * weights["survey"]
            education_final_weighted = education_normalized * weights["education"]

            combined_score = marker_final_weighted + survey_final_weighted + education_final_weighted
            combined_pct = combined_score * 100.0
            improvement_potential = 1.0 - combined_score
            
            # Calculate RELATIVE improvement potential
            improvement_potential_pct = (improvement_potential / combined_score * 100.0) if combined_score > 0 else 0.0
            
            # Calculate marker-specific improvement potential relative to pillar score
            marker_improvement_potential = (weights["markers"] * (1.0 - marker_normalized)) if marker_normalized < 1.0 else 0.0
            marker_improvement_potential_pct = (marker_improvement_potential / combined_score * 100.0) if combined_score > 0 else 0.0

            # Store pillar summary
            patient_record.update({
                f"{pillar}_Marker_Total_Weighted": marker_total_weighted,
                f"{pillar}_Marker_Total_Max": marker_total_max,
                f"{pillar}_Marker_Normalized": marker_normalized,
                f"{pillar}_Survey_Total_Weighted": survey_total_weighted,
                f"{pillar}_Survey_Total_Max": survey_total_max,
                f"{pillar}_Survey_Normalized": survey_normalized,
                f"{pillar}_Education_Score": education_score,
                f"{pillar}_Education_Max": education_max,
                f"{pillar}_Education_Normalized": education_normalized,

                f"{pillar}_Marker_Final_Weighted": marker_final_weighted,
                f"{pillar}_Survey_Final_Weighted": survey_final_weighted,
                f"{pillar}_Education_Final_Weighted": education_final_weighted,

                f"{pillar}_Combined_Score": combined_score,
                f"{pillar}_Combined_Pct": combined_pct,
                f"{pillar}_Max_Possible_Score": 1.0,
                f"{pillar}_Improvement_Potential": improvement_potential,
                f"{pillar}_Improvement_Potential_Pct": improvement_potential_pct,
                
                f"{pillar}_Marker_Improvement_Potential": marker_improvement_potential,
                f"{pillar}_Marker_Improvement_Potential_Pct": marker_improvement_potential_pct,

                f"{pillar}_Allocation_Markers": weights["markers"],
                f"{pillar}_Allocation_Survey": weights["survey"],
                f"{pillar}_Allocation_Education": weights["education"],
            })

            # Per-marker normalized share-of-pillar
            if marker_total_max > 0:
                suffix = f"_{pillar}_max_weighted"
                marker_keys = [
                    key for key in patient_record.keys()
                    if key.startswith("marker_") and key.endswith(suffix)
                ]

                for key in marker_keys:
                    marker_name = key[len("marker_"):-len(suffix)]
                    max_weight = float(patient_record.get(key, 0.0) or 0.0)
                    if max_weight <= 0:
                        continue

                    norm_pct = weights["markers"] * (max_weight / marker_total_max)
                    max_points = norm_pct * 100.0

                    raw_key = f"marker_{marker_name}_raw_score"
                    raw_val = float(patient_record.get(raw_key, 0.0) or 0.0)
                    raw_val = max(0.0, min(1.0, raw_val))  # clamp 0-1

                    current_points = raw_val * max_points
                    improve_points = (1.0 - raw_val) * max_points

                    patient_record[f"marker_{marker_name}_{pillar}_norm_pct"] = norm_pct
                    patient_record[f"marker_{marker_name}_{pillar}_max_points"] = max_points
                    patient_record[f"marker_{marker_name}_{pillar}_current_points"] = current_points
                    patient_record[f"marker_{marker_name}_{pillar}_improve_points"] = improve_points

            # Per-survey-question normalized share-of-pillar
            if survey_total_max > 0:
                suffix = f"_{pillar}_max_weighted"
                survey_keys = [
                    key for key in patient_record.keys()
                    if key.startswith("survey_") and key.endswith(suffix)
                ]

                for key in survey_keys:
                    base_key = key[len("survey_"):-len("_max_weighted")]
                    pillar_clean = pillar.replace(" ", "_").replace("+", "").replace("__", "_")
                    
                    if base_key.endswith(f"_{pillar_clean}") or base_key.endswith(f"_{pillar}"):
                        question_id = base_key.replace(f"_{pillar_clean}", "").replace(f"_{pillar}", "")
                    else:
                        continue
                        
                    max_weight = float(patient_record.get(key, 0.0) or 0.0)
                    if max_weight <= 0:
                        continue

                    norm_pct = weights["survey"] * (max_weight / survey_total_max)
                    max_points = norm_pct * 100.0

                    score_key = f"survey_{question_id}_{pillar}_score"
                    raw_val = float(patient_record.get(score_key, 0.0) or 0.0)
                    raw_val = max(0.0, min(1.0, raw_val))  # clamp 0-1

                    current_points = raw_val * max_points
                    improve_points = (1.0 - raw_val) * max_points

                    patient_record[f"survey_{question_id}_{pillar}_norm_pct"] = norm_pct
                    patient_record[f"survey_{question_id}_{pillar}_max_points"] = max_points
                    patient_record[f"survey_{question_id}_{pillar}_current_points"] = current_points
                    patient_record[f"survey_{question_id}_{pillar}_improve_points"] = improve_points

        # Overall wellness score
        pillar_combined_scores = [patient_record[f"{pillar}_Combined_Score"] for pillar in pillar_names]
        overall_wellness = float(np.mean(pillar_combined_scores)) if pillar_combined_scores else 0.0
        overall_wellness_pct = overall_wellness * 100.0
        overall_improvement_potential = 1.0 - overall_wellness
        overall_improvement_potential_pct = (overall_improvement_potential / overall_wellness * 100.0) if overall_wellness > 0 else 0.0

        patient_record.update({
            "Overall_Wellness_Score": overall_wellness,
            "Overall_Wellness_Pct": overall_wellness_pct,
            "Overall_Max_Possible_Score": 1.0,
            "Overall_Improvement_Potential": overall_improvement_potential,
            "Overall_Improvement_Potential_Pct": overall_improvement_potential_pct,
        })

        comprehensive_results.append(patient_record)
    
    # Create comprehensive DataFrame
    comprehensive_df = pd.DataFrame(comprehensive_results)
    
    # Save comprehensive file
    comprehensive_file = os.path.join(combined_output_dir, "comprehensive_patient_scores_detailed.csv")
    comprehensive_df.to_csv(comprehensive_file, index=False)
    print(f"✓ Comprehensive patient file saved to: {comprehensive_file}")
    
    # Create ALL summary reports
    create_detailed_summary_report(comprehensive_df, combined_output_dir)
    create_marker_contribution_analysis(comprehensive_df, combined_output_dir)
    create_all_survey_summary(comprehensive_df, combined_output_dir)
    create_patient_comparison_analysis(comprehensive_df, combined_output_dir)
    create_pillar_breakdown_analysis(comprehensive_df, combined_output_dir)
    markers_df = create_markers_for_impact_scoring(comprehensive_df, combined_output_dir)
    
    return comprehensive_df, markers_df

def process_complex_survey_calculations(patient_record, survey_raw_row, pillar_names, pillar_weights):
    """Process ALL complex survey calculations using the exact logic from your source survey runner."""
    
    # Get patient demographics with safe defaults
    age = patient_record.get('age', 40)
    sex = patient_record.get('sex', 'F') 
    weight_lb = patient_record.get('weight_lb', 150)
    
    # Handle missing/invalid demographic data
    if pd.isna(age) or age == 'N/A':
        age = 40
    if pd.isna(sex) or sex == 'N/A':
        sex = 'F'
    if pd.isna(weight_lb) or weight_lb == 'N/A':
        weight_lb = 150
        
    age = float(age)
    weight_lb = float(weight_lb)

    # 1. PROTEIN INTAKE (Question 2.11) - Using your exact calc_protein_target logic
    protein_response = survey_raw_row.get('2.11', '')
    if protein_response and str(protein_response) not in ['', 'nan', 'No response']:
        try:
            protein_g = float(protein_response)
            raw_score = protein_intake_score_exact(protein_g, weight_lb, age)
            
            # Apply to Healthful Nutrition pillar - using your exact logic
            pillar = 'Healthful Nutrition'
            weight = 5.0  # From your source scoring
            scaled_score = raw_score / 10.0 if raw_score > 1.0 else raw_score
            weighted_score = scaled_score * weight
            max_weighted = weight
            
            prefix = f"survey_2.11_{pillar}"
            patient_record.update({
                f"{prefix}_response": f"{protein_g}g daily",
                f"{prefix}_score": scaled_score,
                f"{prefix}_weight": weight,
                f"{prefix}_weighted_score": weighted_score,
                f"{prefix}_max_weighted": max_weighted,
                f"{prefix}_improvement_potential": max_weighted - weighted_score
            })
        except (ValueError, TypeError):
            pass

    # 2. CALORIE INTAKE (Question 2.62) - Using your exact calc_calorie_target logic
    calorie_response = survey_raw_row.get('2.62', '')
    if calorie_response and str(calorie_response) not in ['', 'nan', 'No response']:
        try:
            calories = float(calorie_response)
            raw_score = calorie_intake_score_exact(calories, weight_lb, age, sex)
            
            # Apply to Healthful Nutrition pillar
            pillar = 'Healthful Nutrition'
            weight = 4.0
            scaled_score = raw_score / 10.0 if raw_score > 1.0 else raw_score
            weighted_score = scaled_score * weight
            max_weighted = weight
            
            prefix = f"survey_2.62_{pillar}"
            patient_record.update({
                f"{prefix}_response": f"{calories} calories daily",
                f"{prefix}_score": scaled_score,
                f"{prefix}_weight": weight,
                f"{prefix}_weighted_score": weighted_score,
                f"{prefix}_max_weighted": max_weighted,
                f"{prefix}_improvement_potential": max_weighted - weighted_score
            })
        except (ValueError, TypeError):
            pass

    # 3. MOVEMENT/EXERCISE (Questions 3.04-3.11) - Using your exact movement_questions config
    movement_scores = score_movement_pillar_exact(survey_raw_row)
    
    for (move_type, pillar_key), score in movement_scores.items():
        # Map your pillar key to full pillar name
        pillar = 'Movement + Exercise' if pillar_key == 'Movement' else pillar_key
        
        # Get the config for this movement type
        movement_config = {
            "Cardio": {"freq_q": "3.04", "weight": 16},
            "Strength": {"freq_q": "3.05", "weight": 16},
            "Flexibility": {"freq_q": "3.06", "weight": 13},
            "HIIT": {"freq_q": "3.07", "weight": 16}
        }
        
        if move_type in movement_config:
            freq_q = movement_config[move_type]["freq_q"]
            max_weight = movement_config[move_type]["weight"]
            
            # Get the actual responses
            freq_ans = survey_raw_row.get(freq_q, "")
            dur_q = {"3.04": "3.08", "3.05": "3.09", "3.06": "3.10", "3.07": "3.11"}[freq_q]
            dur_ans = survey_raw_row.get(dur_q, "")
            
            raw_score = score / max_weight if max_weight > 0 else 0
            
            prefix = f"survey_{freq_q}_{pillar}"
            patient_record.update({
                f"{prefix}_response": f"{move_type}: {freq_ans}, {dur_ans}",
                f"{prefix}_score": raw_score,
                f"{prefix}_weight": max_weight,
                f"{prefix}_weighted_score": score,
                f"{prefix}_max_weighted": max_weight,
                f"{prefix}_improvement_potential": max_weight - score
            })

    # 4. SLEEP ISSUES (Questions 4.12-4.19) - Using your exact SLEEP_ISSUES config
    sleep_scores = score_sleep_issues_exact(survey_raw_row)
    
    # Map your pillar keys to full names
    pillar_mapping = {'Sleep': 'Restorative Sleep', 'CoreCare': 'Core Care', 'Movement': 'Movement + Exercise'}
    
    for pillar_key, total_score in sleep_scores.items():
        pillar = pillar_mapping.get(pillar_key, pillar_key)
        if pillar in pillar_names:
            # Get max possible for this pillar from SLEEP_ISSUES config
            max_possible = sum(pillar_wts.get(pillar_key, 0) for _, _, pillar_wts in get_sleep_issues_config())
            
            raw_score = total_score / max_possible if max_possible > 0 else 0
            
            # Store as a consolidated sleep issues entry
            prefix = f"survey_4.12_{pillar}"
            sleep_issues_reported = [x.strip() for x in str(survey_raw_row.get("4.12", "")).split("|") if x.strip()]
            
            patient_record.update({
                f"{prefix}_response": ", ".join(sleep_issues_reported) if sleep_issues_reported else "None",
                f"{prefix}_score": raw_score,
                f"{prefix}_weight": max_possible,
                f"{prefix}_weighted_score": total_score,
                f"{prefix}_max_weighted": max_possible,
                f"{prefix}_improvement_potential": max_possible - total_score
            })

    # 5. SLEEP HYGIENE PROTOCOLS (Question 4.07) - Using your exact score_sleep_protocols logic
    hygiene_response = survey_raw_row.get('4.07', '')
    if hygiene_response and str(hygiene_response) not in ['', 'nan', 'No response']:
        try:
            weighted_score = score_sleep_protocols_exact(hygiene_response)
            max_weighted = 9.0  # Your WEIGHT constant
            raw_score = weighted_score / max_weighted if max_weighted > 0 else 0
            
            # Apply to Restorative Sleep pillar
            pillar = 'Restorative Sleep'
            
            n_protocols = len([p.strip() for p in hygiene_response.split('|') if p.strip()]) if '|' in hygiene_response else 1
            prefix = f"survey_4.07_{pillar}"
            patient_record.update({
                f"{prefix}_response": f"{n_protocols} sleep hygiene protocols",
                f"{prefix}_score": raw_score,
                f"{prefix}_weight": max_weighted,
                f"{prefix}_weighted_score": weighted_score,
                f"{prefix}_max_weighted": max_weighted,
                f"{prefix}_improvement_potential": max_weighted - weighted_score
            })
        except:
            pass

    # 6. COGNITIVE ACTIVITIES (Question 5.08) - Using your exact score_cognitive_activities logic
    cognitive_response = survey_raw_row.get('5.08', '')
    if cognitive_response and str(cognitive_response) not in ['', 'nan', 'No response']:
        try:
            weighted_score = score_cognitive_activities_exact(cognitive_response)
            max_weighted = 8.0  # Your WEIGHT constant
            raw_score = weighted_score / max_weighted if max_weighted > 0 else 0
            
            # Apply to Cognitive Health pillar
            pillar = 'Cognitive Health'
            
            n_activities = len([p.strip() for p in cognitive_response.split('|') if p.strip()]) if '|' in cognitive_response else 1
            prefix = f"survey_5.08_{pillar}"
            patient_record.update({
                f"{prefix}_response": f"{n_activities} cognitive activities",
                f"{prefix}_score": raw_score,
                f"{prefix}_weight": max_weighted,
                f"{prefix}_weighted_score": weighted_score,
                f"{prefix}_max_weighted": max_weighted,
                f"{prefix}_improvement_potential": max_weighted - weighted_score
            })
        except:
            pass

    # 7. STRESS ASSESSMENT (Questions 6.01 & 6.02) - Using your exact stress_score logic
    level_response = survey_raw_row.get('6.01', '')
    freq_response = survey_raw_row.get('6.02', '')

    if level_response and freq_response:
        try:
            weighted_score = stress_score_exact(level_response, freq_response)
            max_weighted = 19.0  # Your "Out of 19" logic
            raw_score = weighted_score / max_weighted if max_weighted > 0 else 0
            
            # Apply to Stress Management pillar for both questions
            pillar = 'Stress Management'
            
            for question_id, response_text in [('6.01', level_response), ('6.02', freq_response)]:
                prefix = f"survey_{question_id}_{pillar}"
                patient_record.update({
                    f"{prefix}_response": response_text,
                    f"{prefix}_score": raw_score,
                    f"{prefix}_weight": max_weighted,
                    f"{prefix}_weighted_score": weighted_score,
                    f"{prefix}_max_weighted": max_weighted,
                    f"{prefix}_improvement_potential": max_weighted - weighted_score
                })
        except:
            pass

    # 8. COPING SKILLS (Question 6.07) - Using your exact coping_score logic
    coping_response = survey_raw_row.get('6.07', '')
    if coping_response and str(coping_response) not in ['', 'nan', 'No response']:
        try:
            # Need stress level and frequency for your coping logic
            stress_level = survey_raw_row.get('6.01', '')
            stress_freq = survey_raw_row.get('6.02', '')
            
            weighted_score = coping_score_exact(coping_response, stress_level, stress_freq)
            max_weighted = 7.0  # Your max coping score
            raw_score = weighted_score / max_weighted if max_weighted > 0 else 0
            
            # Apply to Stress Management pillar
            pillar = 'Stress Management'
            
            n_coping = len([p.strip() for p in coping_response.split('|') if p.strip()]) if '|' in coping_response else 1
            prefix = f"survey_6.07_{pillar}"
            patient_record.update({
                f"{prefix}_response": f"{n_coping} coping strategies",
                f"{prefix}_score": raw_score,
                f"{prefix}_weight": max_weighted,
                f"{prefix}_weighted_score": weighted_score,
                f"{prefix}_max_weighted": max_weighted,
                f"{prefix}_improvement_potential": max_weighted - weighted_score
            })
        except:
            pass

    # 9. SUBSTANCE USE SCORING - Using your exact get_substance_score logic
    substance_scores = get_substance_score_exact(survey_raw_row)

    # Get substance weights and process ALL substances (including never used)
    substance_weights = {
        "Tobacco": 15, "Nicotine": 4, "Alcohol": 10, 
        "Recreational Drugs": 8, "OTC Meds": 6, "Other Substances": 6
    }

    for substance_name, max_weight in substance_weights.items():
        # Get the weighted score (defaults to max if never used)
        weighted_score = substance_scores.get(substance_name, max_weight)
        raw_score = weighted_score / max_weight
        
        # Apply to Core Care pillar only
        pillar = 'Core Care'
        question_id = f"substance_{substance_name.lower().replace(' ', '_')}"
        
        # Determine status and response text
        current_list = [x.strip() for x in str(survey_raw_row.get('8.01', '')).split('|')]
        former_list = [x.strip() for x in str(survey_raw_row.get('8.20', '')).split('|')]
        
        substance_questions = get_substance_questions_config()
        if substance_name in substance_questions:
            config = substance_questions[substance_name]
            is_current = config['current_in_which'] in current_list
            is_former = (not is_current) and (config['former_in_which'] in former_list)
            
            if is_current:
                use_band = survey_raw_row.get(config['current_band'], "")
                years_band = survey_raw_row.get(config['current_years'], "")
                response_text = f"Current user: {use_band}, {years_band}"
            elif is_former:
                use_band = survey_raw_row.get(config['former_band'], "")
                time_since_quit = survey_raw_row.get(config['time_since_quit'], "")
                response_text = f"Former user: {use_band}, quit {time_since_quit}"
            else:
                response_text = "Never used"
        else:
            response_text = "Never used"
        
        prefix = f"survey_{question_id}_{pillar}"
        patient_record.update({
            f"{prefix}_response": response_text,
            f"{prefix}_score": raw_score,
            f"{prefix}_weight": max_weight,
            f"{prefix}_weighted_score": weighted_score,
            f"{prefix}_max_weighted": max_weight,
            f"{prefix}_improvement_potential": max_weight - weighted_score
        })

    # 10. SCREENING GUIDELINES (Questions 10.01-10.08) - Using your exact screen_guidelines logic
    screen_guidelines = {
        '10.01': 6,    # Dental exam: 6 months
        '10.02': 12,   # Skin check: 12 months
        '10.03': 12,   # Vision: 12 months
        '10.04': 120,  # Colon: 120 months (10 years)
        '10.05': 12,   # Mammogram: 12 months
        '10.06': 36,   # PAP: 36 months
        '10.07': 36,   # DEXA: 36 months
        '10.08': 36,   # PSA: 36 months
    }
    
    for question_id, window_months in screen_guidelines.items():
        date_response = survey_raw_row.get(question_id, '')
        if date_response and str(date_response) not in ['', 'nan', 'No response']:
            try:
                raw_score = score_date_response_exact(date_response, window_months)
                
                # Apply to Core Care pillar
                pillar = 'Core Care'
                weight = 8.0 if question_id in ['10.04', '10.05'] else 5.0  # Higher weight for major screenings
                weighted_score = raw_score * weight
                max_weighted = weight
                
                prefix = f"survey_{question_id}_{pillar}"
                patient_record.update({
                    f"{prefix}_response": date_response,
                    f"{prefix}_score": raw_score,
                    f"{prefix}_weight": weight,
                    f"{prefix}_weighted_score": weighted_score,
                    f"{prefix}_max_weighted": max_weighted,
                    f"{prefix}_improvement_potential": max_weighted - weighted_score
                })
            except:
                pass

# Exact implementations of your source functions with proper imports

def protein_intake_score_exact(protein_g, weight_lb, age):
    """Your exact calc_protein_target and protein_intake_score logic."""
    try:
        protein_g = float(protein_g)
        # Your exact calc_protein_target logic
        weight_kg = weight_lb / 2.205
        if age < 65:
            target = 1.2 * weight_kg
        else:
            target = 1.5 * weight_kg
        target = round(target, 1)
        
        # Your exact protein_intake_score logic
        pct = protein_g / target if target else 0
        if pct >= 1:
            return 10
        elif pct >= 0.8:
            return 8
        elif pct >= 0.6:
            return 6
        elif pct > 0:
            return 4
        else:
            return 0
    except Exception:
        return 0

def calorie_intake_score_exact(calories, weight_lb, age, sex):
    """Your exact calc_calorie_target and calorie_intake_score logic."""
    try:
        calories = float(calories)
        # Your exact calc_calorie_target logic
        weight_kg = weight_lb / 2.205
        if sex.lower().startswith("m"):
            bmr = 88.362 + (13.397 * weight_kg) + (4.799 * 175) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight_kg) + (3.098 * 162) - (4.330 * age)
        calorie_target = bmr * 1.2
        target = round(calorie_target)
        
        # Your exact calorie_intake_score logic
        pct = calories / target if target else 0
        if 0.85 <= pct <= 1.15:
            return 10
        elif 0.75 <= pct < 0.85 or 1.15 < pct <= 1.25:
            return 8
        elif 0.65 <= pct < 0.75 or 1.25 < pct <= 1.35:
            return 6
        else:
            return 2
    except Exception:
        return 0

def score_movement_pillar_exact(row):
    """Your exact score_movement_pillar logic."""
    FREQ_SCORES = {
        "": 0.0,
        "Rarely (a few times a month)": 0.4,
        "Occasionally (1–2 times per week)": 0.6,
        "Regularly (3–4 times per week)": 0.8,
        "Frequently (5 or more times per week)": 1.0
    }
    
    DUR_SCORES = {
        "": 0.0,
        "Less than 30 minutes": 0.6,
        "30–45 minutes": 0.8,
        "45–60 minutes": 0.9,
        "More than 60 minutes": 1.0
    }
    
    movement_questions = {
        "Cardio": {"freq_q": "3.04", "dur_q": "3.08", "pillar_weights": {"Movement": 16}},
        "Strength": {"freq_q": "3.05", "dur_q": "3.09", "pillar_weights": {"Movement": 16}},
        "Flexibility": {"freq_q": "3.06", "dur_q": "3.10", "pillar_weights": {"Movement": 13}},
        "HIIT": {"freq_q": "3.07", "dur_q": "3.11", "pillar_weights": {"Movement": 16}}
    }
    
    movement_scores = {}
    for move_type, cfg in movement_questions.items():
        freq_ans = row.get(cfg["freq_q"], "")
        dur_ans = row.get(cfg["dur_q"], "")
        freq = FREQ_SCORES.get(freq_ans, 0.0)
        dur = DUR_SCORES.get(dur_ans, 0.0)
        
        for pillar, weight in cfg["pillar_weights"].items():
            if freq == 0 and dur == 0:
                movement_scores[(move_type, pillar)] = 0
            else:
                total = freq + dur
                if total >= 1.6:
                    movement_scores[(move_type, pillar)] = weight
                else:
                    movement_scores[(move_type, pillar)] = total * (weight / 2)
    
    return movement_scores

def get_sleep_issues_config():
    """Your exact SLEEP_ISSUES configuration."""
    return [
        ("Difficulty falling asleep", "4.13", {"Sleep": 5}),
        ("Difficulty staying asleep", "4.14", {"Sleep": 5}),
        ("Waking up too early", "4.15", {"Sleep": 5}),
        ("Frequent nightmares", "4.16", {"Sleep": 3}),
        ("Restless legs", "4.17", {"Sleep": 6, "Movement": 1}),
        ("Snoring", "4.18", {"Sleep": 4, "CoreCare": 2}),
        ("Sleep apnea", "4.19", {"Sleep": 7, "CoreCare": 3}),
    ]

def score_sleep_issues_exact(patient_answers):
    """Your exact score_sleep_issues logic."""
    SLEEP_FREQ_MAP = {
        "Always": 0.2,
        "Frequently": 0.4,
        "Occasionally": 0.6,
        "Rarely": 0.8,
        "": 1.0,
    }
    
    SLEEP_ISSUES = get_sleep_issues_config()
    
    sleep_issues_reported = [x.strip() for x in str(patient_answers.get("4.12", "")).split("|") if x.strip()]
    
    # Full credit if none reported or "None" selected
    if not sleep_issues_reported or any("none" in s.lower() for s in sleep_issues_reported):
        pillar_totals = {}
        for _, _, pillar_wts in SLEEP_ISSUES:
            for p, w in pillar_wts.items():
                pillar_totals[p] = pillar_totals.get(p, 0.0) + w
        return pillar_totals

    # Otherwise, score each reported issue
    pillar_scores = {}
    for issue, freq_qid, pillar_wts in SLEEP_ISSUES:
        if issue in sleep_issues_reported:
            freq_ans = str(patient_answers.get(freq_qid, "")).strip()
            mult = SLEEP_FREQ_MAP.get(freq_ans, 0.2)
        else:
            mult = 1.0  # Not selected = full credit
        for p, w in pillar_wts.items():
            pillar_scores[p] = pillar_scores.get(p, 0.0) + (w * mult)
    
    return pillar_scores

def score_sleep_protocols_exact(answer_str):
    """Your exact score_sleep_protocols logic."""
    WEIGHT = 9.0
    protocols = [x.strip() for x in (answer_str or "").split("|") if x.strip()]
    n = len(protocols)
    if n >= 7:
        score = 1.0
    elif n >= 5:
        score = 0.8
    elif n >= 3:
        score = 0.6
    elif n >= 1:
        score = 0.4
    else:
        score = 0.2
    return round(score * WEIGHT, 2)

def score_cognitive_activities_exact(answer_str):
    """Your exact score_cognitive_activities logic."""
    WEIGHT = 8.0
    activities = [x.strip() for x in (answer_str or "").split("|") if x.strip()]
    n = len(activities)
    if n >= 5:
        score = 1.0
    elif n == 4:
        score = 0.8
    elif n == 3:
        score = 0.6
    elif n == 2:
        score = 0.4
    elif n == 1:
        score = 0.2
    else:
        score = 0.0
    return round(score * WEIGHT, 2)

def stress_score_exact(stress_level_ans, freq_ans):
    """Your exact stress_score logic."""
    level_map = {
        "No stress": 1.0,
        "Low stress": 0.8,
        "Moderate stress": 0.5,
        "High stress": 0.2,
        "Extreme stress": 0.0,
        "Stress levels vary from low to moderate": 0.5,
        "Stress levels vary from moderate to high": 0.5,
    }
    freq_map = {
        "Rarely": 1.0,
        "Occasionally": 0.7,
        "Frequently": 0.4,
        "Always": 0.0,
    }
    s = level_map.get(str(stress_level_ans).strip(), 0.5)
    f = freq_map.get(str(freq_ans).strip(), 0.5)
    raw_score = (s + f) / 2
    return round(raw_score * 19, 2)  # Out of 19

def coping_score_exact(answer_str, stress_level_ans, freq_ans):
    """Your exact coping_score logic."""
    responses = [r.strip() for r in str(answer_str or "").split("|") if r.strip()]
    has_none = any("none" in r.lower() for r in responses)
    n_coping = sum([1 for r in responses if r.lower() not in ("none", "")])
    high_stress = (str(stress_level_ans).strip() in ["High stress", "Extreme stress"] or
                   str(freq_ans).strip() in ["Frequently", "Always"])
    if not n_coping or has_none:
        if high_stress:
            return 0.0
        else:
            return 5.5  
    elif n_coping >= 1:
        return 7.0
    else:
        return min(n_coping / 2 * 7.0, 7.0)

def get_substance_questions_config():
    """Your exact SUBSTANCE_QUESTIONS configuration."""
    return {
        "Tobacco": {
            "current_band": "8.02",
            "current_years": "8.03",
            "current_trend": "8.04",
            "former_band": "8.22",
            "former_years": "8.21",
            "time_since_quit": "8.23",
            "current_in_which": "Tobacco (cigarettes, cigars, smokeless tobacco)",
            "former_in_which": "Tobacco (cigarettes, cigars, smokeless tobacco)",
        },
        "Alcohol": {
            "current_band": "8.05",
            "current_years": "8.06",
            "current_trend": "8.07",
            "former_band": "8.25",
            "former_years": "8.24",
            "time_since_quit": "8.26",
            "current_in_which": "Alcohol",
            "former_in_which": "Alcohol",
        },
        "Recreational Drugs": {
            "current_band": "8.08",
            "current_years": "8.09",
            "current_trend": "8.10",
            "former_band": "8.28",
            "former_years": "8.27",
            "time_since_quit": "8.29",
            "current_in_which": "Recreational drugs (e.g., marijuana)",
            "former_in_which": "Recreational drugs (e.g., marijuana)",
        },
        "Nicotine": {
            "current_band": "8.11",
            "current_years": "8.12",
            "current_trend": "8.13",
            "former_band": "8.31",
            "former_years": "8.30",
            "time_since_quit": "8.32",
            "current_in_which": "Nicotine",
            "former_in_which": "Nicotine",
        },
        "OTC Meds": {
            "current_band": "8.14",
            "current_years": "8.15",
            "current_trend": "8.16",
            "former_band": "8.34",
            "former_years": "8.33",
            "time_since_quit": "8.35",
            "current_in_which": "Over-the-counter medications (e.g., sleep aids)",
            "former_in_which": "Over-the-counter medications (e.g., sleep aids)",
        },
        "Other Substances": {
            "current_band": "8.17",
            "current_years": "8.18",
            "current_trend": "8.19",
            "former_band": "8.37",
            "former_years": "8.36",
            "time_since_quit": "8.38",
            "current_in_which": "Other",
            "former_in_which": "Other",
        }
    }

def get_substance_score_exact(patient_answers):
    """Your exact get_substance_score logic."""
    USE_BAND_SCORES = {
        "Heavy": 0.0, "Moderate": 0.25, "Light": 0.5, "Minimal": 0.75, "Occasional": 1.0
    }
    DURATION_SCORES = {
        "Less than 1 year": 1.0, "1-2 years": 0.8, "3-5 years": 0.6,
        "6-10 years": 0.4, "11-20 years": 0.2, "More than 20 years": 0.0
    }
    QUIT_TIME_BONUS = {
        "Less than 3 years": 0.0, "3-5 years": 0.1, "6-10 years": 0.2,
        "11-20 years": 0.4, "More than 20 years": 0.6
    }
    SUBSTANCE_WEIGHTS = {
        "Tobacco": 15, "Nicotine": 4, "Alcohol": 10, 
        "Recreational Drugs": 8, "OTC Meds": 6, "Other Substances": 6
    }
    
    def score_substance_use(use_band, years_band, is_current, usage_trend=None, time_since_quit=None):
        band_level = use_band.split(":")[0].strip() if use_band else "Heavy"
        band_score = USE_BAND_SCORES.get(band_level, 0.0)
        duration_score = DURATION_SCORES.get(years_band, 0.0)
        base_score = min(band_score, duration_score)
        
        if not is_current:
            if time_since_quit:
                quit_bonus = QUIT_TIME_BONUS.get(time_since_quit, 0.15)
            else:
                quit_bonus = 0.15
            base_score = min(base_score + quit_bonus, 1.0)
        
        if is_current and usage_trend:
            if usage_trend == "I currently use more than I used to":
                base_score = max(base_score - 0.1, 0.0)
            elif usage_trend == "I currently use less than I used to":
                base_score = min(base_score + 0.1, 1.0)
        
        return base_score
    
    substance_scores = {}
    SUBSTANCE_QUESTIONS = get_substance_questions_config()
    
    for sub, qmap in SUBSTANCE_QUESTIONS.items():
        current_list = [x.strip() for x in str(patient_answers.get('8.01', '')).split('|')]
        former_list = [x.strip() for x in str(patient_answers.get('8.20', '')).split('|')]
        is_current = qmap['current_in_which'] in current_list
        is_former = (not is_current) and (qmap['former_in_which'] in former_list)
        score = 1.0  # default (never used = perfect)
        
        if is_current:
            use_band = patient_answers.get(qmap['current_band'], "")
            years_band = patient_answers.get(qmap['current_years'], "")
            usage_trend = patient_answers.get(qmap['current_trend'], "")
            score = score_substance_use(use_band, years_band, True, usage_trend)
        elif is_former:
            use_band = patient_answers.get(qmap['former_band'], "")
            years_band = patient_answers.get(qmap['former_years'], "")
            time_since_quit = patient_answers.get(qmap['time_since_quit'], "")
            score = score_substance_use(use_band, years_band, False, time_since_quit=time_since_quit)
        
        weighted = score * SUBSTANCE_WEIGHTS[sub]
        substance_scores[sub] = weighted
    
    return substance_scores

def score_date_response_exact(date_str, window_months):
    """Your exact score_date_response logic."""
    import pandas as pd
    from datetime import datetime
    
    if not date_str or pd.isnull(date_str):
        return 0
    try:
        exam_date = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return 0
    today = datetime.today()
    months_ago = (today.year - exam_date.year) * 12 + (today.month - exam_date.month)
    if months_ago <= window_months:
        return 1.0
    elif months_ago <= int(window_months * 1.5):
        return 0.6
    else:
        return 0.2

def calculate_education_score(patient_id, pillar):
    """Calculate education score for a given patient and pillar."""
    import random
    random.seed(hash(f"{patient_id}_{pillar}"))
    
    articles_opened = random.randint(0, 4)
    education_score = articles_opened * 25
    
    return min(education_score, 100.0)

# All the existing summary report functions remain the same...
def create_detailed_summary_report(df, output_dir):
    """Create a detailed summary report of the comprehensive scoring."""
    pillar_names = [
        "Healthful Nutrition", "Movement + Exercise", "Restorative Sleep", 
        "Cognitive Health", "Stress Management", "Connection + Purpose", "Core Care"
    ]
    
    summary_data = []
    
    for pillar in pillar_names:
        pillar_data = {
            'Pillar': pillar,
            'Avg_Combined_Pct': df[f"{pillar}_Combined_Pct"].mean(),
            'Std_Combined_Pct': df[f"{pillar}_Combined_Pct"].std(),
            'Min_Combined_Pct': df[f"{pillar}_Combined_Pct"].min(),
            'Max_Combined_Pct': df[f"{pillar}_Combined_Pct"].max(),
            'Avg_Improvement_Potential_Pct': df[f"{pillar}_Improvement_Potential_Pct"].mean(),
            'Avg_Marker_Improvement_Pct': df[f"{pillar}_Marker_Improvement_Potential_Pct"].mean(),
            'Avg_Marker_Contribution': df[f"{pillar}_Marker_Final_Weighted"].mean(),
            'Avg_Survey_Contribution': df[f"{pillar}_Survey_Final_Weighted"].mean(),
            'Avg_Education_Contribution': df[f"{pillar}_Education_Final_Weighted"].mean(),
            'Allocation_Markers': df[f"{pillar}_Allocation_Markers"].iloc[0],
            'Allocation_Survey': df[f"{pillar}_Allocation_Survey"].iloc[0],
            'Allocation_Education': df[f"{pillar}_Allocation_Education"].iloc[0],
        }
        summary_data.append(pillar_data)
    
    summary_df = pd.DataFrame(summary_data)
    summary_file = os.path.join(output_dir, "detailed_scoring_summary.csv")
    summary_df.to_csv(summary_file, index=False)
    print(f"✓ Detailed summary report saved to: {summary_file}")
    
    print("\n" + "="*80)
    print("COMPREHENSIVE SCORING SUMMARY WITH INTEGRATED COMPLEX CALCULATIONS")
    print("="*80)
    
    print(f"\nOverall Wellness Statistics:")
    print(f"  Average: {df['Overall_Wellness_Pct'].mean():.1f}%")
    print(f"  Range: {df['Overall_Wellness_Pct'].min():.1f}% - {df['Overall_Wellness_Pct'].max():.1f}%")
    print(f"  Average Relative Improvement Potential: {df['Overall_Improvement_Potential_Pct'].mean():.1f}%")

def create_marker_contribution_analysis(df, output_dir):
    """Create an analysis of individual marker contributions across patients."""
    marker_columns = [col for col in df.columns if col.startswith('marker_') and col.endswith('_weighted_score')]
    
    marker_analysis = []
    
    for col in marker_columns:
        parts = col.replace('marker_', '').replace('_weighted_score', '').rsplit('_', 1)
        if len(parts) >= 2:
            marker_parts = parts[:-1]
            marker_name = '_'.join(marker_parts)
            pillar = parts[-1]
            
            improvement_col = col.replace('_weighted_score', '_improvement_potential')
            max_col = col.replace('_weighted_score', '_max_weighted')
            
            if improvement_col in df.columns and max_col in df.columns:
                marker_analysis.append({
                    'marker': marker_name,
                    'pillar': pillar,
                    'avg_weighted_score': df[col].mean(),
                    'avg_max_weighted': df[max_col].mean(),
                    'avg_improvement_potential': df[improvement_col].mean(),
                    'total_patients': len(df),
                    'patients_with_data': (df[col] > 0).sum(),
                    'avg_utilization_pct': (df[col] / df[max_col] * 100).mean() if df[max_col].sum() > 0 else 0
                })
    
    if marker_analysis:
        marker_df = pd.DataFrame(marker_analysis)
        marker_df = marker_df.sort_values(['avg_improvement_potential'], ascending=[False])
        
        marker_file = os.path.join(output_dir, "marker_contribution_analysis.csv")
        marker_df.to_csv(marker_file, index=False)
        print(f"✓ Marker contribution analysis saved to: {marker_file}")

def create_all_survey_summary(df, output_dir):
    """Create a summary of ALL survey questions for UI reference."""
    survey_q_columns = [col for col in df.columns if col.startswith('survey_q_') and col.endswith('_response')]
    
    survey_summary = []
    
    for col in survey_q_columns:
        question_id = col.replace('survey_q_', '').replace('_response', '')
        
        raw_score_col = f"survey_q_{question_id}_raw_score"
        max_score_col = f"survey_q_{question_id}_max_score"
        normalized_col = f"survey_q_{question_id}_normalized_score"
        
        if all(c in df.columns for c in [raw_score_col, max_score_col, normalized_col]):
            responses = df[col].value_counts().to_dict()
            
            survey_summary.append({
                'question_id': question_id,
                'total_patients': len(df),
                'avg_raw_score': df[raw_score_col].mean(),
                'avg_max_score': df[max_score_col].mean(),
                'avg_normalized_score': df[normalized_col].mean(),
                'avg_improvement_potential': df[f"survey_q_{question_id}_improvement_potential"].mean(),
                'unique_responses': len(responses),
                'most_common_response': max(responses.items(), key=lambda x: x[1])[0] if responses else "N/A",
                'response_distribution': str(responses)[:200] + "..." if len(str(responses)) > 200 else str(responses)
            })
    
    if survey_summary:
        survey_df = pd.DataFrame(survey_summary)
        survey_df = survey_df.sort_values(['question_id'])
        
        survey_file = os.path.join(output_dir, "all_survey_questions_summary.csv")
        survey_df.to_csv(survey_file, index=False)
        print(f"✓ All survey questions summary saved to: {survey_file}")

def create_patient_comparison_analysis(df, output_dir):
    """Create a detailed patient comparison analysis showing distribution across pillars."""
    pillar_names = [
        "Healthful Nutrition", "Movement + Exercise", "Restorative Sleep", 
        "Cognitive Health", "Stress Management", "Connection + Purpose", "Core Care"
    ]
    
    num_patients = min(10, len(df))
    sample_patients = df.sample(n=num_patients, random_state=42)
    
    detailed_data = []
    
    for _, patient in sample_patients.iterrows():
        patient_id = patient['patient_id']
        
        for pillar in pillar_names:
            marker_final = patient.get(f"{pillar}_Marker_Final_Weighted", 0)
            survey_final = patient.get(f"{pillar}_Survey_Final_Weighted", 0)
            education_final = patient.get(f"{pillar}_Education_Final_Weighted", 0)
            combined_pct = patient.get(f"{pillar}_Combined_Pct", 0)
            improvement_pct = patient.get(f"{pillar}_Improvement_Potential_Pct", 0)
            
            detailed_data.append({
                'Patient_ID': patient_id,
                'Pillar': pillar,
                'Marker_Final_Weighted': marker_final,
                'Survey_Final_Weighted': survey_final,
                'Education_Final_Weighted': education_final,
                'Combined_Pct': combined_pct,
                'Improvement_Potential_Pct': improvement_pct,
                'Marker_Share_Pct': (marker_final / (marker_final + survey_final + education_final) * 100) if (marker_final + survey_final + education_final) > 0 else 0,
                'Survey_Share_Pct': (survey_final / (marker_final + survey_final + education_final) * 100) if (marker_final + survey_final + education_final) > 0 else 0,
                'Education_Share_Pct': (education_final / (marker_final + survey_final + education_final) * 100) if (marker_final + survey_final + education_final) > 0 else 0,
            })
    
    detailed_df = pd.DataFrame(detailed_data)
    detailed_file = os.path.join(output_dir, "patient_comparison_analysis.csv")
    detailed_df.to_csv(detailed_file, index=False)
    print(f"✓ Patient comparison analysis saved to: {detailed_file}")

def create_pillar_breakdown_analysis(df, output_dir):
    """Create a detailed breakdown of pillar components across all patients."""
    pillar_names = [
        "Healthful Nutrition", "Movement + Exercise", "Restorative Sleep", 
        "Cognitive Health", "Stress Management", "Connection + Purpose", "Core Care"
    ]
    
    pillar_analysis = []
    
    for pillar in pillar_names:
        marker_scores = df[f"{pillar}_Marker_Final_Weighted"]
        survey_scores = df[f"{pillar}_Survey_Final_Weighted"] 
        education_scores = df[f"{pillar}_Education_Final_Weighted"]
        combined_scores = df[f"{pillar}_Combined_Score"]
        improvement_scores = df[f"{pillar}_Improvement_Potential_Pct"]
        
        pillar_analysis.append({
            'Pillar': pillar,
            'Marker_Avg': marker_scores.mean(),
            'Marker_Std': marker_scores.std(),
            'Marker_Min': marker_scores.min(),
            'Marker_Max': marker_scores.max(),
            'Survey_Avg': survey_scores.mean(),
            'Survey_Std': survey_scores.std(),
            'Survey_Min': survey_scores.min(),
            'Survey_Max': survey_scores.max(),
            'Education_Avg': education_scores.mean(),
            'Education_Std': education_scores.std(),
            'Education_Min': education_scores.min(),
            'Education_Max': education_scores.max(),
            'Combined_Avg': combined_scores.mean(),
            'Combined_Std': combined_scores.std(),
            'Combined_Min': combined_scores.min(),
            'Combined_Max': combined_scores.max(),
            'Improvement_Potential_Avg': improvement_scores.mean(),
            'Improvement_Potential_Std': improvement_scores.std(),
            'Improvement_Potential_Min': improvement_scores.min(),
            'Improvement_Potential_Max': improvement_scores.max(),
        })
    
    pillar_df = pd.DataFrame(pillar_analysis)
    pillar_file = os.path.join(output_dir, "pillar_breakdown_analysis.csv")
    pillar_df.to_csv(pillar_file, index=False)
    print(f"✓ Pillar breakdown analysis saved to: {pillar_file}")

def create_markers_for_impact_scoring(df, output_dir):
    """Create a specialized file focused on markers/metrics for impact scoring."""
    marker_columns = [col for col in df.columns if col.startswith('marker_')]
    
    demo_columns = ['patient_id', 'age', 'sex', 'weight_lb', 'height_cm']
    pillar_columns = [col for col in df.columns if any(pillar in col for pillar in [
        'Healthful Nutrition', 'Movement + Exercise', 'Restorative Sleep', 
        'Cognitive Health', 'Stress Management', 'Connection + Purpose', 'Core Care'
    ]) and any(suffix in col for suffix in ['_Combined_Score', '_Combined_Pct', '_Improvement_Potential', '_Marker_Improvement_Potential_Pct'])]
    
    overall_columns = [col for col in df.columns if col.startswith('Overall_')]
    
    impact_scoring_columns = demo_columns + marker_columns + pillar_columns + overall_columns
    available_columns = [col for col in impact_scoring_columns if col in df.columns]
    
    markers_df = df[available_columns].copy()
    
    markers_file = os.path.join(output_dir, "markers_for_impact_scoring.csv")
    markers_df.to_csv(markers_file, index=False)
    print(f"✓ Markers-focused file for impact scoring saved to: {markers_file}")
    
    return markers_df

# Main execution
if __name__ == "__main__":
    print("Starting COMPLETE comprehensive scoring with INTEGRATED complex survey calculations...")
    
    result = create_comprehensive_patient_file()
    
    if result is not None:
        comprehensive_df, markers_df = result
        print(f"\n✅ Successfully created COMPLETE comprehensive file with {len(comprehensive_df)} patients")
        print(f"✓ Total columns in comprehensive file: {len(comprehensive_df.columns)}")
        print(f"✓ Total columns in markers file: {len(markers_df.columns)}")
        
        # Show complex calculations integration
        complex_survey_cols = [col for col in comprehensive_df.columns if any(qid in col for qid in ['2.11', '2.62', '3.04', '4.07', '6.01']) and 'survey_' in col]
        print(f"✓ Complex survey calculation columns found: {len(complex_survey_cols)}")
        
        print(f"\n" + "="*80)
        print(f"🎯 COMPLETE COMPREHENSIVE SCORING WITH INTEGRATED COMPLEX CALCULATIONS!")
        print("="*80)
        print("Files created in WellPath_Score_Combined/:")
        print("✓ comprehensive_patient_scores_detailed.csv (main detailed file)")
        print("✓ detailed_scoring_summary.csv (summary statistics)")  
        print("✓ marker_contribution_analysis.csv (individual marker analysis)")
        print("✓ all_survey_questions_summary.csv (all survey questions for UI)")
        print("✓ patient_comparison_analysis.csv (patient comparison details)")
        print("✓ pillar_breakdown_analysis.csv (pillar component breakdown)")
        print("✓ markers_for_impact_scoring.csv (markers-only file for impact calculations)")
        
        print(f"\n🚀 KEY FEATURES:")
        print(f"✅ INTEGRATED: Complex survey calculations now part of main scoring pipeline")
        print(f"✅ NORMALIZED: Complex calculations get proper pillar contribution columns")
        print(f"✅ PROTEIN: Personalized protein targets based on weight and age")
        print(f"✅ CALORIES: BMR-based calorie targets with activity factor")
        print(f"✅ EXERCISE: Frequency + duration combined scoring for all types")
        print(f"✅ SLEEP: Hygiene protocol counting and sleep issue frequency scoring")
        print(f"✅ STRESS: Combined level + frequency assessment")
        print(f"✅ PILLARS: All complex calculations properly distributed across pillars")
        print(f"✅ BREAKDOWN: Complex calculations will now show normalized pillar contributions")
        
    else:
        print("❌ Failed to create comprehensive scoring file.")
        print("   Check the error messages above for details.")