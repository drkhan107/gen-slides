def get_ppt_prompt():
    
    PROMPT = """
    Summarize the input text and arrange it in an array of JSON objects to to be suitable for a powerpoint presentation. 
    Determine the needed number of json objects (slides) based on the length of the text and agenda. 
    Each key point in a slide should be limited to up to 10 words. 
    Consider maximum of 5 bullet points per slide. 
    Return the response as an array of json objects. 
    The first item in the list must be a json object for the title slide. 
    
    This is a sample of such json object:
    {
    "id": 1,
    "title_text": "My Presentation Title",
    "subtitle_text": "My presentation subtitle",
    "is_title_slide": "yes"
    }
    And here is the sample of json data for slides:
    {"id": 2, title_text": "Slide 1 Title", "text": ["Bullet 1", "Bullet 2"]},
    {"id": 3, title_text": "Slide 2 Title", "text": ["Bullet 1", "Bullet 2", "Bullet 3"]}
    {"id": 4, title_text": "Slide 2 Title", 
     "table": [[' ', '2022', '2021'],['Revenue (USD Million)','92,379','642,338',],
     ['Operating profit (USD Million)', '6,071', '42,216',],
     ['Operating margin', '6.6%', '6.6%', '19.1%', '8.1%', '9.1%']]
    }

    Please make sure the json object is correct and valid. 
    Don't output explanation. I just need the JSON array as your output.

    """

    return PROMPT