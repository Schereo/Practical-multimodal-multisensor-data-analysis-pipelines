# Practical-multimodal-multisensor-data-analysis-pipelines


## Description of variables

- STATIONS_ID: ID of the station
    - Not needed since we only got values of the same station in one document
- MESS_DATUM (date of measurement) 
    - Needed since we want to analyze time series data
- QN_8 (quality of the measurement)
    - Kept since it could yield us important information for outliers
- R1 (precipitation in mm)
    - Needed and main focus of analysis
- RS_IND (flag for indicating rain)
    - Kept since it might be interesting to just analyze whether it rained or not
- WRTR (type of precipitation)
    - Mostly error values, not really usable
- eor (end of data record)