# Deploy the ExplainerDashboard into AWS EC2 and Docker

Upload the loadFiles.py into the AWS EC2 instance (using filezilia for example)

Download the needed files for the deployement by running the loadFile.py
```Shell
python3 loadFile.py
```

Build and run your docker container
```Shell
sudo docker-compose build
sudo docker-compose up
```

Then you can acces the ExplainerDashboard from your instance IPadress at port 5000