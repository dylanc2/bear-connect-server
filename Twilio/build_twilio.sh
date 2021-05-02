docker network ls|grep bearconnect > /dev/null || docker network create --driver bridge bearconnect
docker stop bearconnect_twilio
docker rm   bearconnect_twilio
docker rmi bearconnect-twilio
docker build . -t bearconnect-twilio
docker run  -dit --name=bearconnect_twilio -e FLASK_APP=receivesms.py -p 5002:5000 --network bearconnect bearconnect-twilio
