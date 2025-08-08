"""
Loading, merging, and cleaning data for analysis
ves 08/2025
"""

import os 
import pandas as pd

def load_mics_data(base_dir):
    """
    Load MICS datasets (child, women, household) from a given directory
    Expects spss (.sav) files
    """
    child_path = os.path.join(base_dir, 'ch.sav')
    women_path = os.path.join(base_dir, 'wm.sav')
    household_path = os.path.join(base_dir, 'hh.sav')

    df_child = pd.read_spss(child_path)
    df_women = pd.read_spss(women_path)
    df_household = pd.read_spss(household_path)

    return df_child, df_women, df_household


