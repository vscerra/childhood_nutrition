def merge_mics_data(df_child, df_women, df_household):
    """
    Merge child, women, and household data.
    This version assumes simple merge on household ID (hhid)
    """
    df = df_child.merge(df_women, on='HH1', suffixes=('', '_mom'), how='left')
    df = df.merge(
        df_household[['HH1', 'WS1', 'WS4', 'HH48', 'windex5']], 
        on='HH1', how='left'
    )
    return df

def create_target_variables(df):
    """
    Add binary targets for stunting and developmental status.
    Requires HAZ (height-for-age z-score) and ECDI component variables
    """
    df['stunted'] = (df['HAZ'] < -2).astype(int) #HC70 is typically HAZ in MICS
    ec_items = ['EC6', 'EC7', 'EC8', 'EC9', 'EC10', 'EC11', 'EC12', 'EC13', 'EC14', 'EC15']
    for col in ec_items:
        df[col] = df[col].map({'YES':1, 'NO':0})
    
    df['ecd_i_count'] = df[ec_items].sum(axis=1)
    df['ecd_on_track'] = (df['ecd_i_count'] >= 6).astype(int) #may vary threshold

    return df

def extract_features(df):
    """
    Select and return the core feature set for modeling
    """
    feature_columns = [
        'UB2', 'MN34', 'EC6', 'EC7', 'EC8', 'EC9', 'EC10', 'EC11', 'EC12', 'EC13', 'EC14', 'EC15',  #Child's age, birth weight (in g), early childhood development indicators
        'WB6A', 'WB6B', 'WAGE', 'MN5', 'WB14', #Mother's years of education, mother's age, # antenatal visits (healthcare proxy), literacy status (agency and education proxy)
        'windex5', 'HH48',      #Wealth quintile, household size, urban/rural residence
        'WS1', 'WS4',                   #main water source, time to collect water
        'BD2', 'BD3', 'CA1'     #Received vitamin A, breastfed, still being breastfed, child had diarrhea in the past 12 weeks
    ]
    return df[feature_columns + ['stunted', 'ecd_on_track']]


def impute_missing_values(df):
    """
    Impute missign values  in the modeling feature set. 
    Numeric features: median imputation
    Categorical features: mode imputation
    """
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(df[col].median())
        else:
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode.iloc[0])
    return df