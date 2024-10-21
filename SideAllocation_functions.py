import pandas as pd

'''def check_excel_format(df, required_columns, additional_column):
  
  try:
    #df = pd.read_excel(excel_path)
    if set(required_columns) == set(df.columns):
      return True, df
    elif set(required_columns[:-1]) == set(df.columns):  
      df[f'{additional_column}'] = ' '
      #df.to_excel(excel_path, index=False)
      return True, df
    else:
      print("Incorrect extraction format.")
      return False, df
  except Exception as e:
    print(f"Error reading Excel file: {e}")
    return False, df     

def check_excel_format(df, required_columns, additional_column):
    try:
        # If df is a single DataFrame
        if isinstance(df, pd.DataFrame):
            if set(required_columns) == set(df.columns):
                return True, df
            elif set(required_columns[:-1]) == set(df.columns):
                df[f'{additional_column}'] = ' '
                return True, df
            else:
                print("Incorrect extraction format.")
                return False, df

        # If df is a list of DataFrames
        elif isinstance(df, list) and all(isinstance(d, pd.DataFrame) for d in df):
            all_successful = True  # To track if we successfully add the column to all DataFrames
            updated_dfs = []

            for dataframe in df:
                if set(required_columns) == set(dataframe.columns):
                    updated_dfs.append(dataframe)  # No changes needed
                elif set(required_columns[:-1]) == set(dataframe.columns):
                    dataframe[f'{additional_column}'] = ' '  # Add the additional column
                    updated_dfs.append(dataframe)
                else:
                    all_successful = False  # Mark it as not successful for one or more DataFrames
                    print("Incorrect extraction format for one DataFrame.")
                    updated_dfs.append(dataframe)

            return all_successful, updated_dfs

        else:
            print("Input is neither a DataFrame nor a list of DataFrames.")
            return False, df

    except Exception as e:
        print(f"Error processing the input: {e}")
        return False, df'''

def check_excel_format_dict(df_dict, required_columns, additional_column):
    flag = True
    
    for key, df in df_dict.items():
        if set(required_columns) != set(df.columns):
            if set(required_columns[:-1]) == set(df.columns):
                df[additional_column] = ' '
            else:
                print(f"Incorrect extraction format for DataFrame '{key}'.")
                flag = False
    
    return flag, {key: df for key, df in df_dict.items()}

def check_excel_format(df, required_columns, additional_column):
    try:
        # If df is a DataFrame
        if isinstance(df, pd.DataFrame):
            if set(required_columns) == set(df.columns):
                return True, df
            elif set(required_columns[:-1]) == set(df.columns):
                df[additional_column] = ' '
                return True, df
            else:
                print("Incorrect extraction format.")
                return False, df
        
        # If df is a dictionary of DataFrames
        elif isinstance(df, dict):
            return check_excel_format_dict(df, required_columns, additional_column)
        
        else:
            print("Invalid input type: must be a DataFrame or dictionary of DataFrames.")
            return False, df

    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return False, df


########################################################################################33




