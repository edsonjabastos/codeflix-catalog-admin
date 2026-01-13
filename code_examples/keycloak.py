import jwt
import json

public_key = b"\n-----BEGIN PUBLIC KEY-----\n\n-----END PUBLIC KEY-----\n"

token = ""

decoded = jwt.decode(token, public_key, algorithms=["RS256"], audience="account")
# Print the decoded token formatted as JSON

print(json.dumps(decoded, indent=4))
