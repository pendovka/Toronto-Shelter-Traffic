






model_sarimax = SARIMAX(weather_calls_occupancy_flow_daily.unmatched_callers,  
                       exog = weather_calls_occupancy_flow_daily[current_features],
                       order=(2, 1, 1), 
                       seasonal_order=(1, 0, 1, 7))

results_sarimax = model_sarimax.fit(disp=0)
predictions_sarimax = results_sarimax.predict()
