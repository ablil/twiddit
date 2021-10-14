# Wooosh

A programmed bot to post the most hottest posts from subreddit r/woooosh to twitter

# How to use

create a credentials file called `credentails.json` and run the docker container.

Don't forget to:
* pass the credentials files to docker container
* mapp a volume for the `logs` directory

```
docker build -t woooosh:latest .
docker run -v $PWD/logs:/usr/src/app woooosh
```

# Todo

- [ ] multi-thread
- [ ] self-brand: like some tweet which contains the word woooosh or memej