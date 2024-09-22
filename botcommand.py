from config import *
def my_cmd(a):
	if a.text=="/ban":
		bnn=bot.ban_chat_member(a.chat.id,a.reply_to_message.from_user.id)
		if bnn:
			bot.send_message(a.chat.id,"تم دفر:"+"  @"+ a.reply_to_message.from_username)