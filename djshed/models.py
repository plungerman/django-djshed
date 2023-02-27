# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models



class Department(models.Model):
    """Supplemental data model for mailman list software."""

    name = models.CharField(max_length=255)
    sup_org = models.CharField(max_length=255)
    orbit = models.CharField(max_length=32)
    status = models.BooleanField(default=True)
    primary = models.BooleanField(default=False)

    def __str__(self):
        """Default display value."""
        return "{0} ({1})".format(self.name, self.orbit)


class Course(models.Model):
    """
    Data class model for course data.

    API JSON structure:
    {
        "Academic_Units_group": [{"Department": "Political Science"}],
        "Year": "2023",
        "Course_Subjects_group": [{"Course_Subject": "POL"}],
        "Section_Listings_group": [{
            "Meeting_Time": "9:15 AM - 10:20 AM",
            "Credits": "4",
            "Capacity": "12",
            "Course_Subject_Abbreviation___Number": "POL 2400",
            "Course_Title": "American Government: National, State, and Local (SOC)(SI)",
            "Section_Number": "01",
            "Meeting_Day_Patterns": "MWF"
        }],
        "Academic_Period": "2023 Fall",
        "Course_Description": "<p>4cr This course involves a study of the institutions of American government at the national, state, and local levels and is designed to serve students seeking teacher certification. It will stress the informal as well as the formal dimensions of government and will, and thereby attempt to broaden and deepen insight into the processes of policy-making and implementation. Fall/Spring<\/p>",
        "Start_Date": "2023-09-06",
        "End_Date": "2023-12-22",
        "Instructors_group": [{
            "Instructor_Name": "Jerald Mast",
            "Instructor_ID": "491193"
        }],
        "Locations_group": [{
            "Building": "LH",
            "Room_Number": "230"
        }]
    },
    {
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
        "Locations_group": [{
            "Building": "JAC",
            "Room_Number": "205"
        }]
    }
    """

    title = models.CharField(max_length=255)
    time = models.CharField(max_length=64, null=True, blank=True)
    credits = models.CharField(max_length=8)
    capacity = models.CharField(max_length=8)
    number = models.CharField(max_length=24)
    section = models.CharField(max_length=8)
    days = models.CharField(max_length=12, null=True, blank=True)
    department = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    group = models.CharField(max_length=8)
    term = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    instructors = models.CharField(max_length=255, null=True, blank=True)
    building = models.CharField(max_length=32, null=True, blank=True)
    room = models.CharField(max_length=8, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        """Default display value."""
        return '{0} [{1}]'.format(self.title, self.number)
