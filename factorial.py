#!/usr/bin/env python

import random
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

LOGIN_URL = "https://api.factorialhr.com/en-US/users/sign_in"
GRAPHQL_URL = "https://api.factorialhr.com/graphql?CreateAttendanceShift"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0"


def login_and_get_session(email, password):
    # Create a session object to persist cookies across requests.
    session = requests.Session()

    # Step 1: Retrieve the login page to extract the authenticity_token.
    get_response = session.get(LOGIN_URL)
    if not get_response.ok:
        print("Failed to retrieve the login page.")
        return None

    # Parse the login page HTML to extract the authenticity_token.
    soup = BeautifulSoup(get_response.text, "html.parser")
    token_input = soup.find("input", {"name": "authenticity_token"})
    if token_input is None:
        print("Could not find the authenticity_token on the login page.")
        return None

    authenticity_token = token_input.get("value")
    print(f"Found authenticity_token: {authenticity_token}")

    # Step 2: Prepare the login payload including the authenticity_token.
    payload = {
        "authenticity_token": authenticity_token,
        "return_host": "factorialhr.com",
        "return_to": "https://app.factorialhr.com/",
        "user[email]": email,
        "user[password]": password,
        "commit": "Sign in",
    }

    # Optionally, add headers if required by the server.
    post_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://api.factorialhr.com",
        "Referer": "https://api.factorialhr.com/en/users/sign_in?&return_to=https%3A%2F%2Fapp.factorialhr.com%2F",
    }

    # Step 3: Perform the POST request to log in.
    post_response = session.post(LOGIN_URL, data=payload, headers=post_headers)
    if post_response.ok:
        print("Login successful!")
    else:
        print(
            f"Login failed with status code: {post_response.status_code}, error {post_response.reason}"
        )
        return None

    return session


