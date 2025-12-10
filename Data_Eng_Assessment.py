import pandas as pd

casino = pd.read_csv("casino_settup2.csv",low_memory=False)
corelare = pd.read_csv("corelare_locatii2.csv",low_memory=False)
jackpot = pd.read_csv("jackpot_history2.csv",low_memory=False)


m23 = pd.read_csv("mechanical_counters2023-12-01till2024-01-01.csv",low_memory=False)
m24 = pd.read_csv("mechanical_counters2024-1-1till2025-1-1.csv",low_memory=False)
m25 = pd.read_csv("mechanical_counters2025-1-1tillNow.csv",low_memory=False)


print("Casino:", casino.shape)
print("Corelare:", corelare.shape)
print("Jackpot:", jackpot.shape)
print("Mechanical 2023 → 2024:", m23.shape)
print("Mechanical 2024 → 2025:", m24.shape)
print("Mechanical 2025 → Now:", m25.shape)


m23["year"] = 2023
m24["year"] = 2024
m25["year"] = 2025
mechanical = pd.concat([m23, m24, m25], ignore_index=True)
print("Combined mechanical rows:", mechanical.shape)
mechanical.head()


mechanical = mechanical.drop_duplicates()
mechanical = mechanical.dropna(subset=["total_in", "total_out"])
mechanical["total_in"] = pd.to_numeric(mechanical["total_in"], errors="coerce")
mechanical["total_out"] = pd.to_numeric(mechanical["total_out"], errors="coerce")
mechanical = mechanical.dropna(subset=["total_in", "total_out"])
mechanical = mechanical[(mechanical["total_in"] >= 0) & (mechanical["total_out"] >= 0)]
print("Mechanical cleaned:", mechanical.shape)


mechanical["GGR"] = mechanical["total_in"] - mechanical["total_out"]
mechanical[["total_in", "total_out", "GGR"]].head()


corelare.columns


mechanical['ID_CASINO'] = mechanical['ID_CASINO'].astype(str).str.strip()
corelare['ID_CASINO'] = corelare['ID_CASINO'].astype(str).str.strip()
mechanical_with_location = mechanical.merge(
    corelare[['ID_CASINO', 'id_locatie']],  # use the correct column name
    on='ID_CASINO',
    how='left'
)
mechanical_with_location = mechanical_with_location.merge(
    casino[['ID_CASINO', 'id']],  # 'id' in casino is probably the casino name or id
    on='ID_CASINO',
    how='left'
)
mechanical_with_location = mechanical_with_location.rename(columns={'id': 'Casino_name', 'id_locatie': 'Location_id'})
mechanical_with_location[['ID_CASINO', 'Casino_name', 'Location_id', 'GGR']].head()


print(mechanical_with_location.columns.tolist())
mechanical_with_location = mechanical_with_location.rename(columns={'id_y': 'Casino_name'})
mechanical_with_location[['ID_CASINO', 'Casino_name', 'Location_id', 'GGR']].head()


mechanical_with_location = mechanical_with_location.rename(
    columns={'id_locatie': 'Location_id', 'label': 'Casino_name'}
)
mechanical_with_location[['ID_CASINO', 'Casino_name', 'Location_id', 'GGR']].head()
l_ggr = mechanical_with_location.groupby(['Location_id', 'year']).agg({'GGR': 'sum'}).reset_index()
l_ggr.head()


mechanical_with_location_clean = mechanical_with_location[
    mechanical_with_location['Location_id'].notna() &   
    (mechanical_with_location['Location_id'] != '0')  
].copy()  
print("Rows after removing missing/invalid locations:", mechanical_with_location_clean.shape)
mechanical_with_location_clean.head()


location_ggr = mechanical_with_location_clean.groupby(
    ['Location_id', 'year']
).agg({'GGR': 'sum'}).reset_index()
print(location_ggr.head())


top10_2025 = location_ggr[location_ggr['year'] == 2025].sort_values(
    'GGR', ascending=False
).head(10)
print("Top 10 most profitable locations in 2025:")
print(top10_2025)


