from app.database import get_connection


def get_all_users(limit: int = 20):
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, name, email FROM public.users ORDER BY id LIMIT %s",
            (limit,),
        ).fetchall()


def get_user_by_id(user_id: int):
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, name, email FROM public.users WHERE id = %s",
            (user_id,),
        ).fetchone()


def create_user(name: str, email: str):
    with get_connection() as conn:
        return conn.execute(
            """INSERT INTO public.users (name, email, password_hash)
               VALUES (%s, %s, %s)
               RETURNING id, name, email""",
            (name, email, "!dummy-no-login"),
        ).fetchone()


def update_user_name(user_id: int, name: str):
    with get_connection() as conn:
        return conn.execute(
            """UPDATE public.users SET name = %s WHERE id = %s
               RETURNING id, name, email""",
            (name, user_id),
        ).fetchone()


def delete_user(user_id: int):
    with get_connection() as conn:
        return conn.execute(
            "DELETE FROM public.users WHERE id = %s RETURNING id",
            (user_id,),
        ).fetchone()
