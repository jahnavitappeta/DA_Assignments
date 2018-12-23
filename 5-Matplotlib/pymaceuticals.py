
# coding: utf-8

# In[193]:


# Dependencies and Setup
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Hide warning messages in notebook
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These) Read the Mouse and Drug Data and the Clinical Trial Data
mouse_drug_data_to_load = pd.read_csv("data/mouse_drug_data.csv")
clinical_trial_data_to_load = pd.read_csv("data/clinicaltrial_data.csv")


# Combine the data into a single dataset
pymaceuticals_data_df = pd.merge( clinical_trial_data_to_load,mouse_drug_data_to_load, on = ('Mouse ID'))

# Display the data table for preview
pymaceuticals_data_df.head()


# In[315]:


# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint
mean_tumor_volume_df = pymaceuticals_data_df.groupby(['Drug', 'Timepoint'], as_index=False)
# Convert to DataFrame
mean_tumor_volume_df = pd.DataFrame(mean_tumor_volume_df["Tumor Volume (mm3)"].mean())
# Preview DataFrame
mean_tumor_volume_df.head(12)


# In[195]:


#Tumor Response to Treatment


# In[196]:


# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
SE_tumor_volume_df = pymaceuticals_data_df.groupby(['Drug', 'Timepoint'])
# Convert to DataFrame
SE_tumor_volume_df = pd.DataFrame(SE_tumor_volume_df["Tumor Volume (mm3)"].sem().reset_index())
# Preview DataFrame
SE_tumor_volume_df.head()


# In[197]:


# Minor Data Munging to Re-Format the Data Frames
drugs_df =mean_tumor_volume_df.pivot_table('Tumor Volume (mm3)', ['Timepoint'], 'Drug')
# Preview that Reformatting worked
drugs_df


# In[346]:


# Generate the Plot (with Error Bars)
drugs_plot_df = drugs_df[['Capomulin','Infubinol', 'Ketapril', 'Placebo']].copy()
styles = ['ro:','b^:','gs:','kD:']
fig1 = drugs_plot_df.plot(kind='line', title='Tumor Response to Treatment', grid='On', legend=True, style=styles)
fig1.set_xlabel('Time(Days)')
fig1.set_ylabel('Total Volume(mm3)')
plt.tight_layout()
# Save the Figure
fig1 = fig1.get_figure()
fig1.savefig("tumor_response.png")
# Show the Figure
plt.show()


# In[317]:


#Metastatic Response to Treatment


# In[318]:


# Store the Mean Met. Site Data Grouped by Drug and Timepoint 
mean_met_sites_df = pymaceuticals_data_df.groupby(['Drug', 'Timepoint'])
# Convert to DataFrame
mean_met_sites_df = pd.DataFrame(mean_met_sites_df["Metastatic Sites"].mean())
# Preview DataFrame
mean_met_sites_df.head()


# In[319]:


# Store the Standard Error associated with Met. Sites Grouped by Drug and Timepoint 
SE_met_sites_df = pymaceuticals_data_df.groupby(['Drug', 'Timepoint'])
# Convert to DataFrame
SE_met_sites_df = pd.DataFrame(SE_met_sites_df["Metastatic Sites"].sem())
# Preview DataFrame
SE_met_sites_df.head()


# In[320]:


# Minor Data Munging to Re-Format the Data Frames
drugs_met_df =mean_met_sites_df.pivot_table('Metastatic Sites', ['Timepoint'], 'Drug')
# Preview that Reformatting worked
drugs_met_df.head()


# In[347]:


# Generate the Plot (with Error Bars)
drugs_met_plot_df = drugs_met_df[['Capomulin','Infubinol', 'Ketapril', 'Placebo']].copy()
styles = ['ro:','b^:','gs:','kD:']
#labels = ['Capomulin','Ceftamin', 'Ketapril', 'Infubinol']
fig2 = drugs_met_plot_df.plot(kind='line', title='Metastatic Spread During Treatment', grid='On', legend=True, style=styles)
fig2.set_xlabel('Treatment Duration(Days)')
fig2.set_ylabel('Met Sites')
plt.tight_layout()
# Save the Figure
fig2 = fig2.get_figure()
fig2.savefig("metastatic_spread.png")
# Show the Figure
plt.show()


# In[322]:


#Survival Rates


# In[323]:


# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
mouse_count_df = pymaceuticals_data_df.groupby(['Drug', 'Timepoint'])
# Convert to DataFrame
mouse_count_df = pd.DataFrame(mouse_count_df["Mouse ID"].count().reset_index())
mouse_count_df.rename(columns={'Mouse ID':'Mouse Count'}, inplace = True)
# Preview DataFrame
mouse_count_df.head()


# In[324]:


# Minor Data Munging to Re-Format the Data Frames
drugs_mouse_count_df = mouse_count_df.pivot_table('Mouse Count', ['Timepoint'], 'Drug')
# Preview the Data Frame
drugs_mouse_count_df.head()


# In[325]:


drugs_mouse_count_df["Capomulin_percent"]=drugs_mouse_count_df["Capomulin"]/drugs_mouse_count_df["Capomulin"].iloc[0] * 100
drugs_mouse_count_df["Infubinol_percent"]=drugs_mouse_count_df["Infubinol"]/drugs_mouse_count_df["Infubinol"].iloc[0] * 100
drugs_mouse_count_df["Ketapril_percent"]=drugs_mouse_count_df["Ketapril"]/drugs_mouse_count_df["Ketapril"].iloc[0] * 100
drugs_mouse_count_df["Placebo_percent"]=drugs_mouse_count_df["Placebo"]/drugs_mouse_count_df["Placebo"].iloc[0] * 100
drugs_mouse_count_df


# In[326]:


# Generate the Plot  (Accounting for percentages)
drugs_mouse_plot_df = drugs_mouse_count_df[['Capomulin_percent','Placebo_percent', 'Ketapril_percent', 'Infubinol_percent']].copy()
styles = ['ro:','b^:','gs:','kD:']
fig3 = drugs_mouse_plot_df.plot(kind='line', title='Survival During Treatment', grid='On', legend=True, style=styles)
fig3.set_xlabel('Time(Days)')
fig3.set_ylabel('Survival Rate(%)')

# Save the Figure
fig3 = fig3.get_figure()
fig3.savefig("survival_rate.png")
# Show the Figure
plt.show()
plt.tight_layout()


# In[327]:


## Summary Bar Graph


# In[328]:


# Calculate the percent changes for each drug
#used pct_change with parameter periods = 9 because we need percentage change between open and close value.
per_change_df = drugs_df.pct_change(periods=9).dropna(how='any')
#pivot table with only required data(don't need Timepoint) and transposing
per_change_df = pd.pivot_table(per_change_df, index= 'Drug').T
per_change_df['Drug'] = per_change_df['Drug'] * 100
per_change_df.rename(columns={'Drug': ''})


# In[345]:


# Store all Relevant Percent Changes into a Tuple
#per_change_df = per_change_df[['Capomulin','Infubinol', 'Ketapril', 'Placebo']]
per_change_tuple = ([per_change_df.iloc[0].name, float(per_change_df.iloc[0].values[0])],
                   [per_change_df.iloc[2].name, float(per_change_df.iloc[2].values[0])],
                   [per_change_df.iloc[3].name, float(per_change_df.iloc[3].values[0])],
                   [per_change_df.iloc[5].name, float(per_change_df.iloc[5].values[0])])
# Splice the data between passing and failing drugs
Fail = ()
Pass = ()
for key, value in per_change_tuple:
    if value >= 0:
        Fail = Fail + (key, value) 
    else: 
        Pass = Pass + (key, value)
        
# Orient widths. Add labels, tick marks, etc. 
plt.title('Tumor Volume Change over 45 Day Treatment')
plt.ylabel('% Tumour Volume Change')
xlabels = ['Capomulin','Infubinol', 'Ketapril', 'Placebo']
plt.xticks(np.arange(len(xlabels)), xlabels)
plt.axhline(color = 'black')

# Use functions to label the percentages of changes

def setLabel(count, value):
    if value < 0:
        y_coor = -5
    else:
        y_coor = 3.5
    plt.text(count, y_coor, str(int(value)) + '%', ha = 'center', color = 'white')

# Call functions to implement the function calls
for index in range(0,len(per_change_tuple)):
    setLabel(index,per_change_tuple[index][1])

data = [per_change_tuple[index][1] for index in range(0,len(per_change_tuple))]
plt.grid()
plt.bar(np.arange(len(xlabels)), 
        data, align='center',
        color = ['red' if data[r] > 0 else 'green' for r in np.arange(len(xlabels))]
       )

#print(fig1)
# Save the Figure
#fig1 = fig1.get_figure()
plt.savefig("tumor_change.png")
# Show the Figure
#plt.show()

