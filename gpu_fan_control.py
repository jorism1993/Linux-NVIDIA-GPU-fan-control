import os
import time
import csv
import pdb


NUM_GPUS = 4


def get_temps():
	stream = os.popen('nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits')
	out = stream.read()
	temps = out.split('\n')
	temps = temps[0:NUM_GPUS]
	temps = [int(i) for i in temps]
	stream.close()
	return temps


def temp_curve(temp):
	if temp < 50:
		return 30
	elif temp >= 100:
		os.popen('shutdown -h now')
	elif temp >= 80:
		return 100
	elif temp >= 70:
		return 90
	elif temp >= 60:
		return 70
	else:
		return temp


def set_fan_speed(temps):

	for gpu_id in range(NUM_GPUS):
		gpu_temp = temps[gpu_id]
		fan_speed = temp_curve(gpu_temp)

		# set_active_command = f'nvidia-settings -a "[gpu:{gpu_id}]/GPUFanControlState=1"'
		# set_active_stream = os.popen(set_active_command)
		# set_active_out = set_active_stream.read()
		# set_active_stream.close()

		set_fan_speed_command = f'nvidia-settings -a "[gpu:{(NUM_GPUS - 1) - gpu_id}]/GPUFanControlState=1" -a "[fan:{(NUM_GPUS - 1) - gpu_id}]/GPUTargetFanSpeed={fan_speed}"'
		set_fan_speed_stream = os.popen(set_fan_speed_command)
		set_fan_speed_out = set_fan_speed_stream.read()


path_to_file = os.path.join('/home/joris/.nfancurve/logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.txt')
os.makedirs('/home/joris/.nfancurve/logs', exist_ok=True)


while True:
	time.sleep(3)
	temps = get_temps()
	set_fan_speed(temps)

	with open(path_to_file, mode='a') as log_file:
		log_file.write(time.strftime("%Y-%m-%d %H:%M:%S") + ' ' + ' '.join(map(str, temps)) + '\n')
