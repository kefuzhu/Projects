# Import library
import pandas as pd
import numpy as np
import string
import re

def main():
    '''
    The main function to perform the title unification including:
    1. Load the data from 'raw_titles.xlsx' in current directory
    2. Perform unifications for titles with the same starting word after cleaning
    3. Write the original raw titles and unified titles together to an excel
    '''
    
    # Load the data
    data = pd.read_excel('raw_titles.xlsx')
    
    # Sort the dataframe by raw titles alphabetically
    # Titles with same root word are put next to each other
    data.sort_values('raw_title', inplace=True)
    # Reset the index for dataframe and keep the original index
    data.reset_index(inplace = True)
    
    # Unify raw titles that start with the same word
    unified_data = unify_title(dataframe = data, 
                               raw_column = 'raw_title', 
                               unified_column = 'unified_title',
                               ignore = ['THE'],
                               remove = ['INC','PC','SC','GP','LP','LLP','CORP'
                                         'LLLP','LLC','LC','LTD','PLLC'])
    
    # Recover the original index
    unified_data.set_index('index', inplace=True)
    # Sort the dataframe by original index, so it looks the same
    unified_data.sort_index(inplace = True)
    
    # Write the dataframe to excel
    dataframe_to_excel(dataframe = unified_data, 
                       filename = 'unified_titles.xlsx',
                       sheetname = 'unified', 
                       with_index = False)

def dataframe_to_excel(dataframe, filename, sheetname, with_index = False):
    '''
    Write a pandas dataframe to excel
    
    Parameters
    ----------
    dataframe: pandas.core.frame.DataFrame
        Dataframe object that need to be written to excel
    filename: str
        Name of output excel file
    sheetname:
        Name of output sheet in excel
    with_index: bool
        Whether to include dataframe index as a column in excel or not
    
    Raises
    ------
    TypeError
        If input variables are not in correct data type
    '''
    
    # Validate the input variable type
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Input table must be pandas DataFrame")
    if not isinstance(filename, str):
        raise TypeError("Name of output excel file must be a string")
    if not isinstance(sheetname, str):
        raise TypeError("Name of output sheet in excel must be a string")
    if not isinstance(with_index, bool):
        raise TypeError("with_index can only take boolean value")
    
    # Initialize an Excel writier
    writer = pd.ExcelWriter(filename)
    # Write out the unified result
    dataframe.to_excel(writer, sheet_name = sheetname, index = with_index)
    writer.save()

def replace_punctuations(s, delimiter = ' '):
    '''
    Replace every punctuation character in the input string with delimiter
    
    Parameters
    ----------
    s: str
        Input string
    delimiter: str
        Delimiter used to replace punctuation character (the default is ' ')
        
    Returns
    -------
    new_s: str
        Return the string where every original punctuation character is replaced with delimiter
        
    Raises
    ------
    TypeError
        If the input is not a string
    '''
    
    # Validate the input variable type
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    if not isinstance(delimiter, str):
        raise TypeError("Delimiter must be a string")
        
    # Get all punctuations except period(.), which may be used in acronyms
    punctuations = ''.join([punct for punct in string.punctuation if punct != '.'])
    # Create the regex format to capture any punctuation characters
    regex_punct = r'['+re.escape(punctuations)+']'
    # Replace every punctuation character in the input string with a single space
    new_s = re.sub(regex_punct, delimiter, s)
    # Remove redundant spaces
    new_s = re.sub(r''+re.escape(delimiter)+'+',' ', new_s)
    # Return
    return new_s

