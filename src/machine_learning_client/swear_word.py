import json
from googleapiclient import discovery
API_KEY = AIzaSyAGqrHHcohad44sUEK3LnOnMN1b4GoTm0s

def toxic_score(text):
    analyze_request