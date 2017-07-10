# -*- coding: utf-8 -*-
"""
parseMAPdata.py
A script to parse the Murder Accountability Project Data using the data description
in Ret A Rec Description.pdf from now referred to as The Codebook.
The data is in fixed-length unpacked data format, where each line in the data is of length 7385.
Each row in data describes one case. In each row the positions, or slices, of the string describe different 
facets of the data point as described in the Codebook. 
Author: Otto Jolanki
"""

#A dictionary containing the state codes from the Codebook. 
#Positions 1-2 in the row contain a state code
STATEMAPPING = {'01' : 'AL - Alabama',
                '02' : 'AZ - Arizona',
                '03' : 'AR - Arkansas',
                '04' : 'CA - California',
                '05' : 'CO - Colorado',
                '06' : 'CT - Conneticut',
                '07' : 'DE - Delaware',
                '08' : 'DC - District of Columbia',
                '09' : 'FL - Florida',
                '10' : 'GA - Georgia',
                '11' : 'ID - Idaho',
                '12' : 'IL - Illinois',
                '13' : 'IN - Indiana',
                '14' : 'IA - Iowa',
                '15' : 'KS - Kansas',
                '16' : 'KY - Kentucky',
                '17' : 'LA - Louisiana',
                '18' : 'ME - Maine',
                '19' : 'MD - Maryland',
                '20' : 'MA - Massachusetts',
                '21' : 'MI - Michigan',
                '22' : 'MN - Minnesota',
                '23' : 'MS - Mississippi',
                '24' : 'MO - Missouri',
                '25' : 'MT - Montana',
                '26' : 'NB - Nebraska',
                '27' : 'NV - Nevada',
                '28' : 'NH - New Hampshire',
                '29' : 'NJ - New Jersey',
                '30' : 'NM - New Mexico',
                '31' : 'NY - New York',
                '32' : 'NC - North Carolina',
                '33' : 'ND - North Dakota',
                '34' : 'OH - Ohio',
                '35' : 'OK - Oklahoma',
                '36' : 'OR - Oregon',
                '37' : 'PA - Pennsylvania',
                '38' : 'RI - Rhode Island',
                '39' : 'SC - South Carolina',
                '40' : 'SD - South Dakota',
                '41' : 'TN - Tennessee',
                '42' : 'TX - Texas',
                '43' : 'UT - Utah',
                '44' : 'VT - Vermont',
                '45' : 'VA - Virginia',
                '46' : 'WA - Washington',
                '47' : 'WV - West Virginia',
                '48' : 'WI - Wisconsin',
                '49' : 'WY - Wyoming',
                '50' : 'AK - Alaska',
                '51' : 'HI - Hawaii',
                '52' : 'CZ - Canal Zone',
                '53' : 'PR - Puerto Rico',
                '54' : 'AS - American Samoa',
                '55' : 'GM - Guam',
                '62' : 'VI - Virgin Islands'}

def parseline(line):
    '''
    function for parsing MAP data into a python dictionary
    '''
    line_of_data_dictionary = {}
    #to be clearer i'll take the extra effort to code slices as constants
    ID = 0
    STATE = slice(1, 3)
    ORI = slice(3, 10)
    GROUP = slice(10, 12)
    DIVISION = 12
    YEAR = slice(13, 15)
    SEQUENCE_NUMBER = slice(15, 20)
    JUVENILE_AGE = slice(20, 22)
    CORE_CITY_INDICATION = 22
    COVERED_BY = slice(23, 30)
    COVERED_BY_GRP = 30
    LAST_UPDATE = slice(31, 37)
    #Field office whose territory covers the agency
    FIELD_OFFICE = slice(37, 41)
    #Number of the month that was the last month reported that year by the submitting agency
    MONTHS_REPORTED = slice(41, 43)
    #dummy variable for internal use
    AGENCY_COUNT = 43
    #NOTE: population 
    #Population of the city
    POPULATION = slice(44, 53)
    #County the city is in 
    COUNTY = slice(53, 56)
    #If present, the code of the MSA the city is located in
    MSA = slice(56, 59)
    #If city resides in two counties, this is the second largest county population
    GROUP_1 = slice(59, 74)
    #If city resides in two counties, this is the population of the third largest county
    GROUP_2 = slice(74, 89)
    #NOTE:to get the total population of the city add the three above to get the total population of the city
    
    
    
    #get rid of the end of line character
    line.rstrip('\n') 
    line_of_data_dictionary['County'] = line[COUNTY]
    line_of_data_dictionary['Group_2'] = line[GROUP_2]
    line_of_data_dictionary['Group_1'] = line[GROUP_1]
    line_of_data_dictionary['MSA'] = line[MSA]
    line_of_data_dictionary['Population'] = line[POPULATION]
    line_of_data_dictionary['Agency_count'] = line[AGENCY_COUNT]
    line_of_data_dictionary['Months_reported'] = line[MONTHS_REPORTED]
    line_of_data_dictionary['Field_office'] = line[FIELD_OFFICE]
    #position 0 is ID
    line_of_data_dictionary['ID'] = line[ID]
    
    #positions 1-2 contain State
    line_of_data_dictionary['State'] = line[STATE]
    
    #Positions 3-9 in the string are the ORI Code, Originating Agency identifier
    #to parse further TODO: https://www.icpsr.umich.edu/NACJD/ORIs/2010%20ORIs/ALoris.html
    #contains descriptions of these
    line_of_data_dictionary['ORI'] = line[ORI]
    
    #Positions 10-11 are a geographical GROUP identifier
    #TODO add mapping constant to identifier to parse further
    
    line_of_data_dictionary['GROUP'] = line[GROUP]
    
    #position 12 is geographical DIVISION
    #TODO add mapping constant
    
    line_of_data_dictionary['DIVISION'] = line[DIVISION]
    
    #Positions 13-14 are a year "85" = 1985, "90" = 1990 etc.
    
    line_of_data_dictionary['Year'] = line[YEAR]
    
    #Positions 15-19 are Sequence number that places all the cities in alphabetical order
    #blank for groups 0,8,9
    
    line_of_data_dictionary['Sequence_number'] = line[SEQUENCE_NUMBER]
    
    #Positions 20-21 are juvenile age limit in the state 
    
    line_of_data_dictionary['Juvenile_age'] = line[JUVENILE_AGE]
    
    #Position 22 is Core City Indication 'Y' is a MSA (metropolitan statistical area) 'N' is not
    line_of_data_dictionary['Core_city_indication'] = line[CORE_CITY_INDICATION]
    
    #Positions 23-29 'covered by' ORI of the agency submitting the data.
    #blank if not covered by
    line_of_data_dictionary['Covered_by'] = line[COVERED_BY]
    
    #Position 30 is the group of covered by ORI
    line_of_data_dictionary['Covered_by_grp'] = line[COVERED_BY_GRP]
    
    #Positions 31-36 The date the heading or mailing list information
    #was updated (MMDDYY)
    line_of_data_dictionary['Last_update'] = line[LAST_UPDATE]
    
    
    
    return line_of_data_dictionary
    
    
    
                            
    