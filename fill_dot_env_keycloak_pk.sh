#!/bin/bash
# Fetch public key and update .env
PUBLIC_KEY=$(curl -s http://localhost:8080/realms/codeflix | jq -r '.public_key')
sed -i "s|^AUTH_PUBLIC_KEY=.*|AUTH_PUBLIC_KEY=\"$PUBLIC_KEY\"|" .env