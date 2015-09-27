from apmcs import db
from .models import Message
from config import SENTLY_AUTH
import thread
from urllib2 import Request, urlopen
from urllib import urlencode
import json


def sms(text, phone_no, msg_id):
    count = 0
    total = len(phone_no)
    for phone in phone_no:
        try:
            values = {
                "from": "NNMAPM",
                "to": "+91" + phone,
                "text": text}

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer adkk2y5yai7m5u039aketayl0kokdvhk',
                'Accept-Encoding': 'gzip'}

            request = Request('https://apiserver.sent.ly/api/outboundmessage' \
                              , data=json.dumps(values), headers=headers)
            response_body = urlopen(request).read()
            print response_body
            count += 1
        except:
            print "Error"
    result = "Sent %d of %d SMS" % (count, total)
    if msg_id:
        msg = Message.query.get(msg_id)
        msg.info = result
        db.session.commit()
    return


def send_sms(text, phone_no, msg_id=None):
    thread.start_new_thread(sms, (text, phone_no, msg_id))
    return True
