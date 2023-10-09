from bs4 import BeautifulSoup
import requests
import json

pick_up_line_url = 'https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/'

#Send Reqeust To webpage
response = requests.get(pick_up_line_url)

if response.status_code == 200 :
    #Parse the html
    soup = BeautifulSoup(response.content, 'html.parser')
    pickup_line_dict = {}

    #Find all the Title of Each Pick up Line
    titles = soup.find_all('h2')
    print(titles)

    for title in titles:
        new_title = title.text.strip()
        pickup_lines = []
    
        ul = title.find_next_sibling("ul")

        if ul :
            lis = ul.find_all("li")

            print(lis)
            for li in lis:
                pickup_line = li.text.strip()
                pickup_lines.append(pickup_line)
            
            pickup_line_dict[new_title] = pickup_lines
            with open("pickup_lines.json", "w") as json_file:
                json.dump(pickup_line_dict, json_file, indent=4)
        else:
            pickup_line_dict = []
       
else:
    print("Fail to retreived webpage status code : ",response.status_code)

    



