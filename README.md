# TCP Traffic Analyzer

## Description

This application allows you to intercept traffic in real time and look for suspicious activity in packets using regular expressions

## Usage
To use this you need:

- Clone repository
````
git clone https://github.com/logalexus/TTA.git && cd TTA
````
- Go to **.env** and specify the interface and login and password
````
# Interface to capture on:
TTA_INTERFACE=enp0s3

# Web creds
TTA_LOGIN=login
TTA_PASSWORD=pass
````
- Start app
````
docker compose up -d
````
- Go to web 
````
http://localhost:8000
````
- Next, we indicate the service port that we will monitor

![image](https://github.com/logalexus/TTA/assets/83642746/2be14f0f-b360-4423-820a-8f490e6e4b67)

- PROFIT

## Preview

![image](https://github.com/logalexus/TTA/assets/83642746/400adcaa-bcd9-46a6-8848-38c28812743f)

![image](https://github.com/logalexus/TTA/assets/83642746/3ab60d5b-831f-4aa0-97f3-5e89683680ae)


## License

MIT License
