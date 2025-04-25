import pandas as pd
import matplotlib.pyplot as plt


# This methods purpose is to read the chromatogram data from some file using pandas

# The first row will be said to be a header
# Then I want to make sure that the column 0 will contain the time values
# Column 1 will then contain any of the intensity values for each of the transitions

# The return statements are formatted as follows:

# A list of times as float, the exact time points
# The transitions which are also floats, each of the inner list will be one 
# of the transition intensities 

def load_data(file_name):
    df = pd.read_csv(file_name, sep='\t', header=0)
    times = df.iloc[:,0].tolist()
    transitions = [df[col].tolist() for col in df.columns[1:]]
    return times, transitions

# This method will sum all of the transitions at each of the correct time points
# to caculate the Total Ion Chromatogram (TIC)
def get_transitions_tic(transitions):
    df = pd.DataFrame(transitions).T
    return df.sum(axis=1).tolist()

# This method focuses on trying to get the index of that exact time point
# where we can see that TIC is the highest
def get_lc_peak_max_time_index(transitions):
    tic = get_transitions_tic(transitions)
    return pd.Series(tic).idxmax()

#This method will calculate each of the transitions intesity at the peak time, then
# it will normalize it so the largest value is equal to 1.0

def get_relative_intensities(transitions):
   apex_idx = get_lc_peak_max_time_index(transitions)
   raw_vals = [trace[apex_idx] for trace in transitions]
   max_val = max(raw_vals)
   if max_val <= 0:
       raise Exception('No intensity in any transition')
   return [val / max_val for val in raw_vals]

# This method will keep only the transitions that are relative intensity >= threshold
def filter_transitions_by_rel_intensity(transitions, rel_intensity_threshold):
   rels = get_relative_intensities(transitions)
   filtered = [trace for rel, trace in zip(rels, transitions) if rel >= rel_intensity_threshold]
   if not filtered:
       raise Exception(
           f'Relative intensity threshold {rel_intensity_threshold:.4f} resulted in 0 transitions passing the filter'
       )
   return filtered

# This method will plot each of the transition's intensity over time
def plot_transitions(times, transitions):
   fig, ax = plt.subplots(figsize=(10, 6))
   for trace in transitions:
       ax.plot(times, trace)
   ax.set_xlabel('Time (min)')
   ax.set_ylabel('Intensity')
   ax.set_title('Chromatogram Transitions')
   return ax

   # This is the Driver code for TSV file 
   # 1) Save your pasted data in a file named "data.tsv"
   # 2) Load times and transitions from TSV
   # 3) (Optional) Filter transitions by relative intensity (e.g., keep above 0.1)
   # 4) Plot and show
if __name__ == "__main__":
   file_name = "data.tsv"
   times, transitions = load_data(file_name)

   threshold = 0.1
   transitions = filter_transitions_by_rel_intensity(transitions, threshold)

   ax = plot_transitions(times, transitions)
   plt.show()