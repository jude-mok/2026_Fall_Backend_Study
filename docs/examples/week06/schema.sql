CREATE TABLE users (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL CHECK (char_length(btrim(name)) BETWEEN 1 AND 50),
    email text NOT NULL UNIQUE CHECK (email = lower(email)),
    password_hash text NOT NULL
);
