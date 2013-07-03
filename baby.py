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
    for hour in range(0, 24):
      for minute in range(0, 60, 10):
        time = datetime.time(hour, minute)
        times.append(time)
    return times

  def startElement(self, name, attrs):

    if name == 'h3':
      self.h3 = True

    if name == 'li':
      self.li = True
  
  def characters(self, content):

    if self.h3 == True:
      self.currentDate = datetime.datetime.strptime(content, '%Y-%m-%d')

    if self.li == True:
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

      # get the start time and round to the nearest 10 minutes
      date = datetime.datetime.strptime(
          '%s %s' % (self.currentDate.strftime('%Y-%m-%d'),
          content[:8]),
          '%Y-%m-%d %I:%M %p')
      date += datetime.timedelta(minutes=5)
      date -= datetime.timedelta(minutes=date.minute % 10, seconds=date.second)
      self._addTime(date, babyActivity)

      # use the minutes to fill in subsequent times 
      for i in range(10, minutes, 10):
        date = date + datetime.timedelta(minutes=10)
        self._addTime(date, babyActivity)

  def _addTime(self, date, activity):

    formattedDate = date.strftime('%Y-%m-%d')
    if not self.dates.get(formattedDate, None):
      self.dates[formattedDate] = {}
    formattedTime = date.strftime('%H:%M')
    if not self.dates[formattedDate].get(formattedTime, None):
      self.dates[formattedDate][formattedTime] = activity

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
        formattedTime = time.strftime('%H:%M')
        output.write(formattedTime)
        for date in dates:
          output.write(',')
          if self.dates[date].get(formattedTime, None):
            output.write(self.dates[date][formattedTime])
        output.write('\n')


if __name__ == '__main__':
  xml.sax.parse('input.html', XmlHandler())
