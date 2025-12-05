-- Table 01 - Vehicle details
CREATE OR REPLACE VIEW vw_vehicle_details AS
select
	coalesce(nullif(trim(vd.vehicle_no), ''), 'missing') as vehicle_no,
	case
		when vd.vehicle_capacity = '12 ton' then '15 ton'
		else vd.vehicle_capacity
	end as vehicle_capacity,
	case
		when vd.vehicle_capacity = '10 ton' then '45'
		when vd.vehicle_capacity = '12 ton' then '60'
		else '75'
	end as vehicle_cbm
from vehicle_details vd
order by vehicle_no;

--	Table 02 - Supplier details
CREATE OR REPLACE VIEW vw_supplier_details AS
select
	coalesce(nullif(trim(sd.supplier_id), ''), 'missing') as supplier_id,
	case
		when sd.country like '%Light%' then 'Italy'
		when sd.country like '%Cosmetics%' then 'Australia'
		when sd.country like '%Refrigerator%'  then 'Germany'
		when sd.country like '%Furniture%' then 'Italy'
		when sd.country like '%Cosmetics%' then 'Norway'
		when sd.country like '%Clothing%' then 'Nepal'
		when sd.country like '%Food Items%' then 'Iran'
		when sd.country like '%Shoes%' then 'Brazil'
		when sd.country like '%Car%' then 'Oman'
		when sd.country like '%Smartphone%' then 'Qatar'
		when sd.country like '%Jewelry%' then 'India'
		when sd.country like '%Washing Machine%' then 'Japan'
		when sd.country like '%Toys%' then 'Canada'
		when sd.country like '%China%' then 'China'
		when sd.country like '%Appliances%' then 'Vietnam'
		when sd.country like '%Television%' then 'UAE'
		when sd.country like '%Software%' then 'Sri Lanka'
		when sd.country like '%Bicycle%' then 'Maldives'
		when sd.country like '%Indo%' then 'Indonesia'
		else sd.country 
	end as country
from supplier_details sd;

-- Table 03 - Customer details
CREATE OR REPLACE VIEW vw_customer_details AS
select
	coalesce(nullif(trim(cd.customer_id),''), 'missing') as customer_id,
	REGEXP_REPLACE(
        cd.customer_name, '([a-z])([A-Z])', '\1 \2', 'g'
    ) AS customer_name
from customer_details cd
ORDER BY customer_id;

-- Table 04 - Employee details
CREATE OR REPLACE VIEW vw_employee_details AS
with employee as (
	select
		emp_id,
		extract(year from date '2024-12-31') - extract(year from date_of_birth) as age
	from employee_details ed
)
select
	coalesce(nullif(trim(ed.emp_id), ''), 'missingID') as emp_id,
	case
		when ed.emp_name = 'Male Names: Jack' then 'Jack'
		when ed.emp_name like '%Cameron%' then 'Cameron'
		else ed.emp_name
	end as employee_name,
	
	case
		when ed.designation = 'WH labour - outbound' then 'WH Outbound'
		when ed.designation = 'WH labour - inbound' then 'WH Inbound'
		when ed.emp_name = 'Anthony' then 'Warehouse'
		when ed.emp_name = 'Jacob' then 'Transport'
		when ed.emp_name = 'Charles' then 'Inventory Control'
		when ed.emp_name = 'Andrew' then 'Quality Control'
		when ed.emp_name = 'Mark' then 'Admin & HR'
	end as department,
	
	case
		when ed.designation = 'WH labour - outbound' then 'WH labour'
		when ed.designation = 'WH labour - inbound' then 'WH labour'
		else ed.designation
	end as designation,
	
	case
		when ed.email_address = 'male.names:.jack@logisticsone.com' then 'jack@logisticsone.com'
		when ed.email_address like '%emma@logisticsone.com%' then 'cameron@logisticsone.com'
		else ed.email_address
	end as emp_email,
	
	COALESCE(ed.date_of_birth, DATE '1900-01-01') AS date_of_birth,
	e.age as age,
	(60 - e.age) as years_to_retire
from employee_details ed
inner join
	employee e on ed.emp_id = e.emp_id
order by emp_id;
	
-- Table 05 - Product details
CREATE OR REPLACE VIEW vw_product_details AS
select 
	coalesce(nullif(trim(product_id), ''), 'missing') as product_id,
	coalesce(nullif(trim(product_name), ''), 'missingt') as product_name,
    coalesce(nullif(trim(delivery_note_id), ''), 'missing') as delivery_note_id,
    coalesce(nullif(trim(supplier_id), ''), 'missing') as supplier_id,
    coalesce(system_qty , -999) as system_qty,
    coalesce(cast(product_cost as decimal(10,2)), 0) as product_cost,
    coalesce(cast(product_price as decimal(10,2)), 0) as product_price,
    coalesce(cast(product_carton_volume_cbm as decimal(10,2)), 0) as product_cbm
