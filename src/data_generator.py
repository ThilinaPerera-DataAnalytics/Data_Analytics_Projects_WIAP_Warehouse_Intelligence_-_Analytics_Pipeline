import pandas as pd
import random
import os
import datetime
import ollama
from functools import lru_cache
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache LLM responses
@lru_cache(maxsize=1000)
def generate_with_ollama_cached(prompt, model="mistral", num_items=1):
    start_time = time.time()
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': 'Provide realistic names/data as a comma-separated list without extra text.'},
                {'role': 'user', 'content': f'{prompt}. Provide {num_items} items in a comma-separated list.'},
            ],
        )
        generated_text = response['message']['content'].strip()
        items = [item.strip() for item in generated_text.split(',') if item.strip()]
        elapsed = time.time() - start_time
        logger.info(f"LLM call for {prompt} returned {len(items)} items in {elapsed:.2f} seconds")
        if len(items) < num_items:
            logger.warning(f"LLM returned {len(items)} items, expected {num_items}. Using fallback.")
            items.extend([f"Fallback_{i}" for i in range(len(items), num_items)])
        return items
    except Exception as e:
        logger.error(f"LLM error for {prompt}: {e}")
        return [f"Fallback_{i}" for i in range(1, num_items + 1)]

# ------------------------------
# Table Generators
# ------------------------------

def generate_vehicle_details(num_rows=40):
    capacities = [{"capacity": "10 ton", "count": 20}, {"capacity": "12 ton", "count": 12}, {"capacity": "20 ton", "count": 8}]
    capacities_list = [cap["capacity"] for cap in capacities for _ in range(cap["count"])]
    vehicle_numbers = random.sample(range(100000, 999999), num_rows)
    data = [[str(v), c] for v, c in zip(vehicle_numbers, capacities_list)]
    return pd.DataFrame(data, columns=['vehicle_no', 'vehicle_capacity']).dropna()

def generate_supplier_details(num_rows=100):
    supplier_names = generate_with_ollama_cached("Realistic FMCG supplier names", num_items=num_rows)
    countries = generate_with_ollama_cached("20 different supplier countries", num_items=20)
    data = [[f"SUP{i:03d}", supplier_names[i], random.choice(countries)] for i in range(num_rows)]
    return pd.DataFrame(data, columns=['supplier_id', 'supplier_name', 'country']).dropna()

def generate_customer_details(num_rows=100):
    customer_names = generate_with_ollama_cached("Mixed names for supermarkets, hotels, etc.", num_items=num_rows)
    data = [[f"CUST{i:03d}", customer_names[i]] for i in range(num_rows)]
    return pd.DataFrame(data, columns=['customer_id', 'customer_name']).dropna()

def generate_employee_details(num_rows=65):
    employee_names = generate_with_ollama_cached("Realistic male/female names", num_items=num_rows)
    designations = [{"designation": "Manager", "count": 5}, {"designation": "WH labour - inbound", "count": 30}, {"designation": "WH labour - outbound", "count": 30}]
    designation_list = [desig["designation"] for desig in designations for _ in range(desig["count"])]
    random.shuffle(designation_list)
    data = []
    for i in range(num_rows):
        emp_id = f"emp{random.randint(100, 4000)}"
        emp_name = employee_names[i]
        designation = designation_list[i]
        email = f"{emp_name.replace(' ', '.').lower()}@logisticsone.com"
        dob = datetime.date(random.randint(1970, 1979), random.randint(1, 12), 1) if designation == "Manager" else datetime.date(random.randint(1985, 2000), random.randint(1, 12), 1)
        joined = datetime.date(random.randint(2000, 2010), random.randint(1, 12), 1) if designation == "Manager" else datetime.date(random.randint(1990, 2015), random.randint(1, 12), 1)
        data.append([emp_id, emp_name, designation, "", email, dob, joined])
    return pd.DataFrame(data, columns=['emp_id', 'emp_name', 'designation', 'department', 'email_address', 'date_of_birth', 'joined_date']).dropna(subset=['emp_id', 'emp_name', 'designation', 'email_address'])

