-- =====================================================
-- WellPath Unit Conversion Database Schema Updates
-- =====================================================
-- This file contains all database schema changes needed to support
-- flexible unit input and standardized storage.

-- =====================================================
-- 1. User Unit Preferences Table
-- =====================================================
-- Stores user's preferred units for different metric types

CREATE TABLE IF NOT EXISTS user_unit_preferences (
    user_id VARCHAR(50) NOT NULL,
    unit_type VARCHAR(50) NOT NULL,  -- 'volume', 'mass', 'length', 'temperature', etc.
    preferred_unit VARCHAR(50) NOT NULL,  -- 'cup', 'pound', 'feet_inches', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_type),
    INDEX idx_user_preferences (user_id),
    INDEX idx_unit_type (unit_type)
);

-- Default preferences for common unit types
INSERT IGNORE INTO user_unit_preferences (user_id, unit_type, preferred_unit) VALUES
-- System defaults (can be overridden per user)
('default', 'volume', 'cup'),
('default', 'mass', 'pound'), 
('default', 'length', 'feet_inches'),
('default', 'temperature', 'fahrenheit'),
('default', 'time', 'minute'),
('default', 'energy', 'calorie');

-- =====================================================
-- 2. Update Metric Entries Table
-- =====================================================
-- Add columns to store original input alongside converted values

-- Check if columns already exist before adding them
SET @sql = IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
              WHERE table_name = 'metric_entries' AND column_name = 'original_value') = 0,
              'ALTER TABLE metric_entries ADD COLUMN original_value DECIMAL(10,6) NULL AFTER value',
              'SELECT "original_value column already exists"');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
              WHERE table_name = 'metric_entries' AND column_name = 'original_unit') = 0,
              'ALTER TABLE metric_entries ADD COLUMN original_unit VARCHAR(50) NULL AFTER original_value',
              'SELECT "original_unit column already exists"');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
              WHERE table_name = 'metric_entries' AND column_name = 'base_unit') = 0,
              'ALTER TABLE metric_entries ADD COLUMN base_unit VARCHAR(50) NULL AFTER original_unit',
              'SELECT "base_unit column already exists"');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
              WHERE table_name = 'metric_entries' AND column_name = 'conversion_method') = 0,
              'ALTER TABLE metric_entries ADD COLUMN conversion_method VARCHAR(50) DEFAULT "linear" AFTER base_unit',
              'SELECT "conversion_method column already exists"');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_original_unit ON metric_entries(original_unit);
CREATE INDEX IF NOT EXISTS idx_base_unit ON metric_entries(base_unit);
CREATE INDEX IF NOT EXISTS idx_conversion_method ON metric_entries(conversion_method);

-- =====================================================
-- 3. Unit Standardization Reference Table
-- =====================================================
-- Cache the CSV data in database for faster lookups

CREATE TABLE IF NOT EXISTS unit_standards (
    unit_identifier VARCHAR(50) PRIMARY KEY,
    display_name VARCHAR(100) NOT NULL,
    symbol VARCHAR(20),
    unit_type VARCHAR(50) NOT NULL,
    conversion_factor DECIMAL(15,6) NULL,
    is_base_unit BOOLEAN DEFAULT FALSE,
    healthkit_equivalent TEXT,
    base_unit VARCHAR(50),
    special_conversion VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_unit_type (unit_type),
    INDEX idx_base_unit_flag (is_base_unit),
    INDEX idx_base_unit_ref (base_unit)
);

-- Populate from CSV data (this would be done via Python script)
-- INSERT INTO unit_standards VALUES ... (populated by migration script)

-- =====================================================
-- 4. Recommendation Config Updates View
-- =====================================================
-- Create view to show configs with unit information

CREATE OR REPLACE VIEW recommendation_configs_with_units AS
SELECT 
    rc.*,
    us_threshold.display_name as threshold_unit_display,
    us_threshold.symbol as threshold_unit_symbol,
    us_base.display_name as base_unit_display,
    us_base.symbol as base_unit_symbol
FROM recommendation_configs rc
LEFT JOIN unit_standards us_threshold ON rc.unit = us_threshold.unit_identifier
LEFT JOIN unit_standards us_base ON us_threshold.base_unit = us_base.unit_identifier;

-- =====================================================
-- 5. Conversion Audit Log Table
-- =====================================================
-- Track conversion operations for debugging and validation

