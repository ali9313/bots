from config import *
def my_txtrep(a):
	with open("backend/m_replyy.txt","r",encoding="utf-8") as tx :
		for i in tx.readlines() :
			f_first= i.split(':')[0]
			if f_first == a.text :
				lio= i.split(':')[1]
				bot.reply_to(a,lio)