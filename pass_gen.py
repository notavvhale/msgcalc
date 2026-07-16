import streamlit_authenticator as stauth

password = "admin"

hashed = stauth.Hasher.hash(password)

print(hashed)