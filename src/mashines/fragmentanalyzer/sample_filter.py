def need_human_validation(sample_peaks):
    # this function checks peaks of only 1 sample one at a time
    # If Human Validation is needed, return all Peaks and a Booling True
    # If Human Validation is not needed, return only the Correct Size BP Peak and a booling False

    if len(sample_peaks) == 1:
        # is value between 500 - 700?
        if 500 <= sample_peaks[0] <= 700:
            return sample_peaks[0], False
        return sample_peaks[0], True
    else:
        # is only 1 value between 500 - 700 and rest of the other peaks between 100 - 300?
        correct_peaks = [peak for peak in sample_peaks if 500 <= peak <= 700]
        other_peaks = [peak for peak in sample_peaks if peak < 500 or peak > 700]
        if len(correct_peaks) == 1 and all(100 <= peak <= 300 for peak in other_peaks):
            return correct_peaks[0], False 
    return sample_peaks, True