def generate_product_details(supplier_df, num_rows=1000):
    start_time = time.time()
    supplier_ids = supplier_df['supplier_id'].tolist()
    product_names = [f"Product_{i}" for i in range(num_rows)]
    data = [[random.choice(supplier_ids), str(random.randint(100000, 999999)), str(random.randint(100000, 999999)),
             product_names[i], random.randint(20, 1000), round(random.uniform(5.0, 500.0), 2),
             round(random.uniform(5.0, 500.0) * 1.3, 2), round(random.uniform(0.05, 1.50), 2)]
            for i in range(num_rows)]
    elapsed = time.time() - start_time
    logger.info(f"Product details generation took {elapsed:.2f} seconds")
    return pd.DataFrame(data, columns=['supplier_id', 'delivery_note_id', 'product_id', 'product_name',
                                      'system_qty', 'product_cost', 'product_price', 'product_carton_volume_cbm']).dropna()

def generate_inbound_log(supplier_df, product_df, num_rows=25000):
    supplier_ids = supplier_df['supplier_id'].unique().tolist()
    product_details_tuples = list(zip(product_df['delivery_note_id'], product_df['product_id']))
    inbound_statuses = ['Accepted'] * 22500 + ['Rejected'] * 2000 + ['On-hold'] * 500
    random.shuffle(inbound_statuses)
    rejected_reasons = ["Quality Issue", "Regulatory issue"]
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    date_range = (end_date - start_date).days
    data = []
    for i in range(num_rows):
        inbound_date = start_date + datetime.timedelta(days=random.randint(0, date_range))
        unloading_start_dt = datetime.datetime.combine(inbound_date, datetime.time(random.randint(9, 14), random.randint(0, 59)))
        supplier_id = random.choice(supplier_ids)
        delivery_note_id, product_id = random.choice(product_details_tuples)
        received_qty = random.randint(100, 2500)
        inbound_status = inbound_statuses[i]
        rejected_qty = round(received_qty * random.uniform(0.0, 0.05)) if inbound_status in ["Rejected", "On-hold"] else 0
        rejected_reason = random.choice(rejected_reasons) if inbound_status in ["Rejected", "On-hold"] else None
        unloading_completed_dt = unloading_start_dt + datetime.timedelta(minutes=random.randint(60, 180))
        inbound_putaway_completed_dt = unloading_completed_dt + datetime.timedelta(minutes=random.randint(10, 45))
        data.append([inbound_date, supplier_id, delivery_note_id, product_id, received_qty, rejected_qty, inbound_status, rejected_reason,
                     unloading_start_dt.time(), unloading_completed_dt.time(), inbound_putaway_completed_dt.time()])
    return pd.DataFrame(data, columns=['inbound_date', 'supplier_id', 'delivery_note_id', 'product_id', 'received_qty',
                                      'rejected_qty', 'inbound_status', 'rejected_reason', 'unloading_started_time',
                                      'unloading_completed_time', 'inbound_putaway_completed_time']).dropna()

