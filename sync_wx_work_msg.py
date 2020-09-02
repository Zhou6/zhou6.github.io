import base64
import ctypes
import Crypto
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

class WxWorkMsg(BaseDynamicDocument):
    _id = StringField(primary_key=True)
    create_time = StringField(null=False)
    dt = StringField(null=False)
    ts = FloatField(null=False)
    deleted = BooleanField(default=False)

class WxWork:
    CORP_ID = ''
    PRI_KEY = ''
    CHAT_SECRET = ''
    
    @classmethod
    def sync_msg(cls, seq=None):
        """企业微信会话存档内容同步"""
        dll = ctypes.cdll.LoadLibrary(os.getcwd() + "/libWeWorkFinanceSdk_C.so")  # 真实libWeWorkFinanceSdk_C位置
        new_sdk = dll.NewSdk()
        result = dll.Init(new_sdk, cls.CORP_ID.encode(), cls.CHAT_SECRET.encode())
        if result != 0:
            return
        private_key = RSA.import_key(cls.PRI_KEY)
        cipher = Crypto.Cipher.PKCS1_v1_5.new(private_key)
        if seq is None:
            last_msg = WxWorkMsg.find().order_by('-seq').limit(1).first()
            seq = last_msg.seq or 0
        while True:
            s = dll.NewSlice()
            dll.GetChatData(new_sdk, seq, 1000, '', '', 5, ctypes.c_long(s))
            data = dll.GetContentFromSlice(s)
            data = ctypes.string_at(data, -1).decode("utf-8")
            dll.FreeSlice(s)
            data = json.loads(data).get('chatdata')
            if not data:
                break
            seq = data[-1].get('seq')
            for msg in data:
                if WxWorkMsg.get_by_id(msg.get('msgid')):
                    continue
                encrypt_key = cipher.decrypt(base64.b64decode(msg.get('encrypt_random_key')), "ERROR")
                ss = dll.NewSlice()
                dll.DecryptData(encrypt_key, msg.get('encrypt_chat_msg').encode(), ctypes.c_long(ss))
                data = dll.GetContentFromSlice(ss)
                data = ctypes.string_at(data, -1).decode("utf-8")
                data = json.loads(data)
                dll.FreeSlice(ss)
                WxWorkMsg.create(_id=data.pop('msgid'), ts=data.pop('msgtime') / 1000, seq=msg.get('seq'),
                                 **data).save()
        dll.DestroySdk(new_sdk)
        
if __name__ == '__main__':
    WxWork.sync_msg()
