## Instructions to build, run, test

* Build: Dockerfile and /.dockerignore have all libraries and packages necessary to run the server in a container environment.  Use ```./build_db.sh``` to run the build script 
* Run:
 
  -The build script will check to see if the network bearconnect exists, and if not will create one. 
  
  -**CAUTION** Build script will automatically stop any container w/ ```bearconnect_db``` name, delete it, the delete the container image.  
  -The script will then build a node/mongo db server image from scratch. 
  
  -Finally, will run the container image, add it to the bearconnect network, routing port 5000 to 5001 for practical use
  
* Test: Admins can send a dummy user JSON (see below) to postman at http://localhost:5001/users/add to check if the server is setup properly and listening:
   ```json
   {
    "_id": "ef3c201c-f08f-4832-9aab-54287e011b6a",
    "name": "alex",
    "year": "sophomore",
    "major": "CS",
    "selectedClass": "INFO 253B",
    "meetingTimes": "weekdays",
    "studyTimes": "early_bird",
    "studyStyle": "debugging_master"
   }
    ```
