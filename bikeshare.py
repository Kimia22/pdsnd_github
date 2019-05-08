################################
#Author: Kimia
#Project: Udacity Project 2
#Date: 3/9/2019
###############################

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
    list_of_valid_cities = ['chicago', 'new york city', 'washington']
    city = input('Which city (chicago, new york city, washington) ? ').lower()
    while city not in list_of_valid_cities:
        city = input('Which city (chicago, new york city, washington) ? ').lower()
    

    list_of_valid_month = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Which month (all, january, february, ... , june)? ').lower()
    while month not in list_of_valid_month:
        month = input('Which month (all, january, february, ... , june)? ').lower()

    list_of_valid_day_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Which day (all, monday, tuesday, ... , sunday)? ').lower()
    while day not in list_of_valid_day_of_week:
        day = input('Which day (all, monday, tuesday, ... , sunday)? ').lower()

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
    filename = CITY_DATA[city]
    
    df = pd.read_csv(filename, parse_dates=['Start Time', 'End Time'], infer_datetime_format=True)
    if day != 'all':
        list_of_valid_day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_index = list_of_valid_day_of_week.index(day)
        day_filter = df['Start Time'].dt.weekday==day_index
        df = df[day_filter]
    if month != 'all':
        list_of_valid_month = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = list_of_valid_month.index(month) + 1
        month_filter = df['Start Time'].dt.month==month_index
        df = df[month_filter]
    
    #Ask user to see if they like to see the raw data
    check_if_user_wants_to_see_raw_data = input('Do you like to see the raw data? (yes, no) ').lower()
    didUserSaidYes = True if check_if_user_wants_to_see_raw_data == 'yes' else False
    index = 5
    while didUserSaidYes:
        print(df[:].iloc[index:index+5])
        index += 5
        check_if_user_wants_to_see_raw_data = input('Do you like to see more data? (yes, no) ').lower()
        didUserSaidYes = True if check_if_user_wants_to_see_raw_data == 'yes' else False
    
    #return dataframe
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    a = df['Start Time'].dt.month
    most_common_month = a.mode()[0]
    list_of_valid_month = ['january', 'february', 'march', 'april', 'may', 'june']
    print('the most common month is: ', list_of_valid_month[most_common_month - 1])

    # display the most common day of week
    b = df['Start Time'].dt.weekday
    most_common_weekday = b.mode()[0]
    list_of_valid_day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('the most common day of week is: ', list_of_valid_day_of_week[most_common_weekday])

    # display the most common start hour
    c = df['Start Time'].dt.hour
    most_common_start_hour = c.mode()[0]
    print('the most common start hour is: ', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    v = df['Start Station']
    print('most commonly used start station is: ', v.mode()[0])

    # display most commonly used end station
    w = df['End Station']
    print('most commonly used end station is: ', w.mode()[0])

    # display most frequent combination of start station and end station trip
   
    df['Start End'] = df['Start Station'].map(str) + '&' + df['End Station']
    popular_start_end = df['Start End'].value_counts().idxmax()
    print('most frequent combination of start station and end station trip: ', popular_start_end)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    travel_time_list = df['Travel Time']
    total_second_list = list(map(lambda x: x.total_seconds(), travel_time_list))
    total_sum =  sum(total_second_list)
    print('total travel time in seconds is: ', total_sum)
    

    # display mean travel time
    avg = total_sum / len(total_second_list)
    print('mean travel time in seconds is: ', avg)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    k = df['User Type']
    j = set(k)
    print('Counts of User Types: ',len(j))
    # Display counts of gender
    if 'Gender' in df.columns:
        l = df['Gender']
        h = set(l)
        h = {x for x in h if pd.notna(x)}
        print('Counts of Gender: ', len(h))
    else:
        print('No gender data is available')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        u = df['Birth Year']
        print('erliest year: ', min(u))
        print('most recent year: ', max(u))
        print('most common year: ', u.mode()[0])
    else:
        print('No Birth Year data is available')
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
