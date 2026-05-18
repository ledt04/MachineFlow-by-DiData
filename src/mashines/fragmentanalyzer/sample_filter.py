def need_human_validation(sample_peaks):
    for sample_name, peaks in sample_peaks.items():
        # Skip samples with no peaks (e.g., BLANK) if that's intended
        if not peaks:
            continue
            
        # Case 1: Exactly 1 peak between 500-700
        if len(peaks) == 1:
            if 500 <= peaks[0] <= 700:
                continue # This sample is fine
            else:
                return True # Needs validation (1 peak, but out of range)

        # Case 2: Multiple peaks
        # Check if exactly one peak is in the 500-700 target range
        target_peaks = [p for p in peaks if 500 <= p <= 700]
        
        if len(target_peaks) == 1:
            # Check if all OTHER peaks are within 100-300
            other_peaks = [p for p in peaks if not (500 <= p <= 700)]
            if all(100 <= p <= 300 for p in other_peaks):
                continue # This sample is fine
            else:
                return True # Needs validation (other peaks are outside 100-300)
        else:
            # Needs validation if there are 0 or >1 peaks in the 500-700 range
            return True

    return False # If we get through the whole loop, no validation is needed