
import cnf, auth, com


#auth.run()

try:
    auth.run()
except Exception as e:
    print("\n\nError:",e)
    print("Line:",e.__traceback__.tb_lineno)
    com.command_line()

print("\nSE HA PRODUCIDO UN ERROR INESPERADO\n")
