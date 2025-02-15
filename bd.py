import aiosqlite


async def create_table():
    db = await aiosqlite.connect("game_bot.db")
    await db.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY, 
                username TEXT, 
                cnb_wins INTEGER, cnb_losses INTEGER, cnb_draws INTEGER,
                bac_record INTEGER,
                cao_draws INTEGER, cao_wins_crosses INTEGER, cao_wins_nulls INTEGER)""")

    await db.commit()
    await db.close()


async def create_user(user_data):
    db = await aiosqlite.connect("game_bot.db")
    user1 = await db.execute(f"SELECT id,username FROM users WHERE id={user_data.id}")
    user = await user1.fetchone() 
    if not user:
        await db.execute(
            f'INSERT INTO users VALUES({user_data.id}, "{user_data.name}", 0, 0, 0, 0, 0, 0, 0)'
        )
        await db.commit()
    await db.close()


async def update_cnb(user_id, result):
    db = await aiosqlite.connect("game_bot.db")
    await db.execute(f"UPDATE users SET {result} = {result} + 1 WHERE id = {user_id}")
    await db.commit()
    await db.close()


async def get_rate_cnb():
    db = await aiosqlite.connect("game_bot.db")
    user1 = await db.execute("SELECT username, cnb_wins, cnb_draws, cnb_losses FROM users")
    users_data = await user1.fetchall()  # [('grisha', 4, 5, 7 )]
    lst = []
    for user in users_data:
        total_games = user[1] + user[2] + user[3]
        percent = user[1] / total_games * 100
        user_lst = [user[0], percent]
        lst.append(user_lst)
    lst.sort(key = lambda x: x[1], reverse=True)
    return lst


async def update_bak(user_id, record):
    db = await aiosqlite.connect("game_bot.db")
    user1 = await db.execute(f"SELECT bac_record FROM users WHERE id = {user_id}")
    bd_record = await user1.fetchone()
    if record > bd_record[0]:
        await db.execute(f"UPDATE users SET bac_record = {record} WHERE id = {user_id}")
    await db.commit()
    await db.close()


async def get_rate_bak() -> list:
    db = await aiosqlite.connect("game_bot.db")
    user1 = await db.execute("SELECT username, bac_record, id FROM users")
    users_data = await user1.fetchall() 
    users_data.sort(key=lambda x: x[1], reverse=True)
    return users_data


async def update_cao(user_id, result):
    db = await aiosqlite.connect("game_bot.db")
    if result == 'cao_cross':
        await db.execute(f"UPDATE users SET cao_wins_crosses = cao_wins_crosses + 1 WHERE id = {user_id}") 
    elif result == 'cao_nulls':
        await db.execute(f"UPDATE users SET cao_wins_nulls = cao_wins_nulls + 1 WHERE id = {user_id}")
    else:
        await db.execute(f"UPDATE users SET cao_draws = cao_draws + 1 WHERE id = {user_id}")
    await db.commit()
    await db.close()


async def get_rate_cao(user_id):
    db =  await aiosqlite.connect("game_bot.db")
    user_cur = await db.execute(f"SELECT cao_wins_crosses, cao_wins_nulls, cao_draws FROM users WHERE id = {user_id}")
    user = await user_cur.fetchone()
    right_user = f'Победы крестиков - {user[0]} \n Победы ноликов - {user[1]} \n Ничьи - {user[2]}'
    return right_user


if __name__ == "__main__":
    get_rate_cnb()
    get_rate_bak()
    get_rate_cao()
