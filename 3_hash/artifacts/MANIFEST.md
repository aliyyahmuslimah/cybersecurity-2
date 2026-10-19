# MANIFEST — hash track artifacts (from the instructor)

Everything is **dummy data**. The users' real passwords are not included.

| File | For step | Description |
|---|---|---|
| `user_dump.csv` | H2 | 12 dummy users: `user,md5_hash` (unsalted MD5) |
| `small_wordlist.txt` | H2 | 200 guesses (words/passwords), one per line |

What you must find (H2): how many users' passwords fall to the wordlist, why two users appear to
have the same hash, and why the rest survive.
