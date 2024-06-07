import pandas as pd
from datetime import datetime

# with open('PVTL02242200000387-input.trace', 'r') as trace_file:
#     trace_data = trace_file.readlines()
#
# with open('output.txt', 'w') as text_file:
#     all_lines = "".join(line for line in trace_data if "SVTL" not in line)
#     # print(all_lines)
#     text_file.write(all_lines.strip())
#     text_file.close()

df = pd.read_csv('PVTL02242300000583 original input.trace', sep='|', header=None)

df.columns = [f'@{i}' for i in range(1, 9)]
# panel-id
panel_id = df['@4'].iloc[0]
sub_panel_id = panel_id.replace('PV', 'SV')
# drop first two columns
df.drop(['@1', '@2'], axis=1, inplace=True)

# separate column @3
df[['date', 'time']] = df['@3'].str.split(' ', expand=True)

# drop column @3
df.drop(['@3'], axis=1, inplace=True)

# correct of date
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# correct of time
df['time'] = pd.to_datetime(df['time'], format='%H%M%S').dt.time

# static value skvr
df['skvr'] = "SKVR"
df['panel-id'] = panel_id

# generate sub-panel-id
df['sub_panel_id'] = sub_panel_id

df2 = df[["date", "time", "skvr", "panel-id", "sub_panel_id", "@4", "@5", "@6", "@7", "@8"]]  # "@4" is circuit-id

# range the dataframe 1 to 40 number row
main_df = df2.iloc[1:41]

# update sub-panel-id
sub_panels = [[sub_panel_id + "-" + str(i) for g in range(10)] for i in [2, 4, 1, 3]]
sub_panel_list = str(sub_panels).replace('[', '').replace(']', '').replace("'", "")
print(len(sub_panel_list.split(',')))
main_df['sub_panel_id'] = sub_panel_list.split(',')
main_df['sub_panel_id'] = main_df['sub_panel_id'].str.strip()

# main_df.to_csv('PVTL02242300000583_main.csv', index=False)
main_df.to_csv('PVTL02242300000583_main.txt', sep="|", header=None, index=False)

# print(main_df.head(10), main_df.shape)