def priority_order(row, df):
    value = row['Grouping']
    index = row.name  # Get the index from the row object
    
    # Power related cases
    if value == 'Power_Positive':
        return f"A_Power_Positive"
    elif value == 'Power_Ref_Positive':
        return f"A_Power_Ref_Positive"    
    elif value == 'Power_Negetive_Regulator_Capacitor':
        return f"Y_Power_Negetive"
    elif value == 'Power_Negetive':
        return f"Z_Power_Negetive"
    elif value == 'System':
        return f"B_System"
    elif value == 'Reset':
        return f"BR_Reset"
    elif value == 'No_Connect':
        return f"X_No_Connect"

    # Clock-related cases
    elif any(keyword in value for keyword in ('X1', 'X2')):
        return f"CA_Main_Clocks/Oscillators"
    elif 'Main_Clock' in value:
        return f"CA_Main_Clocks/Oscillators"    
    elif 'XT' in value:
        return f"CB_External_Clocks/Oscillators"
    elif 'Clock_Capacitor' in value:
        return f"CC_External_Capacitive_Clocks/Oscillators"
    elif 'Reference_Clk' in value:
        return f"CD_Reference_Clocks/Oscillators"
    elif 'Chip_Select' in value:
        return f"CS_Chip_Select"
    
    #Control Pins 
    elif 'Control' in value:
        return f"CT_Control"   
    elif 'data_lines' in value:
        return f"D_Data_Lines"        

    # I2C, Mode, Interrupts, Output cases
    elif value == 'I2C_Pins':
        return f"D_I2C_Pins"
    elif value == 'Mode':
        return f"E_ModePins"
    elif 'INT' in value:
        return f"I_Interrupts"
    elif 'Output' in value:
        return f"S_Output"
    
    #Handling ADC Pins 
    elif 'ADC_Pins' in value:
        return f"F_ADC_Pins"
    elif 'Cutoff' in value:
        return f"F_C_Cutoff"   
    elif 'Control' in value:
        return f"F_CNT_Control"  
    elif 'GPIO_Pins' in value:
        return f"G_GPIO_Pins"
       

    # Port handling
    elif value.startswith("Port"):
        if row['Electrical Type'] == 'Input':

            if value.startswith("Port"):
                port_number = int(value.split(' ')[1])
                return f"P_Port {port_number:02d}"

            value_alternative = row['Pin Alternate Name']

            # Swap conditions for Input Electrical Type
            if any(keyword in value_alternative for keyword in ('X1', 'X2')):
                swap_pins_for_that_row(df, index)
                return f"CA_Main_Clocks/Oscillators"
            elif 'XT' in value_alternative:
                swap_pins_for_that_row(df, index)
                return f"CB_External_Clocks/Oscillators"
            elif 'MD' in value_alternative:
                swap_pins_for_that_row(df, index)
                return f"E_ModePins"
            elif 'NMI' in value_alternative:
                swap_pins_for_that_row(df, index)
                return f"I_Interrupts"
            elif 'VREF' in value_alternative:
                swap_pins_for_that_row(df, index)
                return f"A_Power_Ref_Positive"
            elif 'VRFF' in value_alternative:
                swap_pins_for_that_row(df, index)
                return f"A_Power_Ref_Positive"                
            else:

                return f"ZZ_Not_Assigned"

        else:
            # Handle non-input electrical type (like Output)
            port_number = int(value.split(' ')[1])
            return f"P_Port {port_number:02d}"

    # Default case for unhandled conditions
    else:
        return None

def swap_pins_for_that_row(df, index):
    df.loc[index, 'Pin Display Name'], df.loc[index, 'Pin Alternate Name'] = df.loc[index, 'Pin Alternate Name'], df.loc[index, 'Pin Display Name']
    return
    
def filter_and_sort_by_priority(df):
    sorted_df = df.sort_values(by='Priority', ascending=True).reset_index(drop=True)
    return sorted_df
       

def allocate_small_dataframe(row, df):
    grouped_indices = df.groupby('Priority').indices
    total_rows = len(df)
    left = []
    right = []
    left_limit = total_rows // 2

    last_side = 'Left'  # Start with the left side

    for group in grouped_indices.values():
        if last_side == 'Left' and len(left) + len(group) <= left_limit:
            left.extend(group)
        else:
            right.extend(group)
            last_side = 'Right'  # Switch to right side

    if row.name in left:
        return 'Left'
    else:
        return 'Right'


def side_allocation(row, df):
    total_rows = len(df)    
    if total_rows > 80:
        return f"Some error Occured"
    else:
        return allocate_small_dataframe(row, df)

def assigning_priority_for_group(df):
    df_copy = df.copy()  
    df_copy['Priority'] = df_copy.apply(lambda row: priority_order(row, df_copy), axis=1)
    return df_copy

def assigning_side_for_priority(df):
    df_copy = df.copy()
    df_new = filter_and_sort_by_priority(df_copy)
    df_new['Side'] = df_new.apply(lambda row: side_allocation(row, df_new), axis=1)
    
    # Apply sorting based on 'Side'
    ascending_order_df = df_new[df_new['Side'] == 'Left']
    ascending_order_df = assigning_ascending_order_for_similar_group(ascending_order_df)
    
    descending_order_df = df_new[df_new['Side'] == 'Right']
    descending_order_df = assigning_descending_order_for_similar_group(descending_order_df)
    
    # Concatenate the two sorted DataFrames back together
    final_df = pd.concat([ascending_order_df, descending_order_df]).reset_index(drop=True)
    
    return final_df

 
def assigning_ascending_order_for_similar_group(df):
    df_copy = df.copy()
    ascending_order_df = df_copy.groupby('Priority').apply(lambda group: group.sort_values('Pin Display Name'))
    ascending_order_df.reset_index(drop=True, inplace=True)
    return ascending_order_df 

def assigning_descending_order_for_similar_group(df):
    df_copy = df.copy()
    descending_order_df = df_copy.groupby('Priority').apply(lambda group: group.sort_values('Pin Display Name', ascending=False))
    descending_order_df.reset_index(drop=True, inplace=True)
    return descending_order_df


