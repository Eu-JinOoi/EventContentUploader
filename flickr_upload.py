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
    raise Exception("Unable to find photoset " + photoSetName + ".")


def GetFilesInDirectory(path, fileExtensionFilter=None):
    try:
        fileList = []

        for fileInPath in os.listdir(path):
            if fileExtensionFilter is None or fileInPath.lower().endswith(fileExtensionFilter):
                fileList.append(os.path.join(path, fileInPath))
        return fileList
    except:
        PrintTimestamp("The specified path (" + path + ") does not exist.")
        raise Exception("The specified path (" + path + ") does not exist.")


def CreatePhotoSetWithName(photoSetName, primaryPhotoId):
    return flickr_api.Photoset.create(title=photoSetName, primary_photo_id=primaryPhotoId)


def PrintTimestamp(log):
    print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] - " + log)


def remove_file(path_to_file):
    PrintTimestamp("Removing " + pendingImage)
    os.remove(path_to_file)
    PrintTimestamp("Removed " + pendingImage)


def upload_image_to_flickr(image_to_upload):
    PrintTimestamp("Uploading Image: " + image_to_upload)

    uploaded_photo = flickr_api.upload(photo_file=image_to_upload,
                                       title=datetime.datetime.now().strftime("%c"),
                                       hidden=0,
                                       is_public=1,
                                       tags='unprocessed WSJ2019 "World Scout Jamboree" "World Scout Jamboree 2019" "ScoutJamboree" "2019 WSJ" "Summit Bechtel Reserve" "24WSJ" "24th World Scout Jamboree"')
    photo_id = uploaded_photo.id
    PrintTimestamp("Uploaded '" + image_to_upload + "' to Flickr with ID " + photo_id)
    return photo_id


PrintTimestamp("Starting Flickr Upload Script")
# photoSetName="Unprocessed Images"
photoSetName = "24th World Scout Jamboree"
processDelimiterString = "================================="

PrintTimestamp("Loading configuration from file.")
config = ConfigParser.ConfigParser()
config.readfp(open('app.config'))

authFile = "flickr_auth.txt"
configSectionFlickr = "Flickr"
flickr_api.set_keys(api_key=config.get(configSectionFlickr, "ApiKey"),
                    api_secret=config.get(configSectionFlickr, "ApiSecret"))
flickr_api.set_auth_handler(authFile)
photoSetUser = config.get(configSectionFlickr, "UserName")
unprocessedPhotoSet = None

pendingImages = GetFilesInDirectory("/media/sda1/photos/", "jpg")
if pendingImages is not None and len(pendingImages) != 0:
    for pendingImage in pendingImages:
        try:
            print(processDelimiterString)
            PrintTimestamp("Processing Image: " + pendingImage)
            photoId = upload_image_to_flickr(pendingImage)

            if unprocessedPhotoSet is None:
                try:
                    unprocessedPhotoSet = GetPhotoSetWithName(photoSetUser, photoSetName)
                except:
                    PrintTimestamp("The photoset '" + photoSetName + "' does not exist. Attempting to create.")
                    unprocessedPhotoSet = CreatePhotoSetWithName(photoSetName, photoId)
                    unprocessedPhotoSet = GetPhotoSetWithName(photoSetUser, photoSetName)
                if unprocessedPhotoSet is None:
                    raise Exception("Unable to create the photoset " + photoSetName)
            try:
                PrintTimestamp("Added photo " + photoId + " to the photoset " + photoSetName + ".")
                unprocessedPhotoSet.addPhoto(photo_id=photoId)
            except:
                PrintTimestamp("Adding photo " + photoId + " to the photoset " + photoSetName + " has failed.")
            remove_file(pendingImage)
            print(processDelimiterString)
        except Exception as e:
            PrintTimestamp("An error occured while uploading "+pendingImage+".")

    PrintTimestamp("All images processed.")
else:
    PrintTimestamp("There are no images to upload.")
