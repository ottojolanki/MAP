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
    #get rid of the end of line character
    line.rstrip('\n') 
    
    #position 0 is ID
    line_of_data_dictionary['ID'] = line[0]
    
    #positions 1-2 contain State
    line_of_data_dictionary['State'] = line[1:3]
    
    #Positions 3-9 in the string are the ORI Code, Originating Agency identifier
    #to parse further TODO: https://www.icpsr.umich.edu/NACJD/ORIs/2010%20ORIs/ALoris.html
    #contains descriptions of these
    line_of_data_dictionary['ORI'] = line[3:10]
    
    #Positions 10-11 are a geographical GROUP identifier
    #TODO add mapping constant to identifier to parse further
    
    line_of_data_dictionary['GROUP'] = line[10:12]
    
    #position 12 is geographical DIVISION
    #TODO add mapping constant
    
    line_of_data_dictionary['DIVISION'] = line[12]
    
    #Positions 13-14 are a year "85" = 1985, "90" = 1990 etc.
    
    line_of_data_dictionary['Year'] = line[13:15]
    
    #Positions 15-19 are Sequence number that places all the cities in alphabetical order
    #blank for groups 0,8,9
    
    line_of_data_dictionary['Sequence_number'] = line[15:20]
    
    #Positions 20-21 are juvenile age limit in the state 
    
    line_of_data_dictionary['Juvenile_age'] = line[20:22]
    
    #Position 22 is Core City Indication 'Y' is a MSA (metropolitan statistical area) 'N' is not
    line_of_data_dictionary['Core_city_indication'] = line[22]
    
    return line_of_data_dictionary
    
    
    
                            
    