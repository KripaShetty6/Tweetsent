# events-example0.py
# Barebones timer, mouse, and keyboard events
#
####STARTER CODE FROM 15-112 TKINTER TUTORIAL: events-example0.py
import nbv2
from Tkinter import *
import math

###THIS IS THE FRONTEND FOR TWEETSENT, AND IT'S YOUR MAIN FILE, AS IT DRAWS
###ALL OF THE STUFF WITH TKINTER

#thanks to dude outside doherty who told me about emoji unicode
#thanks to tscherli for thinking of a sentiment for a user timeline and filtering ideas
#thanks to all the beta testing ppl on my floor

####################################
######ERROR/TODO LIST:
###TODO
#HISTOGRAM + BELL CURVE MATPLOTLIB VISUALIZATION?
#Add colors on the words that affect the sentiment (font color in green/red)
#
###DONE
#FILTER TWEETS THAT ARE JUST LINKS
#GET USER TWEETS AND ANALYSE USER POSITIVITY
#For some reason pressing analyze twitter with empty string doesn't do anything
#PRESSING ARROW KEYS TO SCROLL RECORDS ACTIONS - no more extra logging
#IF YOU SEARCH, GO TO HELP, THEN GO BACK, THE TEXT ALL SHOWS UP IN A WEIRD FONT
#ADD OPTIONS FOR AMT OF TWEETS TO LOOK FOR - done
#Pressing the keys also goes into the text bar
#MAKE SCROLLING FOR THE TOP HALF SO THE TWEETS CAN SCROLL - done
#Tkinter CRASHES on emojis - fixed
#Twitter can have rate limits - make new app before final demo
#ALWAYS POS OR NEG bc the negcount from corpus and poscount from corpus are really different - fixed (mostly)
#SOL: negative = c, since poscount = 8692 and negcount = 22853, lower negcount to increase weight
#tkinter ui is jank - looks better
####################################



def init(data):
    # load data.xyz as appropriate
    #scrolling stuff
    data.cx = 0
    data.cy = 0
    #start page color changing stuff (in redrawallwrapper)
    data.timeCount = 0
    #WHILE DATA.COLOR CHANGES, THE FILLS ARE STATIC BECAUSE IT'S NOT ALIASING
    data.color = '#%02x%02x%02x' % (128,125,128)
    #start button stuff
    data.startButtonX = data.width/2
    data.startButtonY = data.height/1.5
    data.startButtonW = 140
    data.startButtonH = 70
    data.startButtonFill = data.color
    #help button
    data.hButtonX = data.width - 53
    data.hButtonY = data.height - 43
    data.hButtonW = 100
    data.hButtonH = 80
    data.hButtonFill = data.color
    #options button
    data.oButtonX = data.width - 53
    data.oButtonY = data.height - 123
    data.oButtonW = 100
    data.oButtonH = 80
    data.oButtonFill = data.color
    #input text
    data.text = ''
    #output text
    data.output = 'Results appear up here!'
    #analyze button
    data.analyzeButtonX = data.width/2
    data.analyzeButtonY = data.height/1.5 + data.startButtonH
    data.analyzeButtonW = 140
    data.analyzeButtonH = 70
    data.analyzeButtonFill = data.color
    #analyze user button
    data.uButtonX = data.width/2
    data.uButtonY = data.height/1.5 + data.startButtonH + data.analyzeButtonH
    data.uButtonW = 140
    data.uButtonH = 70
    data.uButtonFill = data.color
    #NOTE: have an options page to change amount of tweets to analyze
    data.tweetCount = 10
    data.margin = data.width//6
    data.tweets = None
    ###DATA STATES
    data.mode = 0 #mode = 0 for start, 1 for just the sentiment, 2 for tweet mining, 3 for help, 4 for options
    #the scrolling buttons to scroll up and down


