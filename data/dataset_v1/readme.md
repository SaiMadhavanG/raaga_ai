# Dataset v1

Contains ~149 hours of concert recordings, data sourced from [pymusiccomp](https://dunya.compmusic.upf.edu/)

Link to [onedrive](https://iiitbac-my.sharepoint.com/:u:/g/personal/g_saimadhavan_iiitb_ac_in/EfGj4Z9RyjlIlHhEXVxxN7cBIpXLccF1_x-tI16rdbdd1w?e=zrnEfe)

Code used to create can be found at `../../utils/dunya.py`

Contains (<=)30 sec clips for songs of 20 raagas:

| Raaga             | Hours     |
|-------------------|-----------|
| todi              | 27.525000 |
| bhairavi          | 16.375000 |
| shankaraabharanam | 13.458333 |
| kalyaani          | 12.691667 |
| pantuvaraali      | 9.366667  |
| kharaharapriya    | 8.333333  |
| poorvikalyaani    | 7.375000  |
| mohanam           | 7.175000  |
| saaveri           | 6.850000  |
| shanmukhapriya    | 6.675000  |
| dhanyaasi         | 4.908333  |
| hindolam          | 4.758333  |
| varaali           | 4.350000  |
| kaapi             | 4.191667  |
| madhyamaavati     | 3.966667  |
| aanandabhairavi   | 3.725000  |
| kaanada           | 3.100000  |
| athaanaa          | 2.283333  |
| hamsanaadam       | 1.108333  |
| neelaambari       | 0.858333  |


### Problems
- Not Manual inspected
- Imbalance of classes
- Error in 175 audio files, skipped for now
- Many clips contain speech, often explicitly mentioning name of raaga used.
- What dataset stats should we keep track of?