from product_details
order by product_id;

-- Table 06 - Inbound log
CREATE OR REPLACE VIEW vw_inbound_log AS
select
    coalesce(cast(inbound_date as date), cast('1900-01-01' as date)) AS inbound_date,
    coalesce(nullif(trim(il.supplier_id), ''), 'missing') supplier_id,
    coalesce(nullif(trim(il.delivery_note_id), ''), 'missing') delivery_note_id,
    coalesce(nullif(trim(il.product_id), ''), 'missing') product_id,
	coalesce(il.received_qty, -999) received_qty,
	coalesce(il.rejected_qty, -999) rejected_qty,
	coalesce(nullif(trim(il.inbound_status), ''), 'missing') inbound_status,
	case
		when il.rejected_reason = 'NaN' then 'Accepted'
		else rejected_reason
	end as reason_to_reject,	
	COALESCE(il.unloading_started_time::time, TIME '00:00:00') unloading_started_time,
	COALESCE(il.unloading_completed_time::time, TIME '00:00:00') unloading_completed_time,
	COALESCE(inbound_putaway_completed_time::time, TIME '00:00:00') putaway_completed_time
from inbound_log il
order by inbound_date;

-- Table 07 - Outbound_log
CREATE OR REPLACE VIEW vw_outbound_log AS
select
	coalesce(ol.outbound_date, date '1900-01-01') outbound_date,
	coalesce(nullif(trim(ol.customer_id), ''), 'missing') customer_id,
	coalesce(nullif(trim(ol.order_id), ''), 'missing') order_id,
	coalesce(nullif(trim(ol.product_id), ''), 'missing') product_id,
	coalesce(ol.ordered_qty, -999) ordered_qty,
	coalesce(ol.picked_qty, -999) picked_qty,
	(ol.ordered_qty - ol.picked_qty) pick_failed_qty,
    coalesce(nullif(trim(ol.vehicle_no), ''), 'missing') allocated_vehicle,
	coalesce(ol.pick_sheet_issued_time::time, time '00:00:00') pick_sheet_issued_time,
	coalesce(ol.pick_completed_time::time, time '00:00:00') pick_completed_time,
	coalesce(ol.loading_completed_time::time, time '00:00:00') loading_completed_time
from outbound_log ol
order by outbound_date;

-- Table 08 - Return handling log
CREATE OR REPLACE VIEW vw_return_handling_log AS
select
	coalesce(return_date, date '1900-01-01') return_date,
	coalesce(nullif(trim(customer_id), ''), 'missing') customer_id,
	coalesce(nullif(trim(order_id), ''), 'missing') order_id,
	coalesce(nullif(trim(product_id), ''), 'missing') product_id,
	coalesce(nullif(trim(return_reason), ''), 'missing') return_reason,
	coalesce(returned_qty, -999) returned_qty,
	coalesce(return_unloading_started_time::time, time '00:00:00') unloading_started_time,
	coalesce(return_putaway_completed_time::time, time '00:00:00') putaway_completed_time
FROM return_handling_log rhl
order by return_date;

-- Table 09 - Inbound inspection log -> Will be derived from inbound log

-- Table 10 - Vehicle NCR log
CREATE OR REPLACE VIEW vw_vehicle_ncr_log AS
select
	coalesce(vnl.ncr_raised_date, date '1900-01-01') as ncr_raised_date,
    coalesce(nullif(TRIM(vnl.ncr_id), ''), 'missing') as ncr_id,
	coalesce(nullif(TRIM(vnl.vehicle_no), ''), 'missing')as vehicle_no,
	coalesce(nullif(TRIM(vnl.ncr_reason), ''), 'missing')as ncr_reason,
	case
		when ncr_reason in ('Defective cooling unit', 'Defective truck door', 'Pest', 'Odor') then 'Major'
		when ncr_reason in ('Defective truck box', 'Defective truck floor') then 'Minor'
	end as nc_severity,
	coalesce(vnl.ca_completed_date, date '1900-01-01') ca_completed_date,
	coalesce(nullif(TRIM(vnl.ncr_status), ''), 'missing') ncr_status,
	case 
		when vnl.ncr_status = 'CA completed' then vnl.ca_completed_date - vnl.ncr_raised_date
		else null
	end as days_to_complete
from vehicle_ncr_log vnl
order by ncr_raised_date;

