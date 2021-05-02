## Instructions to build, run, test

* Build: Dockerfile and /.dockerignore have all libraries and packages necessary to run the server in a container environment.  Use ```./build_twilio.sh``` to run the build script 
* Run:
 
  -The build script will check to see if the network bearconnect exists, and if not will create one. 
  
  -**CAUTION** Build script will automatically stop any container w/ ```bearconnect_twilio``` name, delete it, the delete the container image.  
  -The script will then build a node/mongo db server image from scratch. 
  
  -Finally, will run the container image, add it to the bearconnect network, routing port 5000 to 5002 for practical use
  
  * Test: TBD
