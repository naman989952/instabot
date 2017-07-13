import requests,urllib    # requests for making request to fetch the data ,urllib for downloading post/media
#from textblob import TextBlob   # import file textblob to delete negative comment
#from textblob.sentiments import NaiveBayesAnalyzer

'''
# APP_ACCESS_TOKEN & BASE URL in caps because we make them highlighted so that no other user will chnage
# APP_ACCESS_TOKEN = '5629236876.1cc9688.86db895c038043b5960dc2949785299a'
# sandbox users: insta.mriu.test.0,insta.mriu.test.1,insta.mriu.test.2
'''

global APP_ACCESS_TOKEN , BASE_URL
APP_ACCESS_TOKEN = '5629236876.1cc9688.86db895c038043b5960dc2949785299a'
BASE_URL='https://api.instagram.com/v1/'


# -------------------------------------------------------------------------------------------------------------------
# function to get own information and function name: self_information()

def own_information():
    # indentation not compulsory to multiple of four
    request_url = (BASE_URL + 'users/self/?access_token=%s') % APP_ACCESS_TOKEN
    print 'GET request url : %s' % (request_url)
    user_information = requests.get(request_url).json()         # it will convert data in json format by .json()
    print user_information

# if else loop to check whether there is user exist or not and if not then it will show 200 error
    if user_information['meta']['code'] == 200:
        if len(user_information['data']):
            print 'Your Username: %s' % (user_information['data']['username'])
            print 'Number of followers you have : %s' % (user_information['data']['counts']['followed_by'])
            print 'Number of people you are following: %s' % (user_information['data']['counts']['follows'])
            print 'Number of posts you have: %s' % (user_information['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

# -------------------------------------------------------------------------------------------------------------------
# get_user_id function to fetch the user id from username


def get_follower_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_information = requests.get(request_url).json()
  print user_information

  if user_information['meta']['code'] == 200:
    if len(user_information['data']):
      return user_information['data'][0]['id']
    else:
      return None
  else:
    print 'Status code other than 200 received!'
    exit()

# --------------------------------------------------------------------------------------------------------------------
# function for getting user information from username


def get_follower_user_information(insta_username):
  user_id = get_follower_user_id(insta_username)
  print user_id
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_information = requests.get(request_url).json()
  print user_information

  if user_information['meta']['code'] == 200:
    if len(user_information['data']):
      print 'Username: %s' % (user_information['data']['username'])
      print 'No. of followers: %s' % (user_information['data']['counts']['followed_by'])
      print 'No. of people they are following: %s' % (user_information['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_information['data']['counts']['media'])
    else:
      print 'There is no data for this user!'
  else:
    print 'Status code other than 200 received!'

# --------------------------------------------------------------------------------------------------------------------
# function to download own post


def get_own_post():
  request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  own_media = requests.get(request_url).json()

  if own_media['meta']['code'] == 200:
    if len(own_media['data']):
      image_name = own_media['data'][0]['id'] + '.jpeg'
      image_url = own_media['data'][0]['images']['standard_resolution']['url']
      urllib.urlretrieve(image_url, image_name)
      print 'Your image has been downloaded!'
    else:
      print 'There is no post available!'
  else:
    print 'Status code other than 200 received!'

# --------------------------------------------------------------------------------------------------------------------
# function to download user recent post


def get_follower_user_post(insta_username):
  user_id = get_follower_user_id(insta_username)

  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_media = requests.get(request_url).json()

  if user_media['meta']['code'] == 200:
    if len(user_media['data']):
      image_name = user_media['data'][0]['id'] + '.jpeg'
      image_url = user_media['data'][0]['images']['standard_resolution']['url']
      urllib.urlretrieve(image_url, image_name)
      print user_media['data'][0]['caption']
      print 'Your image has been downloaded!'
    else:
      print 'There is no post available!'
  else:
    print 'Status code other than 200 received!'

# --------------------------------------------------------------------------------------------------------------------
# function to get the recent post id


def get_follower_post_id(insta_username):
  user_id = get_follower_user_id(insta_username)

  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_media = requests.get(request_url).json()

  if user_media['meta']['code'] == 200:
    if len(user_media['data']):

      return user_media['data'][0]['id']
    else:
      print 'There is no recent post of the user!'
      exit()
  else:
    print 'Status code other than 200 received!'
    exit()


# --------------------------------------------------------------------------------------------------------------------
# function to get list of likes on the recent post


def get_like_list(insta_username):
  media_id = get_follower_post_id(insta_username)
  print media_id
  if media_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id , APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_like_list = requests.get(request_url).json()
  print user_like_list

  if user_like_list['meta']['code'] == 200:
    if len(user_like_list['data']):
        length=len(user_like_list['data'])
        i=0
        print 'Number of likes you have: %s'%(length)
        while(length):
            print 'Username :%d. %s' % (i+1,user_like_list['data'][i]['username'])
            print 'Name :%d. %s' % (i+1,user_like_list['data'][i]['full_name'])
            i=i+1
            length=length-1

    else:
      print 'There are no likes on this post!'

  else:
    print 'Status code other than 200 received!'


# --------------------------------------------------------------------------------------------------------------------
# function to post like on the recent post

def like_post(insta_username):
  media_id = get_follower_post_id(insta_username)

  print media_id
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": APP_ACCESS_TOKEN}
  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()
  if post_a_like['meta']['code'] == 200:
    print 'Like was successful!'
  else:
    print 'Your like was unsuccessful. Try again!'


# ------------------------------------------------------------------------------------------------------------------
# function to get list of comment on the recent post


def get_comment_list(insta_username):
  media_id = get_follower_post_id(insta_username)
  print media_id
  if media_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_comment_list = requests.get(request_url).json()
  print user_comment_list

  if user_comment_list['meta']['code'] == 200:
    if len(user_comment_list['data']):
        if len(user_comment_list['data']):
            length = len(user_comment_list['data'])
            i = 0
            print 'Number of likes you have: %s' % (length)
            while (length):
                print 'Comment:%d. %s' % (i+1,user_comment_list['data'][i]['text'])
                print 'Username:%d. %s' % (i+1,user_comment_list['data'][i]['from']['username'])
                print 'Name:%d. %s' % (i+1,user_comment_list['data'][i]['from']['full_name'])
                i = i + 1
                length = length - 1

      #comment_list=[user_like_list['data'][0]['text'],user_like_list['data'][0]['from']['username'],user_like_list['data'][0]['from']['full_name']]
      #print comment_list


    else:
      print 'There are no likes on this post!'

  else:
    print 'Status code other than 200 received!'


# ------------------------------------------------------------------------------------------------------------------
# function to post comment on the recent post

def post_comment(insta_username):
  media_id = get_follower_post_id(insta_username)
  comment_text = raw_input("Your comment: ")
  payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
  request_url = (BASE_URL + 'media/%s/comments') % (media_id)
  print 'POST request url : %s' % (request_url)

  make_comment = requests.post(request_url, payload).json()

  if make_comment['meta']['code'] == 200:
    print "Successfully added a new comment!"
  else:
    print "Unable to add comment. Try again!"

# -------------------------------------------------------------------------------------------------------------------
# function to delete the negative comment
'''

def negative_comment_delete(insta_username):
    media_id = get_follower_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            # Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'
'''

# ----------------------------------------------------------------------------------------------------------------
# https://api.instagram.com/v1/locations/search?lat=48.858844&lng=2.294351&access_token=ACCESS-TOKEN
# https://api.instagram.com/v1/locations/{location-id}/media/recent?access_token=ACCESS-TOKEN
# https://api.instagram.com/v1/media/search?lat=48.858844&lng=2.294351&access_token=ACCESS-TOKEN

def media_found(latitude,longitude):

    if latitude == "" or longitude == "":
        print "enter valid latitude and longitute"
        exit()

    else:
        request_url=BASE_URL+'media/search?lat=%s&lng=%s&access_token=%s' %(latitude,longitude,APP_ACCESS_TOKEN)
        media_info = requests.get(request_url).json()
        if media_info['meta']['code']==200:
            length = len(media_info['data'])
            if len(media_info['data']):
                i=0
                k=0
                length=len(media_info['data'])
                while(length):
                    if media_info['data'][i]['type']=="image" and ( media_info['data'][i]['caption']['text']=="flood" or media_info['data'][i]['caption']['text']=="earthquake" ):
                        image_name = media_info['data'][i]['id'] + '.jpeg'
                        image_url = media_info['data'][i]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        print 'Your image has been downloaded! and image id is %s' % (media_info['data'][0]['id'])
                        k=k+1
                    else:
                        print "No image of calamity is found"
                    length=length-1
                    i=i+1
                print "total no image found=%s" %(k)

            else:
                print "No media found in the searched location"

        else:
            print 'Status code other than 200 received!'


#

# ----------------------------------------------------------------------------------------------------------------
# function to start the bot

def bot_start():
    while True:
        print '\n'
        print 'Hey Buddy! Welcome to INSTABOT!\n'
        print 'Please select from menu options:\n'
        print '1.Get your own Instagram details\n'
        print '2.Get details of a user(follower) by username\n'
        print '3.Get your own recent post\n'
        print '4.Get the recent post of a user(follower) by username\n'
        print '5.Get a list of people who have liked the recent post of a user(follower)\n'
        print '6.Like the recent post of a user(follower)\n'
        print '7.Get a list of comments on the recent post of a user(follower)\n'
        print '8.Write a comment on the recent post of a user(follower)\n'
        #print '9.Delete negative comments from the recent post of a user(follower)\n'
        print '9.To predict image using latitude and longitude \n'
        print '10.Exit \n'

        # ---------------------------------------------------------------------------------

        choice = raw_input('Enter you choice: ')
        if choice == '1':
            own_information()
        elif choice == '2':
            insta_username = raw_input('Enter the username of the user: ')
            if insta_username=='':
                print "Enter valid username"
            else:
                get_follower_user_information(insta_username)
            # ---------------------------------------------------------------------------------
            # sub menu
                while True:
                    print insta_username+'\n'
                    print 'Please choose what you want to do with :'+insta_username+'\n'
                    print 'a. Like the post'
                    print 'b. Comment on post'
                    print 'c. Go to main menu'

                    choice_sub_menu=raw_input('Enter your choice:')
                    if choice_sub_menu=='a':
                        like_post(insta_username)
                    elif choice_sub_menu=='b':
                        post_comment(insta_username)
                    elif choice_sub_menu=='c':
                        bot_start()
                    else:
                        exit()
            # -------------------------------------------------------------------------------------


        elif choice == '3':
            get_own_post()
        elif choice == '4':
            insta_username = raw_input('Enter the username of the user: ')
            if insta_username=='':
                print "Enter valid username"
            else:
                get_follower_user_post(insta_username)
        elif choice=='5':
           insta_username = raw_input('Enter the username of the user: ')
           if insta_username=='':
               print "Enter valid username"
           else:
               get_like_list(insta_username)
        elif choice=='6':
           insta_username = raw_input('Enter the username of the user: ')
           if insta_username=='':
               print "Enter valid username"
           else:
               like_post(insta_username)
        elif choice=='7':
           insta_username = raw_input('Enter the username of the user: ')
           if insta_username=='':
               print "Enter valid username"
           else:
               get_comment_list(insta_username)
        elif choice=='8':
           insta_username = raw_input('Enter the username of the user: ')
           if insta_username=='':
               print "Enter valid username"
           else:
               post_comment(insta_username)
               '''
        elif choice=='9':
           insta_username = raw_input('Enter the username of the user: ')
           if insta_username=='':
               print "Enter valid username"
           else:
               negative_comment_delete(insta_username)
'''
        elif choice=='9':
            latitude = (raw_input('Please enter the latitude :'))
            longitude = (raw_input('Please enter the longitude :'))
            media_found(latitude,longitude)

        elif choice == '10':
            exit()
        else:
            print 'Please choose correct option'

bot_start()