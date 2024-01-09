push_stori_test:
	aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 992382549868.dkr.ecr.us-west-1.amazonaws.com
	docker build -t stori-test-ecr .
	docker tag stori-test-ecr:latest 992382549868.dkr.ecr.us-west-1.amazonaws.com/stori-test-ecr:latest
	docker push 992382549868.dkr.ecr.us-west-1.amazonaws.com/stori-test-ecr:latest


docker_prune:
	docker compose down                  # Stops containers and removes containers, networks, volumes, and images created by up.
	docker stop $(docker ps -a -q)       # stop all the containers
	docker rm $(docker ps -a -q)         # remove all the containers
	docker system prune                  # -a --volumes
	docker-compose up


docker_prune_with_volumes:
	docker compose down                  # Stops containers and removes containers, networks, volumes, and images created by up.
	docker stop $(docker ps -a -q)       # stop all the containers
	docker rm $(docker ps -a -q)         # remove all the containers
	docker system prune -a --volumes
	docker-compose up


test_local:
	curl "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{}'
	curl "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{"body": "{\"emails\":\"ente011@gmail.com\"}"}'


test_deploy:
	curl "${AWS_INVOKE_URL}" -d '{}'
	curl "${AWS_INVOKE_URL}" -d '{"emails":"ente011@gmail.com"}'


# https://docs.docker.com/engine/reference/commandline/compose_down/
