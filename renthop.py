import pandas as pd
from lxml import html
import requests
import time
from tqdm import tqdm




url_list = []


number_of_pages = int(input('How many pages do you want to parse?\n'))

i = 0
url = "https://www.renthop.com/search/nyc?min_price=1500&max_price=4500&q=&neighborhoods_str=1%2C10%2C14%2C11%2C18&sort=hopscore&search=0&page=" + str(i)
    
while i < number_of_pages:
    i = i+1
    url = "https://www.renthop.com/search/nyc?min_price=1500&max_price=4500&q=&neighborhoods_str=1%2C10%2C14%2C11%2C18&sort=hopscore&search=0&page=" + str(i)
    url_list.append(url)
    


def agents(things_parse):
   
    agent_list = []
    alist = []
    flist = []
    elist = []
    plist = []
    xlisting = []
    t = time.time()      
    
    
    
    for i in tqdm(things_parse):
        response = requests.get(i)
        tree = html.fromstring(response.content)
        list_of_links = tree.cssselect('a[id*=listing-]')
        links = [link.get('href') for link in list_of_links]
        
        for link in links:
            response = requests.get(link)
            tree = html.fromstring(response.content)
            a_links = tree.xpath("//*[@id='contact-details-block']/div[2]/div[1]/a")
            agent = [link.get('href') for link in a_links]
            if agent not in agent_list:
                agent_list.append(agent)
    
    
        
    print("Finished processing links")
    
    new_agent_list = [j for i in agent_list for j in i]
    new_agent_list = [i for i in new_agent_list if 'https://www.renthop.com/managers/' in i]
    
    
    print("There are", len(new_agent_list), "to iterate through")
    
    for i in tqdm(new_agent_list):
        response = requests.get(i)
        tree = html.fromstring(response.content)
        x_agent = tree.xpath("//h1[@class='b font-size-15']/text()")
        alist.append(x_agent)
        x_firm = tree.xpath("//div[@style='padding-top: 2px;']/text()")
        flist.append(x_firm)
        x_email = tree.xpath("//a[@class='font-blue font-size-10']/text()")
        elist.append(x_email)
        x_phone = tree.xpath("//span[@class='b']/text()")
        plist.append(x_phone)
        x_listing = tree.xpath("//html//div[@class='font-size-10 mt-3']//span[2]/text()")
        x_listing = x_listing[1].replace(" ", "")
        x_listing = x_listing[-12:-8]
        xlisting.append(x_listing)
    
    
    print("Timetook:", time.time()-t)       
    
      
    a_list = [j for i in alist for j in i]
    f_list = [j for i in flist for j in i]
    p_list = [i[0] for i in plist]
    
    
    xlisting = [w.replace('1(', '').replace('(', '').replace(')', '').replace('R', '') for w in xlisting]
    
    elist = [str(i) for i in elist]
    e_list = [w.replace("['", '').replace("']", '').replace("[]", "None") for w in elist]
    
    global df
    
    unsorted_renthop = pd.DataFrame(list(zip(xlisting, a_list, f_list, e_list, p_list, new_agent_list)), columns=['Ads','Agent','Firm', 'Email', 'Phone', 'Url'])
    unsorted_renthop['Ads'] =  unsorted_renthop['Ads'].astype('int')
    unsorted_renthop.sort_values('Ads', inplace=True, ascending=False)
        
    df = pd.DataFrame(unsorted_renthop)
    df.to_csv('renthop_data.csv')



agents(url_list)