def Dual_in_line_as_per_Renesas(df): 
    df_copy = df.copy()

    # Create a new column 'Changed Grouping'
    df_copy['Changed Grouping'] = None

    # Function to get alphabetical inverse of the first letter
    def alphabetical_inverse(letter):
        if letter.isalpha() and letter.isupper():
            return chr(155 - ord(letter))  # A -> Z, B -> Y, etc.
        return letter

    # Function to get the alphabet corresponding to the reverse of a number (e.g., 01 -> Z, 05 -> V)
    def number_to_alphabet_inverse(number_str):
        if number_str.isdigit():
            num = int(number_str)
            if 1 <= num <= 26:
                return chr(91 - num)  # 1 -> Z, 2 -> Y, 3 -> X, ..., 26 -> A
        return number_str

    # Function to sort groups by 'Pin Display Name' in descending order for 'Right' side
    def assigning_descending_order_for_similar_group(group):
        return group.sort_values('Pin Display Name', ascending=False)

    # Sort the right-side groups by 'Pin Display Name' in descending order
    right_side_group = df_copy[df_copy['Side'] == 'Right']
    sorted_right_group = right_side_group.groupby('Priority').apply(assigning_descending_order_for_similar_group)

    # Iterate over the rows
    for index, row in df_copy.iterrows():
        priority = row['Priority']

        # For 'Left' side, keep the priority unchanged
        if row['Side'] == 'Left':
            df_copy.at[index, 'Changed Grouping'] = priority

        # For 'Right' side, modify the priority using the sorted 'Pin Display Name'
        elif row['Side'] == 'Right':
            # Fetch the sorted row from the 'sorted_right_group'
            sorted_row = sorted_right_group.loc[(sorted_right_group['Priority'] == priority) & (sorted_right_group['Pin Display Name'] == row['Pin Display Name'])].iloc[0]

            # Change the first letter of the 'Priority' value to its alphabetical inverse
            first_letter = sorted_row['Priority'][0]
            inverse_first_letter = alphabetical_inverse(first_letter)

            # Check if the priority ends with a number
            if sorted_row['Priority'][-2:].isdigit():  # Assuming numbers are two digits
                num_part = sorted_row['Priority'][-2:]  # The last two characters (numbers)
                inverse_num_part = number_to_alphabet_inverse(num_part)
                
                # Reconstruct the priority with the inverse number and inverse first letter
                df_copy.at[index, 'Changed Grouping'] = inverse_first_letter + sorted_row['Priority'][1:-2] + inverse_num_part + "_" + num_part
            else:
                # If no number at the end, just change the first letter
                df_copy.at[index, 'Changed Grouping'] = inverse_first_letter + sorted_row['Priority'][1:]

    return df_copy

import pandas as pd

