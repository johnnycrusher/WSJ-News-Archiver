
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: 9154566
#    Student name: John Huynh
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  News Archivist
#
#  In this task you will combine your knowledge of HTMl/XML mark-up
#  languages with your skills in Python scripting, pattern matching
#  and Graphical User Interface development to produce a useful
#  application for maintaining and displaying archived news or
#  current affairs stories on a topic of your own choice.  See the
#  instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements that were used in our sample
# solution.  You should be able to complete this assignment using
# these functions only.

# Import the function for opening a web document given its URL.
from urllib.request import urlopen

# Import the function for finding all occurrences of a pattern
# defined via a regular expression, as well as the "multiline"
# and "dotall" flags.
from re import findall, MULTILINE, DOTALL

# A function for opening an HTML document in your operating
# system's default web browser. We have called the function
# "webopen" so that it isn't confused with the "open" function
# for writing/reading local text files.
from webbrowser import open as webopen

# An operating system-specific function for getting the current
# working directory/folder.  Use this function to create the
# full path name to your HTML document.
from os import getcwd

# An operating system-specific function for 'normalising' a
# path to a file to the path-naming conventions used on this
# computer.  Apply this function to the full name of your
# HTML document so that your program will work on any
# operating system.
from os.path import normpath

# Import the standard Tkinter GUI functions.
from tkinter import *

# Import the SQLite functions.
from sqlite3 import *

# Import the date and time function.
from datetime import datetime

import matplotlib
matplotlib.use('Agg')

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Name of the folder containing your archived web documents.  When
# you submit your solution you must include the web archive along with
# this Python program. The archive must contain one week's worth of
# downloaded HTML/XML documents. It must NOT include any other files,
# especially image files.
internet_archive = 'WSJ_Tech'


####### HTML Generation Section ###############
def find_article_image(article, which_head_line):
    #Open and Read the archive file
    news_page = open(article).read()
    #Using Regex to extract the image URL
    article_image = findall('http.*?jpg',news_page)
    #Return the image URL for specified article
    return article_image[which_head_line-1]

def find_article_name(article, which_head_line):
    #Open and Read the archive file
    news_page = open(article).read()
    #Using Regex to extract news article title
    article_name = findall('<title>(.*?)<\/title>', news_page)
    #Return the article title for specified article
    return article_name[which_head_line+1]

def find_article_description(article, which_head_line):
    #Open and Read the archive file
    news_page = open(article).read()
    #Using Regex to extract the desciption
    article_description = findall('<description>(.*?)<\/description>',news_page)
    #Return the article description for specified article
    return article_description[which_head_line]

def find_article_link(article, which_head_line):
    #Open and Read the archive file
    news_page = open(article).read()
    #Using Regex to extract URL of the Article
    article_link = findall('http.*?logy',news_page)
    #Return the URL for specified article
    return article_link[which_head_line-1]

def find_article_time(article, which_head_line):
    #Open and Read the archive file
    news_page = open(article).read()
    #Using Regex to extract the publish date of the article
    article_date = findall('<pubDate>(.*?)<\/pubDate>',news_page)
    #Return the publish date for the speicifed article
    return article_date[which_head_line]

def write_news_articles(article,which_news_number):
    #Open and Read the archive file
    news_page = open(article).read()
    #Base Template for news article section
    news_articles_section = '''
    <h3>number. Article</h3>
    <img src = "Article_Image">
    <p id = "text">Description</p>
    <p id = "text"><b>Full Story:</b><a href="article_Link">article_Link</a></p>
    <p id = "text"><b>Dateline:</b>DateTime</p>
    '''
    #Find the article image
    article_image = find_article_image(article,which_news_number)

    #Detects if the article image still exist
    try:
        urlopen(article_image)
    except:
        #If it doesn't exist then replace the image tag with image not avaliable text
        news_articles_section = news_articles_section.replace('<img src = "Article_Image">',
        '<p id = "noImage">Sorry,image '+ article_image[41:len(article_image)] + ' not found!</p>')
    
    #Replace the article image text with the actual image URL
    news_articles_section = news_articles_section.replace('Article_Image', article_image)

    #Find the article name and replace the article name text with the actual article name
    article_name = find_article_name(article,which_news_number)
    news_articles_section = news_articles_section.replace("Article",article_name)
    
    #Replace number with the actual number
    news_articles_section = news_articles_section.replace("number",str(which_news_number))

    #Find the article description and replace the article description text with the article description
    article_description = find_article_description(article,which_news_number)
    news_articles_section = news_articles_section.replace("Description", article_description)

    #Find the article line and replace the article_Link text with the article link
    article_link = find_article_link(article,which_news_number)
    news_articles_section = news_articles_section.replace("article_Link",article_link)
    
    #find the article publish date and replace DateTime text with article publish date
    article_date = find_article_time(article,which_news_number)
    news_articles_section = news_articles_section.replace("DateTime",article_date)

    #return the news article section as a string
    return news_articles_section

