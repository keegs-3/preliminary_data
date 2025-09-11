# Troubleshooting Guide

Common issues and solutions for the WellPath scoring system.

## 🚨 Common Processing Errors

### 1. Missing Data Files
**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'data/synthetic_patient_survey.csv'`

**Solutions**:
- Run data generation scripts first: `python scripts/generate_survey_dataset_v2.py`
- Check file paths in `config/paths.py`
- Verify data directory structure

### 2. CSV Format Issues  
**Error**: `ParserError: Error tokenizing data. C error: Expected X fields, got Y`

**Solutions**:
- Check CSV encoding (should be UTF-8)
- Verify column headers match expected format
- Remove extra commas or quotes in data
- Use `pd.read_csv()` with appropriate parameters

### 3. Memory Issues with Large Datasets
**Error**: `MemoryError: Unable to allocate array`

**Solutions**:
- Process data in chunks using `chunksize` parameter
- Use `dtype` optimization for numeric columns
- Filter unnecessary columns early in processing
- Consider using Dask for very large datasets

## 🔄 Score Calculation Problems

### 1. Invalid Score Ranges
**Issue**: Scores outside 0-100 range

**Causes & Solutions**:
- **Custom logic errors**: Check scoring function implementations
- **Missing normalization**: Ensure scores are scaled properly (`score = min(max(score, 0), 100)`)
- **Pillar weight errors**: Verify weights sum correctly

### 2. Missing Pillar Scores
**Issue**: Some pillars showing 0 or null scores

**Debugging Steps**:
1. Check if source data exists for that pillar
2. Verify pillar weight mappings in survey/biomarker configs  
3. Look for calculation errors in custom logic functions
4. Review audit trail files for score derivation

### 3. Inconsistent Results
**Issue**: Same input producing different outputs

**Check**:
- Random seed settings for reproducibility
- File timestamps and data versioning
- Configuration file changes
- Caching issues (clear temp files)

## 🧮 Algorithm Configuration Issues

### 1. Config Generation Failures
**Error**: `KeyError: 'metric_types_v3'` or similar

**Solutions**:
- Verify CSV reference files exist in `src/ref_csv_files_airtable/`
- Check CSV file headers match expected format
- Update file paths if CSV location changed
- Validate JSON structure in reference files

### 2. Algorithm Selection Mistakes  
**Issue**: Wrong algorithm type selected for recommendation

**Debugging**:
```python
from src.recommendation_config_generator import RecommendationConfigGenerator
generator = RecommendationConfigGenerator()
analysis = generator.analyze_recommendation("Your recommendation text")
print(f"Algorithm: {analysis.algorithm_type}, Confidence: {analysis.confidence}")
```

**Solutions**:
- Add specific keywords to priority patterns
- Adjust keyword weighting in analysis logic
- Manually specify algorithm type for edge cases

### 3. Missing Metrics or Units
**Issue**: Algorithm config shows generic metrics instead of specific ones

**Check**:
- Metric exists in `metric_types_v3.csv` 
- Unit compatibility between metric and recommendation
- Spelling and naming consistency
- Add custom metric/unit mappings if needed

## 📊 Data Quality Issues

### 1. Unrealistic Biomarker Values
**Issue**: Extreme or impossible lab values

**Solutions**:
- Implement value range validation
- Add outlier detection logic
- Use median imputation for extreme values
- Flag suspicious values for manual review

### 2. Survey Response Inconsistencies
**Issue**: Conflicting survey answers

**Detection**:
- Cross-question validation rules
- Logical consistency checks
- Flag patterns indicating survey fatigue
- Implement skip logic validation

### 3. Missing Survey Responses
**Issue**: Incomplete survey data affecting scores

**Handling Strategies**:
- Use question-specific default values
- Implement smart imputation based on similar questions
- Adjust pillar weights for missing components
- Flag incomplete profiles for follow-up

## 🔧 Performance Optimization

### 1. Slow Processing
**Symptoms**: Long runtime for scoring operations

**Optimization Strategies**:
- **Vectorize calculations**: Use NumPy/Pandas operations instead of loops
- **Parallel processing**: Use multiprocessing for independent patient calculations  
- **Database indexing**: Add indexes on frequently queried columns
- **Caching**: Store intermediate calculations

### 2. Memory Usage
**Issue**: High RAM consumption

**Solutions**:
```python
# Process in chunks
chunk_size = 1000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)

