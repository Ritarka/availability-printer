# availability-printer

This will look through your google calendar and automatically create a list of days/times when you are available to meet.
This does require a bit of setup, so read through this [document](https://developers.google.com/calendar/api/quickstart/python)

## Next steps
- [ ] Timezone and scheduling duration via a command line argument
- [ ] Handle outlook connections as well
- [ ] I also want to add a soft margin blocker (i.e. this should be able to store my preferences and not schedule something 30-min before class for example)
- [ ] 9-5 weekday appoints are allowed so far. Make this more flexible
- [ ] I don't think this can currently handle events that cross midnight. It shouldn't error out at the very least
- [ ] I don't know why it occasionally ends at 6 pm instead of 5, but it's functional enough for me
- [ ] Nicer formatting, maybe break up the text with an extra newline after every week printed


## Example output
```
Here is when I will be available (all times in MDT)
   Thursday   (10/17): 10:00 AM - 06:00 PM
   Friday     (10/18): 10:00 AM - 06:00 PM
   Monday     (10/21): 11:50 AM - 01:30 PM, 02:50 PM - 06:00 PM
   Tuesday    (10/22): 10:00 AM - 06:00 PM
   Wednesday  (10/23): 11:50 AM - 01:30 PM, 02:50 PM - 06:00 PM
   Thursday   (10/24): 10:00 AM - 11:00 AM, 12:00 PM - 05:00 PM
   Friday     (10/25): 10:00 AM - 11:00 AM, 01:50 PM - 06:00 PM
   Monday     (10/28): 11:50 AM - 01:30 PM, 02:50 PM - 05:00 PM
   Tuesday    (10/29): 10:00 AM - 06:00 PM
   Wednesday  (10/30): 11:50 AM - 01:30 PM, 02:50 PM - 06:00 PM
   Thursday   (10/31): 10:00 AM - 11:00 AM, 12:00 PM - 05:00 PM
   Friday     (11/01): 10:00 AM - 11:00 AM, 01:50 PM - 06:00 PM
   Monday     (11/04): 10:00 AM - 11:00 AM, 12:50 PM - 02:30 PM, 03:50 PM - 06:00 PM
   Tuesday    (11/05): 10:00 AM - 06:00 PM
   Wednesday  (11/06): 10:00 AM - 11:00 AM, 12:50 PM - 02:30 PM, 03:50 PM - 06:00 PM
   Thursday   (11/07): 10:00 AM - 12:00 PM, 01:00 PM - 06:00 PM
```