def write_entire_page(article, article_date):
    #allow access to global variables
    global archive_dates
    global html_pages

    #template document for the whole html file
    template='''
    <HTML>
    <Head>
    <style>
    html {
	margin: 0;
	padding: 0;
	background-color: #777;
    }
    body {
        width: 60%;
        margin: 0 auto;
        font: 100% Arial, Helvetica, sans-serif;
        padding: 1em 50px;
        background: lightblue;
    }
    h1 {
        font-family: Georgia, "Times New Roman", Times, serif;
        font-size: 2.5em;
        font-weight: normal;
        font-style: italic;
        text-align: center;
        margin: 0 0 .4em;
        color: darkcyan;
        padding: 5px 10px;
    }
    h2 {font-family:'Times New Roman', Times, serif;
        font-size: 2em;
        font-weight: normal;
        text-align: center}
    h3 {font-family: Cambria, Cochin, Georgia, Times, Times New Roman, serif;
        font-size: 1.5em;
        font-weight: normal;
        text-align: center}
    img{
        display: block;
        margin-left: auto;
        margin-right: auto;
        padding : 15px 5px;
    }
    #startPage{
          margin-left : 25%;
          margin-right: 25%;
    }
    #noImage{
        text-align: center;
        margin:0 auto;
        width: 45%;
        border: 1px solid black;
    }
    #text{
        line-height: 1.6;
        width: 100%;
        margin: 0;
        margin-bottom: 1em;
    }
    </style>
    <Title>The Wall Street Journal Technology</Title>
    </Head>
    <Body>
    <h1 allign="center">The Wall Street Journal Technology Archive</h1>
    <h2>Date</h2>
    <img src= 'Main_Image' width = "436" height = "64">
    <p id = "startPage"><b>News Source:</b><a href="SourceURL">SourceURL</a></p>
    <p id = "startPage"><b>Arcivist:</b> John Huynh</p>
    '''
    #Closing tags for the html file
    closing_tags = '''
    </Body>
    </HTML>
    '''

    #Define the main image URL and replace it with Main_Image text
    main_image ='http://online.wsj.com/img/wsj_sm_logo.gif'
    template = template.replace('Main_Image',main_image)

    sourceURL = "http://www.wsj.com/xml/rss/3_7455.xml"
    template = template.replace('SourceURL', sourceURL)

    #For loop to find which article date it is and replace it
    for page in range(0,len(html_pages)-1):
        if (article_date == html_pages[page]):
            template = template.replace('Date', archive_dates[page])
            break
        elif(page >= len(html_pages)-2):
            template = template.replace('Date', 'Latest News')

    #Intilise list for news segmants
    news_segmant = []
    #Generate the 10 news segmants
    for SubArticles in range(0,10):
        news_segmant.append(write_news_articles(article,SubArticles+1))
    #Open the empty html document and set the property to write
    extracted_archive = open("extracted_archive.html",'w')
    #Write the base template for the article
    extracted_archive.write(template)
    #Writing the news segmants into the html document
    for article in news_segmant:
        extracted_archive.write(article)
    #Write the html closing tags into the html document
    extracted_archive.write(closing_tags)
    extracted_archive.close()


