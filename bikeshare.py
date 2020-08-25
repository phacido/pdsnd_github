
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ['january','february','march', 'april', 'may','june', 'all']
week_day_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
city_list = ['chicago','new york', 'washington']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to look at data from Chicago, New York or Washington?: ').lower()
    city_condition = city in city_list
    while (city_condition==False):
        city = input('Would you like to look at data from Chicago, New York or Washington?: ').lower()
        city_condition = city in city_list
    
    # get user input for month (all, january, february, ... , june)  
    month = input('select a month from january to june to filter by or type all: ').lower()
    # ask if the month is on the defined month list
    month_condition = month in month_list
    
    while (month_condition == False):
        month = input('select a month from january to june to filter by or type all: ').lower()
        # update the condition
        month_condition = month in month_list
    
    # get user input for day of week (all, monday, tuesday, ... sunday)    
    day = input('select a day of the week or type all: ').lower()
    # ask if the day is in the defined day list
    day_condition = day in week_day_list
    while (day_condition==False):
        day = input('select a day of the week or type all: ').lower()
        day_condition = day in week_day_list

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read the specified file
    file_path = CITY_DATA[city]
    df = pd.read_csv(file_path, index_col=0)
    
    # convert data to the correct type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # sepparate date time into components
    df['month']= df['Start Time'].dt.month_name().str.lower()
    df['day']= df['Start Time'].dt.day_name().str.lower()
    df['start_hour'] = df['Start Time'].dt.hour
    
    # create an origin destination column
    df['start_end'] = df['Start Station'] + ' to ' + df['End Station']
    
    # filter by month and day
    if month!='all':
        df = df[df['month']==month]
    if day!='all':
        df = df[df['day']==day]
        
    return df

def time_stats(df):
    # df: a pandas dataframe containing the data
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('most common month: ', df['month'].mode()[0])

    # display the most common day of week
    print('most common day: ', df['day'].mode()[0])

    # display the most common start hour
    print('most common hour: ', df['start_hour'].mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    # df: a pandas dataframe containing the data
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('most common start station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('most common end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    # use our origin destination column
    print('most common start-end combination: ', df['start_end'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    # df: a pandas dataframe containing the data
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time:', df['Trip Duration'].sum())

    # display mean travel time
    print('mean travel time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    # df: a pandas dataframe containing the data
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User types count: ')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print()
    print('User gender count: ')
    # makes sure that the data frame has this field
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print('not available')

    # Display earliest, most recent, and most common year of birth
    print()
    print('----- Birth Year Statistics -----')
    print()
    # makes sure that the data frame has this field
    if 'Birth Year' in df.columns:
        print('Earliest birth year: ')
        print(df['Birth Year'].min())
        print('Latest birth year: ')
        print(df['Birth Year'].max())
        print('Most common birth year: ')
        print(df['Birth Year'].mode())
    else:
        print('not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_trip_info(df):
    #------- input:
    # df: is a pandas data frame
    
    # asks if the user ones to see individual trip info
    # if not a valid answer keeps asking
    show_info = input('would you like to see individual trip information?: ')
    while (show_info!='yes') & (show_info!='no'):
        show_info = input('would you like to see individual trip information?:')
        
    # counter to show the next rows after each iteration
    i=0
    # keeps showing more info until no
    while show_info=='yes':
        # shows 5 rows
        print(df.iloc[i:i+5])
        # updates the counter
        i = i+5
        # updates to stop while
        show_info = input('would you like to see more individual trip information?: ')
        


def main():
    # the while statemente functions as a way to keep asking for the user's
    # input until they explicitly indicate to stop repeating
    while True:
        # get user input
        city, month, day = get_filters()
        # load and pre process the data
        df = load_data(city, month, day)
        # display statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)        
        show_trip_info(df)

        # ask if user wants to restart 
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
           break


if __name__ == "__main__":
    main()





