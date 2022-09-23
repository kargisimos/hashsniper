import argparse
import hashlib
from time import perf_counter, gmtime, strftime
import sys
import string
import colorama
from itertools import product
from requests import get

def parse_the_arguments():
    parser = argparse.ArgumentParser(description=f'Single threaded hash cracker.Supports {len(hashlib.algorithms_available)} hash types and 4 cracking modes.')
    requiredName = parser.add_argument_group('required named arguments')
    requiredName.add_argument('-H', '--hash', required=True, metavar='<hash>',help='The hash to be cracked')
    requiredName.add_argument('-T','--type', required=True, metavar='<hash type>',help=f'Type of hash.Supported hash types: {",".join(hashlib.algorithms_available)}')
    requiredName.add_argument('-M','--mode',required=True, metavar='<crack mode>',type=int, help='Mode of cracking: 1 is for dictionary attack, 2 is for brute force attack (alphanumeric + special characters), 3 is for PIN attack (numeric only) and 4 is for online lookup (using md5decrypt.net API)')
    parser.add_argument('-w','--wordlist', help='The wordlist for a dictionary attack')
    parser.add_argument('--min-length',type=int,default=1,help='The minimum length of password for a brute force attack. Default 1')
    parser.add_argument('--max-length',type=int,default=8,help='The maximum length of password for a brute force attack. Default 8')
    parser.add_argument('--charset',default='all',help='The charset to use for a brute force attack. Accepted values seperated by commas: lowercase, uppercase, digits, punctuation. Default all')
    parser.add_argument('--pin-length',type=int,help='Fixed length of digits for a PIN attack. Zeros are added at the beginning of the password if necessary')
    parser.add_argument('--email',help='The email used for the md5decrypt.net registration')
    parser.add_argument('--key',help='The code (API key) retrieved from md5decrypt.net upon registration')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output. Displays each attempted password')
    args = parser.parse_args()
    return args

def arguments_check(args):
	
	#check wordlist
	if args.mode == 1:
		if not args.wordlist:
			print('[-]You must specify a wordlist for the password attack.\nExiting...')
			sys.exit(1)
	
	#check hash type
	if args.type not in hashlib.algorithms_available:
		print('[-]Supported hash types:')
		for hash_type in hashlib.algorithms_available:
			print('-' + hash_type)
		print('\nExiting...')
		sys.exit(1)
		
	#check mode
	if args.mode not in [1,2,3,4]:
		print('[-]Accepted cracking modes: 1,2,3,4.\nExiting...')
		sys.exit(1)
		
	#check charset
	for c in args.charset.split(','):
		if c not in ['all','ascii_lowercase','ascii_uppercase','digits','punctuation']:
			print(f'[-]{c} is not a supported charset.\nExiting...')
			sys.exit(1)
	
	#check pin length 
	if args.mode == 3:
		if not args.pin_length:
			print('[-]Pin length argument is required for a PIN attack.\nExiting...')
			sys.exit(1)
			
	#check email
	if args.mode == 4:
		if not args.email:
			print('[-]For online lookup, registrated email is required.\nExiting...')
			sys.exit(1)
			
	#check API Key
		elif not args.key:
			print('[-]For online lookup, API key is required.\nExiting...')
			sys.exit(1)


def crack(args):
	colorama.init(autoreset=True)

	if args.mode == 4:
		url = f'https://md5decrypt.net/en/Api/api.php?hash={args.hash}&hash_type={args.type}&email={args.email}&code={args.key}'
		r = get(url)
		if r.text and not 'ERROR CODE' in r.text:
			print(colorama.Fore.GREEN + f'[+]Password found: {r.text}')
			sys.exit(0)
		elif 'ERROR CODE' in r.text:
			print(colorama.Fore.RED + f'[-]{r.text} has occurred. Check https://md5decrypt.net/en/Api/ for API documentation...')
			sys.exit(0)
		else:
			print(colorama.Fore.RED + '[-]No results')
			sys.exit(0)
			
	print(colorama.Fore.GREEN + f'[+]Start time: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')
	print('Please wait while cracking...')
	
	if args.mode == 1:
		try:
			with open(args.wordlist,'rt') as f:
				data = f.readlines()
		except Exception as e:
			print(f'[-]An error occurred.. {e}')
			sys.exit(1)
		
		start = perf_counter()
		for line in data:
			exec("hash_obj = hashlib." + args.type + "()", globals())
			hash_obj.update(line.strip().encode())
			if hash_obj.hexdigest() == args.hash:
				end = perf_counter()
				print(colorama.Fore.GREEN + f'[+]Hash successfully cracked in {str(end - start)} seconds!\n Password: {line.strip()}')
				print(colorama.Fore.GREEN + f'[+]Stop time: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')
				sys.exit(0)
			elif args.verbose:
				print(colorama.Fore.RED + f'[-]Trying password: {line.strip()}')
		else:
			end = perf_counter()
			print(colorama.Fore.RED + f"[-]Couldn't crack the hash in {str(end - start)} seconds...")
			print(colorama.Fore.GREEN + f'[+]Stop time: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')
			sys.exit(0)
			
	elif args.mode == 2:
		global charset
		charset = ''
		if args.charset == 'all':
			charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
		else:
			for choice in args.charset.split(','):
				exec('charset += string.' + choice , globals())
		
		start = perf_counter()
		for i in range(args.min_length, args.max_length + 1):
			for attempt in product(charset, repeat = i):
				exec("hash_obj = hashlib." + args.type + "()", globals())
				hash_obj.update(''.join(attempt).encode())
				if hash_obj.hexdigest() == args.hash:
					end = perf_counter()
					print(colorama.Fore.GREEN + f'[+]Hash successfully cracked in {str(end - start)} seconds!\n Password: {"".join(attempt)}')
					print(colorama.Fore.GREEN + f'[+]Stop time: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')
					sys.exit(0)
				elif args.verbose:
					print(colorama.Fore.RED + f'[-]Trying password: {"".join(attempt)}')
		else:
			end = perf_counter()
			print(colorama.Fore.RED + f"[-]Couldn't crack the hash in {str(end - start)} seconds...")
			print(colorama.Fore.GREEN + f'[+]Stop time: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')
			sys.exit(0)
		
	elif args.mode == 3:
		start = perf_counter()
		for PIN in range (int('1' + '0' * args.pin_length)):
			exec("hash_obj = hashlib." + args.type + "()", globals())
			hash_obj.update(str(PIN).zfill(args.pin_length).encode())
			if hash_obj.hexdigest() == args.hash:
				end = perf_counter()
				print(colorama.Fore.GREEN + f'[+]Hash successfully cracked in {str(end - start)} seconds!\n Password: {str(PIN).zfill(args.pin_length)}')
				print(colorama.Fore.GREEN + f'[+]Stop time: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')
				sys.exit(0)
			elif args.verbose:
				print(colorama.Fore.RED + f'[-]Trying password: {str(PIN).zfill(args.pin_length)}')
		else:
			end = perf_counter()
			print(colorama.Fore.RED + f"[-]Couldn't crack the hash in {str(end - start)} seconds...")
			print(colorama.Fore.GREEN + f'[+]Stop time: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')
			sys.exit(0)
	
	
if __name__ == '__main__':
    args = parse_the_arguments()
    arguments_check(args)
    crack(args)
