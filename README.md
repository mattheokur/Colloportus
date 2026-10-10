# Colloportus
A program that judges your password strength.
## Scoring Metrics
 - Length (35%): Perfected by securing a length of at least 16 characters.
 - Character Diversity (20%): Standard deviation of characters in ascii.
 - Pattern (20%): Repetition of chunks within the password.
 - Commonality (25%): Compares the password against NCSC's 100k Most Used Passwords list.
## Sources
- [NCSC 100k Most Used Passwords](https://github.com/danielmiessler/SecLists/blob/cae9eab995852c183fbe5e03fc92471fcac82f0e/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt)
