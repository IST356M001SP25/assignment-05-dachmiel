from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''    
    # remove any dollar sign
    item = item.replace('$', '')
    # remove any commas
    item = item.replace(',', '')
    return float(item)

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    # parse the date
    date = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S')
    # extract the year
    year = date.year
    # return the year
    return year

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.'
    ]
    # remove any leading or trailing whitespace
    item = item.strip().lower()
    # check if the item is in the list of possibilities
    if item in possibilities:
        return 'United States'
    # if not, return the item
    else:
        return item
    

if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")

