-- Step 1: Standalone Tables
CREATE TABLE IF NOT EXISTS vehicle_details (
    vehicle_no VARCHAR(255) PRIMARY KEY,
    vehicle_capacity VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS supplier_details (
    supplier_id VARCHAR(255) PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_details (
    customer_id VARCHAR(255) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS employee_details (
    emp_id VARCHAR(255) PRIMARY KEY,
    emp_name VARCHAR(255) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    email_address VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    joined_date DATE NOT NULL
);

-- Step 2: Tables based on first set
CREATE TABLE IF NOT EXISTS product_details (
    product_id VARCHAR(255) PRIMARY KEY,
    supplier_id VARCHAR(255) REFERENCES supplier_details(supplier_id) ON DELETE SET NULL,
    delivery_note_id VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    system_qty INT NOT NULL,
    product_cost DECIMAL(12, 2) NOT NULL,
    product_price DECIMAL(12, 2) NOT NULL,
    product_carton_volume_cbm DECIMAL(12, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS inbound_log (
    inbound_log_id SERIAL PRIMARY KEY,
    inbound_date DATE NOT NULL,
    supplier_id VARCHAR(255) REFERENCES supplier_details(supplier_id) ON DELETE SET NULL,
    delivery_note_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) REFERENCES product_details(product_id) ON DELETE CASCADE,
    received_qty INT NOT NULL,
    rejected_qty INT NOT NULL,
    inbound_status VARCHAR(50) NOT NULL,
    rejected_reason VARCHAR(255),
    unloading_started_time TIME NOT NULL,
    unloading_completed_time TIME NOT NULL,
    inbound_putaway_completed_time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS outbound_log (
    outbound_log_id SERIAL PRIMARY KEY,
    outbound_date DATE NOT NULL,
    order_id VARCHAR(255) UNIQUE NOT NULL,
    customer_id VARCHAR(255) REFERENCES customer_details(customer_id) ON DELETE SET NULL,
    product_id VARCHAR(255) REFERENCES product_details(product_id) ON DELETE CASCADE,
    ordered_qty INT NOT NULL,
    picked_qty INT NOT NULL,
    pick_sheet_issued_time TIME NOT NULL,
    pick_completed_time TIME NOT NULL,
    vehicle_no VARCHAR(255) REFERENCES vehicle_details(vehicle_no) ON DELETE SET NULL,
    loading_completed_time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS return_handling_log (
    return_handling_log_id SERIAL PRIMARY KEY,
    return_date DATE NOT NULL,
    customer_id VARCHAR(255) REFERENCES customer_details(customer_id) ON DELETE SET NULL,
    order_id VARCHAR(255) REFERENCES outbound_log(order_id) ON DELETE CASCADE,
    product_id VARCHAR(255) REFERENCES product_details(product_id) ON DELETE CASCADE,
    returned_qty INT NOT NULL,
    return_reason VARCHAR(255) NOT NULL,
    return_unloading_started_time TIME NOT NULL,
    return_putaway_completed_time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS vehicle_ncr_log (
    ncr_id VARCHAR(255) PRIMARY KEY,
    ncr_raised_date DATE NOT NULL,
    vehicle_no VARCHAR(255) REFERENCES vehicle_details(vehicle_no) ON DELETE SET NULL,
    ncr_reason VARCHAR(255) NOT NULL,
    ncr_status VARCHAR(50) NOT NULL,
    ca_completed_date DATE
);

CREATE TABLE IF NOT EXISTS vehicle_hygiene_inspection_log (
    inspection_log_id SERIAL PRIMARY KEY,
    inspection_date DATE NOT NULL,
    vehicle_no VARCHAR(255) REFERENCES vehicle_details(vehicle_no) ON DELETE SET NULL,
    good_truckbox VARCHAR(50) NOT NULL,
    good_truckfloor VARCHAR(50) NOT NULL,
    good_truckdoor VARCHAR(50) NOT NULL,
    good_curtain VARCHAR(50) NOT NULL,
    good_cooling_unit VARCHAR(50) NOT NULL,
    pest_check VARCHAR(50) NOT NULL,
    odor_check VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS inbound_inspection_log (
    inbound_inspection_id SERIAL PRIMARY KEY,
    inbound_date DATE NOT NULL,
    delivery_note_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    received_qty INT NOT NULL,
    rejected_qty INT NOT NULL,
    rejected_reason VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS complaint_handling_log (
    complaint_id VARCHAR(255) PRIMARY KEY,
    complaint_date DATE NOT NULL,
    customer_id VARCHAR(255) REFERENCES customer_details(customer_id) ON DELETE SET NULL,
    product_id VARCHAR(255) REFERENCES product_details(product_id) ON DELETE CASCADE,
    complaint_qty INT NOT NULL,
    complaint_category VARCHAR(255) NOT NULL,
    complaint_status VARCHAR(50) NOT NULL,
    resolution_completed_date DATE
);

-- Step 3: Remaining tables
CREATE TABLE IF NOT EXISTS cycle_count_log (
    cycle_count_id SERIAL PRIMARY KEY,
    count_date DATE NOT NULL,
    product_id VARCHAR(255) REFERENCES product_details(product_id) ON DELETE CASCADE,
    system_qty INT NOT NULL,
    counted_qty INT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_disposal_log (
    disposal_id SERIAL PRIMARY KEY,
    disposal_date DATE NOT NULL,
    product_id VARCHAR(255) REFERENCES product_details(product_id) ON DELETE CASCADE,
    disposal_reason VARCHAR(255) NOT NULL,
    disposal_qty INT NOT NULL,
    qcm_approval VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouse_temperature_monitoring_log (
    monitoring_id SERIAL PRIMARY KEY,
    monitoring_date DATE NOT NULL,
    location_code VARCHAR(100) NOT NULL,
    inspection_time VARCHAR(50) NOT NULL,
    temperature INT NOT NULL
);

-- Step 4: New Table 16 – Warehouse Incident Reporting Log
CREATE TABLE IF NOT EXISTS warehouse_incident_reporting_log (
    reporting_id VARCHAR(255) PRIMARY KEY,
    reporting_date DATE NOT NULL,
    operation_shift VARCHAR(50) NOT NULL,
    no_of_incidents VARCHAR(10) NOT NULL
);

-- Step 5: Indexes
CREATE INDEX idx_inbound_supplier ON inbound_log (supplier_id);
CREATE INDEX idx_inbound_product ON inbound_log (product_id);
CREATE INDEX idx_outbound_customer ON outbound_log (customer_id);
CREATE INDEX idx_outbound_product ON outbound_log (product_id);
CREATE INDEX idx_outbound_vehicle ON outbound_log (vehicle_no);
CREATE INDEX idx_return_customer ON return_handling_log (customer_id);
CREATE INDEX idx_return_order ON return_handling_log (order_id);
CREATE INDEX idx_return_product ON return_handling_log (product_id);
CREATE INDEX idx_ncr_vehicle ON vehicle_ncr_log (vehicle_no);
CREATE INDEX idx_hygiene_vehicle ON vehicle_hygiene_inspection_log (vehicle_no);
CREATE INDEX idx_inspection_delivery ON inbound_inspection_log (delivery_note_id);
CREATE INDEX idx_inspection_product ON inbound_inspection_log (product_id);
CREATE INDEX idx_complaint_customer ON complaint_handling_log (customer_id);
CREATE INDEX idx_complaint_product ON complaint_handling_log (product_id);
CREATE INDEX idx_cycle_product ON cycle_count_log (product_id);
CREATE INDEX idx_disposal_product ON product_disposal_log (product_id);