# Optimize data types
df['age'] = df['age'].astype('uint8')  # Instead of int64
df['score'] = df['score'].astype('float32')  # Instead of float64
```

### 3. Disk Space Issues
**Issue**: Output files consuming too much storage

**Management**:
- Implement automatic file cleanup for temporary files
- Compress output files: `df.to_csv('file.csv.gz', compression='gzip')`
- Archive old results periodically
- Use database storage for frequent queries

## 🔍 Debugging Workflows

### 1. Score Audit Trail
To trace how a score was calculated:

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check individual patient breakdown
patient_breakdown = generate_patient_breakdown('patient_id')
print(patient_breakdown['audit_trail'])
```

### 2. Configuration Validation
```python
# Validate algorithm config
from src.validation.validator import validate_config
validation_result = validate_config('path/to/config.json')
if not validation_result.is_valid:
    print(validation_result.errors)
```

### 3. Data Pipeline Testing
```python  
# Test end-to-end pipeline with small dataset
test_data = generate_test_patients(n=10)
results = run_complete_pipeline(test_data)
validate_results(results)
```

## 📋 Environment Issues

### 1. Python Dependencies
**Issue**: Package compatibility or missing dependencies

**Solutions**:
```bash
# Create fresh environment
python -m venv wellpath_env
source wellpath_env/bin/activate  # Linux/Mac
# or wellpath_env\Scripts\activate  # Windows

# Install exact versions
pip install -r requirements.txt

# Check for conflicts
pip check
```

### 2. Path Configuration
**Issue**: Scripts can't find files after restructuring

**Solutions**:
- Update `config/paths.py` with correct directories
- Use absolute paths in scripts
- Set PYTHONPATH environment variable
- Install package in development mode: `pip install -e .`

### 3. Database Connectivity
**Issue**: Connection failures to external databases

**Check**:
- Database credentials and connection strings
- Network connectivity and firewall settings
- Database server status and availability
- SSL certificate issues

## 🎯 Best Practices for Prevention

### 1. Data Validation
```python
def validate_patient_data(data):
    assert 'patient_id' in data, "Missing patient ID"
    assert data['age'] > 0 and data['age'] < 120, "Invalid age"
    assert data['gender'] in ['male', 'female'], "Invalid gender"
    # ... more validations
```

### 2. Configuration Management
- Use version control for all config files
- Document configuration changes
- Test config changes on subset before full deployment
- Maintain rollback procedures

### 3. Monitoring and Alerting
```python
# Add monitoring to scoring pipeline
def monitor_scores(scores):
    avg_score = np.mean(scores)
    if avg_score < 30 or avg_score > 90:
        send_alert(f"Unusual average score: {avg_score}")
    
    if len(scores) == 0:
        send_alert("No scores generated - check input data")
```

## 📞 Getting Additional Help

### 1. Log Analysis
Check these log files for detailed error information:
- `logs/scoring_pipeline.log`  
- `logs/config_generation.log`
- `logs/data_validation.log`

### 2. Debug Mode
Enable verbose debugging:
```python
import os
os.environ['WELLPATH_DEBUG'] = 'true'
```

### 3. Configuration Dump
Export current configuration for analysis:
```bash
python scripts/export_config.py --output debug_config.json
```

---

**Most issues can be resolved by checking data quality, verifying file paths, and reviewing configuration settings. When in doubt, start with small test datasets to isolate the problem.**