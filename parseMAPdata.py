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

WEAPON_USED_MAPPING = {
                '11' : 'Firearm, type not stated (not mechanics grease gun or caulking gun)',
                '12' : 'Handgun',
                '13' : 'Rifle',
                '14' : 'Shotgun',
                '15' : 'Other gun',
                '20' : 'Knife or cutting instrument like icepick, screwdriver or (HEAVY GUITAR SOLO) AXE',
                '40' : 'Personal weapons (beating, kicking, biting etc)',
                '50' : 'Poison (not gas, see asphyxiation below)',
                '55' : 'Pushed or thrown out of window',
                '60' : 'Explosives',
                '65' : 'Fire',
                '70' : 'Narcotics/Drugs, including sleeping pills',
                '75' : 'Drowning',
                '80' : 'Strangulation/Hanging',
                '85' : 'Asphyxiation including gas',
                '90' : 'Other - type of weapon not designated or unknown'}
#Victim-to-offender
RELATIONSHIP_MAPPING:{
                'HU' : 'Husband',
                'WI' : 'Wife',
                'CH' : 'Common-law husband',
                'CW' : 'Common-law wife',
                'MO' : 'Mother',
                'FA' : 'Father',
                'SO' : 'Son',
                'DA' : 'Daughter',
                'BR' : 'Brother',
                'SI' : 'Sister',
                'IL' : 'In-law',
                'SF' : 'Stepfather',
                'SM' : 'Stepmother',
                'SS' : 'Stepson',
                'SD' : 'Stepdaughter',
                'OF' : 'Other family',
                'NE' : 'Neighbor',
                'AQ' : 'Aquaintance',
                'BF' : 'Boyfriend',
                'GF' : 'Girlfriend',
                'XH' : 'Ex-husband',
                'XW' : 'Ex-wife',
                'EE' : 'Employee',
                'ER' : 'Employer',
                'FR' : 'Friend',
                'HO' : 'Homosexual relationship',
                'OK' : 'Other - known to victim',
                'ST' : 'Stranger',
                'UN' : 'Relationship cannot be determined'}


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
    YEAR = slice(13,15)
    #Total population for the agency for the year reported
    POPULATION = slice(15,24)
    #County code
    COUNTY = slice(24, 27)
    #Metropolitan statistical area
    MSA = slice(27, 30)
    #Suburban agency is an agency with population less than 50000 (groups 4-7) together
    #with MSA counties (group 9) groups from GROUP ABOVE. 0 = non-SU
    #1 = SU
    MSA_INDICATION = 30
    AGENCY_NAME = slice(31, 55)
    STATE = slice(55,61)
    #01-12
    OFFENSE_MONTH = slice(61, 63)
    #MMDDYY
    LAST_UPDATE = slice(63, 69)
    #0 = normal update, 1 = adjustment
    ACTION_TYPE = 69
    #A = Murder and non-negligent manslaughter
    #B = Negligent manslaughter
    HOMICIDE = 70
    #Unique number distinghuishing incident from other within the ORI
    INCIDENT_NUMBER = slice(71, 74)
    """
    A = Single victim Single offender
    B = Single victim Unknown offender(s)
    C = Single victim Multiple offenders
    D = Multiple victims Single offender
    E = Multiple victims Multiple offenders
    F = Multiple victims Unknown offender(s)
    """
    SITUATION = 74
    """
    01-98 = Age in years
    NB = 0-6 days, including abandoned infant
    BB = 7-364 days
    00 = Unknown
    99 = 99y or older
    """
    AGE_OF_VICTIM = slice(75, 77)
    """
    M = Male
    F = Female
    U = Unknown
    """
    SEX_OF_VICTIM = 77
    """
    W = White (includes mexican-americans)
    B = Black
    I = American indian or Alaskan native
    A = Asian or pacific islander
    U = Unknown
    """
    RACE_OF_VICTIM = 78
    """
    H = Hispanic
    N = Non-hispanic
    U = Unknown
    """
    ETHNIC_ORIGIN_OF_VICTIM = 79
    AGE_OF_OFFENDER = slice(80, 82)
    SEX_OF_OFFENDER = 82
    RACE_OF_OFFENDER = 83
    ETHNIC_ORIGIN_OF_OFFENDER = 84
    """
    There is a dictionary for this called WEAPON_USED_MAPPING above
    11 = Firearm, type not stated (not mechanics grease gun or caulking gun)
    12 = Handgun
    13 = Rifle
    14 = Shotgun
    15 = Other gun
    20 = Knife or cutting instrument like icepick, screwdriver or (HEAVY GUITAR SOLO) AXE
    40 = Personal weapons (beating, kicking, biting etc)
    50 = Poison (not gas, see asphyxiation below)
    55 = Pushed or thrown out of window
    60 = Explosives
    65 = Fire
    70 = Narcotics/Drugs, including sleeping pills
    75 = Drowning
    80 = Strangulation/Hanging
    85 = Asphyxiation including gas
    90 = Other - type of weapon not designated or unknown
    """
    WEAPON_USED = slice(85, 87)
    #For documentation see RELATIONSHIP_MAPPING above
    RELATIONSHIP_OF_VICTIM_TO_OFFENDER = slice(87, 89)
    FELONY_TYPE = slice(89, 91)
    #Blank except when above is 80 or 81
    SUB_CIRCUMSTANCE = 91
    VICTIM_COUNT  = slice(92, 95)
    OFFENDER_COUNT = slice(95,98)
    #each addional victim is 5 characters
    VICTIMS_02_11 = slice(98, 148)
    OFFENDERS_02_11 = slice(148, 268)
    #get rid of the end of line character
    line.rstrip('\n')
    line_of_data_dictionary['Offenders_02_11'] = line[OFFENDERS_02_11]
    line_of_data_dictionary['Victims_02_11'] = line[VICTIMS_02_11]
    line_of_data_dictionary['Offender_count'] = line[OFFENDER_COUNT]
    line_of_data_dictionary['Victim_count'] = line[VICTIM_COUNT]
    line_of_data_dictionary['Subcircumstance'] = line[SUB_CIRCUMSTANCE]
    line_of_data_dictionary['Felony_type'] = line[FELONY_TYPE]
    line_of_data_dictionary['Relationship_of_victim_to_offender'] = line[RELATIONSHIP_OF_VICTIM_TO_OFFENDER]
    line_of_data_dictionary['Weapon_used'] = line[WEAPON_USED]
    line_of_data_dictionary['Ethnic_origin_of_offender'] = line[ETHNIC_ORIGIN_OF_OFFENDER]
    line_of_data_dictionary['Race_of_offender'] = line[RACE_OF_OFFENDER]
    line_of_data_dictionary['Sex_of_offender'] = line[SEX_OF_OFFENDER]
    line_of_data_dictionary['Age_of_offender'] = line[AGE_OF_OFFENDER]
    line_of_data_dictionary['Ethnic_origin_of_victim'] = line[ETHNIC_ORIGIN_OF_VICTIM]
    line_of_data_dictionary['Race_of_victim'] = line[RACE_OF_VICTIM]
    line_of_data_dictionary['Sex_of_victim'] = line[SEX_OF_VICTIM]
    line_of_data_dictionary['Age_of_victim'] = line[AGE_OF_VICTIM]
    line_of_data_dictionary['Situation'] = line[SITUATION]
    line_of_data_dictionary['Incident_number'] = line[INCIDENT_NUMBER]
    line_of_data_dictionary['Homicide'] = line[HOMICIDE]
    line_of_data_dictionary['Action_type'] = line[ACTION_TYPE]
    line_of_data_dictionary['Last_update'] = line[LAST_UPDATE] 
    line_of_data_dictionary['Offense_month'] = line[OFFENSE_MONTH]
    line_of_data_dictionary['State'] = line[STATE]
    line_of_data_dictionary['Agency_name'] = line[AGENCY_NAME]
    line_of_data_dictionary['MSA_indication'] = line[MSA_INDICATION]
    line_of_data_dictionary['MSA'] = line[MSA]
    line_of_data_dictionary['County'] = line[COUNTY]
    line_of_data_dictionary['Population'] = line[POPULATION]
    line_of_data_dictionary['Year'] = line[YEAR]
    line_of_data_dictionary['ID'] = line[ID]
    line_of_data_dictionary['State'] = line[STATE]
    line_of_data_dictionary['ORI'] = line[ORI]
    line_of_data_dictionary['Group'] = line[GROUP]
    line_of_data_dictionary['Division'] = line[DIVISION]
    
    
    
    return line_of_data_dictionary
    
    
    
                            
    