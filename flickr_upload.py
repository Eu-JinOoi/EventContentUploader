#!/usr/bin/python
import flickr_api
import datetime
import os
import ConfigParser

def GetPhotoSetWithName(username, photoSetName):
    PrintTimestamp("Looking for photoset " + photoSetName + " for user " + username)
    user = flickr_api.Person.findByUserName(username)
    photosets = user.getPhotosets()

    for photoset in photosets:
        if photoSetName == photoset.title:
            return photoset
    raise Exception("Unable to find photoset "+photoSetName + ".");

def GetFilesInDirectory(path, fileExtensionFilter=None):
    fileList=[]
    
    for file in os.listdir(path):
        if fileExtensionFilter == None or file.endswith(fileExtensionFilter):
            fileList.append(os.path.join(path,file));
    return fileList

def CreatePhotoSetWithName(photoSetName, primaryPhotoId):
    return flickr_api.Photoset.create(title=photoSetName, primary_photo_id=primaryPhotoId)

def PrintTimestamp(log):
    print("["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] - "+ log); 

PrintTimestamp("Starting Flickr Upload Script");
photoSetUser="BNSF4924"
#photoSetName="Unprocessed Images"
photoSetName="Test New Photoset 1";

PrintTimestamp("Loading configuration from file.")
config = ConfigParser.ConfigParser()
config.readfp(open('app.config'))


authFile="flickr_auth.txt"
configSectionFlickr="Flickr"
flickr_api.set_keys(api_key = config.get(configSectionFlickr,"ApiKey"), api_secret = config.get(configSectionFlickr,"ApiSecret"))
flickr_api.set_auth_handler(authFile)

pendingImages=GetFilesInDirectory("images", "jpg")
if pendingImages is not None and len(pendingImages) !=0 :
    for pendingImage in pendingImages:
        print("=================================")
        PrintTimestamp("Processing Image: "+ pendingImage);

        uploadedPhoto=flickr_api.upload(photo_file=pendingImage ,title=datetime.datetime.now().strftime("%c"),hidden=1,is_public=0, tags='unprocessed WSJ2019 "TEST Multiword"');
        photoId = uploadedPhoto.id
        PrintTimestamp("Uploaded '" + pendingImage + "' to Flickr with ID "+ photoId);
        unprocessedPhotoSet=None
        try:
            unprocessedPhotoSet = GetPhotoSetWithName(photoSetUser, photoSetName)
        except:
            PrintTimestamp("The photoset '" + photoSetName + "' does not exist. Attempting to create.")
            unprocessedPhotoSet = CreatePhotoSetWithName(photoSetName, photoId);
            unprocessedPhotoSet = GetPhotoSetWithName(photoSetUser, photoSetName)
        if unprocessedPhotoSet is None:
            raise Exception("Unable to create the photoset "+photoSetName);
        unprocessedPhotoSet.addPhoto(photo_id=photoId);
        PrintTimestamp("Removing "+ pendingImage);
        os.remove(pendingImage);
        PrintTimestamp("Removed "+ pendingImage);
        print("=================================")
    PrintTimestamp("All images processed.")
else:
    PrintTimestamp("There are no images to upload.")

