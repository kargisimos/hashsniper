# hashsniper
Single threaded hash cracker written in python. Currently supports 22 hash types and has 4 cracking modes.

options:

      -h, --help            show this help message and exit
      -w WORDLIST, --wordlist WORDLIST
                            The wordlist for a dictionary attack
      --min-length MIN_LENGTH
                            The minimum length of password for a brute force attack. Default 1
      --max-length MAX_LENGTH
                            The maximum length of password for a brute force attack. Default 8
      --charset CHARSET     The charset to use for a brute force attack. Accepted values seperated by commas: lowercase,
                            uppercase, digits, punctuation. Default all
      --pin-length PIN_LENGTH
                            Fixed length of digits for a PIN attack. Zeros are added at the beginning of the password if
                            necessary
      --email EMAIL         The email used for the md5decrypt.net registration
      --key KEY             The code (API key) retrieved from md5decrypt.net upon registration
      -v, --verbose         Verbose output. Displays each attempted password

required named arguments:

      -H <hash>, --hash <hash>
                            The hash to be cracked
      -T <hash type>, --type <hash type>
                            Type of hash.Supported hash types: sha256,sha512,shake_128,shake_256,sha3_224,ripemd160,blake2
                            s,sha1,sha3_512,md5,mdc2,blake2b,sha3_256,md5-
                            sha1,md4,sha512_256,sha224,sha512_224,sm3,sha384,whirlpool,sha3_384
      -M <crack mode>, --mode <crack mode>
                            Mode of cracking: 1 is for dictionary attack, 2 is for brute force attack (alphanumeric +
                            special characters), 3 is for PIN attack (numeric only) and 4 is for online lookup (using
                            md5decrypt.net API)
