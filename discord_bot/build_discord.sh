docker network ls|grep bearconnect > /dev/null || docker network create --driver bridge bearconnect
docker stop bearconnect_discord
docker rm   bearconnect_discord
docker rmi bearconnect-discord
docker build . -t bearconnect-discord
docker run  -dit --name=bearconnect_discord -e FLASK_APP=quart_discord_bot.py -p 5003:5000 --network bearconnect bearconnect-discord
