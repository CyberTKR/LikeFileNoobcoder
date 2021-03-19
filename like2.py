_B='db_postid.txt'
_A='DESKTOPWIN\t6.0.3\tDESKTOPWIN\t10.0'

from linepy import *
import json,time,os,threading,asyncio,random
access=['']
postid=str(open(_B,'r').read()).split('\n')
token=str(open('db_token.txt','r').read()).split('\n')
picture=0

def loginClient():global bot,poll;bot=LINE(token[0],appName=_A);poll=OEPoll(bot)
def operationStart(op):
	B='bot_pict.txt';A=' ';global picture
	if op.type not in[25,26]:return
	msg=op.message
	if msg.contentType==0:
		text=msg.text
		if text.lower()=='check':
			if msg._from in access:bot.sendMessage(msg._from,"ACTIVE WITH STATUSMESSAGE ACCESS 'NB'")
		elif text.lower().startswith('change '):
			if msg._from in access:0
			else:return
			changed=text.split(A)[1].lower()
			if changed=='name':
				newName=text.split(' name ')[1];bot.sendMessage(msg._from,'Waiting for change name....')
				def changeName():
					xxx=0
					for x in token:
						if xxx==0:xxx+=1
						else:
							try:ch=LINE(x,appName=_A);cp=ch.getProfile();cp.displayName=newName;ch.updateProfile(cp)
							except:pass
					return bot.sendMessage(msg._from,f"All bot set name to `{newName}`")
				threading.Thread(target=changeName).start()
			elif changed=='status':
				newStatus=text.split(' status ')[1];bot.sendMessage(msg._from,'Waiting for change status....')
				def changeStatus():
					xxx=0
					for x in token:
						if xxx==0:xxx+=1
						else:
							try:ch=LINE(x,appName=_A);cp=ch.getProfile();cp.statusMessage=newStatus;ch.updateProfile(cp)
							except:pass
					return bot.sendMessage(msg._from,f"All bot set status to {newStatus}")
				threading.Thread(target=changeStatus).start()
			elif changed=='pict':picture=1;return bot.sendMessage(msg._from,'Please send a photo to set as Avatar Bot!')
			else:return bot.sendMessage(msg._from,f"Keyword `{text.split(A)[1]}` not found!\nMaybe u think ['name', 'status', 'pict']")
		else:return
	elif msg.contentType==1:
		if'nb'in bot.getContact(msg._from).statusMessage.lower():0
		else:return
		if picture==1:
			try:pathPhoto=bot.downloadObjectMsg(msg.id,saveAs=B)
			except:return bot.sendMessage(msg._from,'Im sorry... Please send photo again :(')
			bot.sendMessage(msg._from,'Waiting for change avatar bot....')
			def changePict():
				xxx=0
				for x in token:
					if xxx==0:xxx+=1
					else:
						try:ch=LINE(x,appName=_A);ch.updateProfilePicture(B)
						except:pass
				picture=0;return bot.sendMessage(msg._from,'Successfully changed all bot avatar!')
			threading.Thread(target=changePict).start()
		else:return
	elif msg.contentType==16:
		if msg._from in access:
			bot.sendMessage(msg._from,'Checking post id....');purl=msg.contentMetadata['postEndUrl'].split('userMid=')[1].split('&postId=')
			if purl[1]not in postid:
				with open(_B,'a')as xdb:xdb.write(f"\n{purl[1]}")
				def runBotLike():
					xxx=0;bot.sendMessage(msg._from,f"Starting like {len(token)-1}....")
					for x in token:
						if xxx==0:xxx+=1
						else:
							try:ch=TIMELINE(x,appName=_A);ch.likePost(purl[0],purl[1],random.choice([1001,1002,1003,1004,1005]))
							except:pass
					return bot.sendMessage(msg._from,f"Success give like ur post to {len(token)-1} likes")
				threading.Thread(target=runBotLike).start()
def fetchOperation():
	while True:
		try:
			ops=poll.singleTrace(count=1)
			if ops!=None:
				for op in ops:operationStart(op);poll.setRevision(op.revision)
		except Exception as e:print(e)
if __name__=='__main__':loginClient();fetchOperation()