def mousePressed(event, data):
    # use event.x and event.y
    #if you click analyze my tweet
    if data.mode > 0 and abs(event.x - data.startButtonX) < data.startButtonW/2 and \
    abs(event.y - data.startButtonY) < data.startButtonH/2:
        data.text = data.e.get()
        data.mode = 1
        data.output = nbv2.classify(data.text)
        #if it's an empty string
        if(len(data.text.strip()) == 0):
            data.output = "Yo, that's an empty string!"

    #if you click analyze twitter
    elif data.mode > 0 and \
    abs(event.x - data.analyzeButtonX) < data.analyzeButtonW/2 and \
    abs(event.y - data.analyzeButtonY) < data.analyzeButtonH/2:
        data.text = data.e.get()
        data.mode = 2
        #if it's an empty string
        if(len(data.text.strip()) == 0):
            data.output = "" #It'll already say 'no tweets found' so it all good
        else:
            #gets the outputs of the tweets
            data.output = nbv2.analyze(data.text, data.tweetCount)
            #gets the colors
            data.tweets = nbv2.analyzeColor(data.text, data.tweetCount)

    #if you click analyze user
    elif data.mode > 0 and \
    abs(event.x - data.uButtonX) < data.uButtonW/2 and \
    abs(event.y - data.uButtonY) < data.uButtonH/2:
        data.text = data.e.get()
        data.mode = 2
        #if it's an empty string
        if(len(data.text.strip()) == 0):
            data.output = "" #It'll already say 'no tweets found' so it all good
        else:
            #gets the outputs of the tweets
            data.output = nbv2.analyzeUser(data.text, data.tweetCount)
            #gets the colors
            data.tweets = nbv2.analyzeUserColor(data.text, data.tweetCount)

    #if you click help
    elif data.mode > 0 and abs(event.x - data.hButtonX) < data.hButtonW/2 and \
    abs(event.y - data.hButtonY) < data.hButtonH/2:
        data.text = data.e.get()
        data.mode = 3

    #if you click options
    elif data.mode > 0 and abs(event.x - data.oButtonX) < data.oButtonW/2 and \
    abs(event.y - data.oButtonY) < data.oButtonH/2:
        data.text = data.e.get()
        data.mode = 4

    #scrolling
    if(data.mode == 2 and event.y <= data.height/2 - 35 and \
        event.y >= data.height/2 - 100 and data.cy <= 250):
        data.cy += 10
    elif(data.mode == 2 and event.y >= 0 and event.y <= 65 and\
        data.cy >= -200):
        data.cy -= 10


def keyPressed(event, data):
    # use event.char and event.keysym
    #switch to the normal menu from help or start with keypress
    if(data.mode == 0 or data.mode == 3 or data.mode == 4):
        if event.keysym == 't':
            data.mode = 1 #start
            #reset output
            data.output = 'Results appear up here!' 
    #switch amount of tweets
    if(data.mode == 4):
        #clear out the input for commands too
        if(event.keysym.lower() == 't'):
            data.e.delete(0,END)
        if(event.keysym in '0123456789'):
            data.e.delete(0,END)
            if(event.keysym == '0'):
                data.tweetCount = 10
            else:
                data.tweetCount = int(event.keysym)
    #also scrolling
    if(data.mode == 2 and event.keysym == 'Down'):
        data.e.delete(0,END)
        if(data.cy <= 300):
            data.cy += 10
    elif(data.mode == 2 and event.keysym == 'Up'):
        data.e.delete(0,END)
        if(data.cy >= -300):
            data.cy -= 10
    #press 'd' to delete whatever's in the text box
    if(data.mode > 0 and event.keysym == 'Tab'):
        data.e.delete(0,END)
    #if user presses 't' clear the input so it doesn't show up

def timerFired(data):
    data.timeCount += 1
    #background color function for smooth color change in title screen
    time = int(127*math.cos(math.pi*data.timeCount/180) + 128)
    data.color = '#%02x%02x%02x' % (255-time,125, time)

