# Health Screening Compliance Rules

**Risk-stratified preventive care scheduling for optimal health outcomes**

| **Total Rules** | **Screening Types** | **Risk Levels** | **Age/Gender Targeting** |
|-----------------|---------------------|-----------------|--------------------------|
| **16 rules** | **8 screening types** | **4 risk levels** | **Age & gender specific** |

## Overview

Compliance rules define **personalized preventive care schedules** based on medical guidelines, individual risk factors, and demographic characteristics. The system automatically calculates compliance status for each user based on their screening history and risk profile.

## Quick Reference

### 🏥 **Screening Types** (8 types)
| Screening | Base Interval | Risk Variations | Gender Specific |
|-----------|---------------|-----------------|-----------------|
| **Dental** | 6 months | None | No |
| **Physical** | 12 months | None | No |
| **Skin Check** | 12 months | High risk: 6 months | No |
| **Vision** | 12 months | None | No |
| **Colonoscopy** | 10 years | High risk: 5 years | No |
| **Mammogram** | 12-24 months | Age & risk dependent | Female only |
| **Cervical (HPV/PAP)** | 3-5 years | Test type dependent | Female only |
| **PSA** | 36 months | High risk: 12 months | Male only |

### ⚡ **Risk Levels** (4 levels)
| Level | Interval Adjustment | Criteria |
|-------|-------------------|----------|
| **Average** | Standard intervals | Population baseline risk |
| **High** | 2x more frequent | Family history, genetic factors |
| **Very High** | 3x more frequent | Multiple risk factors |
| **Above Average** | 1.5x more frequent | Single risk factor |

---

## Complete Compliance Rules

### 🦷 Dental Screening (1 rule)
*Maps to: `dental_compliance_status` calculated metric*

| Rule ID | Risk | Age | Gender | Interval | Display Name |
|---------|------|-----|--------|----------|--------------|
| `dental_male_female_all_ages_average` | Average | All adults | All | **6 months** | Dental Exam in the Last 6 Months |

**Clinical Rationale:** Preventive dental care every 6 months prevents cavities, gum disease, and detects oral health issues early.

### 🩺 Physical Examination (1 rule)  
*Maps to: `physical_compliance_status` calculated metric*

| Rule ID | Risk | Age | Gender | Interval | Display Name |
|---------|------|-----|--------|----------|--------------|
| `physical_male_female_all_ages_average` | Average | All adults | All | **12 months** | Physical in the Last 12 Months |

**Clinical Rationale:** Annual comprehensive physical exams monitor overall health, vital signs, and screening for chronic diseases.

### 🔍 Skin Check Screening (2 rules)
*Maps to: `skin_check_compliance_status` calculated metric*

| Rule ID | Risk | Age | Gender | Interval | Display Name |
|---------|------|-----|--------|----------|--------------|
| `skin_check_male_female_all_ages_average` | Average | All adults | All | **12 months** | Skin Check in the Last 12 Months (avg risk) |
| `skin_check_male_female_all_ages_high` | High | All adults | All | **6 months** | Skin Check in the Last 6 Months (high risk) |

**Clinical Rationale:** Regular skin examinations detect melanoma and other skin cancers early. High-risk individuals (family history, fair skin, many moles) need more frequent screening.

### 👁️ Vision Check Screening (1 rule)
*Maps to: `vision_check_compliance_status` calculated metric*

| Rule ID | Risk | Age | Gender | Interval | Display Name |
|---------|------|-----|--------|----------|--------------|
| `vision_check_male_female_all_ages_average` | Average | All adults | All | **12 months** | Vision Check in the Last 12 Months |

**Clinical Rationale:** Annual eye exams detect vision changes, glaucoma, diabetic retinopathy, and other eye conditions.

### 🔬 Colonoscopy Screening (2 rules)
*Maps to: `colonoscopy_compliance_status` calculated metric*

| Rule ID | Risk | Age | Gender | Interval | Display Name |
|---------|------|-----|--------|----------|--------------|
| `colonoscopy_male_female_over_50_average` | Average | Over 50 | All | **120 months** | Colonoscopy in the Last 10 Years (avg risk) |
| `colonoscopy_male_female_over_50_high` | High | Over 50 | All | **60 months** | Colonoscopy in the Last 5 Years (high risk) |

**Clinical Rationale:** Colonoscopy screening prevents colorectal cancer. High-risk factors include family history, inflammatory bowel disease, or previous polyps.

### 🩷 Mammogram Screening (4 rules)
*Maps to: `mammogram_compliance_status` calculated metric*

| Rule ID | Risk | Age | Gender | Interval | Display Name |
|---------|------|-----|--------|----------|--------------|
| `mammogram_male_female_under_50_average` | Average | Under 50 | Female | **24 months** | Mammogram in the Last 24 Months (under 50) |
| `mammogram_male_female_over_50_average` | Average | Over 50 | Female | **12 months** | Mammogram in the Last 12 Months (over 50) |
| `mammogram_male_female_under_50_high` | High | Under 50 | Female | **12 months** | Mammogram in the Last 12 Months (high risk under 50) |
| `breast_mri_female_all_very_high` | Very High | All females | Female | **12 months** | Breast MRI in the Last 12 Months (very high risk) |

**Clinical Rationale:** Mammography frequency increases with age and risk factors. Very high-risk women (BRCA mutations) may need MRI screening.

### 🔬 Cervical Screening (2 rules)
*Maps to: `cervical_compliance_status` calculated metric*

