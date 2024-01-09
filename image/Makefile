push_stori_test:
	aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-west-1.amazonaws.com
	docker build -t stori-test-ecr .
	docker tag stori-test-ecr:latest <aws_account_id>.dkr.ecr.us-west-1.amazonaws.com/stori-test-ecr:latest
	docker push <aws_account_id>.dkr.ecr.us-west-1.amazonaws.com/stori-test-ecr:latest


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


# https://docs.docker.com/engine/reference/commandline/compose_down/