def Dual_in_line_as_per_Renesas(df):
    # Check if the input is a dictionary of DataFrames
    if isinstance(df, dict):
        df_copy_dict = {}  # Initialize a dictionary to store modified DataFrames
        
        # Iterate through each DataFrame in the input dictionary
        for table_name, df_copy in df.items():
            # Create a copy of the current DataFrame
            df_copy = df_copy.copy()

            # Create a new column 'Changed Grouping'
            df_copy['Changed Grouping'] = None

            # Function to get alphabetical inverse of the first letter
            def alphabetical_inverse(letter):
                if letter.isalpha() and letter.isupper():
                    return chr(155 - ord(letter))  # A -> Z, B -> Y, etc.
                return letter

            # Function to get the alphabet corresponding to the reverse of a number (e.g., 01 -> Z, 05 -> V)
            def number_to_alphabet_inverse(number_str):
                if number_str.isdigit():
                    num = int(number_str)
                    if 1 <= num <= 26:
                        return chr(91 - num)  # 1 -> Z, 2 -> Y, 3 -> X, ..., 26 -> A
                return number_str

            # Function to sort groups by 'Pin Display Name' in descending order for 'Right' side
            def assigning_descending_order_for_similar_group(group):
                return group.sort_values('Pin Display Name', ascending=False)

            # Sort the right-side groups by 'Pin Display Name' in descending order
            right_side_group = df_copy[df_copy['Side'] == 'Right']
            sorted_right_group = right_side_group.groupby('Priority').apply(assigning_descending_order_for_similar_group)

            # Iterate over the rows
            for index, row in df_copy.iterrows():
                priority = row['Priority']

                # For 'Left' side, keep the priority unchanged
                if row['Side'] == 'Left':
                    df_copy.at[index, 'Changed Grouping'] = priority

                # For 'Right' side, modify the priority using the sorted 'Pin Display Name'
                elif row['Side'] == 'Right':
                    # Fetch the sorted row from the 'sorted_right_group'
                    sorted_row = sorted_right_group.loc[(sorted_right_group['Priority'] == priority) & (sorted_right_group['Pin Display Name'] == row['Pin Display Name'])].iloc[0]

                    # Change the first letter of the 'Priority' value to its alphabetical inverse
                    first_letter = sorted_row['Priority'][0]
                    inverse_first_letter = alphabetical_inverse(first_letter)

                    # Check if the priority ends with a number
                    if sorted_row['Priority'][-2:].isdigit():  # Assuming numbers are two digits
                        num_part = sorted_row['Priority'][-2:]  # The last two characters (numbers)
                        inverse_num_part = number_to_alphabet_inverse(num_part)

                        # Reconstruct the priority with the inverse number and inverse first letter
                        df_copy.at[index, 'Changed Grouping'] = inverse_first_letter + sorted_row['Priority'][1:-2] + inverse_num_part + "_" + num_part
                    else:
                        # If no number at the end, just change the first letter
                        df_copy.at[index, 'Changed Grouping'] = inverse_first_letter + sorted_row['Priority'][1:]

            # Add the modified DataFrame to the output dictionary
            df_copy_dict[table_name] = df_copy
        
        return df_copy_dict  # Return the modified dictionary of DataFrames

    # If the input is not a dictionary, proceed with single DataFrame processing
    df_copy = df.copy()
    df_copy['Changed Grouping'] = None

    # [Same processing logic as above for a single DataFrame]

    return df_copy


def process_dataframe(df_copy):
    # Create a new column 'Changed Grouping'
    df_copy['Changed Grouping'] = None

    # Function to get alphabetical inverse of the first letter
    def alphabetical_inverse(letter):
        if letter.isalpha() and letter.isupper():
            return chr(155 - ord(letter))  # A -> Z, B -> Y, etc.
        return letter

    # Function to get the alphabet corresponding to the reverse of a number (e.g., 01 -> Z, 05 -> V)
    def number_to_alphabet_inverse(number_str):
        if number_str.isdigit():
            num = int(number_str)
            if 1 <= num <= 26:
                return chr(91 - num)  # 1 -> Z, 2 -> Y, 3 -> X, ..., 26 -> A
        return number_str

    # Function to sort groups by 'Pin Display Name' in descending order for 'Right' side
    def assigning_descending_order_for_similar_group(group):
        return group.sort_values('Pin Display Name', ascending=False)
    
    def assigning_ascending_order_for_similar_group(group):
        return group.sort_values('Pin Display Name', ascending=True)    

    # Sort the right-side groups by 'Pin Display Name' in descending order
    right_side_group = df_copy[df_copy['Side'] == 'Right']
    sorted_right_group = right_side_group.groupby('Priority').apply(assigning_descending_order_for_similar_group)    

    # Iterate over the rows
    for index, row in df_copy.iterrows():
        priority = row['Priority']

        # For 'Left' side, keep the priority unchanged
        if row['Side'] == 'Left':
            df_copy.at[index, 'Changed Grouping'] = priority

        # For 'Right' side, modify the priority using the sorted 'Pin Display Name'
        elif row['Side'] == 'Right':
            # Fetch the sorted row from the 'sorted_right_group'
            sorted_row = sorted_right_group.loc[
                (sorted_right_group['Priority'] == priority) &
                (sorted_right_group['Pin Display Name'] == row['Pin Display Name'])
            ].iloc[0]

            # Change the first letter of the 'Priority' value to its alphabetical inverse
            first_letter = sorted_row['Priority'][0]
            inverse_first_letter = alphabetical_inverse(first_letter)

            # Check if the priority ends with a number
            if sorted_row['Priority'][-2:].isdigit():  # Assuming numbers are two digits
                num_part = sorted_row['Priority'][-2:]  # The last two characters (numbers)
                inverse_num_part = number_to_alphabet_inverse(num_part)

                # Reconstruct the priority with the inverse number and inverse first letter
                df_copy.at[index, 'Changed Grouping'] = inverse_first_letter + sorted_row['Priority'][1:-2] + inverse_num_part + "_" + num_part
            else:
                # If no number at the end, just change the first letter
                df_copy.at[index, 'Changed Grouping'] = inverse_first_letter + sorted_row['Priority'][1:]

    return df_copy


