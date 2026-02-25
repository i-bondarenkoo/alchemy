SELECT users.username, users.email, users.created_at, users.id 
FROM users
WHERE users.id = 1

SELECT posts.user_id AS posts_user_id, posts.title AS posts_title, posts.body AS posts_body, posts.id AS posts_id
FROM posts
WHERE posts.user_id IN (1)

SELECT posts_1.id AS posts_1_id, tags.name AS tags_name, tags.color AS tags_color, tags.id AS tags_id
FROM posts AS posts_1 JOIN post_tag_table AS post_tag_table_1 ON posts_1.id = post_tag_table_1.post_id JOIN tags ON tags.id = post_tag_table_1.tag_id
WHERE posts_1.id IN (1, 2)
-- 

SELECT tags.name, tags.color, tags.id
FROM tags
WHERE tags.id = 3

SELECT tags_1.id AS tags_1_id, posts.title AS posts_title, posts.body AS posts_body, posts.user_id AS posts_user_id, posts.id AS posts_id, users_1.username AS users_1_username, users_1.email AS users_1_email, users_1.created_at AS users_1_created_at, users_1.id AS users_1_id
FROM tags AS tags_1 
JOIN post_tag_table AS post_tag_table_1 ON tags_1.id = post_tag_table_1.tag_id 
JOIN posts ON posts.id = post_tag_table_1.post_id 
LEFT OUTER JOIN users AS users_1 ON users_1.id = posts.user_id
WHERE tags_1.id IN (3)





SELECT users.username, users.email, users.created_at, users.id 
FROM users
WHERE users.id = 1

SELECT posts.user_id AS posts_user_id, posts.title AS posts_title, posts.body AS posts_body, posts.id AS posts_id
FROM posts
WHERE posts.user_id IN (1)

SELECT post_tags.post_id AS post_tags_post_id, post_tags.tag_id AS post_tags_tag_id, post_tags.created_at AS post_tags_created_at, 
post_tags.id AS post_tags_id, tags_1.name AS tags_1_name, tags_1.color AS tags_1_color, tags_1.id AS tags_1_id

FROM post_tags LEFT OUTER JOIN tags AS tags_1 ON tags_1.id = post_tags.tag_id
WHERE post_tags.post_id IN (1, 2)

-- 
SELECT tags.name, tags.color, tags.id
FROM tags
WHERE tags.id = 4

SELECT post_tags.tag_id AS post_tags_tag_id, post_tags.post_id AS post_tags_post_id, post_tags.created_at AS post_tags_created_at, 
post_tags.id AS post_tags_id, users_1.username AS users_1_username, users_1.email AS users_1_email, users_1.created_at AS users_1_created_at, 
users_1.id AS users_1_id, posts_1.title AS posts_1_title, posts_1.body AS posts_1_body, posts_1.user_id AS posts_1_user_id, posts_1.id AS posts_1_id
FROM post_tags LEFT OUTER JOIN posts AS posts_1 ON posts_1.id = post_tags.post_id LEFT OUTER JOIN users AS users_1 ON users_1.id = posts_1.user_id
WHERE post_tags.tag_id IN (4)
