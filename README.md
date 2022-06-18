# Twiddit - Twitter reddit bot

A Twitter bot that post the hottest posts from Reddit to Twitter.

## Get started

### Prerequisites

#### Create reddit app

Go to https://www.reddit.com/prefs/apps/, create a reddit app.
Set app type to **script** and set **redirect url** to localhost (this is mandatory even though we are not using it).

Make sure to save the client id (under app name) and the client secret, we are going to use them later.

#### Create Twitter app

Go to https://developer.twitter.com/en/portal/projects-and-apps and create a Twitter app,
copy the following keys adn make sure to save them somewhere we are going to use them later:

* consumer key
* consumer secret
* access token
* access token secret

### Usage

Clone the repo

```shell
$ git clone https://github.com/ablil/twiddit twiddit
```

Install requirements

```shell
$ pip install -r requirements.txt
```

Fill `.env` file with the keys you save before from Reddit and Twitter. and set the following
necessary parameters:

| param           | description                                            |
|-----------------|--------------------------------------------------------|
| bot_subreddit   | Sub-reddit to use for retrieving posts                 |
| bot_posts_limit | Number of posts to retrieve from Reddit each time      |
| bot_frequency   | Interval between each tweet in minutes                 |
| bot_hashtag     | List of hashtags to use when posting (comma seperated) |

**Run locally**

Before your run make sure you are in the root directory of the repository and `.env` is there.

```shell
$ python3 src/app.py
```

**Run with Docker**

Build Docker image

```shell
$ docker build -t twiddit:<mybotname> .
```

Run Docker container

```shell
$ docker run --name=<mybotname> -v <path/where/to/save/logs>:/usr/src/app/logs  twiddit:<mybotname>
```

*Whenever you change content of .env file, you have to re-build the image and start the container again*