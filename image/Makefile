
push-stori:
	aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 992382549868.dkr.ecr.us-west-1.amazonaws.com
	docker build -t stori-test-ecr .
	docker tag stori-test-ecr:latest 992382549868.dkr.ecr.us-west-1.amazonaws.com/stori-test-ecr:latest
	docker push 992382549868.dkr.ecr.us-west-1.amazonaws.com/stori-test-ecr:latest


docker-prune:
	docker compose down                  # Stops containers and removes containers, networks, volumes, and images created by up.
	# docker stop $(docker ps -a -q)       # stop all the containers
	# docker rm $(docker ps -a -q)         # remove all the containers
	docker system prune                  # -a --volumes
	docker-compose up


docker-prune-volumes:
	docker compose down                  # Stops containers and removes containers, networks, volumes, and images created by up.
	# docker stop $(docker ps -a -q)       # stop all the containers
	# docker rm $(docker ps -a -q)         # remove all the containers
	docker system prune -a --volumes
	docker-compose up

bash-lambda:
	docker exec -it stori-lambda bash

bash-db:
	docker exec -it stori-db bash
# psql -h localhost -U postgres

test-local:
	curl "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{}'
	curl "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{"body": "{\"emails\":\"ente011@gmail.com\"}"}'


test-deploy:
	curl "${AWS_INVOKE_URL}" -d '{}'
	curl "${AWS_INVOKE_URL}" -d '{"emails":"ente011@gmail.com"}'


# https://docs.docker.com/engine/reference/commandline/compose_down/
