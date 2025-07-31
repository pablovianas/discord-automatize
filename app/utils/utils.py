import discord

async def manage_user(
    interaction: discord.Interaction,
    discord_noob_role_id: str,
    discord_student_role_id: str,
    discord_classroom_role_id: str,
    discord_nickname_from_cademi: str
) -> None:
    """
    Gerencia a atribuição, edição de nickname e remoção de roles com base no sucesso da verificação.

    Args:
        interaction (discord.Interaction): A interação do Discord que contém o usuário e o guild.
        discord_noob_role_id (str): O ID da role "noob" a ser removida.
        discord_student_role_id (str): O ID da primeira role a ser adicionada.
        discord_classroom_role_id (str): O ID da segunda role a ser adicionada.
        discord_nickname_from_cademi (str): O nickname a ser atribuído ao usuário.

    Returns:
        None
    """
    guild = interaction.guild

    if not guild:
        print("Erro: A interação não está associada a um guild.")
        return

    if discord_noob_role_id and discord_student_role_id and discord_classroom_role_id:
        try:
            member = guild.get_member(interaction.user.id)
            if not member:
                member = await guild.fetch_member(interaction.user.id)

            noob_role = guild.get_role(int(discord_noob_role_id))
            student_role = guild.get_role(int(discord_student_role_id))
            classroom_role = guild.get_role(int(discord_classroom_role_id))

            if noob_role:
                await member.remove_roles(noob_role)
            if student_role and classroom_role:
                await member.add_roles(student_role, classroom_role)
                await member.edit(nick=discord_nickname_from_cademi)
            print(
                f"Role 'noob' removida e roles {student_role.name if student_role else 'N/A'}, {classroom_role.name if classroom_role else 'N/A'} adicionadas a {member.name}#{member.discriminator}"
            )
        except discord.Forbidden:
            print("Erro: O bot não tem permissão para gerenciar essas roles.")
        except discord.HTTPException as e:
            print(f"Erro ao gerenciar roles: {e}")
