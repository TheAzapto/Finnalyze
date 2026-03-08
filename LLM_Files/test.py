import requests

response = requests.post(
        'http://localhost:5000/analyze',
        json={"article": r"24% rally in 3 months puts this bank stock on track for next target of ₹1,500"}
        )

for i in response.json():
    print(i)
