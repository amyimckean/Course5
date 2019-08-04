import wx
import wx.lib.masked as masked
from datetime import datetime
import random
import imageTamper
import piexif
import wx.adv

# Panel class houses all of the controls
class ImagePanel(wx.Panel):
 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.ExifData = imageTamper.getExifDataFromPicture("")

        # Image Label
        imageLabel = wx.StaticText(self, wx.ALIGN_CENTRE_HORIZONTAL, label="Select an Image to modify:")

        # File picker control
        self.filePickerControl = wx.FilePickerCtrl(self)
        self.filePickerControl.Bind(wx.EVT_FILEPICKER_CHANGED, self.showImage)

        # Control to show image
        self.imageControl = wx.StaticBitmap(self,-1, wx.Bitmap(0,0))

        # Divider to separate content
        dividerLine = wx.StaticLine(self, wx.ID_ANY, size=(350, 2), style=wx.LI_HORIZONTAL)

        # Latitude random button
        latRandomButton = wx.Button(self, label='Random')
        latRandomButton.Bind(wx.EVT_BUTTON, self.latRandomUpdate)

        # Control to set latitude
        self.latControl = wx.SpinCtrlDouble(self, -1, '')
        self.latControl.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.ExifData.setLat(self.latControl.GetValue()))
        self.latControl.SetRange(0.00, 90.00)
        self.latControl.SetValue(0.00)

        # Latitude Label
        latLabel = wx.StaticText(self, wx.ALIGN_CENTRE_HORIZONTAL, label="Latitude")

        # Latitude panel
        latPanel = wx.BoxSizer()
        latPanel.Add(latRandomButton, proportion=0,  flag=wx.ALL,  border=5)
        latPanel.Add(self.latControl, proportion=0,  flag=wx.ALL,  border=5)
        latPanel.Add(latLabel, proportion=1, flag=wx.RIGHT|wx.BOTTOM|wx.TOP, border=10 )

        # Latitude Direction random button
        latDirectionRandomButton = wx.Button(self, label='Random')
        latDirectionRandomButton.Bind(wx.EVT_BUTTON, self.latDirectionRandomUpdate)

        # Control to set latitude Direction
        self.latNDirectionControl = wx.RadioButton(self, label="N", style = wx.RB_GROUP)
        self.latSDirectionControl = wx.RadioButton(self, label="S")
        self.latNDirectionControl.Bind(wx.EVT_RADIOBUTTON, lambda event: self.ExifData.setLatRef('N')) 
        self.latSDirectionControl.Bind(wx.EVT_RADIOBUTTON, lambda event: self.ExifData.setLatRef('S')) 
        self.latNDirectionControl.SetValue(True)

        # Latitude Direction Label
        latDirectionLabel = wx.StaticText(self, wx.ALIGN_CENTRE_HORIZONTAL, label="Latitude Direction")

        # Latitude Direction panel
        latDirectionPanel = wx.BoxSizer()
        latDirectionPanel.Add(latDirectionRandomButton, proportion=0,  flag=wx.ALL,  border=5)
        latDirectionPanel.Add(self.latNDirectionControl, proportion=0,  flag=wx.ALL,  border=5)
        latDirectionPanel.Add(self.latSDirectionControl, proportion=0,  flag=wx.ALL,  border=5)
        latDirectionPanel.Add(latDirectionLabel, proportion=1, flag=wx.RIGHT|wx.BOTTOM|wx.TOP, border=10 )

        # Longitude random button
        lonRandomButton = wx.Button(self, label='Random')
        lonRandomButton.Bind(wx.EVT_BUTTON, self.lonRandomUpdate)

        # Longitude value control
        self.lonControl = wx.SpinCtrlDouble(self, -1, '')
        self.lonControl.Bind(wx.EVT_SPINCTRLDOUBLE,lambda event: self.ExifData.setLon(self.lonControl.GetValue()))
        self.lonControl.SetRange(0.0000, 180.0000)
        self.lonControl.SetValue(0)

        # Logitude label
        lonLabel = wx.StaticText(self, label="Longitude")

        # Longitude panel
        lonPanel = wx.BoxSizer()
        lonPanel.Add(lonRandomButton, proportion=0,  flag=wx.ALL,  border=5)
        lonPanel.Add(self.lonControl, proportion=0,  flag=wx.ALL,  border=5)
        lonPanel.Add(lonLabel, proportion=1, flag=wx.RIGHT|wx.BOTTOM|wx.TOP, border=10 )

        # Longitude Direction random button
        lonDirectionRandomButton = wx.Button(self, label='Random')
        lonDirectionRandomButton.Bind(wx.EVT_BUTTON, self.lonDirectionRandomUpdate)

        # Control to set Longitude Direction
        self.lonWDirectionControl = wx.RadioButton(self, label="W", style = wx.RB_GROUP)
        self.lonEDirectionControl = wx.RadioButton(self, label="E")
        self.lonWDirectionControl.Bind(wx.EVT_RADIOBUTTON, lambda event: self.ExifData.setLonRef('W')) 
        self.lonEDirectionControl.Bind(wx.EVT_RADIOBUTTON, lambda event: self.ExifData.setLonRef('E')) 
        self.lonWDirectionControl.SetValue(True)

        # Longitude Direction Label
        lonDirectionLabel = wx.StaticText(self, wx.ALIGN_CENTRE_HORIZONTAL, label="Longitude Direction")

        # Longitude Direction panel
        lonDirectionPanel = wx.BoxSizer()
        lonDirectionPanel.Add(lonDirectionRandomButton, proportion=0,  flag=wx.ALL,  border=5)
        lonDirectionPanel.Add(self.lonWDirectionControl, proportion=0,  flag=wx.ALL,  border=5)
        lonDirectionPanel.Add(self.lonEDirectionControl, proportion=0,  flag=wx.ALL,  border=5)
        lonDirectionPanel.Add(lonDirectionLabel, proportion=1, flag=wx.RIGHT|wx.BOTTOM|wx.TOP, border=10 )

        # Time random button
        timeRandomButton = wx.Button(self, label='Random')
        timeRandomButton.Bind(wx.EVT_BUTTON, self.timeRandomUpdate)

        # Time value control
        self.timeControl = masked.TimeCtrl(self, value='00:00:00', name="Time", fmt24hr=True)
        self.timeControl.Bind(wx.lib.masked.EVT_TIMEUPDATE, lambda event: self.ExifData.setTime(self.timeControl.GetValue())) 

        # Time label
        timeLabel = wx.StaticText(self, label="Time")

        # Time panel
        timePanel = wx.BoxSizer()
        timePanel.Add(timeRandomButton, proportion=0,  flag=wx.ALL,  border=5)
        timePanel.Add(self.timeControl, proportion=0,  flag=wx.ALL,  border=5)
        timePanel.Add(timeLabel, proportion=1, flag=wx.RIGHT|wx.BOTTOM|wx.TOP, border=10 )

        # Date random button
        dateRandomButton = wx.Button(self, label='Random')
        dateRandomButton.Bind(wx.EVT_BUTTON, self.dateRandomUpdate)

        # Date value control
        self.dateControl = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime)
        self.dateControl.Bind(wx.adv.EVT_DATE_CHANGED, lambda event: self.ExifData.setDate(self.dateControl.GetValue()))  

        # Date label
        dateLabel = wx.StaticText(self, label="Date")

        # Date panel
        datePanel = wx.BoxSizer()
        datePanel.Add(dateRandomButton, proportion=0,  flag=wx.ALL,  border=5)
        datePanel.Add(self.dateControl, proportion=0,  flag=wx.ALL,  border=5)
        datePanel.Add(dateLabel, proportion=1, flag=wx.RIGHT|wx.BOTTOM|wx.TOP, border=10 )

        # Date label
        fileLabel = wx.StaticText(self, label="Enter a file or path and file for your new image:")

        # New File control
        self.newFileControl = wx.TextCtrl(self,size = (315,25))

        # Save Button
        self.saveButton = wx.Button(self, label='Save')
        self.saveButton.Bind(wx.EVT_BUTTON, self.saveFile)
        self.saveButton.Disable()

        # Vertical organizer
        vertBox = wx.BoxSizer(wx.VERTICAL)
        vertBox.Add(imageLabel, proportion=0, flag=wx.LEFT|wx.TOP, border=10)
        vertBox.Add(self.filePickerControl, proportion=0, flag=wx.LEFT, border=10)
        vertBox.Add(self.imageControl, proportion=0, flag=wx.LEFT, border=10)
        vertBox.Add(dividerLine, proportion=0, flag=wx.BOTTOM|wx.TOP, border=10)
        vertBox.Add(latPanel, proportion=0, flag=wx.LEFT, border=5)
        vertBox.Add(latDirectionPanel, proportion=0, flag=wx.LEFT, border=5)
        vertBox.Add(lonPanel, proportion=0,  flag=wx.LEFT,  border=5)
        vertBox.Add(lonDirectionPanel, proportion=0, flag=wx.LEFT, border=5)
        vertBox.Add(timePanel, proportion=0,  flag=wx.LEFT,  border=5)
        vertBox.Add(datePanel, proportion=0,  flag=wx.LEFT,  border=5)
        vertBox.Add(fileLabel, proportion=0,  flag=wx.LEFT|wx.TOP, border=10)
        vertBox.Add(self.newFileControl, proportion=0, flag=wx.LEFT, border=10)
        vertBox.Add(self.saveButton, proportion=0, flag=wx.LEFT|wx.TOP, border=10)


        # Finally, I use the SetSizer function to automatically size the windows based on the
        # the definitions above
        self.SetSizer(vertBox)

        #Update layout controls to be correctly sized on load
        self.Layout()

    # Event to generate a random lat and update the control and property
    def latRandomUpdate(self, event):
        self.ExifData.setLat(random.uniform(0,90))
        self.latControl.SetValue(self.ExifData.Latitude)

    # Event to generate a random lon and update the control and property
    def lonRandomUpdate(self, event):
        self.ExifData.setLon(random.uniform(0,180))
        self.lonControl.SetValue(self.ExifData.Longitude)

    # Event to generate a random time and update the control and property
    def timeRandomUpdate(self, event):
        self.ExifData.setTime(imageTamper.getRandomTime())
        self.setTimeControl(self.ExifData.TimeValue)

    # Sets the time control
    def setTimeControl(self, time):
        if(time != ""):
            self.timeControl.SetValue(time)

    # Event to generate a random date and update the control and property
    def dateRandomUpdate(self, event):
        self.ExifData.setDate(imageTamper.getRandomDate())
        self.setDateControl(self.ExifData.DateValue)

    # Sets the date control
    def setDateControl(self, date):
        if date != "":
            splitParts = date.split(':')

            # The date picker control is apparently 0 based for the month
            # So, unless you subtract 1 from each of the incoming dates, they're
            # all one month off. 
            wxDate = wx.DateTime.FromDMY(int(splitParts[2]), int(splitParts[1])-1,
                                    int(splitParts[0]))
            self.dateControl.SetValue(wxDate)

    # Event to generate a random lon ref and update the control and property
    def lonDirectionRandomUpdate(self, event):
        self.ExifData.setLonRef(random.choice(['E','W']))
        self.setLonRefControl(self.ExifData.LongtitudeRef)

    # Sets the lon ref control
    def setLonRefControl(self, choice):
        if choice is 'E':
            self.lonEDirectionControl.SetValue(True)
        else:
            self.lonWDirectionControl.SetValue(True)

    # Event to generate a random lat ref and update the control and property
    def latDirectionRandomUpdate(self, event):
        self.ExifData.setLatRef(random.choice(['N','S']))
        self.setLatRefControl(self.ExifData.LatitudeRef)

    # Sets the lat ref control
    def setLatRefControl(self, choice):
        if choice is 'N':
            self.latNDirectionControl.SetValue(True)
        else:
            self.latSDirectionControl.SetValue(True)

    # Sets a new image in the control from the user provided image
    def setImage(self, pictureFile):
        self.Refresh()
        image = wx.Image(pictureFile, wx.BITMAP_TYPE_ANY)
        height = image.GetHeight()
        width = image.GetWidth()
        if(height > 200):
            width = (200 * width) / height
            image.Rescale(width ,200)
        picture = wx.Bitmap(image)
        self.imageControl.SetBitmap(picture)
        #Update layout controls to be correctly sized on load
        self.Layout()

    # Takes the image and populates all the controls with data from the new picture
    def populateImageData(self, pictureFile):
        self.ExifData =  imageTamper.getExifDataFromPicture(pictureFile)
        self.latControl.SetValue(self.ExifData.Latitude)
        self.lonControl.SetValue(self.ExifData.Longitude)
        self.setLonRefControl(self.ExifData.LongtitudeRef)
        self.setLatRefControl(self.ExifData.LatitudeRef)
        self.setDateControl(self.ExifData.DateValue)
        self.timeControl.SetValue(self.ExifData.TimeValue)

    # User executed save of the file with the new user provided values
    def saveFile(self, event):
        pictureFile = self.newFileControl.GetValue()
        if(pictureFile != ""):
            exif = imageTamper.getPieExif(self.ExifData)
            result = imageTamper.writeExifDataToFile(exif, self.filePickerControl.GetPath(), pictureFile)
            if result:
                dial = wx.MessageDialog(None, 'Success!!', 'Info', wx.OK)
                dial.ShowModal()
            else:
                dial = wx.MessageDialog(None, 'Failed to write photo', 'Info', wx.OK)
                dial.ShowModal()

    # User has selected a new picture to modify. Populate all the controls with new data
    def showImage(self, event):
        self.saveButton.Enable()
        try:
            pictureFile = self.filePickerControl.GetPath()
            self.setImage(pictureFile)
            self.populateImageData(pictureFile)
        except Exception as ex:
            print ex

# Frame contains the panel
class ImageFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="Image Tamper", size =(350,650))
        panel = ImagePanel(self)
        self.Show()
        
# Main method to execute program 
if __name__ == '__main__':
    app = wx.App(False)
    frame = ImageFrame()
    app.MainLoop()
