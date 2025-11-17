CREATE TABLE patients (
    patient_hash SERIAL PRIMARY KEY,
    age INTEGER NOT NULL CHECK (age >= 0 AND age <= 120),
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Female', 'Male')),
    menopausal_status VARCHAR(20) CHECK (menopausal_status IN ('premenopausal', 'perimenopausal', 'postmenopausal')),
    family_history BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pathological_profiles (
    profile_id SERIAL PRIMARY KEY,
    patient_hash INTEGER NOT NULL REFERENCES patients(patient_hash),
    molecular_subtype VARCHAR(50) CHECK (molecular_subtype IN ('HR+HER2-', 'HR+HER2+', 'TNBC', 'Unknown')),
    er_status VARCHAR(10) CHECK (er_status IN ('TRUE', 'FALSE', 'Unknown')),
    pr_status VARCHAR(10) CHECK (pr_status IN ('TRUE', 'FALSE', 'Unknown')),
    her2_status VARCHAR(10) CHECK (her2_status IN ('TRUE', 'FALSE', 'Unknown')),
    brca_mutation VARCHAR(10) CHECK (brca_mutation IN ('TRUE', 'FALSE', 'Unknown')),
    ki67_level DECIMAL(5,2) CHECK (ki67_level >= 0 AND ki67_level <= 100),
    tumor_grade VARCHAR(5) CHECK (tumor_grade IN ('1', '2', '3', 'X', 'Unknown')),
    lymph_node_status VARCHAR(10) CHECK (lymph_node_status IN ('positive', 'negative', 'Unknown')),
    positive_lymph_nodes INTEGER CHECK (positive_lymph_nodes >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE treatments (
    treatment_id SERIAL PRIMARY KEY,
    patient_hash INTEGER NOT NULL REFERENCES patients(patient_hash),
    treatment_description TEXT,
    surgery_type VARCHAR(50) CHECK (surgery_type IN ('lumpectomy', 'mastectomy', 'None')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE tumor_measurements (
    measurement_id SERIAL PRIMARY KEY,
    patient_hash INTEGER NOT NULL REFERENCES patients(patient_hash),
    measurement_date DATE NOT NULL, -- Заменяет статичные столбцы на временную шкалу
    tumor_size DECIMAL(6,2) CHECK (tumor_size >= 0),
    measurement_period VARCHAR(10) CHECK (measurement_period IN ('Baseline', '3m', '6m', '12m', '24m', 'Other')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE metastases (
    metastasis_id SERIAL PRIMARY KEY,
    patient_hash INTEGER NOT NULL REFERENCES patients(patient_hash),
    has_metastasis VARCHAR(10) CHECK (has_metastasis IN ('TRUE', 'FALSE', 'Unknown')),
    metastasis_sites VARCHAR(200),
    diagnosis_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE performance_statuses (
    status_id SERIAL PRIMARY KEY,
    patient_hash INTEGER NOT NULL REFERENCES patients(patient_hash),
    performance_status VARCHAR(20) CHECK (performance_status IN ('0', '1', '2', '3', '4', 'Unknown')),
    assessment_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE model_results (
    result_id SERIAL PRIMARY KEY,
    patient_hash INTEGER NOT NULL REFERENCES patients(patient_hash),
    model_name VARCHAR(50) NOT NULL, -- Например, 'model_1', 'model_2'
    result_data VARCHAR(200) NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
