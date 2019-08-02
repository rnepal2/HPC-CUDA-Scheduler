import os
import math

# Taking input from the keyboard
max_field = eval(input("Enter the upper value of magnetic field in mT: "))
min_field = eval(input("Enter the lower value of magnetic field in mT: "))
divide_into = int(input("Enter the number of files/division in field range: "))
number_of_copies = int(input("Enter the number to average over for each magnetic field: "))

# Creating mumax3 scripts and job submit files of N copies for each magnetic field
def create_mumax_and_jobsubmit_file(B):
	B_field = B  # at magnetic field B_field = B mT
	N = number_of_copies
	mumax_template = open("mumax_template.mx3", "rt").read()
	job_submit_template = open("job_submit_template.submit", "rt").read()
	mumax_script_list = []
	job_submit_file_list = []
	for i in range(N):
		# Create input (job.submit files and mumax scripts) directories
		input_dir_path = '/home/kovalev/rnepal2/transition/' + 'source-B-{0:.2f}'.format(B_field)
		if not os.path.exists(input_dir_path):
			os.makedirs(input_dir_path)
		# Create the output file directories
		output_dir_path = '/work/kovalev/rnepal2/transition/out-B-{0:.2f}'.format(B_field) + '/copy-{}'.format(i)
		if not os.path.exists(output_dir_path):
			os.makedirs(output_dir_path)

		mumax_script_name = '/mumax-script-'+'B-{0:.2f}-'.format(B_field) + 'copy-{}'.format(i) + '.mx3'
		mumax_script_dir = '/home/kovalev/rnepal2/transition/source-B-{0:.2f}'.format(B_field)
		mumax_script_path = mumax_script_dir  +  mumax_script_name
		job_submit_file_name = '/job-submit-' + 'B-{0:.2f}-'.format(B_field) + 'copy-{}'.format(i) + '.submit'
		# folder_name = 'source-B-{}/'.format(B_field) + 'mumax-transition' + 'B-{0:.3f}'.format(B_field) + 'copy-{i}'.format(i) + '.out'
		out_folder_path = '/work/kovalev/rnepal2/transition/out-B-{0:.2f}-'.format(B_field) + '/copy-{}'.format(i)
		mumax_script_replacements = {"field": B_field}
		# Dividing jobs into two different GPU partitions in HCC
		if B_field < (min_field + max_field)/2:
			job_submit_replacements = {"which_gpu": gpu_m2070, "J": '%J', "out_folder_path": out_folder_path, "mumax_script_path": mumax_script_path}
		else:
			job_submit_replacements = {"which_gpu": gpu_k20, "J": '%J', "out_folder_path": out_folder_path, "mumax_script_path": mumax_script_path}
		# Creating the mumax3 script files
		with open(input_dir_path + mumax_script_name, "wt") as mumax_file:
			mumax_file.write(mumax_template % mumax_script_replacements)
			mumax_file_name = mumax_file.name
			mumax_script_list.append(mumax_file_name)
		# Creating the job submit files
		with open(input_dir_path + job_submit_file_name, "wt") as job_submit_file:
			job_submit_file.write(job_submit_template % job_submit_replacements)
			job_submit_file_name = job_submit_file.name
			job_submit_file_list.append(job_submit_file_name)
	return job_submit_file_list


def create_source_files_over_B(max_field, min_field, divide_into):
	Bmax = max_field
	Bmin = min_field
	num = divide_into
	jobsubmit_files_lists_for_all_B = []
	for i in range(num):
		B = Bmin + i*(Bmax - Bmin)/num
		job_file_list_for_B = create_mumax_and_jobsubmit_file(B)
		jobsubmit_files_lists_for_all_B.append(job_file_list_for_B)
	return jobsubmit_files_lists_for_all_B
	print("Created mumax scripts and job submit files and submitted jobs for all magnetic fields !")

def submit_all_jobs():
	job_files_lists = create_source_files_over_B(max_field, min_field, divide_into)
	print("The lenght of job files list and its one element: ", len(job_files_lists), len(job_files_lists[1]))
	print("Just to check the name of one job file name format:  ", job_files_lists[1][2])
	for i in range(len(job_files_lists)):
		for script in job_files_lists[i]:
			os.system("sbatch " + "{}".format(script))
		print("Jobs submitted for one magnetic field  value.")
	print("All the jobs submitted, HAPPY WAITING !")

submit_all_jobs()