def create_attendance_shift(session, date, clock_in, clock_out, employee_id):
    """
    Uses the authenticated session to perform a GraphQL mutation that creates an attendance shift.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Referer": "https://app.factorialhr.com/",
        "content-type": "application/json",
        "Origin": "https://app.factorialhr.com",
    }

    reference_date = date
    location_type = "office"
    source = "desktop"
    time_settings_break_configuration_id = 11959
    workable = True

    payload = {
        "operationName": "CreateAttendanceShift",
        "variables": {
            "date": date,
            "employeeId": employee_id,
            "clockIn": clock_in,
            "clockOut": clock_out,
            "referenceDate": reference_date,
            "locationType": location_type,
            "source": source,
            "timeSettingsBreakConfigurationId": time_settings_break_configuration_id,
            "workable": workable,
            "fetchDependencies": True,
        },
        "query": 
            "mutation CreateAttendanceShift($clockIn: ISO8601DateTime, $clockOut: ISO8601DateTime, $date: ISO8601Date!, $employeeId: Int!, $fetchDependencies: Boolean!, $halfDay: String, $locationType: AttendanceShiftLocationTypeEnum, $observations: String, $referenceDate: ISO8601Date!, $source: AttendanceEnumsShiftSourceEnum, $timeSettingsBreakConfigurationId: Int, $workable: Boolean) {"
              "\n  attendanceMutations {"
              "\n    createAttendanceShift("
              "\n      clockIn: $clockIn"
              "\n      clockOut: $clockOut"
              "\n      date: $date"
              "\n      employeeId: $employeeId"
              "\n      halfDay: $halfDay"
              "\n      locationType: $locationType"
              "\n      observations: $observations"
              "\n      referenceDate: $referenceDate"
              "\n      source: $source"
              "\n      timeSettingsBreakConfigurationId: $timeSettingsBreakConfigurationId"
              "\n      workable: $workable"
              "\n    ) {"
              "\n      errors {"
              "\n        ...ErrorDetails"
              "\n        __typename"
              "\n      }"
              "\n      shift {"
              "\n        employee {"
              "\n          id"
              "\n          attendanceBalancesConnection(endOn: $referenceDate, startOn: $referenceDate) @include(if: $fetchDependencies) {"
              "\n            nodes {"
              "\n              ...TimesheetBalance"
              "\n              __typename"
              "\n            }"
              "\n            __typename"
              "\n          }"
              "\n          attendanceWorkedTimesConnection(endOn: $referenceDate, startOn: $referenceDate) @include(if: $fetchDependencies) {"
              "\n            nodes {"
              "\n              ...TimesheetWorkedTime"
              "\n              __typename"
              "\n            }"
              "\n            __typename"
              "\n          }"
              "\n          __typename"
              "\n        }"
              "\n        ...TimesheetPageShift"
              "\n        __typename"
              "\n      }"
              "\n      __typename"
              "\n    }"
              "\n    __typename"
              "\n  }"
              "\n}"
              "\n"
              "\nfragment TimesheetBalancePoolBlock on AttendanceTimeBlock {"
              "\n  _uniqueKey"
              "\n  equivalentMinutesInCents"
              "\n  minutes"
              "\n  name"
              "\n  rawMinutesInCents"
              "\n  sourcePoolType"
              "\n  timeSettingsCustomTimeRangeCategoryId"
              "\n  __typename"
              "\n}"
              "\n"
              "\nfragment TimesheetWorkedTimeBlock on AttendanceWorkedTimeBlock {"
              "\n  approved"
              "\n  date"
              "\n  extraHour"
              "\n  minutes"
              "\n  poolType"
              "\n  timeRangeCategoryId"
              "\n  timeRangeCategoryName"
              "\n  timeSettingsBreakConfigurationId"
              "\n  timeType"
              "\n  workable"
              "\n  __typename"
              "\n}"
              "\n"
              "\nfragment TimesheetTimeSettingsBreakConfiguration on TimeSettingsBreakConfiguration {"
              "\n  id"
              "\n  paid"
              "\n  __typename"
              "\n}"
              "\n"
              "\nfragment TimesheetPageWorkplace on LocationsLocation {"
              "\n  id"
              "\n  name"
              "\n  __typename"
              "\n}"
              "\n"
              "\nfragment ErrorDetails on MutationError {"
              "\n  ... on SimpleError {"
              "\n    message"
              "\n    type"
              "\n    __typename"
              "\n  }"
              "\n  ... on StructuredError {"
              "\n    field"
              "\n    messages"
              "\n    __typename"
              "\n  }"
              "\n  __typename"
              "\n}"
              "\n"
              "\nfragment TimesheetBalance on AttendanceBalance {"
              "\n  id"
              "\n  accumulationEndOn"
              "\n  accumulationStartOn"
              "\n  balancePools {"
              "\n    transfers {"
              "\n      ...TimesheetBalancePoolBlock"
              "\n      __typename"
              "\n    }"
              "\n    type"
              "\n    usages {"
              "\n      ...TimesheetBalancePoolBlock"
              "\n      __typename"
              "\n    }"
              "\n    __typename"
              "\n  }"
              "\n  dailyBalance"
              "\n  dailyBalanceFromContract"
              "\n  dailyBalanceFromPlanning"
              "\n  date"
              "\n  __typename"
              "\n}"
              "\n"
              "\nfragment TimesheetWorkedTime on AttendanceWorkedTime {"
              "\n  id"
              "\n  breaksMinutesRounded"
              "\n  date"
              "\n  dayType"
              "\n  minutes"
              "\n  multipliedMinutes"
              "\n  pendingMinutes"
              "\n  toleranceMinutesRounded"
              "\n  trackedMinutes"
              "\n  workedTimeBlocks {"
              "\n    ...TimesheetWorkedTimeBlock"
              "\n    __typename"
              "\n  }"
              "\n  __typename"
              "\n}"
              "\n"
              "\nfragment TimesheetPageShift on AttendanceShift {"
              "\n  id"
              "\n  automaticClockIn"
              "\n  automaticClockOut"
              "\n  clockIn"
              "\n  clockInWithSeconds"
              "\n  clockOut"
              "\n  crossesMidnight"
              "\n  date"
              "\n  employeeId"
              "\n  halfDay"
              "\n  isOvernight"
              "\n  locationType"
              "\n  minutes"
              "\n  observations"
              "\n  periodId"
              "\n  referenceDate"
              "\n  showPlusOneDay"
              "\n  timeSettingsBreakConfiguration {"
              "\n    ...TimesheetTimeSettingsBreakConfiguration"
              "\n    __typename"
              "\n  }"
              "\n  workable"
              "\n  workplace {"
              "\n    ...TimesheetPageWorkplace"
              "\n    __typename"
              "\n  }"
              "\n  __typename"
              "\n}",
    }

    print("Submitting GraphQL mutation to create attendance shift...")
    response = session.post(GRAPHQL_URL, json=payload, headers=headers)

    if response.ok:
        print("Attendance shift created successfully!")
    else:
        print("Failed to create attendance shift.")
        print("Status code:", response.status_code)


def get_datetimes(date_str):
    morning_start = datetime.strptime(date_str + " 08:30:00", "%Y-%m-%d %H:%M:%S")
    offset = random.randint(0, 60)  # offset in minutes
    clock_in_morning = morning_start + timedelta(minutes=offset)
    clock_in_morning_str = clock_in_morning.strftime("%Y-%m-%dT%H:%M:%S") + "+01:00"

    # Morning clock-out is fixed at 13:00.
    clock_out_morning = datetime.strptime(date_str + " 13:00:00", "%Y-%m-%d %H:%M:%S")
    clock_out_morning_str = clock_out_morning.strftime("%Y-%m-%dT%H:%M:%S") + "+01:00"

    # Calculate worked minutes in the morning.
    morning_minutes = (clock_out_morning - clock_in_morning).total_seconds() / 60

    # Total working time is 8 hours (480 minutes); compute afternoon duration.
    afternoon_minutes = 480 - morning_minutes

    # Afternoon clock-in is fixed at 14:00.
    clock_in_afternoon = datetime.strptime(date_str + " 14:00:00", "%Y-%m-%d %H:%M:%S")
    clock_in_afternoon_str = clock_in_afternoon.strftime("%Y-%m-%dT%H:%M:%S") + "+01:00"

    # Compute afternoon clock-out.
    clock_out_afternoon = clock_in_afternoon + timedelta(minutes=afternoon_minutes)
    clock_out_afternoon_str = (
        clock_out_afternoon.strftime("%Y-%m-%dT%H:%M:%S") + "+01:00"
    )

    return (
        clock_in_morning_str,
        clock_out_morning_str,
        clock_in_afternoon_str,
        clock_out_afternoon_str,
    )


def validate_args(parser, args):
    # Validate email format.
    if not re.match(r"[^@]+@[^@]+\.[^@]+", args.email):
        parser.error("Invalid email address format.")

    # Validate date format.
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        parser.error("Invalid date format. Expected YYYY-MM-DD.")

    # Validate employee id is positive.
    if args.employee_id <= 0:
        parser.error("Employee ID must be a positive integer.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Create attendance shifts for Factorial."
    )
    parser.add_argument("--email", required=True, help="User email for login")
    parser.add_argument("--password", required=True, help="User password for login")
    parser.add_argument("--date", required=True, help="Date for the shift (YYYY-MM-DD)")
    parser.add_argument("--employee-id", required=True, type=int, help="Employee ID")
    args = parser.parse_args()

    validate_args(parser, args)

    # Log in and retrieve the session.
    session = login_and_get_session(args.email, args.password)
    if not session:
        print("Login failed. Exiting.")
        exit(1)

    # Get clock times for the provided date.
    first_clock_in, first_clock_out, second_clock_in, second_clock_out = get_datetimes(
        args.date
    )

    # Create attendance shifts using the authenticated session.
    create_attendance_shift(
        session, args.date, first_clock_in, first_clock_out, args.employee_id
    )
    create_attendance_shift(
        session, args.date, second_clock_in, second_clock_out, args.employee_id
    )
