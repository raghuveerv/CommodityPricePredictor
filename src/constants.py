# src/constants.py

column_rename_dict = {
    'adm0_id': 'country_id',
    'adm0_name': 'country_name',
    'adm1_id': 'region_id',
    'adm1_name': 'region_name',
    'mkt_id': 'market_id',
    'cm_id': 'commodity_id',
    'cur_id': 'currency_id',
    'pt_id': 'price_type_id',
    'um_id': 'unit_measure_id',
    'mp_month': 'price_month',
    'mp_year': 'price_year',
    'mp_price': 'price'
}

currency_conversion_dict = {
    'BDT': 0.0091,
    'BTN': 0.012,
    'INR': 0.012,
    'NPR': 0.0075,
    'PKR': 0.0036,
    'LKR': 0.0031
}
