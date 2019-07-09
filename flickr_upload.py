#!/usr/bin/python

import flickr_api
import datetime

def GetPhotoSetWithName(username, photoSetName):
    print ("Looking for photoset " + photoSetName + " for user " + username)
    user = flickr_api.Person.findByUserName(username)
    photosets = user.getPhotosets()

    for photoset in photosets:
        print ("->"+photoset.title)
        if photoSetName == photoset.title:
            return photoset



x = datetime.datetime.now()
print(x.strftime("%Y-%m-%d"))


authFile="flickr_auth.txt"
flickr_api.set_keys(api_key = 'a728291d2f58107fd0d54d3e0989a0c7', api_secret = 'd51a879aa9a164a9')
flickr_api.set_auth_handler(authFile)

photo=flickr_api.upload(photo_file="images/23.jpg",title=x.strftime("%c"),hidden=1,is_public=0, tags='unprocessed WSJ2019 "TEST Multiword"');
photoId = photo.id
print photoId


#user = flickr_api.Person.findByUserName("BNSF4924")
#photosets = user.getPhotosets()
#print photosets
#photosetName="Unprocessed Images";
#unprocessedPhotoset = None;

#find photoset
#for photoset in photosets:
#    print photoset.title
#    if photosetName==photoset.title:
#        unprocessedPhotoset = photoset
#        break
#unprocessedPhotoset.addPhoto(photo_id=photoId);

unprocessedPhotoset=GetPhotoSetWithName("BNSF4924","Unprocessed Images")
print unprocessedPhotoset
unprocessedPhotoset.addPhoto(photo_id=photoId);


#unprocessedAlbum="72157709523482812"
#flickr_api.Photoset.addPhoto(photoset_id=unprocessedAlbum, photo_id=photoId);