-- Table 11 - Vehicle hygiene inspection log
CREATE OR REPLACE VIEW vw_vehicle_hygiene_inspection_log AS
select
	coalesce(inspection_date, date '1900-01-01'),
	coalesce(nullif(trim(vehicle_no),''),'mising') vehicle_no,
	coalesce(nullif(trim(good_truckbox),''),'mising') good_truckbox,
	coalesce(nullif(trim(good_truckfloor),''),'mising') good_truckfloor,
	coalesce(nullif(trim(good_truckdoor),''),'mising') good_truckdoor,
	coalesce(nullif(trim(good_curtain),''),'mising') good_curtain,
	coalesce(nullif(trim(good_cooling_unit),''),'mising') good_cooling_unit,
	coalesce(nullif(trim(pest_check),''),'mising') pest_check,
	coalesce(nullif(trim(odor_check),''),'mising') odor_check
from
	vehicle_hygiene_inspection_log vhil
order by inspection_date

	Table 12 - Complaint handling log
CREATE OR REPLACE VIEW vw_complaint_handling_log AS
Select 
	coalesce(complaint_date, date '1900-01-01') complaint_date,
	coalesce(nullif(trim(complaint_id),''),'mising') complaint_id,
	coalesce(nullif(trim(customer_id),''),'mising') customer_id,
	coalesce(complaint_qty, -999) complaint_qty,
	coalesce(nullif(trim(product_id),''),'mising') product_id,
	CASE
		WHEN chl.complaint_category LIKE 'Off-Taste/ Off-Smell/ Off-Color' THEN 'Off-Sensory'
		WHEN chl.complaint_category LIKE 'Spoilage/ Contamination' THEN 'Spoilage'
		ELSE chl.complaint_category
	END AS complaint_category,
	coalesce(nullif(trim(complaint_status),''),'mising') complaint_status,
	resolution_completed_date,
	case
		when complaint_status = 'Resolved' then resolution_completed_date - complaint_date
		else null
	end as days_to_complete
from complaint_handling_log chl
order by complaint_date;

-- Table 13 - Cycle count log
CREATE OR REPLACE VIEW vw_cycle_count_log AS
with na_qty as (
	select
		cycle_count_id,
		(system_qty - counted_qty) as adjusted_qty
	from cycle_count_log ccl
)
Select 
	coalesce(ccl.count_date, date '1900-01-01') count_date,
	coalesce(nullif(trim(ccl.product_id),''),'mising') product_id,
	coalesce(ccl.system_qty, -999) system_qty,
	coalesce(ccl.counted_qty, -999) counted_qty,
        n.adjusted_qty,
	case
		when n.adjusted_qty = 0 then 'Accurate'
		else 'Adjusted'
	end as cycle_count_status
from cycle_count_log ccl
inner join
	na_qty n on ccl.cycle_count_id = n.cycle_count_id
order by count_date;

-- Table 14 - Product disposal log
CREATE OR REPLACE VIEW vw_product_disposal_log AS
Select 
 	coalesce(pdl.disposal_date, date '1900-01-01') disposal_date,
	coalesce(nullif(trim(pdl.product_id),''),'mising') product_id,
	coalesce(pdl.disposal_qty, -999) disposal_qty,
	coalesce(nullif(trim(pdl.disposal_reason),''),'mising') disposal_reason,
	coalesce(nullif(trim(pdl.qcm_approval),''),'mising') qcm_approval
from product_disposal_log pdl
order by disposal_date;

-- Table 15 – Warehouse temperature monitoring log
CREATE OR REPLACE VIEW public.vw_warehouse_temperature_monitoring_log
select
    coalesce(wtml.monitoring_date, date '1900-01-01')::date as monitoring_date,
    coalesce(nullif(trim(wtml.location_code),''), 'missing') as location_code,
    -- Time format correction
    CASE 
        WHEN UPPER(inspection_time) LIKE '%AM' THEN 
            TO_TIMESTAMP(REPLACE(inspection_time, '.', ':'), 'HH:MI AM')::TIME
        WHEN UPPER(inspection_time) LIKE '%PM' THEN 
            TO_TIMESTAMP(REPLACE(inspection_time, '.', ':'), 'HH:MI PM')::TIME
        ELSE NULL::TIME
    END AS inspection_time,
    coalesce(wtml.temperature, -999) as temperature
FROM warehouse_temperature_monitoring_log wtml
order by monitoring_date;

-- Table 16 – Warehouse incident reporting log
CREATE OR REPLACE VIEW public.vw_warehouse_incident_reporting_log
AS SELECT reporting_id,
    COALESCE(reporting_date, '1900-01-01'::date) AS reporting_date,
    COALESCE(NULLIF(TRIM(BOTH FROM operation_shift), ''::text), 'missing'::text) AS operation_shift,
    COALESCE(NULLIF(TRIM(BOTH FROM no_of_incidents), ''::text), 'missing'::text) AS no_of_incidents
   FROM warehouse_incident_reporting_log
  ORDER BY (COALESCE(reporting_date, '1900-01-01'::date));