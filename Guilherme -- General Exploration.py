# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## General stuff (Using the first 2 hours of the month as a sample -- uploaded to teams)

import pandas as pd

df1 = pd.read_json('2023-04-01-0.json.gz', lines=True)
df2 = pd.read_json('2023-04-01-1.json.gz', lines=True)

df1

df2

concatenated_df = pd.concat([df1, df2], ignore_index=True)

concatenated_df

concatenated_df['actor'][2]

# ## Email Analysis

# +
import json
from graphqlclient import GraphQLClient

access_token = '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'
endpoint_url = 'https://api.github.com/graphql'
client = GraphQLClient(endpoint_url)
client.inject_token('Bearer ' + access_token)

def get_user_email(username):
    query = """
    query($username: String!) {
      user(login: $username) {
        email
      }
    }
    """
    variables = {"username": username}

    result = client.execute(query, variables)
    response_json = json.loads(result)

    if "errors" in response_json:
        error_message = response_json.get("errors")[0].get("message")
        print(f"Error querying user {username}: {error_message}")
        return None

    data = response_json["data"]["user"]
    email = data.get("email")
    return email


emails = []
for row in concatenated_df['actor']:
    login = row.get('login')
    if login:
        email = get_user_email(login)
        if email:
            emails.append(email)
        else:
            print(f"No email found for user {login}")

print(emails)
# -

print(emails)

# +
it_emails = []

for email in emails:
    if email.endswith(".ca"):
        it_emails.append(email)

print("Emails ending with '.it':")
for it_email in it_emails:
    print(it_email)

count_it_emails = len(it_emails)
print(f"Number of emails ending with '.it': {count_it_emails}")
# -

# ## Getting rid of Github Bot commits

filtered_df = concatenated_df[~concatenated_df['actor'].apply(lambda x: x.get('login').endswith('[bot]'))]
filtered_df

filtered_df.reset_index(drop=True, inplace=True)

filtered_df['repo'][0]

filtered_df['payload'][0]


# ## Email Analysis with Resulting dataframe only consisting of users with .it emails (Testing to see if it works with only the first ".it" email that shows up)

# +
def get_user_email(username):
    query = """
    query($username: String!) {
      user(login: $username) {
        email
      }
    }
    """
    variables = {"username": username}

    result = client.execute(query, variables)
    response_json = json.loads(result)

    if "errors" in response_json:
        error_message = response_json.get("errors")[0].get("message")
        print(f"Error querying user {username}: {error_message}")
        return None

    data = response_json["data"]["user"]
    email = data.get("email")
    return email

first_email_with_it = None
for i, row in enumerate(concatenated_df['actor']):
    login = row.get('login')
    if login:
        email = get_user_email(login)
        if email and email.endswith('.ca'):
            first_email_with_it = email
            break

if first_email_with_it:
    new_dataset = concatenated_df.iloc[[i]]
    print(new_dataset)
else:
    print("No email ending with '.it' found in the dataset")
# -

new_dataset

get_user_email('francisbilo')


# ## Getting repository languages from API

def get_repository_languages(owner, name):
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        name
        languages(first: 10) {
          nodes {
            name
          }
        }
      }
    }
    """
    variables = {"owner": owner, "name": name}

    result = client.execute(query, variables)
    response_json = json.loads(result)

    if "errors" in response_json:
        error_message = response_json.get("errors")[0].get("message")
        print(f"Error querying repository languages: {error_message}")
        return None

    repository = response_json["data"]["repository"]
    languages = repository["languages"]["nodes"]
    return languages


get_repository_languages('jhsul','battle-craft-rl')


# ## Get new Dataframe made only of repos that have Python as language (Unfinished on the new dataframe creation part, still dodgy and only 50 to test)

# +
def get_repository_languages(owner, name):
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        name
        languages(first: 10) {
          nodes {
            name
          }
        }
      }
    }
    """
    variables = {"owner": owner, "name": name}

    result = client.execute(query, variables)
    response_json = json.loads(result)

    if "errors" in response_json:
        error_message = response_json.get("errors")[0].get("message")
        print(f"Error querying repository languages: {error_message}")
        return None

    repository = response_json["data"]["repository"]
    languages = repository["languages"]["nodes"]
    return languages

python_repositories_df = filtered_df[[]]  

for index, repo_data in filtered_df.iterrows():
    if index >= 50:
        break 
    
    repo_info = repo_data['repo']
    print(repo_info)
    repo_id = repo_info['id']
    repo_stuff = repo_info['name'].split('/')
    repo_owner = repo_stuff[0]
    repo_name = repo_stuff[1]

   
    repository_languages = get_repository_languages(repo_owner, repo_name)

    if repository_languages:
        python_language_present = any(lang['name'] == 'Python' for lang in repository_languages)

        if python_language_present:
            python_repositories_df = python_repositories_df.append(repo_data, ignore_index=True)


print(python_repositories_df)
# -

python_repositories_df


