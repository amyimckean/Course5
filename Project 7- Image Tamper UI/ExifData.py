import piexif
from datetime import datetime


# This class should flatten the data from the pie exif library and make it easier to work with
# for the UI
class ExifData:
    Latitude = 0
    ExifLat = ((0, 1), (0, 1), (0, 1))
    OrigExifLat = ((0, 1), (0, 1), (0, 1)) #Exists to save the original data
    LatitudeRef = 'N'
    Longitude = 0
    ExifLon = ((0, 1), (0, 1), (0, 1))
    OrigExifLon = ((0, 1), (0, 1), (0, 1)) #Exists to save the original data
    LongtitudeRef = 'W'
    DateValue = datetime.now().strftime("%Y:%m:%d")
    TimeValue = datetime.now().strftime("%H:%M:%S")
    #If these aren't dirty, use the original data. Preserves exact calculations
    LatDirty = False
    LonDirty = False

    #Takes a picture file parameter and returns a populated object
    def __init__(self, pictureFile):
        if pictureFile is "":
            return
        try:
            self.ExifInfo =  piexif.load(pictureFile)
            
            # Populate the GPS properties
            gpsinfo = self.ExifInfo["GPS"]
            if gpsinfo:
                self.ExifLat = gpsinfo[piexif.GPSIFD.GPSLatitude]
                self.OrigExifLat = gpsinfo[piexif.GPSIFD.GPSLatitude]
                self.LatitudeRef = gpsinfo[piexif.GPSIFD.GPSLatitudeRef]
                self.ExifLon = gpsinfo[piexif.GPSIFD.GPSLongitude]
                self.OrigExifLon = gpsinfo[piexif.GPSIFD.GPSLongitude]
                self.LongtitudeRef = gpsinfo[piexif.GPSIFD.GPSLongitudeRef]

            # Populate the time property
            timeInfo = self.ExifInfo["Exif"]
            if timeInfo:
                try:
                    dateTime = timeInfo[piexif.ExifIFD.DateTimeOriginal]
                    if(len(dateTime.split()) > 1):
                        self.DateValue = dateTime.split()[0]
                        self.TimeValue = dateTime.split()[1]
                except:
                    # Sometimes getting an exception related to importing the time data
                    print "Error processing provided time."
        except Exception as ex:
            print ex

    # This section will set the properties and be bound to the data changed events. It
    # also consolidates the location of the properties being set
    def setLon(self, value):
        self.LonDirty = True
        self.Longitude = value

    def setLonRef(self, value):
        self.LongtitudeRef = value
        
    def setLatRef(self, value):
        self.LatitudeRef = value

    def setLat(self, value):
        self.LatDirty = True
        self.Latitude = value

    def setTime(self, value):
        self.TimeValue = value

    # Data comes into this in string and wx.DateTime format so it needs to handle both
    def setDate(self, value):
        if type(value) is not str:
            self.DateValue = value.Format("%Y:%m:%d") 
        else:
            self.DateValue = value

    # Get the new or original latitude values dependent on user modification
    def getCorrectLat(self):
        if(self.LatDirty):
            return self.ExifLat
        else:
            return self.OrigExifLat
        
    # Get the new or original longitude values dependent on user modification
    def getCorrectLon(self):
        if(self.LonDirty):
            return self.ExifLon
        else:
            return self.OrigExifLon

    # This will the pie exif expected format of the data
    def getExifInfo(self):
        if self.ExifInfo["GPS"]:
            self.ExifInfo["GPS"][piexif.GPSIFD.GPSLatitudeRef] = self.LatitudeRef
            self.ExifInfo["GPS"][piexif.GPSIFD.GPSLongitudeRef] = self.LongtitudeRef
            self.ExifInfo["GPS"][piexif.GPSIFD.GPSLatitude] = self.getCorrectLat()
            self.ExifInfo["GPS"][piexif.GPSIFD.GPSLongitude] = self.getCorrectLon()
        else:
            self.ExifInfo["GPS"] = {  piexif.GPSIFD.GPSLatitudeRef: self.LatitudeRef,
                                      piexif.GPSIFD.GPSLongitudeRef: self.LongtitudeRef,
                                      piexif.GPSIFD.GPSLatitude: self.getCorrectLat(),
                                      piexif.GPSIFD.GPSLongitude: self.getCorrectLon()
                                    }

        if self.ExifInfo["Exif"]:
            self.ExifInfo["Exif"][piexif.ExifIFD.DateTimeOriginal] = self.DateValue + " " + self.TimeValue
        else:
            self.ExifInfo["Exif"] = { piexif.ExifIFD.DateTimeOriginal : self.DateValue + " " + self.TimeValue
                                     }
        return self.ExifInfo