ggr_2024 = location_ggr[location_ggr['year'] == 2024][['Location_id', 'GGR']].rename(columns={'GGR':'GGR_2024'})
ggr_2025 = location_ggr[location_ggr['year'] == 2025][['Location_id', 'GGR']].rename(columns={'GGR':'GGR_2025'})
ggr_compare = ggr_2025.merge(ggr_2024, on='Location_id', how='left')
ggr_compare['GGR_change'] = ggr_compare['GGR_2025'] - ggr_compare['GGR_2024']
ggr_compare.head()


top10_growth = ggr_compare.sort_values('GGR_change', ascending=False).head(10)
print("Top 10 locations with highest GGR growth 2025 vs 2024:")
print(top10_growth)
top10_decline = ggr_compare.sort_values('GGR_change', ascending=True).head(10)
print("Top 10 locations with largest GGR decrease 2025 vs 2024:")
print(top10_decline)


print("jackpot columns:", jackpot.columns.tolist())
jackpot.head()

jackpot_clean = jackpot[jackpot["deleted"] == 0].copy()
jackpot_clean["ID_CASINO"] = jackpot_clean["ID_CASINO"].astype(str).str.strip()
jackpot_clean["value"] = pd.to_numeric(jackpot_clean["value"], errors="coerce")
jackpot_clean = jackpot_clean.dropna(subset=["value"])
jackpot_by_casino = jackpot_clean.groupby("ID_CASINO")["value"].sum().reset_index()
jackpot_by_casino = jackpot_by_casino.rename(columns={"value": "Total_Jackpot"})
print("Clean jackpot data:")
display(jackpot_by_casino.head())


import pandas as pd
casino = pd.read_csv("casino_settup2.csv", low_memory=False)
corelare = pd.read_csv("corelare_locatii2.csv", low_memory=False)
m23 = pd.read_csv("mechanical_counters2023-12-01till2024-01-01.csv", low_memory=False)
m24 = pd.read_csv("mechanical_counters2024-1-1till2025-1-1.csv", low_memory=False)
m25 = pd.read_csv("mechanical_counters2025-1-1tillNow.csv", low_memory=False)


m23["year"] = 2023
m24["year"] = 2024
m25["year"] = 2025
mechanical = pd.concat([m23, m24, m25], ignore_index=True)
mechanical = mechanical.drop_duplicates()
mechanical = mechanical.dropna(subset=["total_in", "total_out"])
mechanical["total_in"] = pd.to_numeric(mechanical["total_in"], errors="coerce")
mechanical["total_out"] = pd.to_numeric(mechanical["total_out"], errors="coerce")
mechanical = mechanical.dropna(subset=["total_in", "total_out"])
mechanical = mechanical[(mechanical["total_in"] >= 0) & (mechanical["total_out"] >= 0)]
mechanical["GGR"] = mechanical["total_in"] - mechanical["total_out"]


mechanical['ID_CASINO'] = mechanical['ID_CASINO'].astype(str).str.strip()
corelare['ID_CASINO'] = corelare['ID_CASINO'].astype(str).str.strip()
mechanical_with_location = mechanical.merge(
    corelare[['ID_CASINO', 'id_locatie']],
    on='ID_CASINO',
    how='left'
)
mechanical_with_location = mechanical_with_location.rename(columns={'id_locatie': 'Location_id'})


mechanical_with_location_clean = mechanical_with_location[
    mechanical_with_location['Location_id'].notna() &
    (mechanical_with_location['Location_id'] != '0')
].copy()


ggr_by_casino = mechanical_with_location_clean.groupby("ID_CASINO")["GGR"].sum().reset_index()
ggr_by_casino = ggr_by_casino.rename(columns={"GGR": "Total_GGR"})
print("GGR by casino:")
display(ggr_by_casino.head())

roi_df["ROI"] = (roi_df["Total_GGR"] - roi_df["Total_Jackpot"]) / (
    roi_df["Total_Jackpot"].replace(0, 1))

roi_df_sorted = roi_df.sort_values("ROI", ascending=False)

roi_df_sorted.head(10)
