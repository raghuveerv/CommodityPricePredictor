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
    'LKR': 0.0031,
    'COP': 0.00024,
    'GTQ': 0.13
}

commodity_mapping = {
    'Wheat': 'Grains and Cereals',
    'Wheat flour': 'Grains and Cereals',
    'Rice (coarse)': 'Grains and Cereals',
    'Rice (local)': 'Grains and Cereals',
    'Rice (imported, Indian)': 'Grains and Cereals',
    'Rice (basmati, broken)': 'Grains and Cereals',
    'Rice (red nadu)': 'Grains and Cereals',
    'Rice (long grain)': 'Grains and Cereals',
    'Lentils (masur)': 'Pulses and Lentils',
    'Lentils (moong)': 'Pulses and Lentils',
    'Lentils (urad)': 'Pulses and Lentils',
    'Beans(mash)': 'Pulses and Lentils',
    'Oil (palm)': 'Edible Oils',
    'Oil (mustard)': 'Edible Oils',
    'Oil (soybean)': 'Edible Oils',
    'Oil (sunflower)': 'Edible Oils',
    'Oil (groundnut)': 'Edible Oils',
    'Oil (cooking)': 'Edible Oils',
    'Potatoes': 'Vegetables',
    'Tomatoes': 'Vegetables',
    'Onions': 'Vegetables',
    'Sugar': 'Sweeteners',
    'Sugar (jaggery/gur)': 'Sweeteners',
    'Ghee (vanaspati)': 'Dairy Products',
    'Ghee (artificial)': 'Dairy Products',
    'Milk': 'Dairy Products',
    'Milk (pasteurized)': 'Dairy Products',
    'Eggs': 'Proteins',
    'Poultry': 'Proteins',
    'Salt': 'Salt',
    'Salt (iodised)': 'Salt',
    'Fuel (diesel)': 'Fuel',
    'Fuel (petrol-gasoline)': 'Fuel',
    'Tea (black)': 'Miscellaneous',
    'Wage (non-qualified labour, non-agricultural)': 'Miscellaneous'
}
