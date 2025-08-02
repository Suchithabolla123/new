
import streamlit as st

def validate_token(token: str) -> bool:
    return token.startswith("AIza") or token.startswith("hf_")
