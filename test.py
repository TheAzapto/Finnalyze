import requests

response = requests.post(
    'http://localhost:5000/analyze',
    json={"article": r"Vedanta poised for 16% annual growth in pre-tax earnings through FY28 on volume ramp-up"}
)

print(response.json())