def generate_outbound_log(customer_df, product_df, vehicle_df, num_rows=25000):
    customer_ids = customer_df['customer_id'].tolist()
    product_ids = product_df['product_id'].tolist()
    vehicle_nos = vehicle_df['vehicle_no'].tolist()
    mismatch_indices = random.sample(range(num_rows), 750)
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    date_range = (end_date - start_date).days
    data = []
    for i in range(num_rows):
        outbound_date = start_date + datetime.timedelta(days=random.randint(0, date_range))
        order_id = f"ORD{i+1:05d}"
        ordered_qty = random.randint(11, 1000)
        picked_qty = random.randint(1, ordered_qty - 1) if i in mismatch_indices else ordered_qty
        pick_sheet_issued_dt = datetime.datetime.combine(outbound_date, datetime.time(random.randint(21, 23), random.randint(0, 59)))
        if pick_sheet_issued_dt.hour >= 0 and pick_sheet_issued_dt.hour <= 3:
            outbound_date_adjusted = outbound_date + datetime.timedelta(days=1)
            pick_sheet_issued_dt = datetime.datetime.combine(outbound_date_adjusted, pick_sheet_issued_dt.time())
        else:
            outbound_date_adjusted = outbound_date
        pick_completed_dt = pick_sheet_issued_dt + datetime.timedelta(minutes=random.randint(30, 90))
        loading_completed_dt = pick_completed_dt + datetime.timedelta(minutes=random.randint(20, 40))
        data.append([outbound_date_adjusted, order_id, random.choice(customer_ids), random.choice(product_ids),
                     ordered_qty, picked_qty, pick_sheet_issued_dt.time(), pick_completed_dt.time(),
                     random.choice(vehicle_nos), loading_completed_dt.time()])
    return pd.DataFrame(data, columns=['outbound_date', 'order_id', 'customer_id', 'product_id', 'ordered_qty',
                                      'picked_qty', 'pick_sheet_issued_time', 'pick_completed_time',
                                      'vehicle_no', 'loading_completed_time']).dropna()

def generate_return_handling_log(customer_df, product_df, outbound_log_df, num_rows=1000):
    customer_ids = customer_df['customer_id'].tolist()
    product_ids = product_df['product_id'].tolist()
    order_qty_lookup = dict(zip(outbound_log_df['order_id'], outbound_log_df['ordered_qty']))
    order_ids = list(order_qty_lookup.keys())
    return_reasons = ["Low shelf life", "Quality issue", "Incorrect item", "Temperature issue"]
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    date_range = (end_date - start_date).days
    data = []
    for i in range(num_rows):
        return_date = start_date + datetime.timedelta(days=random.randint(0, date_range))
        customer_id = random.choice(customer_ids)
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        ordered_qty = order_qty_lookup.get(order_id, 10)
        returned_qty = random.randint(1, ordered_qty)
        if returned_qty == ordered_qty and ordered_qty > 1:
            returned_qty = random.randint(1, ordered_qty - 1)
        elif ordered_qty == 1:
            returned_qty = 1
        return_reason = random.choice(return_reasons)
        unloading_start_dt = datetime.datetime.combine(return_date, datetime.time(random.randint(9, 14), random.randint(0, 59)))
        putaway_completed_dt = unloading_start_dt + datetime.timedelta(minutes=random.randint(20, 40))
        data.append([return_date, customer_id, order_id, product_id, returned_qty, return_reason,
                     unloading_start_dt.time(), putaway_completed_dt.time()])
    return pd.DataFrame(data, columns=['return_date', 'customer_id', 'order_id', 'product_id', 'returned_qty',
                                      'return_reason', 'return_unloading_started_time', 'return_putaway_completed_time']).dropna()

