
import xml.sax
import datetime


class XmlHandler(xml.sax.handler.ContentHandler):

  def __init__(self):

    self.h3 = False
    self.li = False
    self.currentDate = ''
    self.dates = {}
    self.allTimes = self._initTimes()

  def _initTimes(self):

    times = []
    for meridiem in ['AM', 'PM']:
    	for hour in range(1, 13):
		  	for minute in ['00', '10', '20', '30', '40', '50']:
			  	time = u'%02d:%s %s' % (hour, minute, meridiem)
			  	times.append(time)
    return times

  def startElement(self, name, attrs):

    if name == 'h3':
      self.h3 = True

    if name == 'li':
      self.li = True
  
  def characters(self, content):

    if self.h3 == True:
      self.currentDate = content

    if self.li == True:
      startTime = content[:8]
      activity = content[8:].strip()
      length = activity.split(' ', 1)
      if len(length) == 1:
        length = '10min'
      else:
	      length = length[1]
      babyActivity = ''
      minutes = 0

      if activity.startswith('Sleep'):
		    babyActivity = 'Sleep'
		    length = length.split()
		    minutes = self._getHourMinute(length)

      elif activity.startswith('Nurse'):
        babyActivity = 'Nurse'
        length = length.split()
        if len(length) == 1:
          length = ['0', '10min']
        else:
          length = length[:-1]
        minutes = self._getHourMinute(length)

      # use the start time to find the first time in the times dict
      splitTime = startTime.split()
      meridiem = splitTime[1]

      # round time to the nearest 10 minutes
      startTime = splitTime[0]
      splitTime = startTime.split(':')
      hour = int(splitTime[0])
      minute = int(10 * round(float(splitTime[1])/10))
      date, hour, minute, meridiem = self._adjustStartTime(
          self.currentDate, hour, minute, meridiem)
      self._addTime(date, hour, minute, meridiem, babyActivity)

      # use the minutes to fill in subsequent times 
      for i in range(10, minutes, 10):
        minute += 10
        date, hour, minute, meridiem = self._adjustStartTime(
            date, hour, minute, meridiem)
        self._addTime(date, hour, minute, meridiem, babyActivity)

  def _adjustStartTime(self, date, hour, minute, meridiem):

    if minute >= 60:
      minute = 0
      hour += 1
      if hour > 12:
        hour = 1
      if hour == 12 and minute == 0:
        if meridiem == 'PM':
          meridiem = 'AM'
          date = datetime.datetime.strptime(date, '%Y-%m-%d')
          date = date + datetime.timedelta(days=1)
          date = date.strftime('%Y-%m-%d')
        else: meridiem = 'PM'
    return date, hour, minute, meridiem

  def _addTime(self, date, hour, minute, meridiem, activity):

    time = '%02d:%02d %s' % (hour, minute, meridiem)
    if not self.dates.get(date, None):
      self.dates[date] = {}
    if not self.dates[date].get(time, None):
      self.dates[date][time] = activity

  def _getHourMinute(self, length):

    hour = minute = 0

    if len(length) > 1:
			hour = int(length[0].strip('hr '))
			minute = int(length[1].strip('min '))

    else:
      if length[0].endswith('min'):
        hour = 0
        minute = int(length[0].strip('min '))
      else:
	      hour = int(length[0].strip('hr '))
	      minute = 0

    minutes = 60 * hour + minute
    return minutes

  def endElement(self, name):

    if name == 'h3':
      self.h3 = False

    if name == 'li':
      self.li = False

    if name == 'html':
      output = open('output.csv', 'w')
      output.write(',')
      dates = self.dates.keys()
      dates.sort(reverse=True)
      output.write(','.join(dates))
      output.write('\n')
      for time in self.allTimes:
        output.write(time)
        for date in dates:
          output.write(',')
          if self.dates[date].get(time, None):
            output.write(self.dates[date][time])
        output.write('\n')


if __name__ == '__main__':
	xml.sax.parse('input.html', XmlHandler())
