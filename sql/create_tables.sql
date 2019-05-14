create table clicks(id SERIAL PRIMARY KEY, uid varchar, user_agent varchar, screen_x varchar, screen_y varchar, enqueued_at date);
create table impressions(id SERIAL PRIMARY KEY, uid varchar, user_agent varchar, enqueued_at date);

