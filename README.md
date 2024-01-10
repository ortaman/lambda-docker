
## Installation
- Install [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository1) 
- Install [docker descktop](https://docs.docker.com/desktop/install/ubuntu/)


## Set up and run the project:
- Clone the repository to your local machine:
```bash
git clone https://github.com/ortaman/lambda-docker.git
```

- Add the environment variables in the console:
```
- export EMAIL_HOST=smtp_host
- export EMAIL_PORT=smtp_port
- export EMAIL_FROM=email_from@gmail.com"
- export EMAIL_USER=smtp_username
- export EMAIL_PASS=smtp_password

- Open a terminal and go to image folder and run:
```bash
docker compose up
```

- Open a new terminal and run the next command with the email to send the information:
```bash
curl "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{"body": "{\"emails\":\"username@domain.com\"}"}'
```
