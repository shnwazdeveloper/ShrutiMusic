@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    A = await wlcm.find_one({"chat_id": chat_id})

    if A and A.get("disabled", False):
        return

    # Check if this is a NEW member joining (not a leave/ban/restriction event)
    new = member.new_chat_member
    old = member.old_chat_member

    # Only welcome if user is now a member/admin/owner
    new_status = new.status if new else None
    old_status = old.status if old else None

    # Skip if new status is not "member" or "administrator"
    if new_status not in (
        enums.ChatMemberStatus.MEMBER,
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        return

    # Skip if they were already a member before (not a fresh join)
    if old_status in (
        enums.ChatMemberStatus.MEMBER,
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        return

    user = new.user if new else member.from_user

    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"downloads/pp{user.id}.png"
        )
    except AttributeError:
        pic = "ShrutiMusic/assets/upic.png"

    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)

    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption=f"""🌟 <b>ᴡᴇʟᴄᴏᴍᴇ {user.mention}!</b>

📋 <b>ɢʀᴏᴜᴘ:</b> {member.chat.title}
🆔 <b>ʏᴏᴜʀ ɪᴅ:</b> <code>{user.id}</code>
👤 <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{user.username if user.username else "ɴᴏᴛ sᴇᴛ"}

<b><u>ʜᴏᴘᴇ ʏᴏᴜ ғɪɴᴅ ɢᴏᴏᴅ ᴠɪʙᴇs, ɴᴇᴡ ғʀɪᴇɴᴅs, ᴀɴᴅ ʟᴏᴛs ᴏғ ғᴜɴ ʜᴇʀᴇ!</u> 🌟</b>""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎵 ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🎵", url=f"https://t.me/{app.username}?startgroup=True")]
            ]),
        )
    except Exception as e:
        LOGGER.error(e)

    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception:
        pass
