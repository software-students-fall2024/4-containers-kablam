![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

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
