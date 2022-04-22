from datetime import datetime

def logthis(message):
	last_100_lines=[]
	truncate = False
	with open('log.txt', 'a') as log:
		log.write("----------------\n")
		log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		log.write("\n")
		log.write(message)
		log.write('\n')
	log.close()
	with open('log.txt', 'r') as log:
		data=log.readlines()
		if len(data)>2000:
			last_100_lines=data[-100:]
			truncate=True
			print("Time To Truncate")
	log.close()
	if truncate:
		with open('log.txt', 'w') as log:
			for line in last_100_lines:
				log.write(line)
		log.close()
	
		
	