import sqlite3

import discord

async def create_connection():
    with sqlite3.connect("./app/db/usuarios_discord.db") as conn:
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS usuarios_discord (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id TEXT,
                nome_cademi TEXT,
                email_cademi TEXT,
                id_cademi TEXT,
                discord_username TEXT,
                cademi_user_created_at DATETIME,
                timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
            )"""
        )
        conn.commit()

async def save_user(interaction: discord.Interaction, nome_cademi: str, email_cademi: str, id_cademi: int, cademi_user_created_at: str):
    with sqlite3.connect('./app/db/usuarios_discord.db') as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO usuarios_discord (discord_id, nome_cademi, email_cademi, id_cademi, discord_username, cademi_user_created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (interaction.user.id, nome_cademi, email_cademi, id_cademi, interaction.user.name, cademi_user_created_at)
        )
        conn.commit()

async def check_if_user_exists(discord_id: int):
    with sqlite3.connect('./app/db/usuarios_discord.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios_discord WHERE discord_id = ?", (discord_id,))
        return c.fetchone() is not None