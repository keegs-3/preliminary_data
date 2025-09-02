// Final JSON Updater Script with Complete Mapping
// This script updates the recommendations_list.json with new marker/metric categorizations from CSV

import Papa from 'papaparse';

async function updateRecommendationsWithCSVData() {
    try {
        // Step 1: Read the JSON file
        const jsonData = await window.fs.readFile('recommendations_list.json', { encoding: 'utf8' });
        const recommendations = JSON.parse(jsonData);
        
        // Step 2: Read the CSV file
        const csvData = await window.fs.readFile('WellPath Tiered Markers.csv', { encoding: 'utf8' });
        const parsedCsv = Papa.parse(csvData, {
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true,
            delimitersToGuess: [',', '\t', '|', ';']
        });
        
        console.log(`Found ${recommendations.recommendations.length} recommendations in JSON`);
        console.log(`Found ${parsedCsv.data.length} records in CSV`);
        
        // Step 3: Complete marker name mapping from CSV to JSON format
        const csvToJsonMapping = {
            // Blood lipids and cardiovascular
            'Total Cholesterol': 'total_cholesterol',
            'LDL': 'ldl',
            'HDL': 'hdl',
            'Lp(a)': 'lp_a',
            'Triglycerides': 'triglycerides',
            'ApoB': 'apob',
            'Omega-3 Index': 'omega_3_index',
            
            // Blood chemistry and markers
            'RDW': 'rdw',
            'Magnesium (RBC)': 'magnesium_rbc',
            'Vitamin D': 'vitamin_d',
            'Serum Ferritin': 'serum_ferritin',
            'Total Iron Binding Capacity (TIBC)': 'tibc',
            'Transferrin Saturation': 'transferrin_saturation',
            'hsCRP': 'hscrp',
            
            // Blood cell counts
            'White Blood Cell Count': 'white_blood_cell_count',
            'Neutrophils': 'neutrophils',
            'Lymphocytes': 'lymphocytes',
            'Neutrocyte/Lymphocyte Ratio': 'neutrocyte_lymphocyte_ratio',
            'Eosinophils': 'eosinophils',
            'Red Blood Cell Count': 'red_blood_cell_count',
            'Platelet Count': 'platelet_count',
            
            // Glucose and insulin
            'HbA1c': 'hba1c',
            'Fasting Glucose': 'fasting_glucose',
            'Fasting Insulin': 'fasting_insulin',
            'HOMA-IR': 'homa_ir',
            
            // Liver function
            'ALT': 'alt',
            'GGT': 'ggt',
            'AST': 'ast',
            'ALP': 'alp',
            'Albumin': 'albumin',
            
            // Hormones
            'Testosterone': 'testosterone',
            'Free Testosterone': 'free_testosterone',
            'Cortisol': 'cortisol',
            'Estradiol': 'estradiol',
            'Progesterone': 'progesterone',
            'TSH': 'tsh',
            'DHEA-S': 'dhea_s',
            'SHBG': 'shbg',
            
            // Other blood chemistry
            'Uric Acid': 'uric_acid',
            'Hemoglobin': 'hemoglobin',
            'Hematocrit': 'hematocrit',
            'Vitamin B12': 'vitamin_b12',
            'Folate Serum': 'folate_serum',
            'Folate (RBC)': 'folate_rbc',
            'Homocysteine': 'homocysteine',
            'Creatine Kinase': 'creatine_kinase',
            'Sodium': 'sodium',
            'Potassium': 'potassium',
            'Ferritin': 'ferritin',
            'Mean Corpuscular Hemoglobin (MCH)': 'mch',
            'Mean Corpuscular Hemoglobin Concentration (MCHC)': 'mchc',
            
            // Kidney function
            'eGFR': 'egfr',
            'Cystatin C': 'cystatin_c',
            'BUN': 'bun',
            'Creatinine': 'creatinine',
            
            // Minerals
            'Calcium (Serum)': 'calcium_serum',
            'Calcium (Ionized)': 'calcium_ionized',
            
            // Physical metrics
            'VO2 Max': 'vo2_max',
            '% Bodyfat': 'bodyfat',
            'Skeletal Muscle Mass to Fat-Free Mass': 'skeletal_muscle_mass_to_fat_free_mass',
            'Hip-to-Waist Ratio': 'hip_to_waist_ratio',
            'BMI': 'bmi',
            'Resting Heart Rate': 'resting_heart_rate',
            'Blood Pressure - Systolic': 'blood_pressure_systolic',
            'Blood Pressure - Diastolic': 'blood_pressure_diastolic',
            'Visceral Fat': 'visceral_fat',
            'Grip Strength': 'grip_strength',
            'HRV': 'hrv',
            
            // Sleep metrics
            'REM Sleep': 'rem_sleep',
            'Deep Sleep': 'deep_sleep',
            'Total Sleep': 'total_sleep',
            
            // Activity metrics
            'Steps/Day': 'steps_day'
        };
        
        // Step 4: Create a mapping object for CSV data by ID
        const csvMapping = {};
        parsedCsv.data.forEach(row => {
            if (row.ID) {
                csvMapping[row.ID] = {
                    primaryMarkers: parseAndConvertMarkers(row["Primary Markers"], csvToJsonMapping),
                    secondaryMarkers: parseAndConvertMarkers(row["Secondary Markers"], csvToJsonMapping),
                    tertiaryMarkers: parseAndConvertMarkers(row["Tertiary Markers"], csvToJsonMapping),
                    primaryMetrics: parseAndConvertMarkers(row["Primary Metrics"], csvToJsonMapping),
                    secondaryMetrics: parseAndConvertMarkers(row["Secondary Metrics"], csvToJsonMapping),
                    tertiaryMetrics: parseAndConvertMarkers(row["Tertiary Metrics"], csvToJsonMapping)
                };
            }
        });
        
        // Step 5: Update recommendations with CSV data
        let updatedCount = 0;
        let notFoundCount = 0;
        
        recommendations.recommendations.forEach(rec => {
            if (csvMapping[rec.id]) {
                const csvData = csvMapping[rec.id];
                
                // Update with CSV data
                rec.primary_markers = csvData.primaryMarkers;
                rec.secondary_markers = csvData.secondaryMarkers;
                rec.tertiary_markers = csvData.tertiaryMarkers;
                rec.primary_metrics = csvData.primaryMetrics;
                rec.secondary_metrics = csvData.secondaryMetrics;
                rec.tertiary_metrics = csvData.tertiaryMetrics;
                
                updatedCount++;
            } else {
                notFoundCount++;
                console.log(`Warning: No CSV data found for recommendation ID: ${rec.id}`);
            }
        });
        
        console.log(`✅ Updated ${updatedCount} recommendations`);
        console.log(`⚠️  ${notFoundCount} recommendations had no matching CSV data`);
        
        // Step 6: Generate updated JSON
        const updatedJsonString = JSON.stringify(recommendations, null, 2);
        
        console.log("\n📊 Sample of updated recommendation:");
        const sampleRec = recommendations.recommendations.find(r => 
            r.primary_markers.length > 0 || r.primary_metrics.length > 0
        );
        if (sampleRec) {
            console.log(`ID: ${sampleRec.id}`);
            console.log(`Title: ${sampleRec.title}`);
            console.log(`Primary Markers: [${sampleRec.primary_markers.join(', ')}]`);
            console.log(`Primary Metrics: [${sampleRec.primary_metrics.join(', ')}]`);
        }
        
        return updatedJsonString;
        
    } catch (error) {
        console.error("❌ Error updating recommendations:", error);
        return null;
    }
}

