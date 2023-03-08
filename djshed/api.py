# -*- coding: utf-8 -*-

import requests

from djshed.models import Course
from django.conf import settings


def set_course(jason):
    """Construct a course object from API data."""

    '''
        "Academic_Units_group": [{"Department": "Art"}],
        "Year": "2023",
        "Course_Subjects_group": [{"Course_Subject": "ARH"}],
        "Section_Listings_group": [{
            "Meeting_Time": "2:20 PM - 4:00 PM",
            "Credits": "4",
            "Capacity": "18",
            "Course_Subject_Abbreviation___Number": "ARH 3740",
            "Course_Title": "Modern Art (FAR)(CL)(WI)(WC)",
            "Section_Number": "01",
            "Meeting_Day_Patterns": "TR"
        }],
        "Academic_Period": "2023 Fall",
        "Course_Description": "4cr  Modern Art focuses on the arts of the 20th and 21st centuries, allowing students to engage with the artistic experimentation of their own era. This study of the arts, beginning with our Age of Anxiety, traces the competing and often rebellious styles of the Post Impressionists up through the Post Modernists. The course stimulates students to grapple with the question: What is art?  Prerequisite: None",
        "Start_Date": "2023-08-30",
        "End_Date": "2023-12-13",
        "Instructors_group": [{
            "Instructor_Name": "Karl Marx",
            "Instructor_ID": "91025"
        }],
        "Locations_group": [{
            "Building": "JAC",
            "Room_Number": "205"
        }]
    '''

    building = None
    room = None
    location = jason.get('Locations_group')
    if location:
        building = jason['Locations_group'][0].get('Building')
        room = jason['Locations_group'][0].get('Room_Number')

    instructors = None
    instructors_group = jason.get('Instructors_group')
    if instructors_group:
        instructors = []
        for instructor in instructors_group:
            instructors.append(instructor.get('Instructor_Name'))
        if instructors:
            instructors = ', '.join(instructors)

    course, created = Course.objects.update_or_create(
        # Art
        department = jason['Academic_Units_group'][0].get('Department'),
        # ARH
        group = jason['Course_Subjects_group'][0].get('Course_Subject'),
        year = jason.get('Year'),
        credits = jason['Section_Listings_group'][0].get('Credits'),
        capacity = jason['Section_Listings_group'][0].get('Capacity'),
        number = jason['Section_Listings_group'][0].get('Course_Subject_Abbreviation___Number'),
        title = jason['Section_Listings_group'][0].get('Course_Title'),
        section = jason['Section_Listings_group'][0].get('Section_Number'),
        days = jason['Section_Listings_group'][0].get('Meeting_Day_Patterns'),
        time = jason['Section_Listings_group'][0].get('Meeting_Time'),
        term = jason.get('Academic_Period'),
        description = jason.get('Course_Description'),
        start_date = jason.get('Start_Date'),
        end_date = jason.get('End_Date'),
        instructors = instructors,
        building = building,
        room = room,
        status = True,
    )

    return course


def get_courses(test=False):
    """Fetch the workday course data from cache or API."""
    courses = []
    response = requests.get(
        settings.WORKDAY_EARL,
        auth=(settings.WORKDAY_USERNAME, settings.WORKDAY_PASSWORD),
    )
    print(response)
    jason = response.json()
    report = jason['Report_Entry']
    for course in report:
        if test:
            print(course)
        else:
            course = set_course(course)
            courses.append(course)
    return courses
