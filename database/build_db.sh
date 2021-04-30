docker network ls|grep bearconnect > /dev/null || docker network create --driver bridge bearconnect
docker stop bearconnect_db
docker rm   bearconnect_db
docker rmi bearconnect-db
docker build . -t bearconnect-db
docker run -dit --name=bearconnect_db -p 5001:5000 --network bearconnect -d bearconnect-db
