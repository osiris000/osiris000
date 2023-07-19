
import os , shlex , cnf , auth, fhelp


def command_line():
	com = input(">>> ")
	if com == "":
		command_line()
	args = shlex.split(com)
	if args[0] == "agenda":
		if len(args) == 1:
			print(fhelp.fhelp(args[0]))
			fs = "XP"
			import agenda
		else:
			print("AGENDA MAS ",args)
	elif com == "exit":
		exit()
	elif com == "Reset Password":
		auth.makeauth()
	else:
		print(args)
	command_line()




def exit():
	exitf = input("¿ Desea salir del programa ? type 'yes' or 'no' ")
	if exitf == "no" :
		command_line()
	elif exitf == "yes" :
		print("\nEXIT PROGRAM\n")
		auth.access()
	else:
		exit()
