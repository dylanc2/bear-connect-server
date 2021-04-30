# Bear Connect Mongo Database Server

Members: Justin Norman, Dylan Chow, Elaine Wang, Hongyang Zheng, Nidhi Kakulawaram

[Description by @DylanChow]

## Instructions to build, run test

* Build: Dockerfile and /.dockerignore have all libraries and packages necessary to run the server in a container environment.  Use ```./build_db.sh``` to run the build script 
* Run: 
  -The build script will check to see if the network bearconnect exists, and if not will create one. 
  -**CAUTION** Build script will automatically stop any container w/ ```bearconnect_db``` name, delete it, the delete the container image.  
  -The script will then build a node/mongo db server image from scratch. 
  -Finally, will run the container image, add it to the bearconnect network, routing port 5000 to 5001 for practical use
  
* Test: Admins can send a dummy user JSON (see below) to postman at http://localhost:5001/users/add to check if the server is setup properly and listening:
   ```json
   {
    "id": "UUID",
    "name": "alex",
    "year": "sophomore",
    "major": "senior",
    "classes": "info253b",
    "studyTime": " early_bird",
    "meetingTimes": "weekdays",
    "studyStyle": "debugging master"
}
```
