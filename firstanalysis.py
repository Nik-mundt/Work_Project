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

import pandas as pd
df = pd.read_json("data/2015-04-01-15.json.gz", lines=True)
df

df.info()

df["actor"][0]

df["repo"][0]

df["payload"][0]

df2 = pd.read_json("tt.gz", lines=True)
df2

df2["actor"][0]

df2["repo"][1]

df2["payload"][1]

df2["payload"][2]

df2["payload"][3]

df2["payload"][4]

df2["payload"][5]

from github import Github

g = Github(login_or_token="----", password="----")

user = g.get_user("ishuduwal")

print(user.name)
print(user.created_at)
print(user.location)

user = g.get_user("FlorBera")

print(user.name)
print(user.created_at)
print(user.location)
print(user.email)


