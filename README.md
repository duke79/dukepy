## dukepy
collection of useful python snippets

`pip install dukepy`

### config
Confiuration manager (using json) with the ability to 
* add new keys
* remove deprecated keys (i.e. keys not in defaults)
* backup the older versions of the (json) configuration file

Generated sample file -

C:\Users\xyz\.myconfig\config.json
```json
{
    "newkey1": "newvalue1",
    "newkeygroup1": {
        "newkey2": "newvalue2"
    },
    "newkey3": [
        "newvalue4",
        "newvalue4"
    ],
    "newkey5": "newvalue5"
}
```

Usage example -
```python
import os

from dukepy.config import Config

config_dir = os.path.join(os.path.expanduser("~"), ".myconfig")
config_file = os.path.join(config_dir, "config.json")
Config(path=config_file, defaults={
    "newkey1": "newvalue1",
    "newkeygroup1": {
        "newkey2": "newvalue2"
    },
    "newkey3": ["newvalue4", "newvalue4"]
})

Config()["newkey5"] = "newvalue5"
Config().commit()
```

### converge
To find the extremes of a finite sequence, given that the sequence is continuous.
Provide at least two known numbers in the sequence,
and a method to check the validity of the number predicted by the algorithm.

Usage example -
```python
def check_validity(val):
    if val > -30 and val < 101:
        return True
    else:
        return False


low, high = Converge(-28, 50, check_validity).run()
print(low)
print(high)
```

Output -
```
-29
100
```

### dict_diff
* To find the recursive differences between two dictionaries.
* To update one dictionary with the other (each one optional)-
  * Add keys from the other
  * Remove keys which are not part of the other
  * Update values from the keys of the other

Usage example -
```python
dictionary_1 = {"abc": "value_abc",
                    "prs": "value_prs"}
    dictionary_2 = {"abc": "value_abc",
                    "xyz": "value_xyz"}
    dict_diff(dictionary_1, dictionary_2)
    print(dictionary_1)
    print(dictionary_2)

    dict_diff(dictionary_1, dictionary_2,
              udpate_added_keys=True)

    print(dictionary_1)
    print(dictionary_2)
```

Output -
```
:
 -  prs  :  value_prs
 :
 +  xyz  :  value_xyz
{'abc': 'value_abc', 'prs': 'value_prs'}
{'abc': 'value_abc', 'xyz': 'value_xyz'}
 :
 -  prs  :  value_prs
 :
 +  xyz  :  value_xyz
{'abc': 'value_abc', 'prs': 'value_prs', 'xyz': 'value_xyz'}
{'abc': 'value_abc', 'xyz': 'value_xyz'}
```
### logger
### mail_bot
### safe_dict
### singleton
### taces
Prints the origin of the exception, not just the exception string.
Usage example -
```python
mydict = dict()
    try:
        print(mydict["sdf"])
    except Exception as e:
        print_exception_traces(e)
```

Output -
```
Traceback (most recent call last):
  File "C:/Dev/libpython/src/dukepy/traces.py", line 16, in <module>
    print(mydict["sdf"])
KeyError: 'sdf'
```