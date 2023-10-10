#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install --upgrade google-cloud-bigquery')


# To get the credential.json do the following:
# 1. Go to Google API -> choose BigQuery API
# https://console.cloud.google.com/apis/dashboard
# 2. Create a project and activate the API
# 3. Go to login credentials and create a service Account
# 4. Download the credentials as json and save it in the data folder (we don't sync the data folder so its save)
# 5. Change the name of the credentials path to your id (or should we all have the same?)

# In[91]:


from google.cloud import bigquery
from google.oauth2 import service_account

# Set up credentials and client
credentials_path = 'data/work-thesis-7b6f35ce5dfc.json'
credentials = service_account.Credentials.from_service_account_file(credentials_path)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Example Query
query = """
    SELECT *
    FROM `bigquery-public-data.github_repos.sample_commits`
"""

# Execute the query
query_job = client.query(query)
df = query_job.to_dataframe()

# Displaying first few rows of the DataFrame
print(df.head())


# In[95]:


df.to_csv("data/sample_commits_full.csv")


# In[92]:


df.committer[0]


# In[102]:


df.committer[0]["date"].month


# In[104]:


df.committer[0]["date"].year


# In[105]:


import datetime
# Convert timestamp to datetime object
dt_object = df.committer[0]["date"]

# Extract the year
year = dt_object.year
month = dt_object.month

year, month


# In[106]:


df.columns


# In[ ]:


df.describe()


# ## Big Dataset: Proceed with caution
# Going on the Big Dataset and trying to get all dara for April 2023
# -> still no success as it is too much

# In[ ]:


#    WHERE 
#      EXTRACT(YEAR FROM TIMESTAMP_SECONDS(committer.date.seconds)) = 2023 AND 
#      EXTRACT(MONTH FROM TIMESTAMP_SECONDS(committer.date.seconds)) = 4;
query = """
    SELECT committer, repo_name, subject, message,
    FROM `bigquery-public-data.github_repos.commits`
    WHERE 
        EXTRACT(YEAR FROM TIMESTAMP_SECONDS(committer.date.seconds)) = 2023 AND 
        EXTRACT(MONTH FROM TIMESTAMP_SECONDS(committer.date.seconds)) = 4 AND
        EXTRACT(DAY FROM TIMESTAMP_SECONDS(committer.date.seconds)) BETWEEN 1 AND 2 AND
        RAND() <= 0.01
    LIMIT 5000;
"""

# Execute the query
query_job = client.query(query)
df_april = query_job.to_dataframe()


# In[ ]:


df_april.committer[0]


# In[ ]:


import datetime
# Convert timestamp to datetime object
dt_object = datetime.datetime.utcfromtimestamp(df_april.committer[0]["date"]["seconds"])

# Extract the year
year = dt_object.month
year


# In[ ]:


import pandas as pd
# Extract unique repo names
unique_repo_names = list(pd.Series([repo for sublist in df_april['repo_name'] for repo in sublist]).unique())

# Extract unique committer names
unique_committer_names = list(df_april['committer'].apply(lambda x: x['name']).unique())

unique_repo_names, unique_committer_names

