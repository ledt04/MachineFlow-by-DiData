    
def extract_sample_peaks(csv_df):
    rows = csv_df.values
    # Extract Sample Names and Peak Values from csv file
    sample_peaks = {}
    
    for i, row in enumerate(rows):
        first_cell = str(row[0])
        if first_cell[0].isalpha() and first_cell[1:].isdigit():
            sample_name = row[1]
            peak_list = []
            
            # skip 2 rows
            for j in range(i + 2, len(rows)):
                inner_row = rows[j]
                
                # stop if we reach row include LM or UM, empty, TIC/TIM, E2, E3
                size_val = str(inner_row[1])
            
                if str(inner_row[0])[0].isalpha() and str(inner_row[0])[1:].isdigit():
                    break
                if '(LM)' in size_val or '(UM)' in size_val:
                    continue
                if size_val.strip() == '' or 'TIC:' in size_val or size_val == 'nan':
                    break
                peak_list.append(int(size_val))
                
            # Save to our dictionary
            sample_peaks[sample_name] = peak_list
    return sample_peaks