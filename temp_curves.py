import os


NUM_GPUS = 2
MAPPING = {0: 0, 1: 1}
REVERSE_MAPPING = {v: k for k, v in MAPPING.items()}
GPU_2_FAN = {0:(0, ), 1:(1, )}
POWER_LIMIT_STRING = "#!/bin/bash\nsudo nvidia-smi -pm 1\nsudo nvidia-smi -i {} -pl {}\n"


def set_power_limit(temp, gpu_id):
	if temp > 85:
		pl = 250
	elif temp > 80:
		pl = 300
	else:
		pl = 375

	pl_string = POWER_LIMIT_STRING.format(REVERSE_MAPPING[gpu_id], pl)
	
	with open("/home/joris/.nfancurve/temp_pl_file.sh", "w") as text_file:
		text_file.write(pl_string)

	os.popen('bash /home/joris/.nfancurve/temp_pl_file.sh')


def temp_curve(temp):
	if temp < 50:
		return 30
	elif temp >= 100:
		with open(path_to_file, mode='a') as log_file:
			log_file.write('Now shutting down because temp has been exceeded.')
		os.popen('shutdown -h now')
	elif temp >= 75:
		return 100
	elif temp >= 70:
		return 98
	elif temp >= 60:
		return 75
	else:
		return temp
