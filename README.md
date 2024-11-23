![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![ML Client](https://github.com/software-students-fall2024/4-containers-kablam/actions/workflows/ml-tests.yaml/badge.svg)

# Swear Jar Web App

## Description

A web app that accesses the user’s microphone and detects when a swear word is said. A swear jar/total swear count is displayed.

## Team Members

- Madison Phung, [Github](https://github.com/mkphung29)
- Stephen Spencer-Wong, [Github](https://github.com/StephenS2021)
- William Xie, [Github](https://github.com/seeyeh)
- May Zhou, [Github](https://github.com/zz4206)

## Docker Network
Before starting any containers, run this command to create the Docker network swear_jar
```bash
docker network create swear_jar
```

## Database: Setting Up

First, run this command in the terminal to pull the latest mongo image:

```bash
docker pull mongodb/mongodb-community-server:latest
```

Then, instantiate a container from that image named `mongodb` in a network called `swear_jar`:

```bash
docker run --name mongodb -d -p 27017:27017 --network swear_jar mongo
```

Make sure you are in outermost directory/the same directory as `sampledata.json`. `sampledata.json` contains some starter "swear words" with existing counts to check if the web app's connection to the mongo container was successful. Your jar should not start empty. Copy `sampledata.json` into a tmp folder in the mongo container:

```bash
docker cp sampledata.json mongodb:/tmp/sampledata.json
```

Now that the JSON file is in the container, we will use `mongoimport` to import the JSON data into a 'swearDB' database inside a 'swears' collection:

```bash
docker exec mongodb mongoimport -d swearDB -c swears --file /tmp/sampledata.json
```

The database is now all setup!

### Some helpful reminders

If the mongodb container stops, to restart it:

```bash
docker restart mongodb
```

To start mongosh through the container:

```bash
docker exec -it mongodb mongosh
```

## Web App: Setting Up

Build the image from the Dockerfile. While in the `web_app` directory:

```bash
docker build -t web-app .
```

Now that you have the `web-app` image (check by running `docker images` and it should appear in the list), instantiate a new container called `webapp` in the `swear_jar` network:

```bash
docker run --name webapp -d -p 5000:5000 --network swear_jar web-app
```

If we go to `localhost:5000`, we should be able to see the jar interface now. Before we can start enabling microphone access, we need to set up our Speech Recognition container first.

## Speech Recognition: Setting Up

Build the image from the Dockerfile. While in the `src/machine_learning_client` directory:

```bash
docker build -t speech-recog .
```

Now that you have the `speech-recog` image (check by running `docker images` and it should appear in the list), instantiate a new container called `speech` in the `swear_jar` network:

```bash
docker run --name speech -d -p 8080:8080 --network swear_jar speech-recog
```

We're all set to run the app now!

## How to Use

Go to `localhost:5000` and click on the 'Request Microphone Access' button - your browser will prompt you to allow microphone use on the page. Once allowed, you can try saying anything! The words the jar currently detects as "swear words" are:

- hello
- apple
- orange
- goodbye
- test

Speak these words loud and clear and watch the jar fill up!

If you want to add to the list of detectable swear words, you can add to the list of strings at [line 49 of speech_recog.py in src/machine_learning_client.](https://github.com/software-students-fall2024/4-containers-kablam/blob/b4afdd01ac248f0cc8bfd75250765ec2307fe4de/src/machine_learning_client/speech_recog.py#L49)