#darw the twitter sentiment graphic
def drawTweetGraphic(canvas, data):
    tweets = data.tweets
    if(len(tweets) < 1):
        return None
    #greens are positive, reds are negative. blues are unidentifiable
    greens = []
    reds = []
    blues = []
    for i in range(len(tweets)):
        #choose color based on results
        if(tweets[i][0] == 1):
            #*127, not 255, for more weight / pixelation for effect
            greens.append(tweets[i][2] * 127)
        elif(tweets[i][0] == 0):
            reds.append(tweets[i][2] * 127)
        #it's a random case
        else:
            blues.append(tweets[i][2] * 127)
    # + biggest green -> 0 -> biggest red -
    greens = sorted(greens)
    reds = sorted(reds)[::-1]
    #assign red/green status to each number so i can tell which is which
    for i in range(len(greens)):
        greens[i] = ('g', greens[i])
    for i in range(len(reds)):
        reds[i] = ('r', reds[i])
    #assign color to blue ones too
    for i in range(len(blues)):
        blues[i] = ('b', blues[i])
    #reversing makes a more pleasing aesthetic
    colors = greens[::-1] + reds[::-1] + blues
    #width of each rectangle
    w = (data.width - data.margin*2) / len(colors)
    #draw the bar of sentiment
    for i in range(len(colors)):
        f = '#%02x%02x%02x' % (0,0,0)
        if(colors[i][0] == 'r'):
            f = '#%02x%02x%02x' % (2*colors[i][1],0,0)
        elif colors[i][0] == 'g':
            f = '#%02x%02x%02x' % (0,2*colors[i][1],0)
        else:
            f = '#%02x%02x%02x' % (0,0, 2*colors[i][1])
        #draw rectangle
        canvas.create_rectangle(data.margin + w * i, \
            data.height/2, data.margin + w*(i+1),\
            data.height/2+40, width = 0,\
            fill = f)