def Dual_in_line_as_per_Renesas(df):
    # Check if the input is a dictionary of DataFrames
    if isinstance(df, dict):
        df_copy_dict = {}  # Initialize a dictionary to store modified DataFrames
        
        # Iterate through each DataFrame in the input dictionary
        for table_name, df_copy in df.items():
            # Create a copy of the current DataFrame
            df_copy = df_copy.copy()
            # Process the DataFrame
            df_copy_dict[table_name] = process_dataframe(df_copy)
        
        return df_copy_dict  # Return the modified dictionary of DataFrames

    # If the input is not a dictionary, process the single DataFrame
    df_copy = df.copy()
    return process_dataframe(df_copy)



########    Partitioning   ###############

def filter_out_power_pins(row, df):
    df['Priority'] = df['Priority'].fillna('')

    left_power_mask = df['Priority'].str.startswith('A')
    right_power_mask = df['Priority'].str.startswith('Z')

    # Create lists of indices for left and right power using the masks
    left_power = df.index[left_power_mask].tolist()
    right_power = df.index[right_power_mask].tolist()

    # Return based on the allocation
    if row.name in left_power:
        return 'Left'
    elif row.name in right_power:
        return 'Right'
    else:
        return None

def allocate_ports_after_partitioning(df):
    # Filter the DataFrame based on priority
    filtered_df = df[df['Priority'].str.startswith('P')]
    grouped_indices = filtered_df.groupby('Priority').indices

    #print(f"Grouped Indices: {grouped_indices}")

    left_first = []   # Groups allocated to the left side
    right_first = []  # Groups allocated to the right side
    left_next = []    # Extra groups for left side (if limit exceeded)
    right_next = []   # Extra groups for right side (if limit exceeded)

    left_limit = 40   # Limit for the left side
    right_limit = 40  # Limit for the right side

    current_left_count = 0
    current_right_count = 0

    # Iterate over the groups of indices
    for group_name, indices in grouped_indices.items():
        group_size = len(indices)

        # Try to allocate to the left_first side if there's space
        if current_left_count + group_size <= left_limit:
            left_first.append(group_name)
            current_left_count += group_size
        # If left_first is full, allocate to the right_first if there's space
        elif current_right_count + group_size <= right_limit:
            right_first.append(group_name)
            current_right_count += group_size
        # If both left_first and right_first are full, allocate to left_next
        elif len(left_next) < left_limit:
            left_next.append(group_name)
        # If left_next is also full, allocate to right_next
        elif len(right_next) < right_limit:
            right_next.append(group_name)
        else:
            print("All sides are full: Left, Right, Left Next, and Right Next")

    return left_first, right_first, left_next, right_next

def filter_out_port_pins(row, df):
    #df['Priority'] = df['Priority'].fillna('')
    #port_mask = df['Priority'].str.startswith('P')
    
    # Call allocate_ports_after_partitioning to get the allocations
    left_first, right_first , left_next, right_next = allocate_ports_after_partitioning(df)
    #print(f" Left : {left_first} \n Right : {right_first} \n Left_Next : {left_next} \n Right_Next : {right_next}")

    # Check the Priority of the current row
    priority_value = row['Priority']

    # Determine the allocation category for the given priority
    if priority_value in left_first:
        return 'Left'
    elif priority_value in left_next:
        return 'Left_Next'
    elif priority_value in right_first:
        return 'Right'
    elif priority_value in right_next:
        return 'Right_Next'
    
    return None


