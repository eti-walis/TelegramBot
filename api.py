import requests


def get_links(category:str, color: str, size:str):
    url = "https://apidojo-forever21-v1.p.rapidapi.com/products/search"
    #print(category, "  ", type(category))
    querystring = {"query": category, "rows": "5", "start": "0", "color_groups": color, "sizes": size}

    headers = {
        'x-rapidapi-key': "4220ebf33emsh3f4b41d857bf47fp11a27ejsnf472e9f7acd7",
        'x-rapidapi-host': "apidojo-forever21-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    link_list = []
    txt = response.text
    for i in range(5):
        start_url = txt.find("url")
        end_url = txt.find("brand")
        link_list.append(txt[start_url+6:end_url-3])
        txt = txt[end_url+5:]

    return link_list