################# GUI Section #################
def extract_news():
    #allow access to these global variables
    global internet_archive
    global lastest_downloaded
    global has_archive
    global event_checkbox
    global log_counter
    global connection

    #Grabs the current selection for the Listbox
    which_option = display_choice()
    # Show Error if Latest File has not been archive
    if (latest_downloaded == False and which_option =='Latest.html' ):
        instruction_label['text'] = 'Error:Latest news has not been downloaded'
    
    else:
        #Set the path of the internet archive
        path = normpath(getcwd() + '/' + internet_archive)
        #Grabs the archive file name based on listbox selection
        article = display_choice()
        #Define path for the archived document
        article_path = normpath(path + '/' + article)
        #Write entire page
        write_entire_page(article_path, article)
        #Change the instruction text
        instruction_label['text'] = 'News extrated from archive'
        has_archive = True
        #Check if checkbox is ticked if ticked then add an entry in the sql data base
        if(event_checkbox.get() == 1):
            log_counter += 1
            sql_query_extract = "INSERT INTO Event_Log VALUES(" + str(log_counter) + \
                                 ",'News extracted from archive')"
            event_log.execute(sql_query_extract)
            connection.commit()

def display_news():
    #allow access to these global variables
    global has_archive
    global event_checkbox
    global log_counter
    global connection
    #Check if it has any extracted archives
    if (not has_archive):
        instruction_label['text'] = "Please choose a date to archive..."
    else:
        #Define path to extracted archive
        path = normpath(getcwd()+'/extracted_archive.html')
        #Open Extracted archive
        webopen(path)
        #Change instruction label
        instruction_label['text'] = "Choose another day's news you would like to extract..."
        #Check if checkbox is ticked if ticked then add an entry in the sql data base
        if(event_checkbox.get() == 1):
            log_counter += 1
            sql_query_display = "INSERT INTO Event_Log VALUES(" + str(log_counter) + \
                                ",'Extracted news displayed in web broswer')"
            event_log.execute(sql_query_display)
            connection.commit()
    

def archive_news():
    #allow access to these global variables
    global internet_archive
    global latest_downloaded
    global event_checkbox
    global log_counter
    global connection

    url = 'http://www.wsj.com/xml/rss/3_7455.xml'
    #Open the URL
    latest_copy = urlopen(url)
    #Read the page contents
    latest_page_contents = latest_copy.read().decode('UTF-8')
    #Define the internet archive path
    internet_archive_path = normpath(getcwd() + '/' + internet_archive )
    #Define internet archive latest file path
    latest_archive_path = normpath(internet_archive + '/latest.html')
    #Open the latest arhcive html doc and set to writing mode
    latest_html_page = open(latest_archive_path,'w', encoding = 'UTF-8')
    #Write page contents
    latest_html_page.write(latest_page_contents)
    latest_html_page.close()
    #Change instruction text
    instruction_label['text'] = "Downloaded latest news..."
    latest_downloaded = True
    #Check if checkbox is ticked if ticked then add an entry in the sql data base
    if(event_checkbox.get() == 1):
        log_counter += 1
        sql_query_archive = "INSERT INTO Event_Log VALUES(" + str(log_counter) + \
                                ",'Latest news downloaded and store in archive')"
        event_log.execute(sql_query_archive)
        connection.commit()

def display_choice():
    #allow access to these global variables
    global archive_dates
    global html_pages
    global connection
    #Define current selection
    if (archive_dates_list.curselection() != ()):
        #For loop to interate all the archive dates
        for page in range(0,len(archive_dates)):
            #Check if archive dates match the archive_dates list
            if(archive_dates_list.get(archive_dates_list.curselection()) == archive_dates[page]):
                #set document to html page name
                document = html_pages[page]
                break
    #return html document name
    return document


def activate_logger():
    #allow access to these global variables
    global event_checkbox
    global first_time
    global event_log
    global log_counter
    global connection
    #Check if checkbox is ticked
    if (event_checkbox.get() == 1):
        log_counter += 1
        #connect to SQL Data Base
        connection = connect(database = "event_log.db")
        event_log = connection.cursor()
        #Execute SQL Query
        sql_query_on = "INSERT INTO Event_Log VALUES(" + str(log_counter) + ",'Event logging switched on')" 
        event_log.execute(sql_query_on)
        #Commit the SQL Query to the Database
        connection.commit()         
        first_time = False
    elif(event_checkbox.get() == 0 and first_time == False):
        log_counter += 1
        #Execute SQL Query
        sql_query_off = "INSERT INTO Event_Log VALUES(" + str(log_counter) + ",'Event logging switched off')"
        event_log.execute(sql_query_off)
        #Commit the SQL Query to the Database
        connection.commit()
        #Close the connection to the data base
        event_log.close()
        connection.close()
        
