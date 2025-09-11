#!/usr/bin/env python3
"""
Statistical WellPath Impact Scorer - Calculate raw impact points then scale intelligently
"""

import pandas as pd
import numpy as np
import json
import os
from typing import Dict, List, Set, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class StatisticalImpactScorer:
    """Impact Scorer that calculates raw points then applies statistical scaling"""
    
    def __init__(self, recommendations_file: str, markers_file: str, comprehensive_file: str):
        """Initialize with statistical approach"""
        self.recommendations = self._load_recommendations(recommendations_file)
        self.markers_df = pd.read_csv(markers_file)
        self.comprehensive_df = pd.read_csv(comprehensive_file)
        
        # WellPath pillar weights (evidence-based)
        self.PILLAR_WEIGHTS = {
            'Healthful Nutrition': 0.25,
            'Movement + Exercise': 0.20,
            'Restorative Sleep': 0.15,
            'Stress Management': 0.15,
            'Cognitive Health': 0.10,
            'Connection + Purpose': 0.10,
            'Core Care': 0.15
        }
        
        # Category weights for primary/secondary/tertiary markers
        self.CATEGORY_WEIGHTS = {
            'primary': 1.0,
            'secondary': 0.7,
            'tertiary': 0.4
        }
        
        print(f"🎯 Initialized Statistical Impact Scorer")
        print(f"   Recommendations: {len(self.recommendations)}")
        print(f"   Patients: {len(self.markers_df)}")

    def _load_recommendations(self, file_path: str) -> List[Dict]:
        """Load and parse recommendations from JSON file, selecting one per base ID"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_recommendations = data.get('recommendations', [])
            
            # Group recommendations by base ID (e.g., REC0001, REC0002, etc.)
            recommendation_groups = {}
            for rec in all_recommendations:
                # Extract base ID: "REC0001.1" -> "REC0001", "REC0001.3 (i)" -> "REC0001"
                base_id = rec['id'].split('.')[0]  # Gets "REC0001" from "REC0001.1" or "REC0001.3"
                
                if base_id not in recommendation_groups:
                    recommendation_groups[base_id] = []
                recommendation_groups[base_id].append(rec)
            
            # Select one recommendation per base ID (prefer highest complexity/most markers)
            selected_recommendations = []
            for base_id, recs in recommendation_groups.items():
                # Select the recommendation with the most total markers/metrics
                best_rec = max(recs, key=lambda r: (
                    len(r.get('primary_markers', [])) +
                    len(r.get('secondary_markers', [])) +
                    len(r.get('tertiary_markers', [])) +
                    len(r.get('primary_metrics', [])) +
                    len(r.get('secondary_metrics', [])) +
                    len(r.get('tertiary_metrics', []))
                ))
                selected_recommendations.append(best_rec)
            
            print(f"📋 Recommendation Selection:")
            print(f"   Total recommendations in JSON: {len(all_recommendations)}")
            print(f"   Unique base IDs found: {len(recommendation_groups)}")
            print(f"   Selected recommendations: {len(selected_recommendations)}")
            
            return selected_recommendations
            
        except Exception as e:
            print(f"Error loading recommendations: {e}")
            return []

    def calculate_raw_impact_points(self, recommendation: Dict, patient_row: pd.Series) -> Dict:
        """
        Calculate raw impact points using the formula:
        Impact = Improvement_Points × Pillar_Potential_% × Pillar_Weight × Category_Weight
        """
        rec_id = recommendation['id']
        baseline_impact = float(recommendation.get('raw_impact', 0))
        
        total_raw_points = 0.0
        marker_details = []
        affected_pillars = set()
        
        # Process all categories of markers/metrics
        for category in ['primary', 'secondary', 'tertiary']:
            for marker_type in ['markers', 'metrics']:
                key = f'{category}_{marker_type}'
                
                for marker in recommendation.get(key, []):
                    # Calculate raw points for this marker across all pillars
                    marker_impact = self._calculate_marker_raw_points(
                        marker, patient_row, category
                    )
                    
                    if marker_impact['total_raw_points'] > 0:
                        total_raw_points += marker_impact['total_raw_points']
                        marker_details.append(marker_impact)
                        affected_pillars.update(marker_impact['affected_pillars'])
        
        return {
            'recommendation_id': rec_id,
            'recommendation_title': recommendation.get('title', '').strip('"'),
            'baseline_impact': baseline_impact,
            'total_raw_points': round(total_raw_points, 4),
            'affected_markers_count': len(marker_details),
            'affected_pillars': list(affected_pillars),
            'marker_details': marker_details
        }

    def _calculate_marker_raw_points(self, marker: str, patient_row: pd.Series, category: str) -> Dict:
        """Calculate raw impact points for a single marker across all pillars"""
        
        total_raw_points = 0.0
        pillar_impacts = {}
        affected_pillars = []
        
        for pillar in self.PILLAR_WEIGHTS.keys():
            # Get improvement points for this marker-pillar combination
            improve_points_field = f"marker_{marker}_{pillar}_improve_points"
            improve_points = self._get_field_value(patient_row, improve_points_field, 0.0)
            
            if improve_points > 0:
                # Get pillar improvement potential percentage
                pillar_potential_field = f"{pillar}_Marker_Improvement_Potential_Pct"
                pillar_potential_pct = self._get_field_value(patient_row, pillar_potential_field, 0.0)
                
                # Calculate raw impact points for this marker-pillar combination
                raw_points = (
                    improve_points *                           # Real improvement points
                    (pillar_potential_pct / 100.0) *          # Pillar improvement potential (0-1)
                    self.PILLAR_WEIGHTS[pillar] *              # WellPath pillar weight
                    self.CATEGORY_WEIGHTS[category]            # Primary/secondary/tertiary weight
                )
                
                total_raw_points += raw_points
                pillar_impacts[pillar] = {
                    'improve_points': improve_points,
                    'pillar_potential_pct': pillar_potential_pct,
                    'pillar_weight': self.PILLAR_WEIGHTS[pillar],
                    'category_weight': self.CATEGORY_WEIGHTS[category],
                    'raw_points': round(raw_points, 4)
                }
                affected_pillars.append(pillar)
        
        return {
            'marker': marker,
            'category': category,
            'total_raw_points': round(total_raw_points, 4),
            'affected_pillars': affected_pillars,
            'pillar_impacts': pillar_impacts
        }

    def _get_field_value(self, patient_row: pd.Series, field_name: str, default: float) -> float:
        """Safely get field value from patient row"""
        if field_name in patient_row.index:
            value = patient_row[field_name]
            if pd.notna(value) and str(value).strip() != '':
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default
        return default

    def apply_statistical_scaling(self, impact_df: pd.DataFrame, method: str = 'linear') -> pd.DataFrame:
        """
        Apply statistical scaling to convert raw points to 0-10 scores
        
        Methods:
        - 'linear': Simple linear scaling (min=0, max=10)
        - 'percentile': Use percentiles for more normal distribution
        - 'log_normal': Log transformation then linear scaling
        - 'z_score': Z-score normalization then scaling
        """
        
        raw_points = impact_df['total_raw_points'].values
        
        if method == 'linear':
            # Simple min-max scaling: min gets 0, max gets 10
            min_points = raw_points.min()
            max_points = raw_points.max()
            
            if max_points == min_points:
                scaled_scores = np.full_like(raw_points, 5.0)  # All same score
            else:
                scaled_scores = 10.0 * (raw_points - min_points) / (max_points - min_points)
        
        elif method == 'percentile':
            # Use percentiles for better distribution
            # Bottom 10% get 0-2, middle 80% get 2-8, top 10% get 8-10
            percentiles = np.percentile(raw_points, [10, 50, 90])
            scaled_scores = np.zeros_like(raw_points)
            
            # Bottom 10%: 0-2
            mask_low = raw_points <= percentiles[0]
            if np.any(mask_low):
                scaled_scores[mask_low] = 2.0 * (raw_points[mask_low] - raw_points.min()) / (percentiles[0] - raw_points.min() + 1e-10)
            
            # Middle 80%: 2-8  
            mask_mid = (raw_points > percentiles[0]) & (raw_points <= percentiles[2])
            if np.any(mask_mid):
                scaled_scores[mask_mid] = 2.0 + 6.0 * (raw_points[mask_mid] - percentiles[0]) / (percentiles[2] - percentiles[0] + 1e-10)
            
            # Top 10%: 8-10
            mask_high = raw_points > percentiles[2]
            if np.any(mask_high):
                scaled_scores[mask_high] = 8.0 + 2.0 * (raw_points[mask_high] - percentiles[2]) / (raw_points.max() - percentiles[2] + 1e-10)
        
        elif method == 'log_normal':
            # Log transformation then linear scaling (good for skewed data)
            log_points = np.log1p(raw_points)  # log(1 + x) to handle zeros
            min_log = log_points.min()
            max_log = log_points.max()
            
            if max_log == min_log:
                scaled_scores = np.full_like(raw_points, 5.0)
            else:
                scaled_scores = 10.0 * (log_points - min_log) / (max_log - min_log)
        
        elif method == 'z_score':
            # Z-score normalization then scaling to 0-10
            mean_points = raw_points.mean()
            std_points = raw_points.std()
            
            if std_points == 0:
                scaled_scores = np.full_like(raw_points, 5.0)
            else:
                z_scores = (raw_points - mean_points) / std_points
                # Scale z-scores to 0-10 (assuming most are within 3 standard deviations)
                scaled_scores = 5.0 + (10.0/6.0) * z_scores  # Center at 5, scale by 6 std devs
                scaled_scores = np.clip(scaled_scores, 0, 10)  # Ensure 0-10 range
        
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        # Add scaled scores to dataframe
        impact_df = impact_df.copy()
        impact_df['final_score'] = np.round(scaled_scores, 2)
        impact_df['tier'] = impact_df['final_score'].apply(self._get_impact_tier)
        impact_df['scaling_method'] = method
        
        return impact_df

    def _get_impact_tier(self, score: float) -> str:
        """Classify impact score into tier"""
        if score >= 7:
            return 'high'
        elif score >= 4:
            return 'medium'
        else:
            return 'low'

    def process_all_patients(self, patient_subset: Optional[List[str]] = None) -> pd.DataFrame:
        """Process all patients and calculate raw impact points"""
        impact_results = []
        
        # Filter patients if subset provided
        if patient_subset:
            patients_df = self.markers_df[self.markers_df['patient_id'].isin(patient_subset)]
        else:
            patients_df = self.markers_df
        
        print(f"📄 Processing {len(patients_df)} patients...")
        
        for idx, (_, patient_row) in enumerate(patients_df.iterrows()):
            patient_id = patient_row['patient_id']
            
            if idx % 50 == 0:
                print(f"   Processed {idx}/{len(patients_df)} patients...")
            
            # Calculate raw impact points for this patient
            for rec in self.recommendations:
                try:
                    rec_impact = self.calculate_raw_impact_points(rec, patient_row)
                    rec_impact['patient_id'] = patient_id
                    impact_results.append(rec_impact)
                    
                except Exception as e:
                    print(f"⚠ Error calculating impact for {patient_id}-{rec.get('id', 'unknown')}: {e}")
        
        print(f"✅ Raw points calculation complete: {len(impact_results)} recommendation scores")
        return pd.DataFrame(impact_results)

def get_default_file_paths(base_dir: str) -> Dict[str, str]:
    """
    Get default file paths for the scorer.
    Input files come from WellPath_Score_Combined folder.
    Output files go to Recommendation_Impact_Scores folder.
    """
    # Input directory - where the combined scoring data is located
    input_dir = os.path.join(base_dir, "WellPath_Score_Combined")
    
    # Output directory - where impact scoring results will be saved
    output_dir = os.path.join(base_dir, "Recommendation_Impact_Scores")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    return {
        "recommendations_file": os.path.join(base_dir, "recommendations_list.json"),
        "markers_file": os.path.join(input_dir, "markers_for_impact_scoring.csv"),
        "comprehensive_file": os.path.join(input_dir, "comprehensive_patient_scores_detailed.csv"),
        "output_dir": output_dir
    }

def run_statistical_impact_scoring(
    base_dir: str = None,
    scaling_method: str = 'percentile', 
    patient_subset: Optional[List[str]] = None,
    recommendations_file: str = None,
    markers_file: str = None,
    comprehensive_file: str = None,
    output_dir: str = None
):
    """Run the statistical impact scoring with intelligent scaling"""
    
    # If base_dir provided, use default paths
    if base_dir:
        default_paths = get_default_file_paths(base_dir)
        recommendations_file = recommendations_file or default_paths["recommendations_file"]
        markers_file = markers_file or default_paths["markers_file"]
        comprehensive_file = comprehensive_file or default_paths["comprehensive_file"]
        output_dir = output_dir or default_paths["output_dir"]
    
    # Verify all required files exist
    required_files = [recommendations_file, markers_file, comprehensive_file]
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"⚠ Required file not found: {file_path}")
            return None, None
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚀 Starting Statistical WellPath Impact Scoring")
    print(f"   Scaling method: {scaling_method}")
    print(f"   Input files:")
    print(f"     Recommendations: {recommendations_file}")
    print(f"     Markers: {markers_file}")
    print(f"     Comprehensive: {comprehensive_file}")
    print(f"   Output directory: {output_dir}")
    print("="*60)
    
    # Initialize scorer
    scorer = StatisticalImpactScorer(recommendations_file, markers_file, comprehensive_file)
    
    # Step 1: Calculate raw impact points
    print("📊 Step 1: Calculating raw impact points...")
    raw_impact_df = scorer.process_all_patients(patient_subset)
    
    if raw_impact_df.empty:
        print("⚠ No impact points calculated")
        return None, None
    
    # Normalize baseline_impact to a fraction in [0, 1]
    baseline = pd.to_numeric(raw_impact_df['baseline_impact'], errors='coerce')
    bfrac = np.where(baseline > 1, baseline / 100.0, baseline)
    bfrac = np.where(np.isnan(bfrac), 1.0, bfrac)  # treat missing baseline as 1.0
    
    # Gate raw points by baseline
    raw_impact_df['total_raw_points_before_baseline'] = raw_impact_df['total_raw_points']
    raw_impact_df['total_raw_points_adj'] = raw_impact_df['total_raw_points'] * bfrac
    
    # Feed the adjusted points into the scaler
    impact_input = raw_impact_df.copy()
    impact_input['total_raw_points'] = impact_input['total_raw_points_adj']
    
    # Step 2: Apply statistical scaling
    print(f"📈 Step 2: Applying {scaling_method} scaling to convert to 0-10 scores...")
    final_impact_df = scorer.apply_statistical_scaling(impact_input, method=scaling_method)
    
    # Keep both pre and post baseline totals for audit
    cols_to_keep = [
        'patient_id', 'recommendation_id',
        'total_raw_points_before_baseline', 'total_raw_points_adj'
    ]
    final_impact_df = final_impact_df.merge(
        raw_impact_df[cols_to_keep],
        on=['patient_id', 'recommendation_id'],
        how='left'
    )

    # Display scaling statistics
    print(f"\n📊 Raw Points Statistics:")
    raw_stats = raw_impact_df['total_raw_points'].describe()
    print(f"   Min: {raw_stats['min']:.4f}")
    print(f"   Mean: {raw_stats['mean']:.4f}")
    print(f"   Max: {raw_stats['max']:.4f}")
    print(f"   Std: {raw_stats['std']:.4f}")
    
    print(f"\n📊 Final Score Statistics (after {scaling_method} scaling):")
    final_stats = final_impact_df['final_score'].describe()
    print(f"   Min: {final_stats['min']:.2f}")
    print(f"   Mean: {final_stats['mean']:.2f}")
    print(f"   Max: {final_stats['max']:.2f}")
    print(f"   Std: {final_stats['std']:.2f}")
    
    # Save detailed results (all recommendations for all patients)
    detailed_impact_file = os.path.join(output_dir, f"detailed_impact_scores_{scaling_method}.csv")
    final_impact_df.to_csv(detailed_impact_file, index=False)
    print(f"✅ Detailed impact scores saved to: {detailed_impact_file}")
    
    # Save summary results (one file with key metrics)
    summary_impact_df = final_impact_df[['patient_id', 'recommendation_id', 'recommendation_title', 
                                       'total_raw_points', 'final_score', 'tier', 'affected_markers_count']].copy()
    summary_impact_file = os.path.join(output_dir, f"summary_impact_scores_{scaling_method}.csv")
    summary_impact_df.to_csv(summary_impact_file, index=False)
    print(f"✅ Summary impact scores saved to: {summary_impact_file}")
    
    # Generate patient summary recommendations
    patient_summaries = []
    for patient_id in final_impact_df['patient_id'].unique():
        patient_data = final_impact_df[final_impact_df['patient_id'] == patient_id]
        top_recs = patient_data.nlargest(5, 'final_score')
        
        summary = {
            'patient_id': patient_id,
            'scaling_method': scaling_method,
            'total_recommendations': len(patient_data),
            'avg_final_score': round(patient_data['final_score'].mean(), 2),
            'avg_raw_points': round(patient_data['total_raw_points'].mean(), 4),
            'high_impact_count': len(patient_data[patient_data['tier'] == 'high']),
            'top_recommendation': top_recs.iloc[0]['recommendation_title'] if not top_recs.empty else 'None',
            'top_score': round(top_recs.iloc[0]['final_score'], 2) if not top_recs.empty else 0.0,
            'top_5_recommendations': [
                f"{row['recommendation_title']} ({row['final_score']})"
                for _, row in top_recs.iterrows()
            ]
        }
        patient_summaries.append(summary)
    
    patient_summary_df = pd.DataFrame(patient_summaries)
    summary_file = os.path.join(output_dir, f"statistical_patient_summary_{scaling_method}.csv")
    patient_summary_df.to_csv(summary_file, index=False)
    print(f"✅ Patient summaries saved to: {summary_file}")
    
    # Print final summary
    print("\n" + "="*60)
    print("🎯 STATISTICAL IMPACT SCORING SUMMARY")
    print("="*60)
    print(f"📊 Patients processed: {final_impact_df['patient_id'].nunique()}")
    print(f"📋 Total impact scores: {len(final_impact_df)}")
    print(f"⭐ Average final score: {final_impact_df['final_score'].mean():.2f}")
    print(f"🎯 Score distribution:")
    print(f"   High impact (≥7): {len(final_impact_df[final_impact_df['tier'] == 'high'])} ({len(final_impact_df[final_impact_df['tier'] == 'high'])/len(final_impact_df)*100:.1f}%)")
    print(f"   Medium impact (4-7): {len(final_impact_df[final_impact_df['tier'] == 'medium'])} ({len(final_impact_df[final_impact_df['tier'] == 'medium'])/len(final_impact_df)*100:.1f}%)")
    print(f"   Low impact (<4): {len(final_impact_df[final_impact_df['tier'] == 'low'])} ({len(final_impact_df[final_impact_df['tier'] == 'low'])/len(final_impact_df)*100:.1f}%)")
    
    # Show top recommendations across all patients
    print(f"\n🏆 Top 10 Recommendations (All Patients):")
    top_recs_overall = final_impact_df.nlargest(10, 'final_score')
    for i, (_, row) in enumerate(top_recs_overall.iterrows()):
        print(f"   {i+1}. {row['recommendation_title']} - Score: {row['final_score']} (Raw: {row['total_raw_points']:.4f})")
    
    print(f"\n🗂️ Files Created:")
    print(f"   • detailed_impact_scores_{scaling_method}.csv (ALL recommendations for ALL patients)")
    print(f"   • summary_impact_scores_{scaling_method}.csv (key metrics only)")
    print(f"   • statistical_patient_summary_{scaling_method}.csv (patient summaries)")
    
    return final_impact_df, patient_summary_df


def main():
    """Command line interface for the impact scorer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='WellPath Statistical Impact Scorer')
    parser.add_argument('--base-dir', type=str, help='Base directory containing data files')
    parser.add_argument('--recommendations-file', type=str, help='Path to recommendations JSON file')
    parser.add_argument('--markers-file', type=str, help='Path to markers CSV file')
    parser.add_argument('--comprehensive-file', type=str, help='Path to comprehensive CSV file')
    parser.add_argument('--output-dir', type=str, help='Output directory for results')
    parser.add_argument('--scaling-method', type=str, default='percentile', 
                      choices=['linear', 'percentile', 'log_normal', 'z_score'],
                      help='Scaling method for final scores')
    parser.add_argument('--patient-subset', type=str, nargs='+', 
                      help='Specific patient IDs to process (optional)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.base_dir and not all([args.recommendations_file, args.markers_file, 
                                     args.comprehensive_file, args.output_dir]):
        parser.error("Must provide either --base-dir OR all of --recommendations-file, "
                    "--markers-file, --comprehensive-file, and --output-dir")
    
    # Run the scoring
    impact_df, summary_df = run_statistical_impact_scoring(
        base_dir=args.base_dir,
        scaling_method=args.scaling_method,
        patient_subset=args.patient_subset,
        recommendations_file=args.recommendations_file,
        markers_file=args.markers_file,
        comprehensive_file=args.comprehensive_file,
        output_dir=args.output_dir
    )
    
    if impact_df is not None:
        print(f"✅ Impact scoring completed successfully!")
        print(f"📊 Processed {impact_df['patient_id'].nunique()} patients")
        print(f"📋 Generated {len(impact_df)} impact scores")
    else:
        print("❌ Impact scoring failed.")
        return 1
    
    return 0


if __name__ == "__main__":
    # Use parent directory as base (same as other scripts)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    methods_to_test = ['linear', 'percentile', 'log_normal', 'z_score']
    
    print("🎯 WellPath Statistical Impact Scorer")
    print("Running all scaling methods...")
    print()
    
    for method in methods_to_test:
        print(f"\n{'='*60}")
        print(f"🧪 Running {method.upper()} scaling method")
        print('='*60)
        
        impact_df, summary_df = run_statistical_impact_scoring(base_dir, method)
        
        if impact_df is not None:
            print(f"✅ {method.upper()} scaling completed successfully!")
        else:
            print(f"❌ {method.upper()} scaling failed.")
    
    print(f"\n🎉 All scaling methods completed!")




