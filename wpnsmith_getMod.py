
import requests     #   Used to access vendor website
import bs4          #   Used to pull HTML of vendor inventory

### This function scrubs the TodayInDestiny site for vendor inventories and returns the daily Banshee mod
def getMod():
    # Request vendor website
    url = 'https://www.todayindestiny.com/vendors'
    res = requests.get(url)

    # Check for error
    try:
        res.raise_for_status()
    except:
        print("Cannot reach vendor site!!")
        return;

    # Pull site HTML
    soup = bs4.BeautifulSoup(res.text, "html.parser")

  ### Scrape site for Banshee's daily mod
    # Isolate vendor cards
    vendors = soup.findAll('div', class_='vendorCardContainer')
    
    # Search through cards for Banshee-44
    for v in vendors:
        if v.find('p', class_='vendorCardHeaderName').string == "Banshee-44":
            # Isolate the "Material Exchange" portion of the vendor card
            exchange = v.find('div', identifier='category_materials_exchange')
            
            # Separate into individual items
            items = exchange.findAll('div', class_='vendorInventoryItemContainer')
            
            # Obtain the names of each item
            itemNames = [i.find('p', class_='itemTooltip_itemName').string for i in items]

    # Convert modName from bs4 NavigableString to a string
    #   The mod in question is always second in the list
    modName = "".join(map(str, itemNames[1]))

    return modName;

print("Today's mod: " + getMod())

