import requests

# GithubPath of the model file
path_model = 'https://github.com/Sliders122/wildfire/blob/main/src/model/model_lgbm.pkl?raw=true'
# Save the model content in a local file
resp = requests.get(path_model)
with open("./model_lgbm.pkl", 'wb') as file:
    file.write(resp.content)

# GithubPath of the data file
path_csv = 'https://raw.githubusercontent.com/Sliders122/wildfire/main/src/model/df_model.csv'
# Save the data content in a local file
resp_csv = requests.get(path_csv)
with open("./df_model.csv", 'wb') as file:
    file.write(resp_csv.content)

# GithubPath of the dashboard loader
path_dashboard = 'https://raw.githubusercontent.com/Sliders122/wildfire/main/src/deployement/dashboard.py'
# Save the data content in a local file
resp_csv = requests.get(path_dashboard)
with open("./dashboard.py", 'wb') as file:
    file.write(resp_csv.content)

# GithubPath of the dockerfile
path_dockerfile = 'https://raw.githubusercontent.com/Sliders122/wildfire/main/src/deployement/Dockerfile'
# Save the data content in a local file
resp_csv = requests.get(path_dockerfile)
with open("./Dockerfile", 'wb') as file:
    file.write(resp_csv.content)

# GithubPath of the dockerfile
path_dockerfile = 'https://raw.githubusercontent.com/Sliders122/wildfire/main/src/deployement/docker-compose.yml'
# Save the data content in a local file
resp_csv = requests.get(path_dockerfile)
with open("./docker-compose.yml", 'wb') as file:
    file.write(resp_csv.content)
