from config import *
def insert_rep(a):
	tmsg=a.text
	tmsg=tmsg.split()[1:]
	tmsg=" ".join(map(str , tmsg))
	z=open("backend/m_replyy.txt","a",encoding="utf-8")
	z.write("\n")
	z.write(tmsg)
	z.close()