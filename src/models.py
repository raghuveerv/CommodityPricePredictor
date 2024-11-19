import pandas as pd

unit_measure_ids = [5]
commodity_categories = [
    'Grains and Cereals', 'Pulses and Lentils', 'Edible Oils', 
    'Vegetables', 'Sweeteners', 'Miscellaneous', 
    'Dairy Products', 'Salt', 'Proteins', 'Fuel'
]


def predict_data(pipeline, target_year, countries):
    all_predictions = pd.DataFrame()
    for year in range(2017, target_year):  
        for month in range(1, 13):
            for country in countries:
                for unit_measure_id in unit_measure_ids:
                    for category in commodity_categories:
                        
                        future_data = pd.DataFrame({
                            'country_name': [country],
                            'unit_measure_id': [unit_measure_id],
                            'price_month': [month],
                            'price_year': [year],
                            'commodity_category': [category]
                        })

                        # Predict price for this specific combination
                        predicted_price = pipeline.predict(future_data)

                        # Append the prediction with the year, month, and other info
                        future_data['predicted_price'] = predicted_price
                        all_predictions = pd.concat([all_predictions, future_data], ignore_index=True)
    return all_predictions
