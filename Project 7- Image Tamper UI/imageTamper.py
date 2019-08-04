import piexif
import sys
import random
import datetime
from shutil import copyfile
from ExifData import ExifData

# Returns an integer from a float for degrees
def getCoordinateDegrees(number):
    return int(number)

# Returns a calculation of minutes in relation to the randomly generated float
def getCoordinateMinutes(number):
    return int((number - int(number)) *60)

# Returns a randomly generated seconds value for the random float and calculated minutes
def getCoordinateSeconds(number, minutes):
    return int((number - int(number) - minutes/60) * 3600)

# Returns coordinates for the provided random value               
def getCoordinate(number):
    degrees = getCoordinateDegrees(number)
    minutes = getCoordinateMinutes(number)
    seconds = getCoordinateSeconds(number, minutes)
    return ((degrees, 1), (minutes, 1), (seconds, 1))

def getNumberFromCoordinate(coordinates):
    topNumbers, bottomNumbers = zip(*coordinates)
    firstTop, secondTop, thirdTop = topNumbers
    firstBottom, secondBottom, thirdBottom = bottomNumbers
    hour = firstTop/firstBottom
    minutes = (secondTop/thirdBottom)/60.0000
    seconds = (thirdTop/thirdBottom)/3600.0000
    degree = hour + minutes + seconds
    return degree
        
# Returns a random time in string format
# I realize my original assignment missed points because this didn't have the correctly
# padded values. However, using the UI controls has resolved this issue and properly displays and saves
# the padded times
def getRandomTime():
    hours = random.randint(0,23)
    minutes = random.randint(0,59)
    seconds = random.randint(0,59)
    return ("%s:%s:%s") % (hours, minutes, seconds)

# Returns a random date
def getRandomDate():
    endDateOrdinal = datetime.datetime.now().toordinal() #Get today's ordinal date
    startDateOrdinal = (datetime.datetime.now() - datetime.timedelta(days=36500)).toordinal() #Get ordinal date from 100 years ago
    randomDateOrdinal = random.randint(startDateOrdinal, endDateOrdinal) #Select a random date
    randomDate = datetime.date.fromordinal(randomDateOrdinal) #Return ordinal date to standard format
    return ("%s:%s:%s") % (randomDate.year, randomDate.month, randomDate.day)

# Returns the proper string format for date and time
def getRandomDateTime():
    return ("%s %s") % (getRandomDate(), getRandomTime())

# Returns pie exif data from the ExifData object
def getPieExif(ExifData):
    ExifData.ExifLat = getCoordinate(ExifData.Latitude)
    ExifData.ExifLon = getCoordinate(ExifData.Longitude)
    return ExifData.getExifInfo()

# Takes a picture File parameter and returns an ExifData object
def getExifDataFromPicture(pictureFile):
    exifData = ExifData(pictureFile)
    if(exifData.OrigExifLat != ""):
        exifData.Longitude = getNumberFromCoordinate(exifData.OrigExifLon) 
        exifData.Latitude = getNumberFromCoordinate(exifData.OrigExifLat)
    return exifData

# Writers the pie exif data to the provided output file
def writeExifDataToFile(exif, inputFile, outputFileImageName):
    try:
        # Copy file to user specified location   
        copyfile(inputFile, outputFileImageName)
    except IOError:
        print "Destination location is not writeable " + inputFile
        
    # Try getting exif bytes. Catch InvalidImageDataError exceptions and
    # try reprocessing without thumbnail and lst data, per documentation suggestions:
    # https://buildmedia.readthedocs.org/media/pdf/piexif/latest/piexif.pdf
    try:
        exifBytes = piexif.dump(exif)
        piexif.insert(exifBytes, outputFileImageName)
        return True
    except Exception as ex:
        if ex.__class__.__name__ is "InvalidImageDataError":
            del exif["1st"]
            del exif["thumbnail"]
            exifBytes = piexif.dump(exif)
            piexif.insert(exifBytes, outputFileImageName)
        else:
            return False
            
