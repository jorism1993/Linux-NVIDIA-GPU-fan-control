import os
import time
import csv
import psutil
import pdb


def get_temps():
	stream = os.popen('nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits')
	out = stream.read()
	temps = out.split('\n')
	temps = temps[0:NUM_GPUS]
	temps = [int(i) for i in temps if i != '']
	stream.close()
	return temps


def set_fan_speed(temps):

	for gpu_id in range(len(temps)):
		gpu_temp = temps[gpu_id]
		fan_speed = temp_curve(gpu_temp)

		gpu_id = MAPPING[gpu_id]
		fan_ids = GPU_2_FAN[gpu_id]

		for fan_id in fan_ids:
			set_fan_speed_command = f'nvidia-settings -a "[gpu:{gpu_id}]/GPUFanControlState=1" -a "[fan:{fan_id}]/GPUTargetFanSpeed={fan_speed}"'
			set_fan_speed_stream = os.popen(set_fan_speed_command)
			set_fan_speed_out = set_fan_speed_stream.read()

		set_power_limit(gpu_temp, gpu_id)


path_to_file = os.path.join('/home/joris/.nfancurve/logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.txt')
os.makedirs('/home/joris/.nfancurve/logs', exist_ok=True)

max_temp = 0


os.popen('bash init_power_limit.sh')


while True:
	from temp_curves import set_power_limit, temp_curve, NUM_GPUS, MAPPING, GPU_2_FAN
	time.sleep(5)
	temps = get_temps()
	if max(temps) > max_temp:
		max_temp = max(temps)
		with open(path_to_file, mode='a') as log_file:
			log_file.write(time.strftime("%Y-%m-%d %H:%M:%S") + f' max temp is now {max_temp}\n')
	set_fan_speed(temps)

	cpu_temps = psutil.sensors_temperatures()
	cpu_temps = cpu_temps['k10temp']
	cpu_temp_out = ' | CPU '

	for item in cpu_temps:
		if item.label=='Tdie':
			cpu_temp_out += f'{item.current} '

	with open(path_to_file, mode='a') as log_file:
		log_file.write(time.strftime("%Y-%m-%d %H:%M:%S") + ' | GPU ' + ' '.join(map(str, temps)) + cpu_temp_out + '\n')
