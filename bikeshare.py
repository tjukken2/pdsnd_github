import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    try: 
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('Type in the city you would like to explore - Chicago, New York City or Washington:\n').lower()
        while city not in ('chicago','new york city','washington'):
            city = input('Please write in correct city name either Chicago, New York City or Washington:\n').lower()

        # get user input for month (all, january, february, ... , june)
        month = input('Type in the month you would like to explore (All, January, February, March, April, May or June):\n').lower()
        while month not in ('all','january','february','march','april','may','june'):
            month = input('Please write in correct city name either all, january, february, march, april, may or june:\n').lower()

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Type in the day you would like to explore (All, Monday, Tuesday, Wedensday, Thursday, Friday, Saturday, Sunday):\n').lower()
        while day not in ('all','monday','tuesday','wedensday','thursday','friday','saturday','sunday'):
            day = input('Please write in correct city name either all, monday, tuesday, wedensday, thursday, friday, saturday, sunday:\n').lower()

    except KeyboardInterrupt:
        print('\nProgram was ended. Have a nice day\n')
            
    except Exception as e:
        print('\nPlease correct you answer to the question!\n Exception occurred: {}'.format(e))

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name 
    df['hour'] = df['Start Time'].dt.hour 

    # Remove unnecessary column from dataframe (increase speed for calculation?)
    df.drop(df.columns[0], axis = 1, inplace=True)

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        Printed calculation statements
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('Most common day of week: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('Most common start hour: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    # Remove these temp dataframe columns (so it wouldn't show up in raw data output)
    df.drop(['month', 'day_of_week', 'hour'], axis = 1, inplace=True)
    
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        Printed calculation statements
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most commenly used end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Merge Start and End Station'] = df['Start Station'] + ' And ' + df['End Station']
    print('Most frequenct combination of start station and end station: {}'.format(df['Merge Start and End Station'].mode()[0]))
    df.drop('Merge Start and End Station', axis=1, inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        Printed calculation statements
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {} seconds'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean travel time: {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        Printed calculation statements
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of {}\n'.format(df.groupby('User Type').size()))

    # Display counts of gender
    # If chosen city is Washington don't show calc. Reason this data doesn't exists for this city
    if city == 'washington':
        print('Counts of gender: {}'.format('No data exists'))
    else:
        print('Counts of {}\n'.format(df.groupby('Gender').size()))

    # Display earliest, most recent, and most common year of birth
    # If chosen city is Washington don't show. Reason this data doesn't exists for this city
    if city == 'washington':
        print('Year of birth calculations: {}'.format('No data exists'))
    else:
        print('Earliest year of birth: {}'.format(df['Birth Year'].min()))
        print('Most recent year of birth: {}'.format(df['Birth Year'].max()))
        print('Most common year of birth: {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_output(df):
    """
    Asks user if they would like to see the first five or the next five rows of raw data (with filters applied).

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        Printed raw output
    """

    try: 
        # get user input if they would like to the see the raw data 
        show_raw = input('Would like to see the raw output for the first five rows - Yes or No:\n').lower()
        while show_raw not in ('yes', 'no'):
            show_raw = input('Please write in correct option: Yes or No:').lower()

        counter_start = 0
        counter_end = 0
        while show_raw == 'yes':
            increment = 5 
            counter_end += 1
            print('\n{}\n'.format(df[increment * counter_start:increment * counter_end]))
            counter_start += 1
            show_raw = input('Would like to see the raw output for the next five rows - Yes or No:\n').lower()
            while show_raw not in ('yes', 'no'):
                show_raw = input('Please write in correct options: Yes or No:\n').lower()

    except Exception as e:
        print('Please correct you answer to the question! Exception occurred: {}'.format(e))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_output(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
