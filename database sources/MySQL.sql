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

drop table tweets_likes;

CREATE TABLE tweets_likes
(
    user_id         INT UNSIGNED NOT NULL ,
    tweet_id        INT UNSIGNED NOT NULL ,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ,
    FOREIGN KEY(tweet_id) REFERENCES tweets(tweet_id)
        ON DELETE CASCADE,
    PRIMARY KEY(user_id, tweet_id)
);

CREATE TABLE comments
(
    comment_id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
    tweet_id        INT UNSIGNED NOT NULL ,
    user_id         INT UNSIGNED NOT NULL ,
    comment_text   VARCHAR(127) NOT NULL ,
    created_at      TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

drop table comments_likes;
CREATE TABLE comments_likes
(
    user_id         INT UNSIGNED NOT NULL ,
    comment_id      INT UNSIGNED NOT NULL ,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ,
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
        ON DELETE CASCADE,
    PRIMARY KEY (user_id, comment_id)
);

drop VIEW comments_show;
CREATE VIEW comments_show AS
SELECT
       t.tweet_id,
       c.comment_id,
       u.username,
       c.comment_text,
       c.created_at,
       COUNT(cl.user_id) AS "comments_likes"
FROM comments c
         JOIN users u
              ON c.user_id = u.user_id
         JOIN tweets t
             ON t.tweet_id = c.tweet_id
         LEFT JOIN comments_likes cl
              ON c.comment_id = cl.comment_id
GROUP BY c.comment_id
ORDER BY c.comment_id DESC;


drop view tweets_show;

CREATE VIEW tweets_show AS
SELECT
       u.user_id,
       t.tweet_id,
       u.username,
       t.tweet_text,
       t.created_at,
       COUNT(tl.user_id)   AS "tweets_likes",
       COUNT(c.comment_id) AS "comments"
FROM tweets t
     JOIN users u
            ON u.user_id = t.user_id
     LEFT JOIN tweets_likes tl
            ON t.tweet_id = tl.tweet_id
     LEFT JOIN comments c
            ON t.tweet_id = c.tweet_id
GROUP BY t.tweet_id
ORDER BY t.tweet_id DESC;