def remove_words(title, wordList):
    '''
    Remove meaningless words from the title. 
    Mainly abbreviations for the form of business enterprise.
    
    - Coporations:
        - Corp: Corporation
        - INC: Incorporated Company
        - PC: Professional Coporation
        - SC: Service Coporation
    - Partnerships:
        - GP: Genearl Partnership
        - LP: Limited Partnership
        - LLP: Limited Liability Partnership
        - LLLP: Limited Liability Limied Partnership
    - Limited Liability Companies:
        - LLC: Limited Liability Company
        - LC: Limited Liability Company
        - LTD.: Limited Company
        - PLLC: Professional Limited Liability Company
    
    Parameters
    ----------
    title:str
        Input title
    wordList:[str]
        A list of words to remove from the title
    
    Returns
    -------
    clean_title: str
         Cleaned title after words removal
    
    Raises
    ------
    TypeError
        If the input word list for removal are not a list of strings
    '''
    # Validate input variable type
    if not isinstance(wordList, list):
        raise TypeError('The input word list for removal must be a list')
    if not all([isinstance(word, str) for word in wordList]):
        raise TypeError('Every word in the list must be in string format')    
    
    # Remove words from the title if it appears in the given word list for removal
    clean_title = [word for word in title.split() if word not in wordList]
    # Combine the rest of words together in a string separated by whitespace
    clean_title = ' '.join(clean_title)
    
    # Return the cleaned title
    return clean_title

def clean_title(title, wordList):
    '''
    Clean the input title and return the new one
    
    Parameters
    ----------
    wordList: [str]
        The list of words targeted to be removed from titles
        
    Returns
    -------
    new_title: str
        The cleaned title
    '''
    
    # Replace puncatuations in the title with whitespace
    new_title = replace_punctuations(title)
    # Remove words in the given list from the title
    new_title = remove_words(new_title, wordList)
    
    # If after the cleaning, nothing is left
    if new_title == '':
        # Skip the cleaning procedure and restore the original raw title
        new_title = title
    
    # Return the cleaned title
    return new_title

def root_word(title, ignore):
    '''
    Obtain the root word of a title based on the following assumptions:
    (1) The root word is at the beginning of the title
    (2) The root word is consisted of more than one character
    
    Parameters
    ----------
    title: str
        Input title with space as delimiter
    ignore: [str]
        The list of words to ignore when locating the root word of a title
        
    Returns
    -------
    root: str
        The root word of the input title
    
    Raises
    ------
    TypeError
        If the input title is not a string
    '''
    
    # Obtain the list of words in the title
    words = title.split()
    
    # Remove the first word from consideration if it is among the ignore words
    if words[0] in ignore:
        words.pop(0)
    
    # Assume the first word is root word
    root = words.pop(0)
    
    # If the first word has only one character
    if len(root) == 1:
        # Loop through the rest words in the list in order one by one, 
        # stop when reach a word that has more than one characters
        while len(words[0]) <= 1:
            # Pop out the first word from the list
            # Add the first word to root word with space delimiter
            root += ' ' + words.pop(0)

    # Return the root word
    return root

def longest_common_substring(s1, s2):
    '''
    Use dynamic programming to find the longest common substring, with complete words, 
    of two input strings
    
    Parameters
    ----------
    s1: str
        First input string
    s2: str
        Second input string
    
    Returns
    -------
    substring: str
        Return the longest common substring
        
    Raises
    ------
    TypeError
        If the inputs are not strings
    '''
    
    # Validate the input variable type
    if not isinstance(s1, str):
        raise TypeError("First input must be a string")
    if not isinstance(s2, str):
        raise TypeError("Second input must be a string")
    
    # Split the first string into list of words
    s1 = s1.split()
    # Split the second string into list of words
    s2 = s2.split()
    
    # Initialize a matrix M filled with zeroes to store 
    # lengths of the longest common substring
    # M[i][j] contains the lengh of longest common substring between 
    # s1[0,1,...,i-1] and s2[0,1,...,j-1]
    M = np.array([[0] * (1 + len(s2)) for i in range(1 + len(s1))])
    
    # Initialize the lenghth of the longest common substring to zero
    longest_length = 0
    
    # Compare all characters in s1 and all characters in s2 pair by pair
    for i in range(1, 1 + len(s1)):
        for j in range(1, 1 + len(s2)):
            # If i-1 th character in s1 matches j-1 th character in s2
            if s1[i - 1] == s2[j - 1]:
                # Add the longest length by 1
                M[i][j] = M[i - 1][j - 1] + 1
                # Update the longest_length
                longest_length = max(longest_length,M[i][j])
    
    # Find the end position of the longest common substring in s1
    s1_end = np.where(M == longest_length)[0].item(0)
    # Calculate the start position of the the longest common substring in s1
    s1_start = s1_end - longest_length
    # Extract the longest common substring
    substring = ' '.join(s1[s1_start: s1_end])
    
    # Return the longest common substring
    return substring

