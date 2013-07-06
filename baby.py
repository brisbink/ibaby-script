import xml.sax
import datetime

TIME_INCREMENT = 10


class XmlHandler(xml.sax.handler.ContentHandler):

  def __init__(self):

    self.h3 = False
    self.li = False
    self.currentDate = ''
    self.dates = {}
    self.allTimes = self._initTimes()
    self.lastNurseTime = None

  def _initTimes(self):

    times = []
    for hour in range(0, 24):
      for minute in range(0, 60, TIME_INCREMENT):
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
        length = '%dmin' % TIME_INCREMENT
      else:
        length = length[1]

      # get the start date and time and round to the nearest n minutes
      date = datetime.datetime.strptime(
          '%s %s' % (self.currentDate.strftime('%Y-%m-%d'),
          content[:8]),
          '%Y-%m-%d %I:%M %p')
      roundedDate = date + datetime.timedelta(minutes=TIME_INCREMENT/2)
      roundedDate -= datetime.timedelta(
          minutes=roundedDate.minute % TIME_INCREMENT,
          seconds=roundedDate.second)
      formattedDate = roundedDate.strftime('%Y-%m-%d')
      if not self.dates.get(formattedDate, None):
        self.dates[formattedDate] = {
            'Time nursing': 0,
            'Time sleeping': 0,
            'Number nursing': 0,
            'Ave time between nursing': 0,
            'Ave time nursing': 0
        }

      babyActivity = ''
      minutes = 0

      if activity.startswith('Sleep'):
        babyActivity = 'Sleep'
        length = length.split()
        minutes = self._getHourMinute(length)
        self.dates[formattedDate]['Time sleeping'] += minutes / 60.0

      elif activity.startswith('Nurse'):
        babyActivity = 'Nurse'
        length = length.split()
        if len(length) == 1:
          length = ['0', '%dmin' % TIME_INCREMENT]
        else:
          length = length[:-1]
        minutes = self._getHourMinute(length)
        self.dates[formattedDate]['Number nursing'] += 1
        self.dates[formattedDate]['Time nursing'] += minutes / 60.0
        self.dates[formattedDate]['Ave time nursing'] += minutes
        if not self.lastNurseTime:
          self.lastNurseTime = date
        else:
          diff = self.lastNurseTime - date
          self.dates[formattedDate][
              'Ave time between nursing'] += diff.total_seconds() / 60 / 60
          self.lastNurseTime = date

      # add activities to the correct date / time column / row
      self._addTime(roundedDate, babyActivity)
      for i in range(TIME_INCREMENT, minutes, TIME_INCREMENT):
        roundedDate = roundedDate + datetime.timedelta(minutes=TIME_INCREMENT)
        self._addTime(roundedDate, babyActivity)

  def _addTime(self, date, activity):

    formattedDate = date.strftime('%Y-%m-%d')
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
      output.write(',' * len(dates))
      output.write('\n')
      output.write(',' * len(dates))
      output.write('\n')
      output.write(',' * len(dates))
      output.write('\n')
      output.write(',')
      output.write(','.join(dates))
      output.write('\n')
      output.write('Time nursing')
      for date in dates:
        output.write(',')
        output.write('%f' % self.dates[date]['Time nursing'])
      output.write('\n')
      output.write('Ave time between nursing')
      for date in dates:
        output.write(',')
        output.write('%f' % (self.dates[date][
            'Ave time between nursing'] / self.dates[date]['Number nursing']))
      output.write('\n')
      output.write('Ave time nursing')
      for date in dates:
        output.write(',')
        output.write('%f' % (self.dates[date][
            'Ave time nursing'] / 60.0 / self.dates[date]['Number nursing']))


if __name__ == '__main__':
  xml.sax.parse('input.html', XmlHandler())
