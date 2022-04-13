import re
from logzero import logger
from fastapi import FastAPI, HTTPException

import smtplib
import dns.resolver
app = FastAPI()



@app.get("/verify/{email}")
async def check_email(email: str):
    logger.info('got email {}'.format(email))
    from_address = 'nguyenhuuhy@gapo.com.vn'

    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

    input_address = email
    address_to_verify = str(input_address)

    match = re.match(regex, address_to_verify)
    if not match:
        raise HTTPException(status_code=400, detail="Bad")

    split_address = address_to_verify.split('@')
    domain = str(split_address[1])
    logger.info('got domain:{} from email: {}'.format(domain, email))

    records = dns.resolver.resolve(domain, 'MX')
    mx_record = records[0].exchange
    mx_record = str(mx_record)
    logger.info('got mx:{} from email: {}'.format(mx_record, email))
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    server.connect(mx_record)
    server.helo(server.local_hostname)
    server.mail(from_address)
    code, message = server.rcpt(str(address_to_verify))
    server.quit()

    if code != 250:
        raise HTTPException(status_code=400, detail="Bad")
    return {'status': True}
