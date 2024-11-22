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

## Database: Setting Up

First, run this command in the terminal to pull the latest mongo image:

```bash
docker pull mongodb/mongodb-community-server:latest
```

Then, instantiate a container from that image named 'mongodb':

```bash
docker run --name mongodb -d -p 27017:27017 mongodb/mongodb-community-server:latest
```

Make sure you are in outermost directory/the same directory as `sampledata.json`. Copy `sampledata.json` into a tmp folder in the mongo container:

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
docker exec -it mongodb mongsh
```
