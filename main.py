from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import time
import itertools

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

# A user-agent to make it look legit in case some starts inspecting.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
}


def search_for_appointments(preferred_store_id=IKEA_STORE_ID, preferred_date=PREFERRED_DATE, preferred_slots=PREFERRED_SLOT):
    """Search the IKEA website for slots in the preferred store for preferred date and slots."""

    print("🔎  Looking For Appointments @ {} on {} at {}".format(preferred_store_id, preferred_date, preferred_slots))

    response = requests.get('https://cms.ikea-lsp.de/lsp/entryticket/getslotdata/{}/{}'.format(preferred_store_id, preferred_date) , headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    slots = soup.find_all(class_='pill')
    preferred_slot_found = False
    for index, slot in enumerate(slots):
        # Each date is a pill marked with full and high, available ones have no color.
        full_label = slot.find_all('label', class_='full')
        high_label = slot.find_all('label', class_='high')
        # All labels regardless of their availability (since available ones have no class)
        all_label = slot.find_all('label', class_='pill--singleselect')
        # If it's not full then it's either high or available.
        if not full_label:
          slot_timing = all_label[0].find_all('span', class_='pill__label')[0].string

          # If it's not high then only state possible is available.
          status = '🟡'
          if not high_label:
            status = '🟢'

          print(" ... 🗓️  Available {} @ {} {}".format(preferred_date, slot_timing, status))

          if slot_timing in preferred_slots:
            preferred_slot_found = True
            print("... ✨ Bingo! {} @ {}".format(preferred_date, slot_timing))
            try_booking_slot(preferred_store_id, preferred_date, slot_timing)

    if preferred_slot_found is False:
      print("\n ❌  No Slot Found.")
    print("....\n")
    return preferred_slot_found

def try_booking_slot(preferred_store_id, preferred_date, slot_timing):
  """Send an appointment booking request and pray that it works well."""
  appointment_data = {
    'store_id': '{}'.format(preferred_store_id),
    'override': '0',
    'slot': '{} {}:00'.format(preferred_date, slot_timing),
  }
  final_payload = booking_info | appointment_data
  print("🚧 Trying To Book Appointment ...")
  response = requests.post('https://cms.ikea-lsp.de/lsp/entryticket/submit', headers=headers, data=data)
  # The Request fails often since a lot of people are trying to book appontment.
  # And status code is always 200 so we have to check the JSON response to validate
  if response.json().get('status') == True:
    print('🎆 Appointment Booked! - Check your Email for Confirmation')
    exit(1)
  else:
    print('❌ Failed Booking Appointment.')

def poll_for_appointments(limit, polling_delay):
    """
    Polls for available appointments every [polling_delay] seconds for [limit] minutes/hours/days (or until one is booked).
    :param limit: A timedelta. The observer will stop after this amount of time is elapsed
    :param polling_delay: The polling delay, in seconds.
    """
    start = datetime.now()
    duration = timedelta()
    while duration < limit:
        duration = datetime.now() - start
        search_for_appointments()
        time.sleep(polling_delay)


if __name__ == "__main__":
    poll_for_appointments(timedelta(days=90), polling_delay=10)
