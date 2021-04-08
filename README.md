# IKEA Click and Meet Slot Finder 📦 🛠

[![Run on Repl.it](https://repl.it/badge/github/insanoid/ikea-click-meet-slot-finder)](https://repl.it/github/insanoid/ikea-click-meet-slot-finder)

- If you have an IKEA near you and you really need a slot for today/tomorrow for click-and-meet in these COVID-19 times but it's all ful;, this is a solution for you!
- The script keeps looking for a slot at the desired day at the desired IKEA for the desired time.
- [IKEA Germany Link](https://www.ikea.com/de/de/customer-service/services/click-and-meet-pub5c878850) - Here you will get a UI something like this, just click on one of the dates and find the IKEA code

![IKEA Website Image](https://www.ikea.com/images/termin-buchungstool-screenshot-fa03b302a3501e4e271dc12c4adb32f6.png?f=xxxl "ikea booker")

Change the configuration in the following sections:
```python
# Inspect element to get the the store ID after clicking the date (you have to go to the click-and-meet website once to get this)
IKEA_STORE_ID = 324
# Currently works for a single date but could easily be multiple days.
PREFERRED_DATE = '2021-03-30'
# Visiting timeslots are available at every 15 minutes interval.
# Starts at 10:00 and ends at 20:30 in 15 minutes interval.
PREFERRED_SLOT = ['24:30', '24:15']

# Booking information that will be sent to IKEA.
booking_info = {
  'firstname': '...',
  'lastname': '...',
  'street': '...',
  'zip': '...',
  'city': '...',
  'email': '',
  'phone': ''
}
```

### Please ensure your IKEA is open before you run this script!

- Once this is done just run `python main.py` and it will keep polling every few seconds for a slot until it finds one.
- Once it does find a slot that you need, it will send a request to book and exit!
- Check your email and you should have your confirmation! 🎉