| Rule ID | Risk | Age | Gender | Interval | Display Name |
|---------|------|-----|--------|----------|--------------|
| `cervical_hpv_female_21_to_65_average` | Average | 21-65 | Female | **60 months** | HPV Test in the Last 5 Years |
| `cervical_pap_female_21_to_65_average` | Average | 21-65 | Female | **36 months** | PAP Test in the Last 3 Years |

**Clinical Rationale:** HPV testing has longer intervals than PAP smears due to higher sensitivity. Co-testing may extend intervals further.

### 🔬 PSA Screening (2 rules)
*Maps to: `psa_compliance_status` calculated metric*

| Rule ID | Risk | Age | Gender | Interval | Display Name |
|---------|------|-----|--------|----------|--------------|
| `psa_male_50_to_70_average` | Average | 50-70 | Male | **36 months** | PSA Test in the Last 3 Years (avg risk) |
| `psa_male_45_to_70_high` | High | 45-70 | Male | **12 months** | PSA Test in the Last Year (high risk) |

**Clinical Rationale:** PSA screening for prostate cancer is controversial but recommended for men with life expectancy >10 years. High-risk men (African American, family history) start earlier.

---

## Risk Stratification Framework

### Age-Based Categories

| Age Category | Age Range | Clinical Significance |
|--------------|-----------|----------------------|
| `all_adults` | 18+ years | Universal adult recommendations |
| `under_50` | 18-49 years | Lower baseline cancer risk |
| `over_50` | 50+ years | Increased cancer screening |
| `21_to_65` | 21-65 years | Reproductive age screening |
| `45_to_70` | 45-70 years | Peak prostate cancer risk |
| `50_to_70` | 50-70 years | Standard prostate screening age |
| `all_females` | Female, all ages | Gender-specific screening |

### Risk Level Definitions

#### **Average Risk**
- No family history of relevant cancers
- No genetic predisposition
- No previous abnormal results
- **Follow standard guidelines**

#### **High Risk** 
- First-degree family history
- Previous abnormal results requiring follow-up
- Environmental risk factors
- **2x more frequent screening**

#### **Very High Risk**
- Genetic mutations (BRCA1/2, Lynch syndrome)
- Multiple first-degree relatives affected
- Previous cancer diagnosis
- **Specialized screening protocols**

---

## Calculated Metrics Integration

### Compliance Status Calculation

Each screening type generates a calculated metric:

```
compliance_status = {
  "compliant": last_screening_date within interval,
  "overdue": last_screening_date outside interval,
  "never": no screening recorded,
  "not_applicable": outside age/gender criteria
}
```

### Example Calculations

#### **Mammogram Compliance (Female, Age 45, High Risk)**
```
Applicable rule: mammogram_male_female_under_50_high
Required interval: 12 months
Last mammogram: 2023-06-15
Current date: 2024-01-15  
Months since: 7 months
Status: COMPLIANT (within 12-month interval)
```

#### **Colonoscopy Compliance (Male, Age 55, Average Risk)**
```
Applicable rule: colonoscopy_male_female_over_50_average  
Required interval: 120 months (10 years)
Last colonoscopy: 2015-03-20
Current date: 2024-01-15
Months since: 106 months
Status: COMPLIANT (within 120-month interval)
```

---

## Implementation Notes

### **Algorithm Integration**

Compliance rules integrate with scoring algorithms to:
- Weight preventive care in composite health scores
- Generate adherence metrics for screening compliance
- Trigger notifications for overdue screenings
- Provide risk-adjusted scoring

### **Clinical Evidence Base**

Rules follow established guidelines from:
- **US Preventive Services Task Force (USPSTF)**
- **American Cancer Society (ACS)** 
- **American Heart Association (AHA)**
- **Professional medical societies**

### **Personalization Logic**

The system automatically:
1. **Determines applicable rules** based on age, gender, risk factors
2. **Calculates compliance status** from screening dates
3. **Generates reminders** for overdue screenings  
4. **Adjusts intervals** based on results and risk changes

### **Risk Factor Integration**

Risk levels can be determined by:
- **Family history questionnaires**
- **Genetic testing results**
- **Previous screening outcomes**
- **Clinical risk calculators**
- **Lifestyle factor assessments**

---

## Usage Examples

### **Rule Matching Logic**
```json
{
  "user_profile": {
    "age": 52,
    "gender": "female", 
    "risk_factors": ["family_history_breast_cancer"]
  },
  "applicable_rules": [
    {
      "screening": "mammogram",
      "rule": "mammogram_male_female_over_50_average",
      "interval_months": 12,
      "reason": "age >= 50"
    }
  ]
}
```

### **Compliance Calculation**
```json
{
  "screening_type": "colonoscopy",
  "user_age": 58,
  "user_gender": "male",
  "risk_level": "high",
  "applicable_rule": "colonoscopy_male_female_over_50_high",
  "required_interval_months": 60,
  "last_screening_date": "2019-08-15",
  "current_date": "2024-01-15",
  "months_since_screening": 53,
  "compliance_status": "COMPLIANT",
  "next_due_date": "2024-08-15"
}
```

---

## Future Enhancements

### **Planned Improvements**
- **Dynamic risk assessment** based on biomarkers
- **Integration with wearable device data**  
- **Machine learning risk prediction**
- **Personalized screening intervals**
- **Genetic risk score integration**

### **Research Integration**
- **Emerging screening modalities** (liquid biopsies, AI imaging)
- **Updated clinical guidelines** incorporation
- **Population health outcome tracking**
- **Cost-effectiveness optimization**

---

**Next**: [Algorithm Reference](../../algorithms/) | [Getting Started Guide](../../overview/getting-started.md)