from flask import Flask, request, jsonify
from datetime import datetime

IGCSE_DATA = {'0452': [{'subj_name': 'Accounting (Multiple Choice)', 'subj_component': '12', 'duration': 75, 'date': '2026-11-06T00:00:00'}, {'subj_name': 'Accounting', 'subj_component': '22', 'duration': 105, 'date': '2026-10-08T00:00:00'}],
 '0606': [{'subj_name': 'Additional Mathematics', 'subj_component': '12', 'duration': 120, 'date': '2026-09-30T00:00:00'}, {'subj_name': 'Additional Mathematics', 'subj_component': '22', 'duration': 120, 'date': '2026-10-06T00:00:00'}],
 '0600': [{'subj_name': 'Agriculture', 'subj_component': '12', 'duration': 105, 'date': '2026-10-12T00:00:00'}],
 '0610': [{'subj_name': 'Biology (Multiple Choice - Core)', 'subj_component': '12', 'duration': 45, 'date': '2026-11-10T00:00:00'}, {'subj_name': 'Biology (Multiple Choice - Extended)', 'subj_component': '22', 'duration': 45, 'date': '2026-11-10T00:00:00'}, {'subj_name': 'Biology (Core)', 'subj_component': '32', 'duration': 75, 'date': '2026-10-16T00:00:00'}, {'subj_name': 'Biology (Extended)', 'subj_component': '42', 'duration': 75, 'date': '2026-10-16T00:00:00'}, {'subj_name': 'Biology (Practical)', 'subj_component': '52', 'duration': 75, 'date': '2026-10-13T00:00:00'}, {'subj_name': 'Biology (Alternative to Practical)', 'subj_component': '62', 'duration': 60, 'date': '2026-10-13T00:00:00'}],
 '0450': [{'subj_name': 'Business Studies', 'subj_component': '12', 'duration': 90, 'date': '2026-10-06T00:00:00'}, {'subj_name': 'Business Studies', 'subj_component': '22', 'duration': 90, 'date': '2026-10-16T00:00:00'}],
 '0607': [{'subj_name': 'Cambridge International Mathematics (Core)', 'subj_component': '12', 'duration': 75, 'date': '2026-09-29T00:00:00'}, {'subj_name': 'Cambridge International Mathematics (Extended)', 'subj_component': '22', 'duration': 90, 'date': '2026-09-29T00:00:00'}, {'subj_name': 'Cambridge International Mathematics (Core)', 'subj_component': '32', 'duration': 75, 'date': '2026-10-08T00:00:00'}, {'subj_name': 'Cambridge International Mathematics (Extended)', 'subj_component': '42', 'duration': 90, 'date': '2026-10-08T00:00:00'}, {'subj_name': 'Cambridge International Mathematics (Core)', 'subj_component': '52', 'duration': 75, 'date': '2026-10-14T00:00:00'}, {'subj_name': 'Cambridge International Mathematics (Extended)', 'subj_component': '62', 'duration': 90, 'date': '2026-10-14T00:00:00'}],
 '0620': [{'subj_name': 'Chemistry (Multiple Choice - Core)', 'subj_component': '12', 'duration': 45, 'date': '2026-11-12T00:00:00'}, {'subj_name': 'Chemistry (Multiple Choice - Extended)', 'subj_component': '22', 'duration': 45, 'date': '2026-11-12T00:00:00'}, {'subj_name': 'Chemistry (Core)', 'subj_component': '32', 'duration': 75, 'date': '2026-10-12T00:00:00'}, {'subj_name': 'Chemistry (Extended)', 'subj_component': '42', 'duration': 75, 'date': '2026-10-12T00:00:00'}, {'subj_name': 'Chemistry (Practical)', 'subj_component': '52', 'duration': 75, 'date': '2026-10-15T00:00:00'}, {'subj_name': 'Chemistry (Alternative to Practical)', 'subj_component': '62', 'duration': 60, 'date': '2026-10-15T00:00:00'}],
 '0653': [{'subj_name': 'Combined Science (Multiple Choice - Core)', 'subj_component': '12', 'duration': 45, 'date': '2026-11-05T00:00:00'}, {'subj_name': 'Combined Science (Multiple Choice - Extended)', 'subj_component': '22', 'duration': 45, 'date': '2026-11-05T00:00:00'}, {'subj_name': 'Combined Science (Core)', 'subj_component': '32', 'duration': 75, 'date': '2026-10-15T00:00:00'}, {'subj_name': 'Combined Science (Extended)', 'subj_component': '42', 'duration': 75, 'date': '2026-10-15T00:00:00'}, {'subj_name': 'Combined Science (Practical)', 'subj_component': '52', 'duration': 75, 'date': '2026-10-20T00:00:00'}, {'subj_name': 'Combined Science (Alternative to Practical)', 'subj_component': '62', 'duration': 60, 'date': '2026-10-20T00:00:00'}],
 '0478': [{'subj_name': 'Computer Science', 'subj_component': '12', 'duration': 105, 'date': '2026-10-09T00:00:00'}, {'subj_name': 'Computer Science', 'subj_component': '22', 'duration': 105, 'date': '2026-10-19T00:00:00'}],
 '0654': [{'subj_name': 'Co-ordinated Sciences (Double Award) (Multiple Choice - Core)', 'subj_component': '12', 'duration': 45, 'date': '2026-11-05T00:00:00'}, {'subj_name': 'Co-ordinated Sciences (Double Award) (Multiple Choice - Extended)', 'subj_component': '22', 'duration': 45, 'date': '2026-11-05T00:00:00'}, {'subj_name': 'Co-ordinated Sciences (Double Award) (Core)', 'subj_component': '32', 'duration': 120, 'date': '2026-10-15T00:00:00'}, {'subj_name': 'Co-ordinated Sciences (Double Award) (Extended)', 'subj_component': '42', 'duration': 120, 'date': '2026-10-15T00:00:00'}, {'subj_name': 'Co-ordinated Sciences (Double Award) (Practical)', 'subj_component': '52', 'duration': 120, 'date': '2026-10-20T00:00:00'}, {'subj_name': 'Co-ordinated Sciences (Double Award) (Alternative to Practical)', 'subj_component': '62', 'duration': 90, 'date': '2026-10-20T00:00:00'}],
 '0445': [{'subj_name': 'Design & Technology', 'subj_component': '12', 'duration': 75, 'date': '2026-10-23T00:00:00'}, {'subj_name': 'Design & Technology', 'subj_component': '32', 'duration': 60, 'date': '2026-10-30T00:00:00'}, {'subj_name': 'Design & Technology', 'subj_component': '42', 'duration': 60, 'date': '2026-10-30T00:00:00'}, {'subj_name': 'Design & Technology', 'subj_component': '52', 'duration': 60, 'date': '2026-10-30T00:00:00'}],
 '0411': [{'subj_name': 'Drama', 'subj_component': '12', 'duration': 150, 'date': '2026-10-26T00:00:00'}],
 '0455': [{'subj_name': 'Economics (Multiple Choice)', 'subj_component': '12', 'duration': 45, 'date': '2026-11-04T00:00:00'}, {'subj_name': 'Economics', 'subj_component': '22', 'duration': 135, 'date': '2026-10-20T00:00:00'}],
 '0510': [{'subj_name': 'English as a Second Language (Speaking Endorsement)', 'subj_component': '12', 'duration': 120, 'date': '2026-09-29T00:00:00'}, {'subj_name': 'English as a Second Language (Speaking Endorsement) (Listening)', 'subj_component': '22', 'duration': 50, 'date': '2026-10-21T00:00:00'}],
 '0511': [{'subj_name': 'English as a Second Language (Count-in Speaking)', 'subj_component': '12', 'duration': 120, 'date': '2026-09-29T00:00:00'}, {'subj_name': 'English as a Second Language (Count-in Speaking) (Listening)', 'subj_component': '22', 'duration': 50, 'date': '2026-10-21T00:00:00'}],
 '0454': [{'subj_name': 'Enterprise', 'subj_component': '12', 'duration': 90, 'date': '2026-10-05T00:00:00'}],
 '0680': [{'subj_name': 'Environmental Management', 'subj_component': '12', 'duration': 105, 'date': '2026-09-28T00:00:00'}, {'subj_name': 'Environmental Management', 'subj_component': '22', 'duration': 105, 'date': '2026-09-30T00:00:00'}],
 '0508': [{'subj_name': 'First Language Arabic', 'subj_component': '01', 'duration': 120, 'date': '2026-09-30T00:00:00'}, {'subj_name': 'First Language Arabic', 'subj_component': '02', 'duration': 120, 'date': '2026-10-05T00:00:00'}],
 '0500': [{'subj_name': 'First Language English (Oral Endorsement)', 'subj_component': '12', 'duration': 120, 'date': '2026-10-05T00:00:00'}, {'subj_name': 'First Language English (Oral Endorsement)', 'subj_component': '22', 'duration': 120, 'date': '2026-10-07T00:00:00'}],
 '0698': [{'subj_name': 'First Language Setswana', 'subj_component': '01', 'duration': 120, 'date': '2026-09-28T00:00:00'}, {'subj_name': 'First Language Setswana', 'subj_component': '02', 'duration': 120, 'date': '2026-10-13T00:00:00'}],
 '0502': [{'subj_name': 'First Language Spanish', 'subj_component': '12', 'duration': 120, 'date': '2026-09-28T00:00:00'}, {'subj_name': 'First Language Spanish', 'subj_component': '22', 'duration': 120, 'date': '2026-10-08T00:00:00'}],
 '0648': [{'subj_name': 'Food & Nutrition', 'subj_component': '12', 'duration': 120, 'date': '2026-10-26T00:00:00'}],
 '0520': [{'subj_name': 'French (Listening - Multiple Choice)', 'subj_component': '12', 'duration': 50, 'date': '2026-11-03T00:00:00'}, {'subj_name': 'French', 'subj_component': '22', 'duration': 60, 'date': '2026-10-23T00:00:00'}, {'subj_name': 'French', 'subj_component': '42', 'duration': 60, 'date': '2026-10-26T00:00:00'}],
 '0460': [{'subj_name': 'Geography', 'subj_component': '12', 'duration': 105, 'date': '2026-10-21T00:00:00'}, {'subj_name': 'Geography', 'subj_component': '22', 'duration': 90, 'date': '2026-10-14T00:00:00'}, {'subj_name': 'Geography', 'subj_component': '42', 'duration': 90, 'date': '2026-10-27T00:00:00'}],
 '0525': [{'subj_name': 'German (Listening - Multiple Choice)', 'subj_component': '12', 'duration': 50, 'date': '2026-11-11T00:00:00'}, {'subj_name': 'German', 'subj_component': '22', 'duration': 60, 'date': '2026-10-22T00:00:00'}, {'subj_name': 'German', 'subj_component': '42', 'duration': 60, 'date': '2026-10-19T00:00:00'}],
 '0457': [{'subj_name': 'Global Perspectives', 'subj_component': '12', 'duration': 85, 'date': '2026-10-27T00:00:00'}],
 '0549': [{'subj_name': 'Hindi as a Second Language', 'subj_component': '01', 'duration': 120, 'date': '2026-10-27T00:00:00'}, {'subj_name': 'Hindi as a Second Language', 'subj_component': '02', 'duration': 45, 'date': '2026-10-21T00:00:00'}],
 '0470': [{'subj_name': 'History', 'subj_component': '12', 'duration': 120, 'date': '2026-10-09T00:00:00'}, {'subj_name': 'History', 'subj_component': '22', 'duration': 105, 'date': '2026-10-23T00:00:00'}, {'subj_name': 'History', 'subj_component': '42', 'duration': 60, 'date': '2026-10-19T00:00:00'}],
 '0417': [{'subj_name': 'Information & Communication Technology', 'subj_component': '12', 'duration': 90, 'date': '2026-10-13T00:00:00'}],
 '0493': [{'subj_name': 'Islamiyat', 'subj_component': '12', 'duration': 90, 'date': '2026-09-28T00:00:00'}, {'subj_name': 'Islamiyat', 'subj_component': '22', 'duration': 90, 'date': '2026-09-30T00:00:00'}],
 '0475': [{'subj_name': 'Literature in English', 'subj_component': '12', 'duration': 90, 'date': '2026-10-22T00:00:00'}, {'subj_name': 'Literature in English', 'subj_component': '22', 'duration': 90, 'date': '2026-10-28T00:00:00'}, {'subj_name': 'Literature in English', 'subj_component': '32', 'duration': 45, 'date': '2026-10-28T00:00:00'}, {'subj_name': 'Literature in English', 'subj_component': '42', 'duration': 75, 'date': '2026-10-28T00:00:00'}],
 '0474': [{'subj_name': 'Literature in Spanish', 'subj_component': '01', 'duration': 90, 'date': '2026-09-30T00:00:00'}, {'subj_name': 'Literature in Spanish', 'subj_component': '02', 'duration': 120, 'date': '2026-10-16T00:00:00'}],
 '0697': [{'subj_name': 'Marine Science', 'subj_component': '12', 'duration': 105, 'date': '2026-10-26T00:00:00'}, {'subj_name': 'Marine Science', 'subj_component': '22', 'duration': 105, 'date': '2026-10-28T00:00:00'}],
 '0580': [{'subj_name': 'Mathematics (Without Coursework) (Core)', 'subj_component': '12', 'duration': 90, 'date': '2026-10-08T00:00:00'}, {'subj_name': 'Mathematics (Without Coursework) (Extended)', 'subj_component': '22', 'duration': 120, 'date': '2026-10-08T00:00:00'}, {'subj_name': 'Mathematics (Without Coursework) (Core)', 'subj_component': '32', 'duration': 90, 'date': '2026-10-14T00:00:00'}, {'subj_name': 'Mathematics (Without Coursework) (Extended)', 'subj_component': '42', 'duration': 120, 'date': '2026-10-14T00:00:00'}],
 '0410': [{'subj_name': 'Music (Listening)', 'subj_component': '12', 'duration': 75, 'date': '2026-10-29T00:00:00'}],
 '0413': [{'subj_name': 'Physical Education', 'subj_component': '12', 'duration': 105, 'date': '2026-10-13T00:00:00'}],
 '0625': [{'subj_name': 'Physics (Multiple Choice - Core)', 'subj_component': '12', 'duration': 45, 'date': '2026-11-05T00:00:00'}, {'subj_name': 'Physics (Multiple Choice - Extended)', 'subj_component': '22', 'duration': 45, 'date': '2026-11-05T00:00:00'}, {'subj_name': 'Physics (Core)', 'subj_component': '32', 'duration': 75, 'date': '2026-10-07T00:00:00'}, {'subj_name': 'Physics (Extended)', 'subj_component': '42', 'duration': 75, 'date': '2026-10-07T00:00:00'}, {'subj_name': 'Physics (Practical)', 'subj_component': '52', 'duration': 75, 'date': '2026-10-20T00:00:00'}, {'subj_name': 'Physics (Alternative to Practical)', 'subj_component': '62', 'duration': 60, 'date': '2026-10-20T00:00:00'}],
 '0490': [{'subj_name': 'Religious Studies', 'subj_component': '12', 'duration': 105, 'date': '2026-10-27T00:00:00'}, {'subj_name': 'Religious Studies', 'subj_component': '22', 'duration': 105, 'date': '2026-11-02T00:00:00'}],
 '0495': [{'subj_name': 'Sociology', 'subj_component': '12', 'duration': 120, 'date': '2026-10-16T00:00:00'}, {'subj_name': 'Sociology', 'subj_component': '22', 'duration': 105, 'date': '2026-10-21T00:00:00'}],
 '0530': [{'subj_name': 'Spanish (Listening - Multiple Choice)', 'subj_component': '12', 'duration': 50, 'date': '2026-11-06T00:00:00'}, {'subj_name': 'Spanish', 'subj_component': '22', 'duration': 60, 'date': '2026-10-28T00:00:00'}, {'subj_name': 'Spanish', 'subj_component': '42', 'duration': 60, 'date': '2026-10-30T00:00:00'}],
 '0471': [{'subj_name': 'Travel & Tourism', 'subj_component': '12', 'duration': 90, 'date': '2026-09-30T00:00:00'}, {'subj_name': 'Travel & Tourism', 'subj_component': '22', 'duration': 120, 'date': '2026-10-06T00:00:00'}],
 '0408': [{'subj_name': 'World Literature', 'subj_component': '22', 'duration': 75, 'date': '2026-10-28T00:00:00'}, {'subj_name': 'World Literature', 'subj_component': '32', 'duration': 90, 'date': '2026-11-05T00:00:00'}],
 '7180': [{'subj_name': 'Arabic', 'subj_component': '01', 'duration': 90, 'date': '2026-09-29T00:00:00'}, {'subj_name': 'Arabic', 'subj_component': '02', 'duration': 90, 'date': '2026-10-05T00:00:00'}],
 '7707': [{'subj_name': 'Accounting (Multiple Choice)', 'subj_component': '12', 'duration': 75, 'date': '2026-11-06T00:00:00'}, {'subj_name': 'Accounting', 'subj_component': '22', 'duration': 105, 'date': '2026-10-08T00:00:00'}],
 '4037': [{'subj_name': 'Additional Mathematics', 'subj_component': '12', 'duration': 120, 'date': '2026-09-30T00:00:00'}, {'subj_name': 'Additional Mathematics', 'subj_component': '22', 'duration': 120, 'date': '2026-10-06T00:00:00'}],
 '5038': [{'subj_name': 'Agriculture', 'subj_component': '12', 'duration': 105, 'date': '2026-10-12T00:00:00'}],
 '3180': [{'subj_name': 'Arabic', 'subj_component': '01', 'duration': 90, 'date': '2026-09-29T00:00:00'}, {'subj_name': 'Arabic', 'subj_component': '02', 'duration': 90, 'date': '2026-10-05T00:00:00'}],
 '2035': [{'subj_name': 'Biblical Studies', 'subj_component': '12', 'duration': 90, 'date': '2026-09-28T00:00:00'}, {'subj_name': 'Biblical Studies', 'subj_component': '22', 'duration': 90, 'date': '2026-10-01T00:00:00'}],
 '5090': [{'subj_name': 'Biology (Multiple Choice)', 'subj_component': '12', 'duration': 60, 'date': '2026-11-10T00:00:00'}, {'subj_name': 'Biology', 'subj_component': '22', 'duration': 105, 'date': '2026-10-01T00:00:00'}, {'subj_name': 'Biology (Practical)', 'subj_component': '32', 'duration': 90, 'date': '2026-10-13T00:00:00'}, {'subj_name': 'Biology (Alternative to Practical)', 'subj_component': '42', 'duration': 60, 'date': '2026-10-13T00:00:00'}],
 '7115': [{'subj_name': 'Business Studies', 'subj_component': '12', 'duration': 90, 'date': '2026-10-06T00:00:00'}, {'subj_name': 'Business Studies', 'subj_component': '22', 'duration': 90, 'date': '2026-10-16T00:00:00'}],
 '5070': [{'subj_name': 'Chemistry (Multiple Choice)', 'subj_component': '12', 'duration': 60, 'date': '2026-11-12T00:00:00'}, {'subj_name': 'Chemistry', 'subj_component': '22', 'duration': 105, 'date': '2026-09-28T00:00:00'}, {'subj_name': 'Chemistry (Practical)', 'subj_component': '32', 'duration': 90, 'date': '2026-10-15T00:00:00'}, {'subj_name': 'Chemistry (Alternative to Practical)', 'subj_component': '42', 'duration': 60, 'date': '2026-10-15T00:00:00'}],
 '5129': [{'subj_name': 'Combined Science (Multiple Choice)', 'subj_component': '12', 'duration': 60, 'date': '2026-11-05T00:00:00'}, {'subj_name': 'Combined Science', 'subj_component': '22', 'duration': 105, 'date': '2026-10-07T00:00:00'}, {'subj_name': 'Combined Science', 'subj_component': '32', 'duration': 60, 'date': '2026-10-20T00:00:00'}],
 '7100': [{'subj_name': 'Commerce (Multiple Choice)', 'subj_component': '12', 'duration': 60, 'date': '2026-11-11T00:00:00'}, {'subj_name': 'Commerce', 'subj_component': '22', 'duration': 120, 'date': '2026-10-22T00:00:00'}],
 '2210': [{'subj_name': 'Computer Science', 'subj_component': '12', 'duration': 105, 'date': '2026-10-09T00:00:00'}, {'subj_name': 'Computer Science', 'subj_component': '22', 'duration': 105, 'date': '2026-10-19T00:00:00'}],
 '2281': [{'subj_name': 'Economics (Multiple Choice)', 'subj_component': '12', 'duration': 45, 'date': '2026-11-04T00:00:00'}, {'subj_name': 'Economics', 'subj_component': '22', 'duration': 135, 'date': '2026-10-20T00:00:00'}],
 '1123': [{'subj_name': 'English Language', 'subj_component': '12', 'duration': 120, 'date': '2026-09-29T00:00:00'}, {'subj_name': 'English Language', 'subj_component': '22', 'duration': 120, 'date': '2026-10-05T00:00:00'}],
 '6130': [{'subj_name': 'Fashion & Textiles', 'subj_component': '01', 'duration': 120, 'date': '2026-10-02T00:00:00'}],
 '6065': [{'subj_name': 'Food & Nutrition', 'subj_component': '12', 'duration': 120, 'date': '2026-10-26T00:00:00'}],
 '2217': [{'subj_name': 'Geography', 'subj_component': '12', 'duration': 105, 'date': '2026-10-21T00:00:00'}, {'subj_name': 'Geography', 'subj_component': '22', 'duration': 90, 'date': '2026-10-14T00:00:00'}, {'subj_name': 'Geography', 'subj_component': '32', 'duration': 90, 'date': '2026-10-27T00:00:00'}],
 '2147': [{'subj_name': 'History', 'subj_component': '12', 'duration': 120, 'date': '2026-10-09T00:00:00'}, {'subj_name': 'History', 'subj_component': '22', 'duration': 105, 'date': '2026-10-23T00:00:00'}],
 '2068': [{'subj_name': 'Islamic Studies', 'subj_component': '12', 'duration': 90, 'date': '2026-10-26T00:00:00'}, {'subj_name': 'Islamic Studies', 'subj_component': '22', 'duration': 90, 'date': '2026-10-30T00:00:00'}],
 '2058': [{'subj_name': 'Islamiyat', 'subj_component': '12', 'duration': 90, 'date': '2026-09-28T00:00:00'}, {'subj_name': 'Islamiyat', 'subj_component': '22', 'duration': 90, 'date': '2026-09-30T00:00:00'}],
 '2010': [{'subj_name': 'Literature in English', 'subj_component': '12', 'duration': 90, 'date': '2026-10-22T00:00:00'}, {'subj_name': 'Literature in English', 'subj_component': '22', 'duration': 90, 'date': '2026-10-28T00:00:00'}],
 '4024': [{'subj_name': 'Mathematics Syllabus D', 'subj_component': '12', 'duration': 120, 'date': '2026-10-08T00:00:00'}, {'subj_name': 'Mathematics Syllabus D', 'subj_component': '22', 'duration': 120, 'date': '2026-10-14T00:00:00'}],
 '2059': [{'subj_name': 'Pakistan Studies', 'subj_component': '01', 'duration': 90, 'date': '2026-09-29T00:00:00'}, {'subj_name': 'Pakistan Studies', 'subj_component': '02', 'duration': 90, 'date': '2026-10-01T00:00:00'}],
 '5054': [{'subj_name': 'Physics (Multiple Choice)', 'subj_component': '12', 'duration': 60, 'date': '2026-11-05T00:00:00'}, {'subj_name': 'Physics', 'subj_component': '22', 'duration': 105, 'date': '2026-10-07T00:00:00'}, {'subj_name': 'Physics (Practical)', 'subj_component': '32', 'duration': 90, 'date': '2026-10-20T00:00:00'}, {'subj_name': 'Physics (Alternative to Practical)', 'subj_component': '42', 'duration': 60, 'date': '2026-10-20T00:00:00'}],
 '3248': [{'subj_name': 'Second Language Urdu', 'subj_component': '01', 'duration': 105, 'date': '2026-09-28T00:00:00'}, {'subj_name': 'Second Language Urdu', 'subj_component': '02', 'duration': 90, 'date': '2026-09-30T00:00:00'}],
 '2251': [{'subj_name': 'Sociology', 'subj_component': '12', 'duration': 120, 'date': '2026-10-16T00:00:00'}, {'subj_name': 'Sociology', 'subj_component': '22', 'duration': 105, 'date': '2026-10-21T00:00:00'}],
 '4040': [{'subj_name': 'Statistics', 'subj_component': '12', 'duration': 135, 'date': '2026-10-07T00:00:00'}, {'subj_name': 'Statistics', 'subj_component': '22', 'duration': 135, 'date': '2026-10-12T00:00:00'}]}

AS_DATA = ...

AL_DATA = ...

app = Flask(__name__)

BASE = "http://127.0.0.1:5000"

@app.route("/igcse/")
def igcse_route():
    subj = request.args.getlist("subjs")

    return_val = {key: value for key, value in IGCSE_DATA.items() if key in subj}

    if len(return_val) == 0 or return_val is None:
        return jsonify({
            "error": {
                "code": "USER_NOT_FOUND",
                "message": "The requested user does not exist."
            }
        }), 404

    return jsonify(return_val), 200
    

@app.route("/as_lvl")
def as_lvl():
    return "work in progress"

@app.route("/a_lvl")
def a_lvl():
    return "work in progress"

if __name__ == "__main__":
    app.run(debug=True)