// Helper function to parse CSV marker strings and convert to JSON format
function parseAndConvertMarkers(markerString, csvToJsonMapping) {
    if (!markerString || markerString.trim() === '') {
        return [];
    }
    
    // Split by comma and clean up whitespace
    const csvMarkers = markerString.split(',')
        .map(marker => marker.trim())
        .filter(marker => marker !== '');
    
    // Convert CSV names to JSON format
    const jsonMarkers = csvMarkers.map(csvMarker => {
        if (csvToJsonMapping[csvMarker]) {
            return csvToJsonMapping[csvMarker];
        } else {
            console.log(`Warning: No mapping found for CSV marker: "${csvMarker}"`);
            // Fallback: convert to snake_case
            return csvMarker.toLowerCase()
                .replace(/\s+/g, '_')
                .replace(/[^\w_]/g, '')
                .replace(/_+/g, '_')
                .replace(/^_|_$/g, '');
        }
    });
    
    return jsonMarkers;
}

// Main execution function
async function runUpdate() {
    console.log("🚀 Starting recommendation update process...");
    console.log("Reading files and updating recommendations...\n");
    
    const updatedJson = await updateRecommendationsWithCSVData();
    
    if (updatedJson) {
        console.log("\n✅ Update completed successfully!");
        console.log("The updated JSON is ready.");
        
        // You can save the file or return it for further processing
        // To save: await window.fs.writeFile('updated_recommendations.json', updatedJson);
        
        return updatedJson;
    } else {
        console.log("\n❌ Update failed. Check the error messages above.");
        return null;
    }
}

// Run the update (uncomment to execute)
// runUpdate();

console.log("Script loaded. Call runUpdate() to execute the update process.");
