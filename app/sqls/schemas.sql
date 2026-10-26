-- Supabase SQL Editor: run this first on a NEW study database.
-- Matches backend study app/schemas.sql. This does not create Auth accounts.
-- If public.users already exists, this intentionally fails without changing it.
BEGIN;
CREATE TABLE public.users (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL CHECK (char_length(btrim(name)) BETWEEN 1 AND 50),
    email text NOT NULL UNIQUE CHECK (email = lower(email)),
    password_hash text NOT NULL
);
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.users FROM PUBLIC, anon, authenticated;
REVOKE ALL ON SEQUENCE public.users_id_seq FROM PUBLIC, anon, authenticated;
COMMENT ON TABLE public.users IS 'Backend study users; separate from auth.users. Access through SQL Editor or a trusted backend DB connection.';
COMMIT;

-- After importing CSV OR running 02_seed_users.sql:
SELECT id, name, email FROM public.users ORDER BY id;
