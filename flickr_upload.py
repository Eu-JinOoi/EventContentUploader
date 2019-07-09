#!/usr/bin/python
import flickr_api
import datetime
import os

def GetPhotoSetWithName(username, photoSetName):
    print ("Looking for photoset " + photoSetName + " for user " + username)
    user = flickr_api.Person.findByUserName(username)
    photosets = user.getPhotosets()

    for photoset in photosets:
        print ("->"+photoset.title)
        if photoSetName == photoset.title:
            return photoset

def GetFilesInDirectory(path, fileExtensionFilter=None):
    fileList=[]
    
    for file in os.listdir(path):
        if fileExtensionFilter == None or file.endswith(fileExtensionFilter):
            fileList.append(os.path.join(path,file));
    return fileList


print("Script starting at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"));

photoSetUser="BNSF4924"
photoSetName="Unprocessed Images"


authFile="flickr_auth.txt"
flickr_api.set_keys(api_key = 'a728291d2f58107fd0d54d3e0989a0c7', api_secret = 'd51a879aa9a164a9')
flickr_api.set_auth_handler(authFile)

pendingImages=GetFilesInDirectory("images", "jpg")
if pendingImages is not None and len(pendingImages) !=0 :
    for pendingImage in pendingImages:
        print("=================================")
        print("Processing Image: "+ pendingImage);
        uploadedPhoto=flickr_api.upload(photo_file=pendingImage ,title=x.strftime("%c"),hidden=1,is_public=0, tags='unprocessed WSJ2019 "TEST Multiword"');
        photoId = uploadedPhoto.id
        print("Uploaded " + pendingImage + " to Flickr with ID "+ photoId);
        unprocessedPhotoset=GetPhotoSetWithName(photoSetUser, photoSetName)
        unprocessedPhotoset.addPhoto(photo_id=photoId);
        print("Removing "+ pendingImage);
        os.remove(pendingImage);
        print("Removed "+ pendingImage);
        print("=================================")
    print("All images processed at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
else:
    print ("There are no images to upload. Finished at "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

