import backend
import os, time, getpass

def main():
    check_config_file = os.path.exists('./config.json')
    if check_config_file == True: 
        start_time = time.time()
        vars = backend.read_json_config('config.json')
        check_con = backend.conn_test(hostname=vars["junos_login"]["host"], username=vars["junos_login"]["user"], junos_pass=vars["junos_login"]["password"],start_time=start_time)
        backend.get_facts(vars)
        backend.check_eth_status(vars)
        end_time = time.time() - start_time
        backend.log(vars,check_con,end_time)
    else:
        host = input("Please input your host: ")
        user = input("Please input your username: ")
        password = getpass("Please enter your password: ")
        check_con = backend.conn_test(hostname=host, username=user, junos_pass=password)
        backend.check_eth_status(vars)
        end_time = time.time() - start_time
        backend.log(vars,check_con,end_time)

if __name__ == "__main__":
    main()