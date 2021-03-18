import requests
import websocket
# url = 'wss://classchat.hellolms.com/chat/?EIO=3&transport=websocket'
#
# f = open("account", encoding='UTF-8')
# account = f.readlines()
#
# s = requests.Session()
# s.post('https://eclass.kpu.ac.kr/ilos/lo/login.acl', data={'usr_id' : account[0].replace("\n", ''),
#                                                            'usr_pw' : account[1].replace("\n", '')})
# print("[*] SESSION ID :", id(s))

a = requests.post(" https://fr-talk.kakao.com/wp/friends/find_by_uuid.json",data={'uuid':'HROE04'})
print(a.text)