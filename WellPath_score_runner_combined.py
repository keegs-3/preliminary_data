import os
import pandas as pd
import numpy as np

def create_comprehensive_patient_file():
    """
    Enhanced combined scoring that creates a comprehensive patient file with:
    - Each marker's raw value, score, weight, and normalized weighted contribution per pillar
    - All questionnaire responses with their scores and weights per pillar
    - Education scores per pillar
    - Combined pillar scores with proper normalization
    - FIXED: Relative improvement potential calculations (improvement / current_score * 100)
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
    
    # FIXED: Use relative paths from script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input files with relative paths
    marker_detailed_file = os.path.join(base_dir, "WellPath_Score_Markers", "scored_markers_with_max.csv")
    survey_detailed_file = os.path.join(base_dir, "WellPath_Score_Survey", "per_question_scores_full_weighted.csv")
    raw_lab_data = os.path.join(base_dir, "data", "dummy_lab_results_full.csv")
    raw_survey_data = os.path.join(base_dir, "synthetic_patient_survey.csv")
    
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
        
        print(f"✓ Marker detailed data: {len(marker_detailed_df)} rows")
        print(f"✓ Survey detailed data: {len(survey_detailed_df)} rows") 
        print(f"✓ Raw lab data: {len(raw_lab_df)} rows")
        print(f"✓ Raw survey data: {len(raw_survey_df)} rows")
        
    except FileNotFoundError as e:
        print(f"❌ Error loading files: {e}")
        print(f"   Make sure all required files exist in the expected folders:")
        print(f"   - {marker_detailed_file}")
        print(f"   - {survey_detailed_file}")
        print(f"   - {raw_lab_data}")
        print(f"   - {raw_survey_data}")
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
        print(f"   Marker patients: {len(marker_patients)}")
        print(f"   Survey patients: {len(survey_patients)}")
        print(f"   Lab patients: {len(lab_patients)}")
        print(f"   Survey raw patients: {len(survey_raw_patients)}")
        return None
    
    # Get all unique markers and pillars from the detailed marker data
    marker_columns = [col for col in marker_detailed_df.columns if col.endswith('_weighted')]
    unique_markers = set()
    unique_pillars = set()
    
    for col in marker_columns:
        # Parse marker_pillar_weighted format
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
        
        # Add ALL questionnaire responses (for UI display - not used in impact scoring)
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
                        patient_record[f"survey_q_{qid}_normalized_score"] = total_raw_score / total_max_score if total_max_score > 0 else 0
                        patient_record[f"survey_q_{qid}_improvement_potential"] = total_max_score - total_weighted_score
                    else:
                        # No scoring data available for this question
                        patient_record[f"survey_q_{qid}_raw_score"] = 0
                        patient_record[f"survey_q_{qid}_weighted_score"] = 0
                        patient_record[f"survey_q_{qid}_max_score"] = 0
                        patient_record[f"survey_q_{qid}_normalized_score"] = 0
                        patient_record[f"survey_q_{qid}_improvement_potential"] = 0
        
        # Process individual markers with their scores and weights per pillar
        marker_meta_by_pillar = {p: [] for p in pillar_names}  # stage per-pillar marker info

        if len(marker_rows) > 0:
            marker_row = marker_rows.iloc[0]  # one row per patient expected

            # Extract all marker scoring details
            for marker in unique_markers:
                # store shared value/raw score once (first time we find any pillar column for this marker)
                shared_value_key = f"marker_{marker}_value"
                shared_raw_key   = f"marker_{marker}_raw_score"
                shared_set = (shared_value_key in patient_record)

                for pillar in unique_pillars:
                    # map pillar token to full name
                    full_pillar_name = None
                    for full_name in pillar_names:
                        if pillar in full_name or full_name.replace(" ", "").replace("+", "") == pillar.replace(" ", "").replace("+", ""):
                            full_pillar_name = full_name
                            break
                    if not full_pillar_name:
                        continue

                    raw_col      = f"{marker}_{pillar}_raw"
                    weighted_col = f"{marker}_{pillar}_weighted"
                    max_col      = f"{marker}_{pillar}_max"

                    if weighted_col in marker_row.index:
                        raw_score = float(marker_row.get(raw_col, 0) or 0)
                        weighted_score = float(marker_row.get(weighted_col, 0) or 0)
                        max_weighted   = float(marker_row.get(max_col, 0) or 0)

                        # Set shared once
                        if not shared_set:
                            patient_record[shared_value_key] = lab_row.get(marker, np.nan)
                            patient_record[shared_raw_key]   = raw_score
                            shared_set = True

                        # Stage for later normalized/impact math
                        marker_meta_by_pillar[full_pillar_name].append({
                            "marker": marker,
                            "raw": raw_score,                  # in [0,1] per your current runner
                            "weighted": weighted_score,
                            "max_weighted": max_weighted       # equals the item "weight" for this pillar
                        })

                        # Keep pillar-level weighted + max for your existing totals, but
                        # DO NOT write per-pillar raw/value columns anymore (we've de-duped).
                        patient_record[f"marker_{marker}_{full_pillar_name}_weight"] = (
                            (weighted_score / raw_score) if raw_score else 0
                        )
                        patient_record[f"marker_{marker}_{full_pillar_name}_weighted_score"] = weighted_score
                        patient_record[f"marker_{marker}_{full_pillar_name}_max_weighted"]   = max_weighted
                        patient_record[f"marker_{marker}_{full_pillar_name}_improvement_potential"] = max_weighted - weighted_score

        # Process individual survey questions with their scores and weights per pillar  
        if len(survey_rows) > 0:
            survey_row = survey_rows.iloc[0]  # Should be one row per patient
            
            # Extract all survey question scoring details
            survey_weighted_cols = [col for col in survey_row.index if col.endswith('_weighted')]
            
            for weighted_col in survey_weighted_cols:
                if pd.notna(survey_row[weighted_col]) and survey_row[weighted_col] != 0:
                    # Parse question_pillar_weighted format
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
                            
                            # Calculate the weight
                            weight = weighted_score / raw_score if raw_score != 0 else 0
                            
                            # Store individual survey question details
                            patient_record[f"survey_{question_id}_{full_pillar_name}_response"] = survey_raw_row.get(question_id, "")
                            patient_record[f"survey_{question_id}_{full_pillar_name}_score"] = raw_score
                            patient_record[f"survey_{question_id}_{full_pillar_name}_weight"] = weight
                            patient_record[f"survey_{question_id}_{full_pillar_name}_weighted_score"] = weighted_score
                            patient_record[f"survey_{question_id}_{full_pillar_name}_max_weighted"] = max_score
                            patient_record[f"survey_{question_id}_{full_pillar_name}_improvement_potential"] = max_score - weighted_score
        
        # === Calculate pillar totals, normalization, and per-item normalized impact ===
        for pillar in pillar_names:
            weights = pillar_weights[pillar]

            # ------- Pillar totals (markers / survey) -------
            marker_total_weighted = sum(
                float(val or 0.0) for key, val in patient_record.items()
                if key.startswith("marker_") and key.endswith(f"_{pillar}_weighted_score")
            )
            marker_total_max = sum(
                float(val or 0.0) for key, val in patient_record.items()
                if key.startswith("marker_") and key.endswith(f"_{pillar}_max_weighted")
            )

            survey_total_weighted = sum(
                float(val or 0.0) for key, val in patient_record.items()
                if key.startswith("survey_") and key.endswith(f"_{pillar}_weighted_score")
            )
            survey_total_max = sum(
                float(val or 0.0) for key, val in patient_record.items()
                if key.startswith("survey_") and key.endswith(f"_{pillar}_max_weighted")
            )

            # Education (placeholder)
            education_score = calculate_education_score(patient_id, pillar)
            education_max = 100.0

            # ------- Normalize each component to 0–1 -------
            marker_normalized = (marker_total_weighted / marker_total_max) if marker_total_max > 0 else 0.0
            survey_normalized = (survey_total_weighted / survey_total_max) if survey_total_max > 0 else 0.0
            education_normalized = (education_score / education_max) if education_max > 0 else 0.0

            # ------- Apply pillar allocation weights -------
            marker_final_weighted = marker_normalized * weights["markers"]
            survey_final_weighted = survey_normalized * weights["survey"]
            education_final_weighted = education_normalized * weights["education"]

            combined_score = marker_final_weighted + survey_final_weighted + education_final_weighted
            combined_pct = combined_score * 100.0
            improvement_potential = 1.0 - combined_score
            
            # FIXED: Calculate RELATIVE improvement potential
            # For pillars: improvement_potential / combined_score * 100
            improvement_potential_pct = (improvement_potential / combined_score * 100.0) if combined_score > 0 else 0.0
            
            # Calculate marker-specific improvement potential relative to pillar score
            marker_improvement_potential = (weights["markers"] * (1.0 - marker_normalized)) if marker_normalized < 1.0 else 0.0
            marker_improvement_potential_pct = (marker_improvement_potential / combined_score * 100.0) if combined_score > 0 else 0.0

            # ------- Store pillar summary -------
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
                f"{pillar}_Improvement_Potential_Pct": improvement_potential_pct,  # FIXED: Now relative
                
                # ADDED: Marker-specific improvement potential
                f"{pillar}_Marker_Improvement_Potential": marker_improvement_potential,
                f"{pillar}_Marker_Improvement_Potential_Pct": marker_improvement_potential_pct,

                f"{pillar}_Allocation_Markers": weights["markers"],
                f"{pillar}_Allocation_Survey": weights["survey"],
                f"{pillar}_Allocation_Education": weights["education"],
            })

            # ------- Per-marker normalized share-of-pillar -------
            if marker_total_max > 0:
                suffix = f"_{pillar}_max_weighted"

                # SNAPSHOT the keys BEFORE we start writing new fields
                marker_keys = [
                    key for key in patient_record.keys()
                    if key.startswith("marker_") and key.endswith(suffix)
                ]

                for key in marker_keys:
                    marker_name = key[len("marker_"):-len(suffix)]
                    max_weight = float(patient_record.get(key, 0.0) or 0.0)
                    if max_weight <= 0:
                        continue

                    # Item's share of the pillar (decimal, not %): allocation × (weight / pillar marker max)
                    norm_pct = weights["markers"] * (max_weight / marker_total_max)

                    # Points on 0–100 pillar scale
                    max_points = norm_pct * 100.0

                    # Pull raw score for this marker (prefer the shared field)
                    raw_key = f"marker_{marker_name}_raw_score"
                    raw_val = float(patient_record.get(raw_key, 0.0) or 0.0)
                    raw_val = 0.0 if raw_val < 0 else (1.0 if raw_val > 1 else raw_val)  # clamp

                    current_points = raw_val * max_points
                    improve_points = (1.0 - raw_val) * max_points

                    # WRITE new fields (safe now because we're iterating over a snapshot)
                    patient_record[f"marker_{marker_name}_{pillar}_norm_pct"] = norm_pct
                    patient_record[f"marker_{marker_name}_{pillar}_max_points"] = max_points
                    patient_record[f"marker_{marker_name}_{pillar}_current_points"] = current_points
                    patient_record[f"marker_{marker_name}_{pillar}_improve_points"] = improve_points

        # === Overall wellness score ===
        pillar_combined_scores = [patient_record[f"{pillar}_Combined_Score"] for pillar in pillar_names]
        overall_wellness = float(np.mean(pillar_combined_scores)) if pillar_combined_scores else 0.0
        overall_wellness_pct = overall_wellness * 100.0
        overall_improvement_potential = 1.0 - overall_wellness
        
        # FIXED: Calculate RELATIVE improvement potential for overall
        # For overall: overall_improvement_potential / overall_wellness * 100
        overall_improvement_potential_pct = (overall_improvement_potential / overall_wellness * 100.0) if overall_wellness > 0 else 0.0

        patient_record.update({
            "Overall_Wellness_Score": overall_wellness,
            "Overall_Wellness_Pct": overall_wellness_pct,
            "Overall_Max_Possible_Score": 1.0,
            "Overall_Improvement_Potential": overall_improvement_potential,
            "Overall_Improvement_Potential_Pct": overall_improvement_potential_pct,  # FIXED: Now relative
        })

        comprehensive_results.append(patient_record)
    
    # Create comprehensive DataFrame
    comprehensive_df = pd.DataFrame(comprehensive_results)
    
    # Save comprehensive file
    comprehensive_file = os.path.join(combined_output_dir, "comprehensive_patient_scores_detailed.csv")
    comprehensive_df.to_csv(comprehensive_file, index=False)
    print(f"✓ Comprehensive patient file saved to: {comprehensive_file}")
    
    # Create summary reports
    create_detailed_summary_report(comprehensive_df, combined_output_dir)
    create_marker_contribution_analysis(comprehensive_df, combined_output_dir)
    create_all_survey_summary(comprehensive_df, combined_output_dir)
    markers_df = create_markers_for_impact_scoring(comprehensive_df, combined_output_dir)
    
    return comprehensive_df, markers_df

def calculate_education_score(patient_id, pillar):
    """
    Calculate education score for a given patient and pillar.
    Each pillar has 4 core articles, each worth 25 points (total 100 points).
    
    For MVP: This is a placeholder function. In production, this would query
    our education engagement database to see which articles were opened.
    """
    
    # MVP: Simulate random engagement for demonstration
    # In production, replace this with actual database query
    import random
    random.seed(hash(f"{patient_id}_{pillar}"))  # Consistent random for demo
    
    articles_opened = random.randint(0, 4)  # 0-4 articles opened
    education_score = articles_opened * 25  # Each article worth 25 points
    
    return min(education_score, 100.0)  # Cap at 100

def create_detailed_summary_report(df, output_dir):
    """
    Create a detailed summary report of the comprehensive scoring.
    """
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
            'Avg_Improvement_Potential_Pct': df[f"{pillar}_Improvement_Potential_Pct"].mean(),  # Now relative
            'Avg_Marker_Improvement_Pct': df[f"{pillar}_Marker_Improvement_Potential_Pct"].mean(),  # New field
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
    
    # Print key insights with FIXED relative percentages
    print("\n" + "="*80)
    print("DETAILED COMPREHENSIVE SCORING SUMMARY (WITH FIXED RELATIVE IMPROVEMENT %)")
    print("="*80)
    
    print(f"\nOverall Wellness Statistics:")
    print(f"  Average: {df['Overall_Wellness_Pct'].mean():.1f}%")
    print(f"  Range: {df['Overall_Wellness_Pct'].min():.1f}% - {df['Overall_Wellness_Pct'].max():.1f}%")
    print(f"  Average Relative Improvement Potential: {df['Overall_Improvement_Potential_Pct'].mean():.1f}%")
    
    for _, row in summary_df.iterrows():
        print(f"\n{row['Pillar']}:")
        print(f"  Current Score: {row['Avg_Combined_Pct']:.1f}% (±{row['Std_Combined_Pct']:.1f}%)")
        print(f"  Relative Improvement Potential: {row['Avg_Improvement_Potential_Pct']:.1f}%")
        print(f"  Marker Improvement Potential: {row['Avg_Marker_Improvement_Pct']:.1f}%")
        print(f"  Allocation Weights: {row['Allocation_Markers']:.1%} markers, {row['Allocation_Survey']:.1%} survey, {row['Allocation_Education']:.1%} education")
        print(f"  Final Contributions: Markers={row['Avg_Marker_Contribution']:.3f}, Survey={row['Avg_Survey_Contribution']:.3f}, Education={row['Avg_Education_Contribution']:.3f}")

def create_marker_contribution_analysis(df, output_dir):
    """
    Create an analysis of individual marker contributions across patients.
    """
    # Get all marker contribution columns
    marker_columns = [col for col in df.columns if col.startswith('marker_') and col.endswith('_weighted_score')]
    
    marker_analysis = []
    
    for col in marker_columns:
        # Parse marker name and pillar
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
    """
    Create a summary of ALL survey questions for UI reference.
    """
    # Get all survey question columns
    survey_q_columns = [col for col in df.columns if col.startswith('survey_q_') and col.endswith('_response')]
    
    survey_summary = []
    
    for col in survey_q_columns:
        question_id = col.replace('survey_q_', '').replace('_response', '')
        
        # Get corresponding score columns
        raw_score_col = f"survey_q_{question_id}_raw_score"
        max_score_col = f"survey_q_{question_id}_max_score"
        normalized_col = f"survey_q_{question_id}_normalized_score"
        
        if all(c in df.columns for c in [raw_score_col, max_score_col, normalized_col]):
            # Get unique responses and their frequencies
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

def create_markers_for_impact_scoring(df, output_dir):
    """
    Create a specialized file focused on markers/metrics for impact scoring.
    This excludes survey questions since they don't factor into impact calculations.
    """
    # Get all marker-related columns
    marker_columns = [col for col in df.columns if col.startswith('marker_')]
    
    # Also include patient demographics and pillar totals
    demo_columns = ['patient_id', 'age', 'sex', 'weight_lb', 'height_cm']
    pillar_columns = [col for col in df.columns if any(pillar in col for pillar in [
        'Healthful Nutrition', 'Movement + Exercise', 'Restorative Sleep', 
        'Cognitive Health', 'Stress Management', 'Connection + Purpose', 'Core Care'
    ]) and any(suffix in col for suffix in ['_Combined_Score', '_Combined_Pct', '_Improvement_Potential', '_Marker_Improvement_Potential_Pct'])]
    
    overall_columns = [col for col in df.columns if col.startswith('Overall_')]
    
    # Create markers-focused dataset
    impact_scoring_columns = demo_columns + marker_columns + pillar_columns + overall_columns
    available_columns = [col for col in impact_scoring_columns if col in df.columns]
    
    markers_df = df[available_columns].copy()
    
    markers_file = os.path.join(output_dir, "markers_for_impact_scoring.csv")
    markers_df.to_csv(markers_file, index=False)
    print(f"✓ Markers-focused file for impact scoring saved to: {markers_file}")
    
    return markers_df

# Main execution
if __name__ == "__main__":
    print("Starting detailed comprehensive scoring with FIXED relative improvement potential...")
    
    # Create comprehensive patient file
    result = create_comprehensive_patient_file()
    
    if result is not None:
        comprehensive_df, markers_df = result
        print(f"\n✅ Successfully created detailed comprehensive file with {len(comprehensive_df)} patients")
        print(f"✓ Total columns in comprehensive file: {len(comprehensive_df.columns)}")
        print(f"✓ Total columns in markers file: {len(markers_df.columns)}")
        
        # Show example of FIXED calculations for first patient
        first_patient = comprehensive_df.iloc[0]
        patient_id = first_patient['patient_id']
        
        print(f"\n" + "="*60)
        print(f"EXAMPLE: FIXED CALCULATIONS FOR PATIENT {patient_id}")
        print("="*60)
        
        for pillar in ["Cognitive Health", "Healthful Nutrition"]:  # Show 2 examples
            combined_score = first_patient[f"{pillar}_Combined_Score"]
            improvement_potential = first_patient[f"{pillar}_Improvement_Potential"]
            improvement_potential_pct = first_patient[f"{pillar}_Improvement_Potential_Pct"]
            marker_improvement_potential = first_patient[f"{pillar}_Marker_Improvement_Potential"]
            marker_improvement_potential_pct = first_patient[f"{pillar}_Marker_Improvement_Potential_Pct"]
            
            print(f"\n{pillar}:")
            print(f"  Combined Score: {combined_score:.6f}")
            print(f"  Improvement Potential (absolute): {improvement_potential:.6f}")
            print(f"  Improvement Potential (relative %): {improvement_potential_pct:.2f}%")
            print(f"  Marker Improvement Potential: {marker_improvement_potential:.6f}")
            print(f"  Marker Improvement Potential (%): {marker_improvement_potential_pct:.2f}%")
            print(f"  Formula: {improvement_potential:.6f} / {combined_score:.6f} * 100 = {improvement_potential_pct:.2f}%")
        
        overall_wellness = first_patient["Overall_Wellness_Score"]
        overall_improvement = first_patient["Overall_Improvement_Potential"]
        overall_improvement_pct = first_patient["Overall_Improvement_Potential_Pct"]
        
        print(f"\nOverall Wellness:")
        print(f"  Overall Score: {overall_wellness:.6f}")
        print(f"  Improvement Potential (absolute): {overall_improvement:.6f}")
        print(f"  Improvement Potential (relative %): {overall_improvement_pct:.2f}%")
        print(f"  Formula: {overall_improvement:.6f} / {overall_wellness:.6f} * 100 = {overall_improvement_pct:.2f}%")
        
        print("\n" + "="*80)
        print("🎯 COMPREHENSIVE SCORING COMPLETE!")
        print("="*80)
        print("Files created in WellPath_Score_Combined/:")
        print("✓ comprehensive_patient_scores_detailed.csv (main detailed file)")
        print("✓ detailed_scoring_summary.csv (summary statistics)")  
        print("✓ marker_contribution_analysis.csv (individual marker analysis)")
        print("✓ all_survey_questions_summary.csv (all survey questions for UI)")
        print("✓ markers_for_impact_scoring.csv (markers-only file for impact calculations)")
        
        print(f"\n🔧 KEY IMPROVEMENTS:")
        print(f"✅ FIXED: Uses relative paths - works on any machine after git clone")
        print(f"✅ FIXED: Improvement_potential_pct now relative (improvement/current_score*100)")
        print(f"✅ ADDED: Marker_improvement_potential_pct for impact scoring")
        print(f"✅ ADDED: Better error handling and status messages")
        print(f"✅ IMPROVED: All pillar and overall improvement percentages are meaningful")
        
    else:
        print("❌ Failed to create detailed comprehensive scoring file.")
        print("   Check the error messages above for details.")
