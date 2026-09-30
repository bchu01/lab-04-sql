CREATE TABLE users(
	user_id INT PRIMARY KEY,
	post_id INT,
	age INT,
	name VARCHAR(15),
	bio TEXT,
	birthday DATETIME
);

CREATE TABLE posts(
	post_id INT PRIMARY KEY,
	user_id INT,
	likes INT,
	title VARCHAR(15),
	caption TEXT,
	date_posted DATETIME,
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- user inserts
INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (1, 101, 19, 'Brandon', 'Data science student', '2007-10-11 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (2, 102, 20, 'Alex', 'Computer science major', '2006-03-15 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (3, 103, 21, 'Maya', 'Loves photography', '2005-07-22 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (4, 104, 19, 'Jordan', 'Basketball fan', '2007-01-30 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (5, 105, 22, 'Chris', 'Coffee enthusiast', '2004-11-12 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (6, 106, 20, 'Sarah', 'Music and art lover', '2006-05-18 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (7, 107, 21, 'Daniel', 'Future engineer', '2005-09-03 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (8, 108, 19, 'Emma', 'Traveler and foodie', '2007-02-14 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (9, 109, 23, 'Ryan', 'Fitness enthusiast', '2003-06-27 00:00:00');

INSERT INTO users (user_id, post_id, age, name, bio, birthday)
VALUES (10, 110, 20, 'Sophia', 'Aspiring designer', '2006-12-05 00:00:00');

-- post inserts
INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (101, 1, 45, 'First Post', 'Excited to start college!', '2026-09-01 10:30:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (102, 2, 72, 'Coding Day', 'Working on my new project.', '2026-09-02 14:20:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (103, 3, 91, 'New Camera', 'Finally got my new camera!', '2026-09-03 16:45:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (104, 4, 63, 'Game Night', 'Great game with friends.', '2026-09-04 20:10:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (105, 5, 38, 'Coffee Time', 'Trying a new coffee shop.', '2026-09-05 09:15:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (106, 6, 84, 'Concert', 'Amazing night with friends!', '2026-09-06 22:30:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (107, 7, 55, 'Engineering', 'Learning something new today.', '2026-09-07 13:00:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (108, 8, 103, 'Travel Day', 'Exploring somewhere new.', '2026-09-08 11:45:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (109, 9, 67, 'Gym Session', 'Getting stronger every day.', '2026-09-09 18:20:00');

INSERT INTO posts (post_id, user_id, likes, title, caption, date_posted)
VALUES (110, 10, 49, 'New Design', 'Working on a new design project.', '2026-09-10 15:35:00');


