"""
Name: Yuyan Yang

Student ID: 24358018

Description: This script processes and analyzes social media data from a CSV file.
It includes functions to read data, categorize users by profession, calculate engagement
metrics, and perform statistical analyses. The results provide insights into user
behavior based on profession, engagement, and demographic patterns. The script supports
operations like filtering data, calculating cosine similarity between age and income, and
assessing engagement differences using statistical methods.

"""

def read_csv_data(csvfile):
    try:
        # Open the CSV file for reading
        with open(csvfile, 'r') as file:
            lines = file.readlines() # Read all lines in the file
        
        # Extract the first line as headers
        headers = lines[0].strip().split(',')
        # Process the remaining lines as data rows
        data = [line.strip().split(',') for line in lines[1:]]
        return headers, data
    except Exception as e:
        # If an error occurs, print the error message and return empty lists
        print("Error reading the file:", str(e))
        return [], []

def process_social_media_data(headers, data):
    # Find the index of necessary columns
    idx_profession = headers.index('profession')
    idx_id = headers.index('id')
    idx_age = headers.index('age')
    idx_time_spent_hour = headers.index('time_spent_hour')
    idx_engagement_score = headers.index('engagement_score')
    
    # Dictionaries to store data for students and non-students
    students = {}
    non_students = {}
    
    # Loop through each record in data
    for elements in data:
        # Skip lines that do not have the correct number of data columns
        if len(elements) != len(headers):
            continue  # skip lines with incorrect number of columns
        
        # Clean and extract data from each row
        user_id = elements[idx_id].strip().lower()
        profession = elements[idx_profession].strip().lower()
        age = elements[idx_age].strip()
        time_spent_hour = elements[idx_time_spent_hour].strip()
        engagement_score = elements[idx_engagement_score].strip()
        
        # Validate data to ensure it is in the correct format
        if not age.isdigit() or int(age) <= 0:
            continue
        if not time_spent_hour.replace('.', '', 1).isdigit():
            continue
        if not engagement_score.replace('.', '', 1).isdigit():
            continue
        
         # Convert string data to appropriate types (integer or float)
        age = int(age)
        time_spent_hour = float(time_spent_hour)
        engagement_score = float(engagement_score)
        
        # Pack the extracted and converted data into a list
        record = [age, time_spent_hour, engagement_score]
        
        # Store the record in the corresponding dictionary based on the profession
        if profession == "student":
            students[user_id] = record
        else:
            non_students[user_id] = record
    
    return [students, non_students]

def calculate_engagement_metrics(headers, data):
    # Find the index of necessary columns
    idx_platform = headers.index('platform')
    idx_engagement_score = headers.index('engagement_score')
    idx_time_spent_hour = headers.index('time_spent_hour')
    
    # Dictionary to accumulate data for each platform
    platform_data = {}
    
    # Process each row of data
    for elements in data:
        # Skip rows with incorrect column count
        if len(elements) != len(headers):
            continue
        
        platform = elements[idx_platform].strip().lower()
        time_spent_hour = elements[idx_time_spent_hour].strip()
        engagement_score = elements[idx_engagement_score].strip()
        
        # Skip invalid data
        if not time_spent_hour.replace('.', '', 1).isdigit() or not engagement_score.replace('.', '', 1).isdigit():
            continue
        
        # Calculate engagement time as a product of time spent and engagement score, rounded to four decimal places
        engagement_time = round(float(time_spent_hour) * float(engagement_score) / 100, 4)
        
        # Accumulate engagement times for each platform
        if platform not in platform_data:
            platform_data[platform] = []
        platform_data[platform].append(engagement_time)
    
    # Calculate total, average, and standard deviation of engagement times for each platform
    result = {}
    for platform, times in platform_data.items():
        total = round(sum(times), 4)
        average = round(total / len(times), 4)
        variance = sum((x - average) ** 2 for x in times) / (len(times) - 1 if len(times) > 1 else 1)
        stdev = round(variance ** 0.5, 4)
        result[platform] = [total, average, stdev]
    
    return result

def process_data_for_cosine_similarity(headers, data):
    # Find the index of necessary columns
    idx_profession = headers.index('profession')
    idx_age = headers.index('age')
    idx_income = headers.index('income')
    
    # Lists to store age and income data for students and non-students
    student_ages = []
    student_incomes = []
    non_student_ages = []
    non_student_incomes = []
    
    # Loop through each record
    for elements in data:
        # Skip if the number of elements is incorrect
        if len(elements) != len(headers):
            continue
        
        profession = elements[idx_profession].strip().lower()
        age = elements[idx_age].strip()
        income = elements[idx_income].strip()
        
        # Validate and convert data
        if age.isdigit() and income.replace('.', '', 1).isdigit():
            age = int(age)
            income = float(income)
            
            # Append data to the appropriate list based on profession
            if profession == "student":
                student_ages.append(age)
                student_incomes.append(income)
            else:
                non_student_ages.append(age)
                non_student_incomes.append(income)
    
    # Calculate cosine similarity for both groups
    student_similarity = calculate_cosine_similarity(student_ages, student_incomes)
    non_student_similarity = calculate_cosine_similarity(non_student_ages, non_student_incomes)
    
    return [student_similarity, non_student_similarity]

def calculate_cosine_similarity(age_list, income_list):
    if len(age_list) != len(income_list):
        # Make sure the age list and income list are the same length
        raise ValueError("Lists must be of the same length")
    
    dot_product = sum(age_list[i] * income_list[i] for i in range(len(age_list)))
    norm_a = sum(a ** 2 for a in age_list) ** 0.5
    norm_b = sum(b ** 2 for b in income_list) ** 0.5
    
    # Prevents division by zero
    if norm_a == 0 or norm_b == 0:
        return 0
    
    # Returns cosine similarity, keeping four decimals
    return round(dot_product / (norm_a * norm_b), 4)

def calculate_cohens_d(group1, group2):
    # Calculate sample sizes, means, and variances for both groups
    n1, n2 = len(group1), len(group2)
    mean1, mean2 = sum(group1) / n1, sum(group2) / n2
    variance1 = sum((x - mean1) ** 2 for x in group1) / (n1 - 1)
    variance2 = sum((x - mean2) ** 2 for x in group2) / (n2 - 1)
    # Calculate pooled standard deviation
    pooled_std = (((n1 - 1) * variance1 + (n2 - 1) * variance2) / (n1 + n2 - 2)) ** 0.5
    # Calculate and return Cohen's d
    return round((mean1 - mean2) / pooled_std, 4) if pooled_std else 0

def main(csvfile):
    # Read data from the CSV file
    headers, data = read_csv_data(csvfile)
    if not headers or not data:
        return [], {}, [], 0
    
    # Perform various analyses
    OP1 = process_social_media_data(headers, data)
    OP2 = calculate_engagement_metrics(headers, data)
    OP3 = process_data_for_cosine_similarity(headers, data)
    OP4 = calculate_cohens_d(
        [x[1] * x[2] / 100 for x in OP1[0].values()],  # Engagement times of students
        [x[1] * x[2] / 100 for x in OP1[1].values()]   # Engagement times of non-students
    )
    
    return OP1, OP2, OP3, OP4