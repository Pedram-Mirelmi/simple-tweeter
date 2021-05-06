CREATE DATABASE tweeter;
USE tweeter;
CREATE TABLE users
(
    user_id             INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username            VARCHAR(200) UNIQUE NOT NULL,
    password            VARCHAR(200) NOT NULL ,
    name                VARCHAR(200),
    create_date         DATE DEFAULT(NOW())
);


CREATE TABLE tweets
(
    tweet_id        INT UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
    tweet_text      VARCHAR(255) NOT NULL ,
    user_id         INT UNSIGNED NOT NULL ,
    created_at      TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE likes
(
    user_id         INT UNSIGNED NOT NULL ,
    tweet_id        INT UNSIGNED NOT NULL ,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ,
    FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id)
        ON DELETE CASCADE,
    PRIMARY KEY(user_id, tweet_id)
);

CREATE VIEW tweets_show AS
SELECT
       t.tweet_id,
       u.username,
       u.name,
       t.tweet_text,
       t.created_at,
       COUNT(l.user_id) AS "likes"
FROM tweets t
         JOIN users u
              ON u.user_id = t.user_id
         LEFT JOIN likes l
              ON t.tweet_id = l.tweet_id
GROUP BY t.tweet_id;

CREATE TABLE comments
(
    tweet_id        INT UNSIGNED NOT NULL ,
    user_id         INT UNSIGNED NOT NULL ,
    comment_text   VARCHAR(127) NOT NULL ,
    created_at      TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tweet_id, user_id),
    FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);
