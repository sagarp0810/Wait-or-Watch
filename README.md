# Wait-or-Watch
Wait or Watch reminds you the release date of the next episode of your favorite TV Series

## Installation

- Clone this directory \
`git clone https://github.com/sagarp0810/Wait-or-Watch.git`

- Enter the directory \
`cd Wait-or-Watch`

- Install pip package \
`sudo apt-get install python-pip`

- Install the requirements \
`pip install -r requirements.txt`

## Usage
To run the script use the following command \
`python wow.py`

NOTE - Make sure your MySQL is configured with password="qwerty". If not you can change it the wow.py file with your password.

## Example

```python wow.py 
Welcome to Wait-or-Watch!!!

Email address: sagarpamnani77@gmail.com
TV Series: suits, tbbt, got, harry potter, silicon valley, friends

Adding to DB...
Added to DB successfully!

Fetching Data...
No TV Series found with name harry potter.

Fetched Data:
TV Series name: Suits
IMDb Rating: 8.6
Status: The next episode dates are not announced yet.

TV Series name: The Big Bang Theory
IMDb Rating: 8.2
Status: The next episode airs on 18 Oct, 2018.

TV Series name: Game of Thrones
IMDb Rating: 9.5
Status: The next season begins in 2019.

TV Series name: Silicon Valley
IMDb Rating: 8.6
Status: The next season is confirmed, dates yet to be announced.

TV Series name: Friends
IMDb Rating: 8.9
Status: The show has finished streaming all its episodes.

Sending email...
Email sent to sagarpamnani77@gmail.com successfully!
```