def partitioning(df_last):

    df = filter_and_sort_by_priority(df_last)

    df['Side'] = df.apply(filter_out_power_pins, args=(df,), axis=1)
    power_df = df[(df['Side'] == 'Left') | (df['Side'] == 'Right')]
    df['Side'] = power_df['Side']

    print("Power DataFrame:", power_df)

    unfilled_df = df[df['Side'].isna()]   
    number_of_rows_left = len(unfilled_df) 
    print(f"Length of unfilled Dataframe : {number_of_rows_left}")

    if number_of_rows_left < 80 :
        print(f"Only one extra Part")

        #df_copy = unfilled_df.copy()
        df_Part_A = filter_and_sort_by_priority(unfilled_df)
        df_Part_A['Side'] = df_Part_A.apply(lambda row: side_allocation(row, df_Part_A), axis=1)

        unfilled_df.loc[unfilled_df.index, 'Side'] = df_Part_A['Side'].values
        df.loc[unfilled_df.index, 'Side'] = df_Part_A['Side'].values

        #unfilled_df['Side'] = df_Part_A['Side']        
        print(f"Part A Dataframe : {df_Part_A}")

        unfilled_df= df[df['Side'].isna()]   
        number_of_rows_left = len(unfilled_df)
        print(f"Length of unfilled Dataframe : {number_of_rows_left}")
        if  number_of_rows_left == 0 :            
            print(f"Everything is correct and as per expectation")
        else:
            print(f"something is wrong")
            print (f"Unfilled dataframe : {unfilled_df}")    

    else:
        print(f"You will have to create more number of Parts")

        


    '''df['Side'] = df.apply(filter_out_port_pins, args=(df,), axis=1)
    port_df = df[(df['Side'] == 'Left') | (df['Side'] == 'Right')]
    print("Port DataFrame:", port_df)

    port_df_2 = df[(df['Side'] == 'Left_Next') | (df['Side'] == 'Right_Next')]
    port_df_2 = port_df_2.replace({'Left_Next': 'Left', 'Right_Next': 'Right'})
    print("Port DataFrame 2:", port_df_2)

    unfilled_df = df[df['Side'].isna()] 
    #unfilled_df = df[df['Side'].isna() & ~df['A'].str.startswith(('A', 'Z'))]
    print("Unfilled DataFrame:", unfilled_df)'''

    port_df, port_df = pd.DataFrame(),pd.DataFrame()

    #port_df_2, unfilled_df = pd.DataFrame(),pd.DataFrame()

    return power_df, df_Part_A , port_df , unfilled_df


def partitioning(df_last):
    df = filter_and_sort_by_priority(df_last)

    # Apply filter for power pins and update 'Side' column for power pins
    df['Side'] = df.apply(filter_out_power_pins, args=(df,), axis=1)
    power_df = df[df['Side'].isin(['Left', 'Right'])]
    df.loc[power_df.index, 'Side'] = power_df['Side']

    print("Power DataFrame:", power_df)

    # Handle unfilled rows
    unfilled_df = df[df['Side'].isna()]
    number_of_rows_left = len(unfilled_df)
    print(f"Length of unfilled DataFrame: {number_of_rows_left}")

    df_Part_A = pd.DataFrame()
    
    if number_of_rows_left < 80:
        print("Only one extra Part")

        df_Part_A = filter_and_sort_by_priority(unfilled_df)
        df_Part_A['Side'] = df_Part_A.apply(lambda row: side_allocation(row, df_Part_A), axis=1)

        # Update unfilled rows in the original DataFrame
        df.loc[unfilled_df.index, 'Side'] = df_Part_A['Side'].values

        print(f"Part A DataFrame: {df_Part_A}")

        # Recheck unfilled rows after allocation
        number_of_rows_left = df['Side'].isna().sum()
        print(f"Length of unfilled DataFrame: {number_of_rows_left}")

        if number_of_rows_left == 0:
            print("Everything is correct and as per expectation")
        else:
            print("Something is wrong")
            print(f"Unfilled DataFrame: {df[df['Side'].isna()]}")
    else:
        print("You will have to create more Parts")

    # Initialize empty DataFrames for future use
    port_df = pd.DataFrame()

    # Dictionary to store non-empty DataFrames
    df_dict = {
        'Power Table': power_df,
        'Part A Table': df_Part_A,
        'Port Table': port_df,
        'Unfilled Table': df[df['Side'].isna()]
    }

    # Filter out empty DataFrames
    df_divided_into_parts = {key: value for key, value in df_dict.items() if not value.empty}

    return df_divided_into_parts


def assigning_side_for_priority_for_dataframes_within_dictionary(dfs):
    final_dfs = {}

    for title, df in dfs.items():
        df_new = df.copy()
        
        # Apply sorting based on 'Side'
        ascending_order_df = df_new[df_new['Side'] == 'Left']
        ascending_order_df = assigning_ascending_order_for_similar_group(ascending_order_df)

        descending_order_df = df_new[df_new['Side'] == 'Right']
        descending_order_df = assigning_descending_order_for_similar_group(descending_order_df)

        # Concatenate the two sorted DataFrames back together
        final_df = pd.concat([ascending_order_df, descending_order_df]).reset_index(drop=True)
        
        # Store the modified DataFrame in the final dictionary
        final_dfs[title] = final_df
    
    return final_dfs


def convert_dict_to_list(df_dict):
    return [df for df in df_dict.values()]
