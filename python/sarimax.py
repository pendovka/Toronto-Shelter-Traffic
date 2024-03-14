from merge_data import weather_calls_occupancy

train_endog = train_data['unmatched_callers']
test_sarimax = test_data['unmatched_callers']
train_exog = train_data[current_features]
test_exog = test_data[current_features]

history_endog = [x for x in train_endog]
history_exog = train_exog.values.tolist()  
predictions_sarimax = []

for t in range(len(test_sarimax)):
    model = SARIMAX(history_endog, exog=history_exog,
                    order=(2, 1, 1),  
                    seasonal_order=(1, 0, 1, 7))
    model_fit = model.fit(disp = 0)
    
    next_exog = test_exog.iloc[t:t+1].values  
    
    output = model_fit.forecast(exog=next_exog)
    yhat = output[0]
    predictions_sarimax.append(yhat)
    
    obs = test_sarimax.iloc[t]
    history_endog.append(obs)

    history_exog.append(next_exog[0].tolist())  

mae_sarimax = mean_absolute_error(test_sarimax, predictions_sarimax)
print("Mean Absolute Error (MAE) on test data:", mae_sarimax)