def redrawAll(canvas, data):
    if data.mode == 0: #start screen
        canvas.create_text(data.width/2, data.height/2, text = "Welcome to TweetSent", \
            font = "Helvetica 28 bold")
        canvas.create_text(data.width/2, data.height/2 + 30,\
         text = "This young TwitterBoi is ready to read tweets!", font = "Helvetica 18")
        canvas.create_text(data.width/2, data.height/2 + 58, text = "Press 't' to begin analyzing" +\
            " your words", font = "Helvetica 18")
        canvas.create_text(data.width/2, data.height - 20, text = "By Michael Li for 15-112 Fall '17",\
         font = "Helvetica 14")
    elif data.mode == 3:
        canvas.create_text(data.width/2, data.height/2, text = \
            "Welcome to TweetSent!\n\n"+\
            "Here, you can either analyze your own tweet\n" +\
            "to see if your tweet will be recognized as positive or negative\n" +\
            "or you can look up twitter to see what people are thinking about any topic!\n\n"+\
            "The sentiment bar will visualize the mood of \n"+
            "twitter's most retweeted tweets on the topic or a user's tweets\n" +\
            "and shows positivity as shades of green and negativity as shades of red.\n" +\
            "Blue on the bar is for tweets that are just a link or are unreadable.\n" +\
            "When the tweets come up, you can click near the top or bottom \n"+ \
            "of the tweet display to scroll up or down,\n"+ \
            "or press up and down on your keyboard to scroll!\n" +\
            "Press Tab to delete whatever's in the text box.", 
             font = "Helvetica 13 bold")
        canvas.create_text(data.width/2,data.height/2 + 180, text = "Press 't' to go back",\
            font = "Helvetica 11")
    elif data.mode == 4:
        canvas.create_text(data.width/2, data.height/2, text = \
            "OPTIONS:\n" +\
            "To change the number of tweets to analyze, press a digit '1-9', '0' for 10 tweets\n" +\
            "Current number of tweets to read: " + str(data.tweetCount),
             font = "Helvetica 16 bold")
        canvas.create_text(data.width/2,data.height/2 + 100, text = "Press 't' to go back",\
            font = "Helvetica 14")
    #normal menu state
    else:
        #depending on the button
        if data.mode == 2:
            #output text w/ scrolling
            canvas.create_text(data.width/2-data.cx,data.height/4-data.cy, text = data.output, width = \
                data.width/1.5, font = "Helvetica 10 bold")
            #this will cover up the bottom of the screen with a white canvas so overflow text isn't seen
            canvas.create_rectangle(0,data.height/2-44, data.width, data.height + 100, width = 0, fill = 'white')
            '''#draw some rectangles for nice ui
            canvas.create_rectangle(0,0,data.width//6,data.height, width=0, fill = data.color)
            canvas.create_rectangle(data.width*5//6, 0, data.width, data.height, width=0,fill = data.color)'''
            #if there're tweets, draw the sent green-red color graphic
            if len(data.text.strip()) > 0 and len(data.output.strip()) > 0:
                #box around the sentiment bar
                canvas.create_rectangle(data.margin - 10, data.height/2 - 35, \
                 data.width - data.margin + 10, data.height/2 + 60, fill = data.hButtonFill, width = 3)
                #the bar
                drawTweetGraphic(canvas, data)
                #label
                canvas.create_text(data.margin + 20,data.height/2 - 20, text = 'Sentiment:', \
                 font = "Helvetica 10 bold") 
            else:
                 canvas.create_text(data.width/2,data.height/4, text = 'No tweets found...', width = \
                    data.width/1.5) 
        elif data.mode == 1:
            '''#draw some rectangles for nice ui
            canvas.create_rectangle(0,0,data.width//6,data.height, width=0, fill = data.color)
            canvas.create_rectangle(data.width*5//6, 0, data.width, data.height, width=0, fill = data.color)'''
            #show the text
            canvas.create_text(data.width/2,data.height/3, text = data.output, width = \
                data.width/1.5)

        # draw in canvas
        data.e.pack()
        #data.e.place(x=500, y=400)
        
        canvas.create_text(data.width/2,data.height - 20, text = "Enter your text here", font = "Helvetica 12")
        #create the start button
        canvas.create_rectangle(data.startButtonX - data.startButtonW/2,\
         data.startButtonY - data.startButtonH/2, \
            data.startButtonX + data.startButtonW/2,\
            data.startButtonY + data.startButtonH/2, \
            width = 3, fill = data.startButtonFill)
        #create the help button
        canvas.create_rectangle(data.hButtonX - data.hButtonW/2,\
            data.hButtonY - data.hButtonH/2, \
            data.hButtonX + data.hButtonW/2,\
            data.hButtonY + data.hButtonH/2, \
            width = 3, fill = data.hButtonFill)
        #create the help button
        canvas.create_rectangle(data.oButtonX - data.oButtonW/2,\
            data.oButtonY - data.oButtonH/2, \
            data.oButtonX + data.oButtonW/2,\
            data.oButtonY + data.oButtonH/2, \
            width = 3, fill = data.oButtonFill)
        #create the search twitter and analyze button
        canvas.create_rectangle(data.analyzeButtonX - data.analyzeButtonW/2,\
         data.analyzeButtonY - data.analyzeButtonH/2, \
            data.analyzeButtonX + data.analyzeButtonW/2,\
            data.analyzeButtonY + data.analyzeButtonH/2, \
            width = 3, fill = data.analyzeButtonFill)
        #create the analyze user button
        canvas.create_rectangle(data.uButtonX - data.uButtonW/2,\
         data.uButtonY - data.uButtonH/2, \
            data.uButtonX + data.uButtonW/2,\
            data.uButtonY + data.uButtonH/2, \
            width = 3, fill = data.uButtonFill)
        #text
        canvas.create_text(data.startButtonX,data.startButtonY, text = "Analyze my words!")
        canvas.create_text(data.analyzeButtonX,data.analyzeButtonY, text = "Analyze twitter!")
        canvas.create_text(data.uButtonX,data.uButtonY, text = "Analyze user!")
        canvas.create_text(data.hButtonX,data.hButtonY, text = "Help")
        canvas.create_text(data.oButtonX,data.oButtonY, text = "Options")



####################################
# use the run function as-is
####################################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        if(data.mode == 0):
            color = data.color
        else:
            color = 'white'
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill=color, width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    ###text entry box
    data.e = Entry(root, bd = 3, width = 20)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 800)