CREATE TABLE IF NOT EXISTS conversion_audit_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50),
    metric_id VARCHAR(50),
    original_value DECIMAL(15,6),
    original_unit VARCHAR(50),
    converted_value DECIMAL(15,6),
    base_unit VARCHAR(50),
    conversion_method VARCHAR(50),
    conversion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100),
    INDEX idx_user_metric (user_id, metric_id),
    INDEX idx_conversion_timestamp (conversion_timestamp),
    INDEX idx_conversion_method (conversion_method)
);

-- =====================================================
-- 6. Update Existing Data Migration
-- =====================================================
-- Migrate existing metric entries to include unit information

-- For existing entries, assume they're already in base units
UPDATE metric_entries 
SET 
    original_value = value,
    original_unit = (
        SELECT base_unit 
        FROM unit_standards us 
        WHERE us.unit_type = (
            SELECT unit_type 
            FROM metric_types_v3 mt 
            WHERE mt.identifier = metric_entries.metric_id 
            LIMIT 1
        ) 
        AND us.is_base_unit = TRUE 
        LIMIT 1
    ),
    base_unit = (
        SELECT base_unit 
        FROM unit_standards us 
        WHERE us.unit_type = (
            SELECT unit_type 
            FROM metric_types_v3 mt 
            WHERE mt.identifier = metric_entries.metric_id 
            LIMIT 1
        ) 
        AND us.is_base_unit = TRUE 
        LIMIT 1
    ),
    conversion_method = 'none'
WHERE original_value IS NULL;

-- =====================================================
-- 7. Stored Procedures for Common Operations
-- =====================================================

DELIMITER //

-- Get user's preferred unit for a metric type
CREATE PROCEDURE GetUserPreferredUnit(
    IN p_user_id VARCHAR(50),
    IN p_unit_type VARCHAR(50),
    OUT p_preferred_unit VARCHAR(50)
)
BEGIN
    -- Try user-specific preference first
    SELECT preferred_unit INTO p_preferred_unit
    FROM user_unit_preferences 
    WHERE user_id = p_user_id AND unit_type = p_unit_type
    LIMIT 1;
    
    -- Fall back to default if no user preference
    IF p_preferred_unit IS NULL THEN
        SELECT preferred_unit INTO p_preferred_unit
        FROM user_unit_preferences 
        WHERE user_id = 'default' AND unit_type = p_unit_type
        LIMIT 1;
    END IF;
END //

-- Convert and store metric entry with full audit trail
CREATE PROCEDURE StoreMetricWithConversion(
    IN p_user_id VARCHAR(50),
    IN p_metric_id VARCHAR(50),
    IN p_original_value DECIMAL(15,6),
    IN p_original_unit VARCHAR(50),
    IN p_converted_value DECIMAL(15,6),
    IN p_base_unit VARCHAR(50),
    IN p_conversion_method VARCHAR(50),
    IN p_session_id VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Store the metric entry
    INSERT INTO metric_entries (
        user_id, metric_id, value, original_value, original_unit, 
        base_unit, conversion_method, created_at
    ) VALUES (
        p_user_id, p_metric_id, p_converted_value, p_original_value, 
        p_original_unit, p_base_unit, p_conversion_method, NOW()
    );
    
    -- Log the conversion for audit
    INSERT INTO conversion_audit_log (
        user_id, metric_id, original_value, original_unit, 
        converted_value, base_unit, conversion_method, session_id
    ) VALUES (
        p_user_id, p_metric_id, p_original_value, p_original_unit, 
        p_converted_value, p_base_unit, p_conversion_method, p_session_id
    );
    
    COMMIT;
END //

DELIMITER ;

-- =====================================================
-- 8. Performance Indexes
-- =====================================================

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_metrics_user_type_date 
ON metric_entries(user_id, metric_id, base_unit, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_preferences_lookup 
ON user_unit_preferences(user_id, unit_type, preferred_unit);

-- =====================================================
-- 9. Data Validation Constraints
-- =====================================================

-- Ensure conversion factors are positive for non-special conversions
ALTER TABLE unit_standards 
ADD CONSTRAINT chk_positive_conversion_factor 
CHECK (conversion_factor IS NULL OR conversion_factor > 0 OR special_conversion IS NOT NULL);

-- Ensure base units reference valid units
ALTER TABLE unit_standards 
ADD CONSTRAINT fk_base_unit_reference 
FOREIGN KEY (base_unit) REFERENCES unit_standards(unit_identifier);

-- =====================================================
-- Comments and Documentation
-- =====================================================

ALTER TABLE user_unit_preferences 
COMMENT = 'Stores user preferences for unit display and input across different metric types';

ALTER TABLE unit_standards 
COMMENT = 'Master table of supported units with conversion factors and metadata';

ALTER TABLE conversion_audit_log 
COMMENT = 'Audit trail of all unit conversions for debugging and validation';