def generate_vehicle_ncr_log(vehicle_df, num_rows=200):
    vehicle_nos = vehicle_df['vehicle_no'].tolist()
    ncr_reasons = ["Defective truck box", "Defective truck floor", "Defective truck door", "Defective cooling unit", "Odor", "Pest"]
    ncr_statuses = ["CA completed"] * (num_rows // 2) + ["CA pending"] * (num_rows - (num_rows // 2))
    random.shuffle(ncr_statuses)
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    date_range = (end_date - start_date).days
    data = []
    for i in range(num_rows):
        ncr_raised_date = start_date + datetime.timedelta(days=random.randint(0, date_range))
        ncr_id = f"NCR{i+1:05d}"
        vehicle_no = random.choice(vehicle_nos)
        ncr_reason = random.choice(ncr_reasons)
        ncr_status = ncr_statuses[i]
        ca_completed_date = ncr_raised_date + datetime.timedelta(days=random.randint(3, 10)) if ncr_status == "CA completed" else None
        data.append([ncr_raised_date, ncr_id, vehicle_no, ncr_reason, ncr_status, ca_completed_date])
    return pd.DataFrame(data, columns=['ncr_raised_date', 'ncr_id', 'vehicle_no', 'ncr_reason', 'ncr_status', 'ca_completed_date']).dropna()

def generate_vehicle_hygiene_log(outbound_log_df):
    data = []
    yes_no_options = ["Yes"] * 98 + ["No"] * 2
    for index, row in outbound_log_df.iterrows():
        data.append([row['outbound_date'], row['vehicle_no'], random.choice(yes_no_options), random.choice(yes_no_options),
                     random.choice(yes_no_options), random.choice(yes_no_options), random.choice(yes_no_options),
                     random.choice(yes_no_options), random.choice(yes_no_options)])
    return pd.DataFrame(data, columns=['inspection_date', 'vehicle_no', 'good_truckbox', 'good_truckfloor',
                                      'good_truckdoor', 'good_curtain', 'good_cooling_unit', 'pest_check', 'odor_check']).dropna()

def generate_inbound_inspection_log(inbound_log_df):
    required_columns = ['inbound_date', 'delivery_note_id', 'product_id', 'received_qty', 'rejected_qty', 'rejected_reason']
    return inbound_log_df[required_columns].copy().dropna()

def generate_complaint_handling_log(customer_df, product_df, num_rows=125):
    customer_ids = customer_df['customer_id'].tolist()
    product_ids = product_df['product_id'].tolist()
    complaint_categories = ["Spoilage/ Contamination", "Damaged", "Off-Taste/ Off-Smell/ Off-Color", "Expired", "Foreign Substance", "Mold Growth", "Defrosted"]
    complaint_statuses = ["Resolved"] * 100 + ["Pending"] * 25
    random.shuffle(complaint_statuses)
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    date_range = (end_date - start_date).days
    data = []
    for i in range(num_rows):
        complaint_date = start_date + datetime.timedelta(days=random.randint(0, date_range))
        complaint_id = f"CMP{i+1:05d}"
        customer_id = random.choice(customer_ids)
        product_id = random.choice(product_ids)
        complaint_qty = random.randint(1, 100)
        complaint_category = random.choice(complaint_categories)
        complaint_status = complaint_statuses[i]
        resolution_completed_date = complaint_date + datetime.timedelta(days=random.randint(2, 4)) if complaint_status == "Resolved" else None
        data.append([complaint_date, complaint_id, customer_id, product_id, complaint_qty, complaint_category, complaint_status, resolution_completed_date])
    return pd.DataFrame(data, columns=['complaint_date', 'complaint_id', 'customer_id', 'product_id', 'complaint_qty',
                                      'complaint_category', 'complaint_status', 'resolution_completed_date']).dropna()

def generate_cycle_count_log(product_df, num_rows=2500):
    product_qty_lookup = product_df.set_index('product_id')['system_qty'].to_dict()
    product_ids = product_df['product_id'].tolist()
    mismatch_rows = 125
    mismatch_indices = random.sample(range(num_rows), mismatch_rows)
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    date_range = (end_date - start_date).days
    data = []
    for i in range(num_rows):
        count_date = start_date + datetime.timedelta(days=random.randint(0, date_range))
        product_id = random.choice(product_ids)
        system_qty = product_qty_lookup.get(product_id)
        if i in mismatch_indices:
            lower_bound = max(20, int(system_qty * 0.95))
            upper_bound = int(system_qty * 1.05)
            counted_qty = random.randint(lower_bound, upper_bound) if upper_bound >= lower_bound else lower_bound
        else:
            counted_qty = system_qty
        data.append([count_date, product_id, system_qty, counted_qty])
    return pd.DataFrame(data, columns=['count_date', 'product_id', 'system_qty', 'counted_qty']).dropna()

def generate_product_disposal_log(product_df, num_rows=700):
    product_ids = product_df['product_id'].tolist()
    disposal_reasons = ["Expired", "Quality issue", "Physical damage", "Regulatory issue"]
    qcm_approvals = ["Approved"] * 679 + ["Pending"] * 21
    random.shuffle(qcm_approvals)
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    date_range = (end_date - start_date).days
    data = []
    for i in range(num_rows):
        disposal_date = start_date + datetime.timedelta(days=random.randint(0, date_range))
        product_id = random.choice(product_ids)
        disposal_reason = random.choice(disposal_reasons)
        disposal_qty = random.randint(6, 99)
        qcm_approval = qcm_approvals[i]
        data.append([disposal_date, product_id, disposal_reason, disposal_qty, qcm_approval])
    return pd.DataFrame(data, columns=['disposal_date', 'product_id', 'disposal_reason', 'disposal_qty', 'qcm_approval']).dropna()

def generate_warehouse_incident_reporting_log():
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    num_rows = (end_date - start_date).days + 1
    dates = [start_date + datetime.timedelta(days=i) for i in range(num_rows)]
    incident_choices = ["0"] * 70 + ["1"] * 20 + ["2"] * 7 + ["3"] * 3
    shift_choices = ["Day Shift", "Night Shift"]
    data = []
    for i, d in enumerate(dates):
        reporting_id = f"INC{i+1:05d}"
        operation_shift = random.choice(shift_choices)
        no_of_incidents = random.choice(incident_choices)
        data.append([reporting_id, d, operation_shift, no_of_incidents])
    return pd.DataFrame(data, columns=['reporting_id', 'reporting_date', 'operation_shift', 'no_of_incidents']).dropna()

# ------------------------------
# Generate All Tables
# ------------------------------

vehicle_df = generate_vehicle_details()
supplier_df = generate_supplier_details()
customer_df = generate_customer_details()
employee_df = generate_employee_details()
product_df = generate_product_details(supplier_df)
inbound_log_df = generate_inbound_log(supplier_df, product_df)
outbound_log_df = generate_outbound_log(customer_df, product_df, vehicle_df)
return_handling_log_df = generate_return_handling_log(customer_df, product_df, outbound_log_df)
vehicle_ncr_log_df = generate_vehicle_ncr_log(vehicle_df)
vehicle_hygiene_log_df = generate_vehicle_hygiene_log(outbound_log_df)
inbound_inspection_log_df = generate_inbound_inspection_log(inbound_log_df)
complaint_handling_log_df = generate_complaint_handling_log(customer_df, product_df)
cycle_count_log_df = generate_cycle_count_log(product_df)
product_disposal_log_df = generate_product_disposal_log(product_df)
warehouse_incident_reporting_log_df = generate_warehouse_incident_reporting_log()

# ------------------------------
# Save CSV Files
# ------------------------------

tables = [
    ('vehicle_details', vehicle_df),
    ('supplier_details', supplier_df),
    ('customer_details', customer_df),
    ('employee_details', employee_df),
    ('product_details', product_df),
    ('inbound_log', inbound_log_df),
    ('outbound_log', outbound_log_df),
    ('return_handling_log', return_handling_log_df),
    ('vehicle_ncr_log', vehicle_ncr_log_df),
    ('vehicle_hygiene_log', vehicle_hygiene_log_df),
    ('inbound_inspection_log', inbound_inspection_log_df),
    ('complaint_handling_log', complaint_handling_log_df),
    ('cycle_count_log', cycle_count_log_df),
    ('product_disposal_log', product_disposal_log_df),
    ('warehouse_incident_reporting_log', warehouse_incident_reporting_log_df)
]

for table_name, df in tables:
    file_path = f"{table_name}.csv"
    df.to_csv(file_path, index=False)
    logger.info(f"Saved {table_name} to {file_path} ({len(df)} rows)")

