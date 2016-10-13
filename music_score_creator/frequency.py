import math

def getFrequency(numSemitones, baseNote=440):
    """
    numSemitones: Can be positive or negative. It's the number of 
        semitones between baseNote and the note you want.
    
    baseNote: Note take as reference. By default is LA (A4).
    
    return: The interval of the influence of the note
    """
    lowerFreq = baseNote * (1.059463 ** (numSemitones-1))
    centralFreq = baseNote * (1.059463 ** numSemitones)
    upperFreq = baseNote * (1.059463 ** (numSemitones+1))
    
    interLower = round( (lowerFreq + centralFreq) / 2, 1)
    interUpper = round( (centralFreq + upperFreq) / 2, 1)
    
    return [interLower, interUpper]

def getTone(frequency, baseNote=440):
    """
    note: Frequency of a note. Can be anything in the interval.

    baseNote: Note take as reference. By default is LA (A4)

    return: The number of semitones that note is from baseNote.
    """
    result = math.log(float(frequency)/baseNote)/math.log(1.059463)
    return round(result)

def getNoteName(numSemitones):
    """
    numSemitones: The number of semitones that the note is from the base note.
        This base note is LA (A4). So, we need to put it in the base note of the scale,
        that is DO (C4).
    return: A string that is the absolute note. This is, the letter that represents the
        note and the simbol to represents the octave.
    """
    # Define the conversion
    conversionList = { 	0: 'c',
                        1: 'cis',
                        2: 'd',
                        3: 'dis',
                        4: 'e',
                        5: 'f',
                        6: 'fis',
                        7: 'g',
                        8: 'gis',
                        9: 'a',
                        10: 'ais',
                        11: 'b'}
    numSemitones = numSemitones + 9
    octave = abs(math.floor(numSemitones/12))
    note = numSemitones%12
    note = conversionList[note]
    character = ',' if numSemitones < 0 else "'"
    if numSemitones < -9:
        note = 'r'
    else:
        for i in range(0,int(octave+1)):
            note = note + character
    return note