def unify_title(dataframe, raw_column, unified_column, ignore, remove):
    '''
    Unify similar titles in raw_column of dataframe and 
    put the same unified title for all of them in corresponding unified_column
    
    Parameters
    ----------
    dataframe: pandas.core.frame.DataFrame
        Input table containing at least a raw title column which need to be unified
    raw_column: str
        Column name in the dataframe that contains raw titles
    unified_column:str
        Column name in the dataframe that will store the unified titles
    ignore: [str]
        The list of words to ignore when locating the root word of a title
    remove: [str]
        The list of words targeted to be removed from titles
    
    Returns
    -------
    result: pandas.core.frame.DataFrame
        Return a table with both original raw titles and their unified titles
        
    Raises
    ------
    TypeError
        If the input table is not pandas dataframe, or column names are not strings
    '''
    
    # Validate the input variable type
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Input table must be pandas DataFrame")
    if not isinstance(raw_column, str):
        raise TypeError("Column name in the dataframe for raw titles must be a string")
    if not isinstance(unified_column, str):
        raise TypeError("Column name in the dataframe to store unified titles must be a string")
    
    # Make a deep copy of original data
    result = dataframe.copy()
    
    # Obtain the list of raw titles
    raw_title = result[raw_column]
    
    # Initialize i and j
    # i: the index of current raw title
    # j: the index of the raw title to compare with
    i = 0
    j = i
    # Obtain the max value for index j (The number of rows in dataframe)
    _max = result.shape[0]
    
    # While the index j is NOT out of range
    while j < _max:
        # Obtain the current raw title and clean it
        raw = clean_title(raw_title[i], remove)
        # Obtain the root word from the raw_title[i]
        root = root_word(raw, ignore)
        # Create an empty list to store longest common substring for each pair of raw titles
        common_title_list = []

        # Loop through all raw titles starting from index i
        # Find the longest common substring between raw_title[i] and raw_title[j] 
        # Stop when
        # (1) Reach the last row (j == _max - 1)
        # (2) raw_title[i] and raw_title[j] DO NOT have the same root word (Should NOT be unified)
        for j in range(i, _max):
            # Obtain the current raw title and clean it
            new_raw = clean_title(raw_title[j], remove)
            # Obtain the root word for raw_title[j]
            new_root = root_word(new_raw, ignore)
            
            # If the two raw titles have the same root word
            # Try to unify these two titles
            if new_root == root:
                # Find the longest common substring
                common_title = longest_common_substring(raw,new_raw)
                # Add the current longest common substring to the list
                common_title_list.append(common_title)
                # If the index reach the last row
                if j == _max - 1:
                    # Use the shortest substring from the common_title_list
                    # to be the unified title
                    unified_title = min(common_title_list, key = len)
                    # If the unified title does not contain the root word
                    if root not in unified_title:
                        # Discard the longest common substring and
                        # set the root word to be the unified title
                        unified_title = root
                    
                    # Insert the same unified title for all current raw titles
                    result.loc[i:j,unified_column] = unified_title
                    # Return the new dataframe with filled unified_column
                    return result
            
            # If the two raw titles DO NOT have the same root word
            # Finish the current title unification
            else:
                # Use the shortest substring from the common_title_list
                # to be the unified title
                unified_title = min(common_title_list, key = len)
                # If the unified title does not contain the root word
                if root not in unified_title:
                    # Discard the longest common substring and
                    # set the root word to be the unified title
                    unified_title = root
                    
                # Insert the same unified title for all current raw titles
                result.loc[i:j-1,unified_column] = unified_title
                # Reset index i to start title unification for the next raw title
                i = j
                # Jump out of the inner j for loop
                break

# Execute the main() function
main()