#Global Vars
archive_dates = ['Thu, 12th Oct 2017','Fri, 13th Oct 2017','Sat, 14th Oct 2017',
                'Tue, 17th Oct 2017','Wed, 18th Oct 2017', 'Thu, 19th Oct 2017',
                'Fri, 20th Oct 2017','Latest']
html_pages = ['Thu_12th_Oct.html','Fri_13th_Oct.html','Sat_14th_Oct.html',
            'Tue_17th_Oct.html','Wed_18th_Oct.html','Thu_19th_Oct.html',
            'Fri_20th_Oct.html','Latest.html']
has_archive = False
latest_downloaded = False
first_time = True
log_counter = 0

#Clear Database
connection = connect(database = "event_log.db")
event_log = connection.cursor()
event_log.execute("DELETE FROM Event_Log")
connection.commit()
event_log.close()
connection.close()

#Intialise tkinter window
main_window = Tk()
main_window.title('The Wall Street Journal Technology Archive')

main_window.configure(bg = 'Ivory')

#Create button for extract news
extract_news_button = Button(main_window,
                            height = 2,
                            width = 12,
                            wraplength = 80,
                            justify = LEFT,
                            text = "Extract news from archive",
                            command = extract_news,
                            bg = 'Ivory')

#Create button for display news
display_news_button = Button(main_window,
                            height = 2,
                            width = 12,
                            wraplength = 80,
                            justify = LEFT,
                            text = "Display news extracted",
                            command = display_news,
                            bg = 'Ivory')
#Create button for archive news
archive_news_button = Button(main_window,
                            height = 2,
                            width = 12,
                            wraplength = 80,
                            justify = LEFT,
                            text = "Archive the latest news",
                            command = archive_news,
                            bg = 'Ivory')
#Create label for the instruction
instruction_label = Label(main_window,
                        text = "Choose which day's news to extract...",
                        font = ("Helvetica",20),
                        wraplength = 350,
                        bg = 'Ivory')
#Create Label for the WSJ label
WSJ_label = Label(main_window,
                        text = "The Wall Street Journal Technology",
                        font = ("Helvetica",12),
                        bg = 'Ivory')
#Create Listbox for archive dates
archive_dates_list = Listbox(main_window,
                            height = len(archive_dates),
                            font = ("Helvetica",15))
#add dates in the archive dates
for dates in archive_dates:
    archive_dates_list.insert(END,dates)

#setup variable to monitor event checkbox
event_checkbox = IntVar()
#Create checkbox for event logger
event_logger_checkbox = Checkbutton(main_window,
                                text = "Log Events",
                                variable = event_checkbox,
                                command = activate_logger,
                                bg = 'Ivory')

#Create Image for the GUI
WSJ_logo = PhotoImage(file='The Wall Street Journal Logo.gif')
WSJ_logo_label = Label(main_window, image = WSJ_logo)

#Using Geometry Packer to pack objects into the window
margin_size = 5
archive_dates_list.grid(padx = margin_size, pady = margin_size,
                    row = 1, column = 1, rowspan = 10)
extract_news_button.grid(padx = margin_size, pady = margin_size,
                        row = 1,column = 2)
display_news_button.grid(padx = margin_size, pady = margin_size,
                        row = 2,column = 2)
archive_news_button.grid(padx = margin_size, pady = margin_size,
                        row = 3,column = 2)
event_logger_checkbox.grid(padx = margin_size, pady = margin_size,
                        row = 4, column = 2)
instruction_label.grid(padx=margin_size, pady = margin_size,
                        row = 0, column = 1, columnspan = 2)
WSJ_label.grid(padx = margin_size, pady = margin_size,
                row = 4, column = 0)
WSJ_logo_label.grid(padx = margin_size,pady = margin_size,
                row = 0, column = 0, rowspan = 4)
            
# Start the event loop
main_window.mainloop()